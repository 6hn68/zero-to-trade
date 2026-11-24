#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/trade_show.py — trade-show 24h follow-up plans.

Run: python3 -m unittest discover -s tests -v   (from the repo root)
Only the standard library is used, same rule as the scripts themselves.

All company names / emails / phones in this file are fictional:
【示例】 prefix, sample.example domain, +000 placeholder phones.
"""

import csv
import io
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import trade_show as ts  # noqa: E402


def run_cli(*args):
    """Run the trade_show CLI; return (exit_code, stdout+stderr)."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "trade_show.py"), *args],
        capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout + proc.stderr


def exhibitor(company, interest, email="", phone="", whatsapp="", country="Saudi Arabia",
              product="TBR 12.00R20"):
    return ts.make_exhibitor(company, country, product, interest,
                             email, phone, whatsapp)


def three_mixed():
    """高/中/低各一家，录入顺序故意打乱（低在先），验排序只看兴趣度。"""
    return [
        exhibitor("【示例】尼罗河商贸", "低", whatsapp="+000 00 000 0000",
                  country="Egypt", product="PCR tubes"),
        exhibitor("【示例】海湾轮胎贸易", "高", email="demo01@sample.example"),
        exhibitor("【示例】迪拜轮毂行", "中", phone="+000 00 000 0000",
                  country="UAE", product="PCR 195/65R15"),
    ]


class TestSorting(unittest.TestCase):
    def test_sort_high_medium_low(self):
        plan = ts.build_plan(three_mixed())
        self.assertEqual([p["company"] for p in plan],
                         ["【示例】海湾轮胎贸易", "【示例】迪拜轮毂行",
                          "【示例】尼罗河商贸"])
        self.assertEqual([p["interest"] for p in plan], ["高", "中", "低"])

    def test_sort_english_aliases(self):
        rows = [
            exhibitor("【示例】丙公司", "low", email="c@sample.example"),
            exhibitor("【示例】甲公司", "HIGH", email="a@sample.example"),
            exhibitor("【示例】乙公司", "Medium", email="b@sample.example"),
        ]
        plan = ts.build_plan(rows)
        self.assertEqual([p["interest"] for p in plan], ["高", "中", "低"])
        self.assertEqual([p["company"] for p in plan],
                         ["【示例】甲公司", "【示例】乙公司", "【示例】丙公司"])

    def test_same_interest_keeps_input_order(self):
        rows = [
            exhibitor("【示例】先聊的", "高", email="a@sample.example"),
            exhibitor("【示例】后聊的", "高", email="b@sample.example"),
            exhibitor("【示例】最后聊的", "高", email="c@sample.example"),
        ]
        plan = ts.build_plan(rows)
        self.assertEqual([p["company"] for p in plan],
                         ["【示例】先聊的", "【示例】后聊的", "【示例】最后聊的"])

    def test_tier_mapping(self):
        plan = ts.build_plan(three_mixed())
        self.assertEqual([p["tier"] for p in plan], ["T0", "T1", "T2"])


class TestTimetable(unittest.TestCase):
    def test_three_steps_all_present(self):
        plan = ts.build_plan(three_mixed())
        for entry in plan:
            self.assertEqual(len(entry["steps"]), 3)
            self.assertEqual([s["window"] for s in entry["steps"]],
                             ["会后 2 小时内", "会后 12 小时内", "会后 24 小时内"])
            self.assertEqual([s["offset"] for s in entry["steps"]],
                             ["T+2h", "T+12h", "T+24h"])

    def test_step_actions_cover_thanks_quote_call(self):
        plan = ts.build_plan(three_mixed())
        first = plan[0]["steps"]
        self.assertIn("感谢", first[0]["action"])
        self.assertIn("报价线索", first[1]["action"])
        self.assertIn("电话/WhatsApp", first[2]["action"])
        # 第一封不报具体价格数字：草稿里不能出现价单/底价字样
        self.assertNotIn("底价", plan[0]["first_touch"]["en"])

    def test_step3_channel_prefers_phone(self):
        plan = ts.build_plan(three_mixed())
        by_company = {p["company"]: p for p in plan}
        # 只有邮箱的 → 第 3 步只能邮件追一次，并写明原因
        self.assertIn("邮箱", by_company["【示例】海湾轮胎贸易"]["steps"][2]["channel"])
        # 有电话的 → 第 3 步走电话/WhatsApp
        self.assertEqual(by_company["【示例】迪拜轮毂行"]["steps"][2]["channel"],
                         "电话/WhatsApp")


