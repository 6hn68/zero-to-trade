#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/due_diligence.py - L1/L2/L3 due diligence + A/B/C rating.

Run: python3 -m unittest discover -s tests -v   (from the repo root)
"""

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import due_diligence as dd  # noqa: E402


def profile(**overrides):
    """A complete A-grade profile; override fields to lower the rating.

    All companies are fictional (【示例】 prefix, sample.example domain,
    +000 placeholder phone)."""
    base = {
        "company": "【示例】海湾轮胎贸易", "country": "Saudi Arabia",
        "product": "TBR 12.00R20", "website": "sample.example",
        "website_updated": "recent", "years": "18",
        "email_domain": "sample.example", "phone": "+000 00 000 0000",
        "address": "Riyadh, Saudi Arabia", "source": "customs",
        "social": "active", "customs_record": "yes", "import_match": "yes",
        "contact_role": "purchasing manager", "employees": "45",
        "trade_role": "importer", "legal_name_match": "yes",
        "sanctions": "clear", "adverse": "no", "payment": "prepaid",
        "payee_mismatch": "no", "note": "",
    }
    base.update(overrides)
    return base


def flags_of(report):
    return [f["flag"] for f in report["red_flags"]]


class TestL1Screening(unittest.TestCase):
    def test_l1_no_website_eliminates(self):
        report = dd.build_report(profile(website="none"))
        self.assertEqual(report["l1"]["status"], "fail")
        self.assertEqual(report["rating"], "C")
        self.assertIn("官网不存在 / 多年未更新 / 只有 Coming soon",
                      flags_of(report))

    def test_l1_stale_website_eliminates(self):
        report = dd.build_report(profile(website_updated="old"))
        self.assertEqual(report["l1"]["status"], "fail")
        self.assertEqual(report["rating"], "C")

    def test_l1_free_email_only_eliminates(self):
        report = dd.build_report(profile(email_domain="gmail.com"))
        self.assertEqual(report["l1"]["status"], "fail")
        self.assertEqual(report["rating"], "C")
        self.assertIn("唯一联系方式是免费邮箱", flags_of(report))

    def test_l1_unknown_question_downgrades_to_c(self):
        # 没给渠道角色：L1 第 3 问答不上来，先降为 C（不是「没有」，是「待核实」）
        report = dd.build_report(profile(trade_role=""))
        self.assertEqual(report["l1"]["status"], "unknown")
        self.assertEqual(report["rating"], "C")
        self.assertEqual(report["red_flags"], [])

    def test_l1_peer_is_not_a_buyer(self):
        report = dd.build_report(profile(trade_role="peer"))
        self.assertEqual(report["l1"]["status"], "fail")
        self.assertEqual(report["rating"], "C")
        self.assertIn("本身是同行品牌商", flags_of(report))


class TestRating(unittest.TestCase):
    def test_rating_a(self):
        report = dd.build_report(profile())
        self.assertEqual(report["rating"], "A")
        self.assertEqual(report["t_tier"], "T0")
        self.assertEqual(report["red_flags"], [])
        self.assertEqual(report["missing_items"], [])
        self.assertIn("48 小时内首触", report["next_action"])

    def test_rating_b_weak_evidence(self):
        # LinkedIn 来的新客户：L1 全过，但进口记录、身份、信誉都没核实
        report = dd.build_report(profile(
            source="linkedin", customs_record="unknown", import_match="unknown",
            legal_name_match="unknown", adverse="unknown", payment="unknown",
            years="4", employees="6", trade_role="distributor",
            contact_role="sourcing manager"))
        self.assertEqual(report["rating"], "B")
        self.assertEqual(report["t_tier"], "T1/T2")
        self.assertEqual(report["red_flags"], [])
        self.assertTrue(report["missing_items"])
        self.assertIn("补材料再推进", report["next_action"])

    def test_one_red_flag_downgrades_a_to_b(self):
        # 其余全是 A 的条件，只差「首触就要账期」这一项红旗 -> 降一级
        report = dd.build_report(profile(payment="credit"))
        self.assertEqual(report["rating"], "B")
        self.assertIn("首次接触就要大额账期 / 只接受 EXW-FCA 且拒绝任何预付",
                      flags_of(report))

    def test_two_red_flags_drop_to_c(self):
        report = dd.build_report(profile(adverse="yes", payment="credit"))
        self.assertEqual(report["rating"], "C")
        self.assertEqual(report["t_tier"], "T3")
        self.assertEqual(len(report["red_flags"]), 2)

    def test_no_import_record_but_claims_big_distributor(self):
        report = dd.build_report(profile(customs_record="no",
                                         trade_role="distributor"))
        self.assertIn("零进口记录却自称大分销商", flags_of(report))
        self.assertEqual(report["rating"], "B")

    def test_sanctions_terminates_immediately(self):
        report = dd.build_report(profile(sanctions="flagged"))
        self.assertTrue(report["terminated"])
        self.assertEqual(report["rating"], "C")
        self.assertIn("立即终止", report["next_action"])
        self.assertIn("出现在制裁名单上", flags_of(report))

    def test_payee_mismatch_terminates_immediately(self):
        report = dd.build_report(profile(payee_mismatch="yes"))
        self.assertTrue(report["terminated"])
        self.assertEqual(report["rating"], "C")
        self.assertIn("要求把货款付到与合同主体不一致的第三方账户",
                      flags_of(report))

    def test_domain_mismatch_is_a_red_flag(self):
        report = dd.build_report(profile(email_domain="other.example"))
        self.assertIn("邮箱域名与官网域名不一致", flags_of(report))
        self.assertEqual(report["rating"], "B")

    def test_missing_company_raises(self):
        with self.assertRaises(ValueError):
            dd.build_report(profile(company=""))


class TestL3AndCsvNote(unittest.TestCase):
    def test_l3_lists_sources_not_results(self):
        report = dd.build_report(profile())
        self.assertEqual(len(report["l3"]["checklist"]), 5)
        for item in report["l3"]["checklist"]:
            self.assertEqual(item["status"], "待查")
            self.assertTrue(item["where"])  # 去哪查必须写清，不替用户编结果

    def test_note_for_csv_only_verified_facts(self):
        report = dd.build_report(profile())
        self.assertIn("Est. 18 years", report["note_for_csv"])
        self.assertIn("import record found", report["note_for_csv"])

    def test_note_for_csv_empty_when_nothing_verified(self):
        report = dd.build_report(profile(
            website="none", email_domain="gmail.com", years="",
            employees="", social="inactive", customs_record="no",
            import_match="unknown", contact_role="sales", trade_role=""))
        self.assertEqual(report["note_for_csv"], "")


class TestOutputFormats(unittest.TestCase):
    def test_json_internal_roundtrip(self):
        report = dd.build_report(profile())
        data = json.loads(dd.render_json(report, "internal"))
        self.assertEqual(data["rating"], "A")
        self.assertIn("inputs", data)
        self.assertIn("red_flags", data)
        self.assertIn("l1", data)

    def test_json_client_hides_internal_judgment(self):
        report = dd.build_report(profile())
        data = json.loads(dd.render_json(report, "client"))
        for key in ("rating", "red_flags", "terminated", "t_tier",
                    "next_action", "inputs", "l1", "l2"):
            self.assertNotIn(key, data)
        self.assertIn("verified_facts", data)
        self.assertIn("needed_materials", data)

    def test_client_table_hides_rating_and_flags(self):
        report = dd.build_report(profile())
        text = dd.render_table(report, "client")
        # 章节标题一级不能出现；免责声明里提一句「评级不对外提供」不算泄露
        self.assertNotIn("【评级】", text)
        self.assertNotIn("【红旗", text)
        self.assertNotIn("已终止", text)
        self.assertIn("已核实的公开事实", text)

    def test_cli_missing_company_exits_2(self):
        with self.assertRaises(SystemExit) as ctx:
            dd.main([])
        self.assertEqual(ctx.exception.code, 2)

    def test_cli_writes_out_file(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = str(Path(tmp) / "report.txt")
            rc = dd.main(["--company", "【示例】海湾轮胎贸易",
                          "--website", "sample.example", "--years", "18",
                          "--email-domain", "sample.example",
                          "--source", "customs", "--social", "active",
                          "--customs-record", "yes", "--import-match", "yes",
                          "--contact-role", "purchasing manager",
                          "--out", out])
            self.assertEqual(rc, 0)
            self.assertIn("客户背调报告", Path(out).read_text(encoding="utf-8"))


class TestL2ScoringAndEvidence(unittest.TestCase):
    """L2 six-dimension scoring + three-grade evidence labels.

    L2 六维打分 + 证据三档标注：通过 100 / 待核实 40 / 红旗 0，
    默认权重采购力、付款习惯各 2，其余各 1；总分只看证据扎实程度，不改评级。
    """

    def test_a_profile_scores_100_and_band_strong(self):
        report = dd.build_report(profile())
        scores = report["l2_scores"]
        self.assertEqual(scores["total"], 100.0)
        self.assertEqual(scores["band"], "证据扎实")
        self.assertEqual(len(scores["dimensions"]), 6)
        for s in scores["dimensions"]:
            self.assertEqual(s["score"], 100)
            self.assertEqual(s["status"], "pass")
            self.assertIn(s["evidence"], dd.EVIDENCE_GRADES)

    def test_b_profile_scores_55_and_band_middling(self):
        # LinkedIn 来的新客户：4 维待核实（各 40 分），2 维通过（各 100 分）
        # (40 + 100 + 40 + 40*2 + 40*2 + 100) / 8 = 55.0
        report = dd.build_report(profile(
            source="linkedin", customs_record="unknown", import_match="unknown",
            legal_name_match="unknown", adverse="unknown", payment="unknown",
            years="4", employees="6", trade_role="distributor",
            contact_role="sourcing manager"))
        self.assertEqual(report["l2_scores"]["total"], 55.0)
        self.assertEqual(report["l2_scores"]["band"], "证据一般")
        # 打分不改评级：还是 B
        self.assertEqual(report["rating"], "B")

    def test_two_red_flags_scores_below_50(self):
        # 信誉、付款习惯两维红旗（各 0 分），其余四维通过：
        # (100 + 100 + 0 + 100*2 + 0*2 + 100) / 8 = 62.5
        report = dd.build_report(profile(adverse="yes", payment="credit"))
        self.assertEqual(report["l2_scores"]["total"], 62.5)
        self.assertEqual(report["l2_scores"]["band"], "证据一般")
        self.assertEqual(report["rating"], "C")

    def test_red_flag_dimension_scores_zero(self):
        report = dd.build_report(profile(customs_record="no",
                                         trade_role="distributor"))
        by_dim = {s["dimension"]: s
                  for s in report["l2_scores"]["dimensions"]}
        self.assertEqual(by_dim["采购力"]["score"], 0)
        self.assertEqual(by_dim["采购力"]["status"], "red_flag")

    def test_unknown_dimension_scores_40_not_zero(self):
        # 待核实给 40 分不给 0 分：「没查到」不等于「没问题」，但也不能当有问题扣光
        report = dd.build_report(profile(legal_name_match="unknown"))
        by_dim = {s["dimension"]: s
                  for s in report["l2_scores"]["dimensions"]}
        self.assertEqual(by_dim["身份"]["score"], 40)
        self.assertEqual(by_dim["身份"]["evidence"], "待核实")

    def test_nothing_provided_is_all_pending_and_scores_40(self):
        # 只给公司名，其余全空：六维证据全是「待核实」，总分 40，不编任何值
        report = dd.build_report({"company": "【示例】空白公司"})
        for d in report["l2"]["checks"]:
            self.assertEqual(d["evidence"], "待核实")
            self.assertEqual(d["status"], "unknown")
        for c in report["l1"]["checks"]:
            self.assertIn(c["evidence"], dd.EVIDENCE_GRADES)
        self.assertEqual(report["l2_scores"]["total"], 40.0)
        self.assertEqual(report["l2_scores"]["band"], "证据薄弱")
        self.assertEqual(report["rating"], "C")

    def test_verified_beats_inferred(self):
        # 同一维：对着公开来源查到的算「已核实」，对方自述只能算「有据推断」
        verified = dd.build_report(profile())
        by_dim = {d["dimension"]: d for d in verified["l2"]["checks"]}
        self.assertEqual(by_dim["采购力"]["evidence"], "已核实")  # 海关数据
        self.assertEqual(by_dim["身份"]["evidence"], "已核实")    # 注册库
        self.assertEqual(by_dim["规模"]["evidence"], "有据推断")  # 对方报的数
        self.assertEqual(by_dim["付款习惯"]["evidence"], "有据推断")  # 对方自述
        # 公开检索「没查到」不良记录只是没查到，不等于没有：只能算有据推断
        self.assertEqual(by_dim["信誉"]["evidence"], "有据推断")
        self.assertEqual(by_dim["合规"]["evidence"], "有据推断")

    def test_custom_weights_change_total(self):
        report = dd.build_report(profile(
            source="linkedin", customs_record="unknown", import_match="unknown",
            legal_name_match="unknown", adverse="unknown", payment="unknown",
            years="4", employees="6", trade_role="distributor",
            contact_role="sourcing manager"),
            weights={"采购力": 0, "付款习惯": 0})
        # 去掉两维权重后：(40 + 100 + 40 + 100) / 4 = 70.0
        self.assertEqual(report["l2_scores"]["total"], 70.0)
        self.assertEqual(report["l2_scores"]["weights"]["采购力"], 0)
        self.assertEqual(report["l2_scores"]["weights"]["身份"], 1.0)

    def test_score_l2_ignores_unknown_weight_keys(self):
        dims = dd.l2_assess(dd.clean_inputs(profile()))
        scored = dd.score_l2(dims, weights={"不存在的维": 9, "身份": "not-a-number"})
        self.assertEqual(scored["total"], 100.0)
        self.assertEqual(scored["weights"]["身份"], 1.0)
        self.assertNotIn("不存在的维", scored["weights"])

    def test_small_company_note_lists_only_given_facts(self):
        # 只给人数不给年份：备注只写人数，不许出现「成立约 未知 年」
        report = dd.build_report(profile(years="", employees="8"))
        size = [d for d in report["l2"]["checks"]
                if d["dimension"] == "规模"][0]
        self.assertIn("员工约 8 人", size["note"])
        self.assertNotIn("未知", size["note"])

    def test_table_shows_scores_and_evidence_grades(self):
        text = dd.render_table(dd.build_report(profile()), "internal")
        self.assertIn("【L2 六维打分】", text)
        self.assertIn("总分 100.0 / 100（证据扎实）", text)
        self.assertIn("采购力：100 分（权重 2，证据：已核实）", text)
        self.assertIn("证据：已核实", text)
        self.assertIn("证据：有据推断", text)

    def test_json_internal_includes_scores_client_excludes_them(self):
        report = dd.build_report(profile())
        data = json.loads(dd.render_json(report, "internal"))
        self.assertIn("l2_scores", data)
        self.assertEqual(data["l2_scores"]["total"], 100.0)
        client = json.loads(dd.render_json(report, "client"))
        # 打分是内部判断，不进客户视图
        self.assertNotIn("l2_scores", client)

    def test_cli_weights_option(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = str(Path(tmp) / "report.txt")
            rc = dd.main(["--company", "【示例】海湾轮胎贸易",
                          "--website", "sample.example", "--years", "18",
                          "--email-domain", "sample.example",
                          "--source", "customs", "--social", "active",
                          "--customs-record", "yes", "--import-match", "yes",
                          "--contact-role", "purchasing manager",
                          "--weights", '{"采购力": 3}',
                          "--out", out])
            self.assertEqual(rc, 0)
            content = Path(out).read_text(encoding="utf-8")
            # --weights 生效：采购力权重变成 3，总分随之重算
            # (40 + 100 + 40 + 100*3 + 40*2 + 40) / 9 = 66.7
            self.assertIn("采购力：100 分（权重 3，证据：已核实）", content)
            self.assertIn("总分 66.7 / 100", content)

    def test_cli_bad_weights_exits_2(self):
        rc = dd.main(["--company", "【示例】海湾轮胎贸易",
                      "--weights", "not-json"])
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