class TestDraft(unittest.TestCase):
    def test_first_touch_refs_outreach_template(self):
        plan = ts.build_plan(three_mixed())
        by_tier = {p["tier"]: p for p in plan}
        for tier in ("T0", "T1", "T2"):
            draft = by_tier[tier]["first_touch"]
            self.assertIn("outreach_gen.py --tier %s" % tier, draft["draft_from"])
            self.assertIn("--tier %s" % tier, draft["outreach_command"])
            self.assertIn("trade show", draft["en"])
            self.assertTrue(draft["subject"])
        # 高兴趣的草稿直接问规格用量，低兴趣的只求确认
        self.assertIn("monthly volume", by_tier["T0"]["first_touch"]["en"])
        self.assertIn("One word is enough", by_tier["T2"]["first_touch"]["en"])

    def test_whatsapp_only_channel(self):
        ex = exhibitor("【示例】只留WA的", "中", whatsapp="+000 00 000 0000")
        self.assertEqual(ex["channel"], "WhatsApp")
        self.assertEqual(ex["contact"], "+000 00 000 0000")


class TestCsvBatch(unittest.TestCase):
    def _write_csv(self, rows, header=("company", "country", "product",
                                       "contact", "interest")):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                          encoding="utf-8", newline="")
        writer = csv.writer(tmp)
        writer.writerow(header)
        writer.writerows(rows)
        tmp.close()
        return tmp.name

    def test_csv_batch_read(self):
        path = self._write_csv([
            ["【示例】甲公司", "Saudi Arabia", "TBR 12.00R20",
             "a@sample.example", "高"],
            ["【示例】乙公司", "UAE", "PCR 195/65R15",
             "+000 00 000 0000", "中"],
            ["【示例】丙公司", "Egypt", "PCR tubes",
             "+000 00 000 0000", "低"],
        ])
        rows = ts.read_exhibitors(path)
        self.assertEqual(len(rows), 3)
        plan = ts.build_plan(rows)
        self.assertEqual([p["company"] for p in plan],
                         ["【示例】甲公司", "【示例】乙公司", "【示例】丙公司"])

    def test_csv_reads_bundled_example(self):
        rows = ts.read_exhibitors(
            str(REPO_ROOT / "examples" / "trade_show_example.csv"))
        self.assertEqual(len(rows), 3)
        plan = ts.build_plan(rows)
        self.assertEqual([p["interest"] for p in plan], ["高", "中", "低"])

    def test_csv_leads_example_no_interest_defaults_low(self):
        # leads_example.csv 没有 interest 列：10 行里 2 行没留联系方式被跳过，
        # 剩下 8 行全按「低」处理；contact 列的职位词不算联系方式。
        rows = ts.read_exhibitors(
            str(REPO_ROOT / "examples" / "leads_example.csv"))
        self.assertEqual(len(rows), 8)
        self.assertTrue(all(r["interest"] == "低" for r in rows))
        self.assertEqual(rows[0]["company"], "【示例】海湾轮胎贸易")

    def test_csv_missing_company_column(self):
        path = self._write_csv([["【示例】甲公司", "Saudi Arabia", "TBR",
                                 "a@sample.example", "高"]],
                               header=("name", "country", "product",
                                       "contact", "interest"))
        with self.assertRaises(ts.TradeShowError):
            ts.read_exhibitors(path)

    def test_csv_header_only_no_rows(self):
        path = self._write_csv([])
        with self.assertRaises(ts.TradeShowError):
            ts.read_exhibitors(path)

    def test_csv_file_not_found(self):
        with self.assertRaises(ts.TradeShowError):
            ts.read_exhibitors("no_such_file_ever.csv")

    def test_csv_contact_role_does_not_count(self):
        # contact 列只写了职位、email/phone 都空着 → 这行排不进来
        path = self._write_csv([
            ["【示例】只有职位的", "Saudi Arabia", "TBR 12.00R20",
             "purchasing manager", "高"],
        ])
        with self.assertRaises(ts.TradeShowError):
            ts.read_exhibitors(path)


class TestValidation(unittest.TestCase):
    def test_empty_list_raises(self):
        with self.assertRaises(ts.TradeShowError):
            ts.build_plan([])

    def test_no_contact_raises(self):
        with self.assertRaises(ts.TradeShowError):
            exhibitor("【示例】没留联系方式的", "高")

    def test_bad_email_raises(self):
        with self.assertRaises(ts.TradeShowError):
            exhibitor("【示例】邮箱写错的", "高", email="not-an-email")

    def test_short_phone_raises(self):
        with self.assertRaises(ts.TradeShowError):
            exhibitor("【示例】电话太短的", "高", phone="123")

    def test_bad_interest_raises(self):
        with self.assertRaises(ts.TradeShowError):
            exhibitor("【示例】兴趣度乱填的", "很高", email="a@sample.example")

    def test_empty_interest_defaults_low(self):
        ex = exhibitor("【示例】没填兴趣度的", "", email="a@sample.example")
        self.assertEqual(ex["interest"], "低")
        self.assertEqual(ex["tier"], "T2")


class TestJsonOutput(unittest.TestCase):
    def test_json_parses_and_sorted(self):
        plan = ts.build_plan(three_mixed())
        payload = json.loads(ts.render_json(plan, "examples/trade_show_example.csv"))
        self.assertEqual(payload["total"], 3)
        self.assertEqual(payload["interest_counts"], {"高": 1, "中": 1, "低": 1})
        self.assertEqual([e["company"] for e in payload["exhibitors"]],
                         ["【示例】海湾轮胎贸易", "【示例】迪拜轮毂行",
                          "【示例】尼罗河商贸"])
        for entry in payload["exhibitors"]:
            self.assertEqual(len(entry["steps"]), 3)
            self.assertEqual([s["offset"] for s in entry["steps"]],
                             ["T+2h", "T+12h", "T+24h"])
            self.assertIn("outreach_command", entry["first_touch"])
        # 时间点只写相对时间：三档窗口与 offset 里不能出现具体日期
        # （generated_at 是生成时间戳，不算跟进日期，不管它）
        self.assertEqual(payload["windows"],
                         ["会后 2 小时内（T+2h）", "会后 12 小时内（T+12h）",
                          "会后 24 小时内（T+24h）"])
        for entry in payload["exhibitors"]:
            for step in entry["steps"]:
                self.assertNotRegex(step["window"], r"\d{4}-\d{2}-\d{2}")
                self.assertNotRegex(step["offset"], r"\d{4}-\d{2}-\d{2}")


class TestCli(unittest.TestCase):
    def test_cli_single_add(self):
        rc, out = run_cli("--add", "【示例】海湾轮胎贸易",
                          "--country", "Saudi Arabia",
                          "--product", "TBR 12.00R20",
                          "--interest", "高",
                          "--email", "demo01@sample.example")
        self.assertEqual(rc, 0)
        self.assertIn("【示例】海湾轮胎贸易", out)
        self.assertIn("会后 2 小时内", out)
        self.assertIn("会后 12 小时内", out)
        self.assertIn("会后 24 小时内", out)

    def test_cli_csv_json(self):
        rc, out = run_cli("--csv", "examples/trade_show_example.csv",
                          "--format", "json")
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload["total"], 3)
        self.assertEqual([e["interest"] for e in payload["exhibitors"]],
                         ["高", "中", "低"])

    def test_cli_csv_and_add_combine(self):
        rc, out = run_cli("--csv", "examples/trade_show_example.csv",
                          "--add", "【示例】后补的",
                          "--country", "Nigeria",
                          "--product", "TBR 11.00R20",
                          "--interest", "高",
                          "--email", "extra@sample.example")
        self.assertEqual(rc, 0)
        self.assertIn("共 4 家", out)
        self.assertIn("【示例】后补的", out)

    def test_cli_no_args_human_error(self):
        rc, out = run_cli()
        self.assertNotEqual(rc, 0)
        self.assertIn("错误", out)
        self.assertNotIn("Traceback", out)

    def test_cli_invalid_interest_human_error(self):
        rc, out = run_cli("--add", "【示例】测试公司",
                          "--interest", "很高",
                          "--email", "demo01@sample.example")
        self.assertNotEqual(rc, 0)
        self.assertIn("错误", out)
        self.assertIn("高/中/低", out)
        self.assertNotIn("Traceback", out)

    def test_cli_no_contact_human_error(self):
        rc, out = run_cli("--add", "【示例】测试公司", "--interest", "高")
        self.assertNotEqual(rc, 0)
        self.assertIn("错误", out)
        self.assertNotIn("Traceback", out)

    def test_cli_help_has_real_examples(self):
        rc, out = run_cli("--help")
        self.assertEqual(rc, 0)
        self.assertIn("examples/trade_show_example.csv", out)
        self.assertIn("demo01@sample.example", out)


class TestDirectoryRead(unittest.TestCase):
    """--backcheck mode: an official directory is a raw list — rows without
    a contact stay as 待核实 placeholders, only empty-name / duplicate rows
    are skipped, each with an explicit reason. Nothing is dropped silently."""

    def _write_directory(self, rows, header=("company", "country", "product",
                                              "contact", "interest")):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                          encoding="utf-8", newline="")
        writer = csv.writer(tmp)
        writer.writerow(header)
        writer.writerows(rows)
        tmp.close()
        return tmp.name

    def _mixed_directory(self):
        # 8 rows: 2 ready, 4 pending, 2 skipped (1 duplicate, 1 empty name).
        return self._write_directory([
            ["【示例】甲公司", "Saudi Arabia", "TBR 12.00R20",
             "a@sample.example", "高"],
            ["【示例】乙公司", "", "PCR 195/65R15",
             "+000 00 000 0000", ""],
            ["【示例】丙公司", "Egypt", "PCR tubes", "", ""],
            ["【示例】丁公司", "UAE", "TBR 11.00R20", "", ""],
            [" 【示例】甲公司 ", "Saudi Arabia", "TBR 12.00R20",
             "a@sample.example", "高"],  # duplicate (spaces trimmed)
            ["", "UAE", "TBR", "", "低"],  # empty company name
            ["【示例】戊公司", "Nigeria", "TBR 12.00R20",
             "not-an-email", "很高"],  # bad email + bad interest: kept, noted
            ["【示例】己公司", "Kenya", "PCR tubes",
             "purchasing manager", ""],  # role only, not a contact
        ])

    def test_mixed_directory_counts(self):
        directory = ts.read_directory(self._mixed_directory())
        summary = ts.summarize_directory(directory)
        self.assertEqual(summary["total"], 8)
        self.assertEqual(summary["ready"], 2)
        self.assertEqual(summary["pending"], 4)
        self.assertEqual(summary["skipped"], 2)
        self.assertEqual(summary["missing_country"], 1)
        self.assertEqual(summary["ready"] + summary["pending"]
                         + summary["skipped"], summary["total"])

    def test_no_contact_row_is_kept_as_pending(self):
        # Key difference from read_exhibitors: a directory row without a
        # contact is a backcheck task, not a reason to drop the row.
        directory = ts.read_directory(self._mixed_directory())
        by_company = {d["company"]: d for d in directory
                      if d["status"] != ts.DIR_STATUS_SKIPPED}
        self.assertEqual(by_company["【示例】丙公司"]["status"], "待核实")
        self.assertEqual(by_company["【示例】丁公司"]["status"], "待核实")

    def test_missing_country_marked_not_verified(self):
        directory = ts.read_directory(self._mixed_directory())
        by_company = {d["company"]: d for d in directory
                      if d["status"] != ts.DIR_STATUS_SKIPPED}
        self.assertEqual(by_company["【示例】乙公司"]["country"], "没核实")
        self.assertEqual(by_company["【示例】乙公司"]["status"], "已处理")
        self.assertIn("国家没核实", by_company["【示例】乙公司"]["note"])

    def test_duplicate_and_empty_name_skipped_with_reason(self):
        directory = ts.read_directory(self._mixed_directory())
        skipped = [d for d in directory if d["status"] == "跳过"]
        self.assertEqual(len(skipped), 2)
        by_reason = {d["reason"] for d in skipped}
        self.assertTrue(any("重名" in r for r in by_reason))
        self.assertTrue(any("公司名为空" in r for r in by_reason))
        dup = [d for d in skipped if "重名" in d["reason"]][0]
        self.assertEqual(dup["line"], 6)  # source line, header is line 1
        self.assertIn("第 2 行", dup["reason"])

    def test_bad_email_and_bad_interest_do_not_stop_batch(self):
        # Invalid email / unrecognized interest are treated as "not filled",
        # noted on the row, and the batch keeps running — no exception.
        directory = ts.read_directory(self._mixed_directory())
        by_company = {d["company"]: d for d in directory
                      if d["status"] != ts.DIR_STATUS_SKIPPED}
        wu = by_company["【示例】戊公司"]
        self.assertEqual(wu["status"], "待核实")
        self.assertEqual(wu["contact"], "")
        self.assertIn("无法识别", wu["note"])

    def test_directory_missing_company_column(self):
        path = self._write_directory(
            [["【示例】甲公司", "Saudi Arabia", "TBR", "a@sample.example", "高"]],
            header=("name", "country", "product", "contact", "interest"))
        with self.assertRaises(ts.TradeShowError):
            ts.read_directory(path)

    def test_directory_header_only_no_rows(self):
        with self.assertRaises(ts.TradeShowError):
            ts.read_directory(self._write_directory([]))


class TestBackcheckRows(unittest.TestCase):
    def _directory(self):
        path = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                           encoding="utf-8", newline="")
        writer = csv.writer(path)
        writer.writerow(("company", "country", "product", "contact"))
        writer.writerows([
            ["【示例】甲公司", "Saudi Arabia", "TBR 12.00R20",
             "a@sample.example"],
            ["【示例】乙公司", "UAE", "PCR 195/65R15", ""],
            ["【示例】甲公司", "Saudi Arabia", "TBR 12.00R20",
             "a@sample.example"],
        ])
        path.close()
        return ts.read_directory(path.name)

    def test_placeholder_rows_numbered_in_source_order(self):
        rows = ts.build_backcheck_rows(self._directory())
        self.assertEqual(len(rows), 2)  # duplicate gets no placeholder row
        self.assertEqual([r["seq"] for r in rows], [1, 2])
        self.assertEqual([r["company"] for r in rows],
                         ["【示例】甲公司", "【示例】乙公司"])
        self.assertEqual([r["status"] for r in rows], ["已处理", "待核实"])

    def test_unverified_fields_marked_not_verified(self):
        rows = ts.build_backcheck_rows(self._directory())
        for r in rows:
            self.assertEqual(r["website"], "没核实")
            self.assertEqual(r["decision_maker"], "没核实")
            self.assertEqual(r["import_record"], "没核实")
        # No contact on file -> contact is also marked, not invented.
        self.assertEqual(rows[1]["contact"], "没核实")


class TestBackcheckRender(unittest.TestCase):
    def _setup(self):
        directory = ts.read_directory(
            TestDirectoryRead()._mixed_directory())
        summary = ts.summarize_directory(directory)
        rows = ts.build_backcheck_rows(directory)
        return rows, summary

    def test_json_parses_with_summary_and_rows(self):
        rows, summary = self._setup()
        payload = json.loads(ts.render_backcheck_json(
            rows, summary, "my_directory.csv"))
        self.assertEqual(payload["mode"], "backcheck")
        self.assertEqual(payload["summary"]["total"], 8)
        self.assertEqual(len(payload["rows"]), 6)
        self.assertEqual(len(payload["summary"]["skipped_rows"]), 2)
        self.assertTrue(all("line" in s and "reason" in s
                            for s in payload["summary"]["skipped_rows"]))

    def test_csv_worksheet_round_trips(self):
        rows, summary = self._setup()
        text = ts.render_backcheck_csv(rows)
        parsed = list(csv.DictReader(io.StringIO(text)))
        self.assertEqual(len(parsed), 6)
        self.assertEqual(list(parsed[0].keys()), ts.BACKCHECK_COLUMNS)
        self.assertEqual([r["seq"] for r in parsed],
                         ["1", "2", "3", "4", "5", "6"])
        # Placeholder columns are marked, never filled with invented data.
        self.assertTrue(all(r["website"] == "没核实" for r in parsed))
        self.assertTrue(all(r["decision_maker"] == "没核实" for r in parsed))
        self.assertTrue(all(r["import_record"] == "没核实" for r in parsed))
        # Skipped rows are not in the worksheet (they live in the summary).
        self.assertNotIn("重名", text)

    def test_table_shows_counts_and_skipped_reasons(self):
        rows, summary = self._setup()
        text = ts.render_backcheck_table(rows, summary, "my_directory.csv")
        self.assertIn("共 8 家", text)
        self.assertIn("已处理 2 家", text)
        self.assertIn("待核实 4 家", text)
        self.assertIn("跳过 2 家", text)
        self.assertIn("重名", text)
        self.assertIn("公司名为空", text)
        self.assertIn("【示例】丙公司", text)


class TestDirectoryPerf1021(unittest.TestCase):
    """1021-row smoke test (Dubai-show scale): fictional generated rows,
    mixed dirty data, whole pipeline must finish in seconds, counts exact."""

    def _generate_1021(self):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                          encoding="utf-8", newline="")
        writer = csv.writer(tmp)
        writer.writerow(("company", "country", "product", "contact",
                         "interest"))
        for i in range(1021):
            company = "【示例】展商 %04d" % (i + 1)
            if i == 100 or i == 500:
                company = "【示例】展商 0001"  # duplicate of row 1
            if i == 900:
                company = ""  # empty name
            country = "" if i % 50 == 0 else "UAE"
            contact = "" if i % 7 == 0 else "ex%04d@sample.example" % (i + 1)
            writer.writerow([company, country, "TBR 12.00R20", contact, ""])
        tmp.close()
        return tmp.name

    def test_1021_rows_pipeline_fast_and_exact(self):
        path = self._generate_1021()
        start = time.monotonic()
        directory = ts.read_directory(path)
        summary = ts.summarize_directory(directory)
        rows = ts.build_backcheck_rows(directory)
        text = ts.render_backcheck_csv(rows)
        elapsed = time.monotonic() - start
        # i%7==0 -> 146 pending (none of the 3 skipped rows is divisible by
        # 7); i%50==0 -> 21 missing-country, minus the 3 skipped rows that
        # are also multiples of 50 (i==100, 500, 900) -> 18.
        self.assertEqual(summary["total"], 1021)
        self.assertEqual(summary["ready"], 872)
        self.assertEqual(summary["pending"], 146)
        self.assertEqual(summary["skipped"], 3)
        self.assertEqual(summary["missing_country"], 18)
        self.assertEqual(len(rows), 1018)
        self.assertEqual(rows[0]["seq"], 1)
        self.assertEqual(rows[-1]["seq"], 1018)
        self.assertEqual(rows[0]["company"], "【示例】展商 0001")
        self.assertEqual(rows[-1]["company"], "【示例】展商 1021")
        self.assertEqual(len(text.splitlines()), 1019)  # header + 1018 rows
        self.assertLess(elapsed, 5.0, "1021-row pipeline took %.2fs" % elapsed)


class TestBackcheckCli(unittest.TestCase):
    def _write_directory(self, rows):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                          encoding="utf-8", newline="")
        writer = csv.writer(tmp)
        writer.writerow(("company", "country", "product", "contact"))
        writer.writerows(rows)
        tmp.close()
        return tmp.name

    def test_cli_backcheck_json(self):
        path = self._write_directory([
            ["【示例】甲公司", "Saudi Arabia", "TBR", "a@sample.example"],
            ["【示例】乙公司", "UAE", "PCR", ""],
        ])
        rc, out = run_cli("--backcheck", path, "--format", "json")
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload["summary"]["total"], 2)
        self.assertEqual(payload["summary"]["ready"], 1)
        self.assertEqual(payload["summary"]["pending"], 1)

    def test_cli_backcheck_csv_out_file(self):
        path = self._write_directory([
            ["【示例】甲公司", "Saudi Arabia", "TBR", "a@sample.example"],
            ["【示例】乙公司", "UAE", "PCR", ""],
        ])
        out_path = tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False).name
        rc, out = run_cli("--backcheck", path, "--format", "csv",
                          "--out", out_path)
        self.assertEqual(rc, 0)
        with open(out_path, encoding="utf-8") as f:
            parsed = list(csv.DictReader(f))
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["company"], "【示例】甲公司")
        self.assertEqual(parsed[0]["website"], "没核实")

    def test_cli_backcheck_table(self):
        path = self._write_directory([
            ["【示例】甲公司", "Saudi Arabia", "TBR", "a@sample.example"],
            ["【示例】乙公司", "UAE", "PCR", ""],
        ])
        rc, out = run_cli("--backcheck", path)
        self.assertEqual(rc, 0)
        self.assertIn("共 2 家", out)
        self.assertIn("已处理 1 家", out)
        self.assertIn("待核实 1 家", out)

    def test_cli_backcheck_does_not_mix_with_csv(self):
        path = self._write_directory([
            ["【示例】甲公司", "Saudi Arabia", "TBR", "a@sample.example"],
        ])
        rc, out = run_cli("--backcheck", path,
                          "--csv", "examples/trade_show_example.csv")
        self.assertNotEqual(rc, 0)
        self.assertIn("错误", out)
        self.assertNotIn("Traceback", out)

    def test_cli_csv_format_only_in_backcheck_mode(self):
        rc, out = run_cli("--csv", "examples/trade_show_example.csv",
                          "--format", "csv")
        self.assertNotEqual(rc, 0)
        self.assertIn("错误", out)
        self.assertIn("--backcheck", out)
        self.assertNotIn("Traceback", out)

    def test_cli_backcheck_help_mentions_mode(self):
        rc, out = run_cli("--help")
        self.assertEqual(rc, 0)
        self.assertIn("--backcheck", out)


class TestRealFormatDirectory(unittest.TestCase):
    """Real-format readiness: the official Dubai list is a web search page
    (no official downloadable CSV — real file format not verified), and
    the 2016 official PDF lists Exhibitor Name / Country / Product
    Section / Stand Number. The reader must accept that shape instead
    of failing on the header, and carry booth / product section /
    website over instead of dropping them."""

    def _write(self, rows, header, delimiter=","):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                          encoding="utf-8", newline="")
        writer = csv.writer(tmp, delimiter=delimiter)
        writer.writerow(header)
        writer.writerows(rows)
        tmp.close()
        return tmp.name

    def test_real_format_header_aliases(self):
        path = self._write([
            ["【示例】展商甲", "United Arab Emirates", "Tyres & Batteries",
             "S-0001", "ex0001@sample.example",
             "https://www.sample.example/ex0001"],
            ["【示例】展商乙", "China", "Parts & Components",
             "S-0002", "", ""],
        ], header=("Exhibitor Name", "Country", "Product Section",
                   "Stand Number", "E-mail", "Website"))
        directory = ts.read_directory(path)
        summary = ts.summarize_directory(directory)
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["ready"], 1)
        self.assertEqual(summary["pending"], 1)
        self.assertEqual(summary["missing_booth"], 0)
        rows = ts.build_backcheck_rows(directory)
        self.assertEqual(rows[0]["booth"], "S-0001")
        self.assertEqual(rows[0]["product"], "Tyres & Batteries")
        # A website on file is used as-is, not re-marked not verified.
        self.assertEqual(rows[0]["website"],
                         "https://www.sample.example/ex0001")
        self.assertEqual(rows[1]["booth"], "S-0002")
        self.assertEqual(rows[1]["website"], "没核实")
        self.assertEqual(rows[1]["status"], "待核实")
        self.assertEqual(rows[1]["decision_maker"], "没核实")
        self.assertEqual(rows[1]["import_record"], "没核实")

    def test_company_name_alias_for_followup_reader(self):
        path = self._write([
            ["【示例】甲公司", "Saudi Arabia", "TBR 12.00R20",
             "a@sample.example", "高"],
        ], header=("Company Name", "Country", "Product", "Contact",
                   "Interest"))
        rows = ts.read_exhibitors(path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["company"], "【示例】甲公司")

    def test_semicolon_delimited_export(self):
        path = self._write([
            ["【示例】展商甲", "UAE", "Tyres & Batteries", "S-0001",
             "ex0001@sample.example"],
            ["【示例】展商乙", "China", "Parts & Components", "S-0002", ""],
        ], header=("Exhibitor Name", "Country", "Product Section",
                   "Stand Number", "Email"), delimiter=";")
        directory = ts.read_directory(path)
        summary = ts.summarize_directory(directory)
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["ready"], 1)
        self.assertEqual(summary["pending"], 1)
        self.assertEqual(directory[0]["booth"], "S-0001")

    def test_same_company_different_booth_kept(self):
        # One company, two stands / two brands: both rows are kept, the
        # second is noted. Same company, same booth: still a duplicate.
        path = self._write([
            ["【示例】展商甲", "UAE", "Tyres & Batteries", "S-0001",
             "ex0001@sample.example"],
            ["【示例】展商甲", "UAE", "Oils & Lubricants", "S-0002",
             "ex0001@sample.example"],
            ["【示例】展商甲", "UAE", "Tyres & Batteries", "S-0001",
             "ex0001@sample.example"],
        ], header=("Exhibitor Name", "Country", "Product Section",
                   "Stand Number", "Email"))
        directory = ts.read_directory(path)
        summary = ts.summarize_directory(directory)
        self.assertEqual(summary["total"], 3)
        self.assertEqual(summary["ready"], 2)
        self.assertEqual(summary["skipped"], 1)
        kept = [d for d in directory if d["status"] != "跳过"]
        self.assertEqual([d["booth"] for d in kept], ["S-0001", "S-0002"])
        self.assertIn("不同展位", kept[1]["note"])

    def test_location_column_parses_country(self):
        path = self._write([
            ["【示例】展商甲", "Sharjah, United Arab Emirates",
             "Tyres & Batteries", "S-0001", "ex0001@sample.example"],
            ["【示例】展商乙", "Dubai", "Parts & Components", "S-0002", ""],
        ], header=("Exhibitor Name", "Location", "Product Section",
                   "Stand Number", "Email"))
        # Second row has only a city: country stays not verified, city noted.
        path2 = self._write([
            ["【示例】展商乙", "Dubai", "Parts & Components", "S-0002", ""],
        ], header=("Exhibitor Name", "City", "Product Section",
                   "Stand Number", "Email"))
        directory = ts.read_directory(path)
        self.assertEqual(directory[0]["country"], "United Arab Emirates")
        directory2 = ts.read_directory(path2)
        self.assertEqual(directory2[0]["country"], "没核实")
        self.assertIn("Dubai", directory2[0]["note"])


class TestPendingOnly(unittest.TestCase):
    """--pending-only: export only the 待核实 queue (rows with no usable
    contact), without dropping them from the full worksheet. Seq numbers
    stay the full-list numbers so the queue lines up with the full sheet."""

    def _write_directory(self, rows):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                          encoding="utf-8", newline="")
        writer = csv.writer(tmp)
        writer.writerow(("company", "country", "product", "contact"))
        writer.writerows(rows)
        tmp.close()
        return tmp.name

    def _three_rows(self):
        return self._write_directory([
            ["【示例】甲公司", "Saudi Arabia", "TBR", "a@sample.example"],
            ["【示例】乙公司", "UAE", "PCR", ""],
            ["【示例】丙公司", "Egypt", "PCR tubes", ""],
        ])

    def test_pending_only_rows_keep_full_seq(self):
        directory = ts.read_directory(self._three_rows())
        rows = ts.build_backcheck_rows(directory, pending_only=True)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["status"] == "待核实" for r in rows))
        self.assertEqual([r["seq"] for r in rows], [2, 3])
        self.assertEqual([r["company"] for r in rows],
                         ["【示例】乙公司", "【示例】丙公司"])

    def test_cli_pending_only_csv(self):
        rc, out = run_cli("--backcheck", self._three_rows(),
                          "--format", "csv", "--pending-only")
        self.assertEqual(rc, 0)
        parsed = list(csv.DictReader(io.StringIO(out)))
        self.assertEqual(len(parsed), 2)
        self.assertEqual([r["seq"] for r in parsed], ["2", "3"])
        self.assertNotIn("【示例】甲公司", out)

    def test_cli_pending_only_json_keeps_full_summary(self):
        rc, out = run_cli("--backcheck", self._three_rows(),
                          "--format", "json", "--pending-only")
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertTrue(payload["pending_only"])
        self.assertEqual(payload["summary"]["total"], 3)
        self.assertEqual(payload["summary"]["pending"], 2)
        self.assertEqual(len(payload["rows"]), 2)

    def test_cli_pending_only_without_backcheck_errors(self):
        rc, out = run_cli("--csv", "examples/trade_show_example.csv",
                          "--pending-only")
        self.assertNotEqual(rc, 0)
        self.assertIn("错误", out)
        self.assertIn("--backcheck", out)
        self.assertNotIn("Traceback", out)


class TestRealFormatSimulation1021(unittest.TestCase):
    """Simulation CSV in the real-format shape (SIMULATED format — the
    real official file format is not verified): 1,021 rows, header
    Exhibitor Name / Country / Product Section / Stand Number / Email /
    Website, fictional companies only. Whole pipeline end to end, exact
    counts, plus the pending-only queue export."""

    SECTIONS = ["Tyres & Batteries", "Parts & Components",
                "Oils & Lubricants", "Electronics & Systems"]
    COUNTRIES = ["United Arab Emirates", "China", "India", "Turkey",
                 "Germany"]

    def _generate_1021(self):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                          encoding="utf-8", newline="")
        writer = csv.writer(tmp)
        writer.writerow(("Exhibitor Name", "Country", "Product Section",
                         "Stand Number", "Email", "Website"))
        for i in range(1021):
            company = "【示例】展商 %04d" % (i + 1)
            booth = "S-%04d" % (i + 1)
            if i in (100, 500):
                company = "【示例】展商 0001"  # same booth as row 1: duplicate
                booth = "S-0001"
            if i == 300:
                company = "【示例】展商 0001"  # different booth: kept
                booth = "S-0301"
            if i == 900:
                company = ""  # empty name: skipped
            country = "" if i % 50 == 0 else self.COUNTRIES[i % 5]
            email = "" if i % 7 == 0 else "ex%04d@sample.example" % (i + 1)
            website = ("https://www.sample.example/ex%04d" % (i + 1)
                       if i % 3 == 0 else "")
            writer.writerow([company, country, self.SECTIONS[i % 4],
                             booth, email, website])
        tmp.close()
        return tmp.name

    def test_1021_simulation_exact_counts(self):
        path = self._generate_1021()
        start = time.monotonic()
        directory = ts.read_directory(path)
        summary = ts.summarize_directory(directory)
        rows = ts.build_backcheck_rows(directory)
        pending = ts.build_backcheck_rows(directory, pending_only=True)
        text = ts.render_backcheck_csv(rows)
        pending_text = ts.render_backcheck_csv(pending)
        elapsed = time.monotonic() - start
        # i%7==0 -> 146 pending (none of the 3 skipped rows is divisible
        # by 7); i%50==0 -> 21 missing-country, minus the 3 skipped rows
        # that are also multiples of 50 (i==100, 500, 900) -> 18.
        self.assertEqual(summary["total"], 1021)
        self.assertEqual(summary["ready"], 872)
        self.assertEqual(summary["pending"], 146)
        self.assertEqual(summary["skipped"], 3)
        self.assertEqual(summary["missing_country"], 18)
        self.assertEqual(summary["missing_booth"], 0)
        self.assertEqual(len(rows), 1018)
        self.assertEqual(rows[0]["seq"], 1)
        self.assertEqual(rows[-1]["seq"], 1018)
        self.assertEqual(rows[0]["company"], "【示例】展商 0001")
        self.assertEqual(rows[-1]["company"], "【示例】展商 1021")
        self.assertEqual(len(text.splitlines()), 1019)  # header + 1018 rows
        # Same company at a different booth is kept, not dropped.
        dupes = [r for r in rows if r["company"] == "【示例】展商 0001"]
        self.assertEqual(len(dupes), 2)
        self.assertEqual([r["booth"] for r in dupes], ["S-0001", "S-0301"])
        self.assertIn("不同展位", dupes[1]["note"])
        # Website carried over from the directory when present (i%3==0,
        # minus the skipped i==900): 340 rows.
        with_site = [r for r in rows if r["website"] != "没核实"]
        self.assertEqual(len(with_site), 340)
        self.assertEqual(rows[0]["website"],
                         "https://www.sample.example/ex0001")
        self.assertEqual(rows[1]["product"], "Parts & Components")
        # Pending-only queue: 146 rows, full-list seq numbers, CSV lines.
        self.assertEqual(len(pending), 146)
        self.assertTrue(all(r["status"] == "待核实" for r in pending))
        self.assertEqual(pending[0]["seq"], 1)
        self.assertEqual(pending[-1]["seq"], 1013)
        self.assertEqual(len(pending_text.splitlines()), 147)
        self.assertLess(elapsed, 5.0, "1021-row pipeline took %.2fs" % elapsed)


if __name__ == "__main__":
    unittest.main()
