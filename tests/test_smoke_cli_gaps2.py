"""Smoke test, third layer: CLI flags no other test ever invokes (round 2).

Why this file exists / 为什么要有这个文件：
  tests/test_smoke_cli_gaps.py 补了第一批 9 个缺口之后，再逐个核对
  15 个脚本的 --help，又找出下面这些一次都没以 CLI 形式跑过的组合——
  有些只在函数层测过（--local/--contingency/--fx 的函数层），
  有些连函数层都没有（--insurance-rate/--currency/--validity/
  --payment/--website-updated/--employees/--trade-role/
  --legal-name-match/--payee-mismatch/--address/--sender/
  --market(generic)/--avoid-weekend/--company(nudge)，
  以及 lead_score 的 --country 筛选、
  followup/landed/quote/tire_pack 的 --out 落盘）。
  每条都是照抄 --help 里的例子或只加一个没盖到的 flag。

Scope / 范围：
  * Only flags that no test file and no CI step invokes as a CLI arg.
    只收全套测试 + CI 里一次都没以 CLI 形式跑过的 flag。
  * --out 一律写进 tempfile，不往仓库里写东西；lead_score 的 run log
    走仓库 logs/（git-ignored），与现有测试同一口径。
  * All data is fictional: 【示例】 prefix, sample.example domain,
    +000 placeholder phones.
    数据全是虚构的，不往仓库里写东西。
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
EXAMPLES = REPO_ROOT / "examples"


def _run(name, args, cwd=REPO_ROOT):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / (name + ".py"))] + args,
        capture_output=True, text=True, cwd=cwd)


class TestSmokeCliGaps2(unittest.TestCase):
    def test_anchor_price_insurance_rate_overrides_percent(self):
        # --insurance-rate is the advanced entry: 0.0015 must win over
        # --insurance 30 (which alone exits 1 with a human error).
        # --insurance-rate 是高级入口：给了它，--insurance 30 必须被覆盖，
        # 保本价回到默认费率那档 34.90，而不是按 30% 算。
        proc = _run("anchor_price",
                    ["--comp-low", "38", "--comp-high", "46",
                     "--comp-median", "42", "--cost", "28",
                     "--freight", "6", "--insurance", "30",
                     "--insurance-rate", "0.0015", "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)["anchor_price"]
        self.assertEqual(data["insurance_rate"], 0.0015)
        self.assertEqual(data["cif_floor"], 34.90)

    def test_anchor_price_contingency_flag(self):
        # --contingency appears nowhere in tests/: 0.05 must lift the
        # break-even CIF from 34.90 to 35.46.
        # --contingency 在全套测试里一次没出现过；0.05 必须把保本价从
        # 34.90 抬到 35.46。
        proc = _run("anchor_price",
                    ["--comp-low", "38", "--comp-high", "46",
                     "--comp-median", "42", "--cost", "28",
                     "--freight", "6", "--contingency", "0.05",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)["anchor_price"]
        self.assertEqual(data["contingency"], 0.05)
        self.assertEqual(data["cif_floor"], 35.46)

    def test_anchor_price_local_tax_help_example(self):
        # Copied from anchor_price --help: --local 5 --tax-rate 13.
        # The documented numbers must come out exactly.
        # 照抄 --help 里的例子；文档里那几个数必须原样算出来。
        proc = _run("anchor_price",
                    ["--comp-low", "38", "--comp-high", "46",
                     "--comp-median", "42", "--cost", "28",
                     "--freight", "6", "--duty", "10",
                     "--local", "5", "--tax-rate", "13",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)["anchor_price"]
        self.assertEqual(data["cost_base"], 33.84)
        self.assertEqual(data["cif_floor"], 39.91)
        tax_incl = [t["price_cif_tax_incl"] for t in data["tiers"]]
        self.assertEqual(tax_incl, [46.04, 47.46, 48.88])

    def test_anchor_price_currency_validity_payment_round_trip(self):
        # --currency / --validity / --payment never run as CLI flags;
        # they must round-trip into the JSON meta block.
        # --currency/--validity/--payment 三个 flag 一次没跑过；
        # 它们必须原样进 JSON 的 meta。
        proc = _run("anchor_price",
                    ["--comp-low", "38", "--comp-high", "46",
                     "--comp-median", "42", "--cost", "28",
                     "--freight", "6", "--currency", "CNY",
                     "--validity", "7", "--payment", "T/T 30% 定金",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        meta = json.loads(proc.stdout)["meta"]
        self.assertEqual(meta["currency"], "CNY")
        self.assertEqual(meta["quote_validity_days"], 7)
        self.assertEqual(meta["payment_terms"], "T/T 30% 定金")

    def test_landed_cost_insurance_rate_unit_currency(self):
        # --insurance-rate / --unit / --currency never run as CLI flags
        # for landed_cost; the rate must land in the JSON inputs.
        # landed_cost 的这三个 flag 一次没跑过；费率必须进 JSON。
        proc = _run("landed_cost",
                    ["--fob", "30", "--freight", "5", "--duty", "10",
                     "--port-charges", "2",
                     "--insurance-rate", "0.0015",
                     "--unit", "箱", "--currency", "CNY",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["meta"]["currency"], "CNY")
        self.assertEqual(data["meta"]["unit"], "箱")
        self.assertEqual(data["meta"]["inputs"]["insurance_rate"], 0.0015)
        self.assertEqual(data["landed_cost"]["insurance_unit"], 0.06)

    def test_landed_cost_out_writes_file(self):
        # --out never runs for landed_cost; the file must hold the same
        # numbers the screen shows.
        # landed_cost 的 --out 一次没跑过；落盘文件里必须有 DDP 总计。
        with tempfile.TemporaryDirectory() as tmp:
            out_file = str(Path(tmp) / "landed.txt")
            proc = _run("landed_cost",
                        ["--fob", "30", "--freight", "5", "--duty", "10",
                         "--port-charges", "2", "--out", out_file])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            text = Path(out_file).read_text(encoding="utf-8")
            self.assertIn("DDP 总计", text)
            self.assertIn("40.56", text)

    def test_quote_engine_fx_converts_cost_once(self):
        # --fx never runs as a CLI flag: CNY 200 x 0.14 must quote exactly
        # like a USD 28 cost (FOB 33.17), not convert twice.
        # --fx 一次没跑过：200 人民币 × 0.14 必须跟 28 美元成本报出同一
        # 个 FOB 33.17，不能换算两次。
        proc = _run("quote_engine",
                    ["--cost", "200", "--currency", "CNY", "--fx", "0.14",
                     "--freight", "6", "--margin", "15",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["meta"]["inputs"]["fx"], 0.14)
        self.assertEqual(data["quote"]["fob_list"], 33.17)

    def test_quote_engine_insurance_rate_local_contingency_combo(self):
        # --insurance-rate / --local / --contingency never run as CLI
        # flags for quote_engine; all three must land in meta.inputs
        # and move the cost base together.
        # quote_engine 的这三个 flag 一次没跑过；三者必须同时进
        # meta.inputs，并且一起推高成本基数。
        proc = _run("quote_engine",
                    ["--cost", "28", "--freight", "6", "--margin", "15",
                     "--insurance-rate", "0.0015", "--local", "5",
                     "--contingency", "0.05", "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        inputs = data["meta"]["inputs"]
        self.assertEqual(inputs["insurance_rate"], 0.0015)
        self.assertEqual(inputs["local"], 5.0)
        self.assertEqual(inputs["contingency"], 0.05)
        self.assertEqual(data["quote"]["cost_base"], 34.4)
        self.assertEqual(data["quote"]["fob_list"], 39.56)
        self.assertEqual(data["quote"]["cif_list"], 45.64)

    def test_quote_engine_out_writes_file(self):
        # --out never runs for quote_engine.
        # quote_engine 的 --out 一次没跑过。
        with tempfile.TemporaryDirectory() as tmp:
            out_file = str(Path(tmp) / "quote.txt")
            proc = _run("quote_engine",
                        ["--cost", "28", "--freight", "6", "--margin", "15",
                         "--out", out_file])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            text = Path(out_file).read_text(encoding="utf-8")
            self.assertIn("FOB 报价", text)
            self.assertIn("33.17", text)

    def test_due_diligence_full_signal_flags_cli(self):
        # --employees / --trade-role / --legal-name-match /
        # --payee-mismatch / --address / --website-updated / --note
        # never run as CLI flags; a full-signal lead must rate A.
        # due_diligence 这串 flag 一次没端到端跑过；信号拉满的客户
        # 必须评到 A，备注原样带出来。
        proc = _run("due_diligence",
                    ["--company", "【示例】海湾轮胎贸易",
                     "--country", "Saudi Arabia",
                     "--product", "TBR 12.00R20",
                     "--website", "sample.example",
                     "--website-updated", "recent",
                     "--years", "18",
                     "--email-domain", "sample.example",
                     "--phone", "+000 00 000 0000",
                     "--address", "Jeddah, Saudi Arabia",
                     "--source", "trade_show",
                     "--social", "active",
                     "--customs-record", "yes",
                     "--import-match", "yes",
                     "--contact-role", "purchasing manager",
                     "--employees", "45",
                     "--trade-role", "importer",
                     "--legal-name-match", "yes",
                     "--sanctions", "clear",
                     "--adverse", "no",
                     "--payment", "prepaid",
                     "--payee-mismatch", "no",
                     "--note", "展会上聊过，【示例】未核实",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["rating"], "A")
        self.assertEqual(data["t_tier"], "T0")
        self.assertEqual(data["user_note"], "展会上聊过，【示例】未核实")
        self.assertEqual(data["red_flags"], [])

    def test_due_diligence_client_audience_hides_rating(self):
        # --audience client never runs for due_diligence; the client
        # view must not carry the internal rating.
        # due_diligence 的 --audience client 一次没跑过；客户视图
        # 里不许带内部评级。
        proc = _run("due_diligence",
                    ["--company", "【示例】海湾轮胎贸易",
                     "--country", "Saudi Arabia",
                     "--audience", "client", "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertNotIn("rating", data)
        self.assertIn("needed_materials", data)
        self.assertIn("评级与内部判断不对外提供", data["note"])

    def test_followup_avoid_weekend_shifts_saturday_touch(self):
        # --avoid-weekend never runs as a CLI flag: with a Thu start,
        # D2 lands on Sat and must shift to Sun, one day later.
        # --avoid-weekend 一次没跑过：周四起算，D2 落在周六，必须顺延
        # 到周日；不加这个 flag 就留在周六。
        plain = _run("followup_plan",
                     ["--tier", "T0", "--start", "2026-10-08",
                      "--format", "json"])
        shifted = _run("followup_plan",
                       ["--tier", "T0", "--start", "2026-10-08",
                        "--avoid-weekend", "--format", "json"])
        self.assertEqual(plain.returncode, 0, plain.stdout + plain.stderr)
        self.assertEqual(shifted.returncode, 0,
                         shifted.stdout + shifted.stderr)
        plain_steps = json.loads(plain.stdout)["steps"]
        shifted_steps = json.loads(shifted.stdout)["steps"]
        self.assertEqual(plain_steps[1]["date"], "2026-10-10")
        self.assertEqual(shifted_steps[1]["date"], "2026-10-11")
        self.assertIn("已顺延 1 天", shifted_steps[1]["timing_note"])
        self.assertTrue(json.loads(shifted.stdout)["avoid_weekend"])

    def test_followup_generic_market_weekend_is_sat_sun(self):
        # --market generic never runs as a CLI flag: its weekend is
        # Sat+Sun, so the same D2 must shift two days to Monday.
        # --market generic 一次没跑过：它的周末是周六+周日，同一个 D2
        # 必须顺延两天到周一。
        proc = _run("followup_plan",
                    ["--tier", "T0", "--start", "2026-10-08",
                     "--market", "generic", "--avoid-weekend",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["market"], "generic")
        self.assertIn("周六周日", data["market_label"])
        self.assertEqual(data["steps"][1]["date"], "2026-10-12")
        self.assertIn("已顺延 2 天", data["steps"][1]["timing_note"])

    def test_followup_company_flag_plans_one_company(self):
        # --company never runs as a CLI flag; it must replace the
        # whole-tier company list with just that one company.
        # --company 一次没跑过；给了它，计划里只能有这一家公司。
        proc = _run("followup_plan",
                    ["--tier", "T0", "--start", "2026-10-08",
                     "--company", "【示例】海湾轮胎贸易",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["companies"], ["【示例】海湾轮胎贸易"])

    def test_followup_format_csv_writes_to_out(self):
        # --format csv never runs for followup_plan; with --out it must
        # write the worksheet to that path, not the default filename.
        # followup_plan 的 --format csv 一次没跑过；给了 --out 就必须
        # 写到指定路径，别写默认文件名。
        with tempfile.TemporaryDirectory() as tmp:
            out_file = str(Path(tmp) / "plan.csv")
            proc = _run("followup_plan",
                        ["--tier", "T1", "--start", "2026-10-08",
                         "--csv", str(EXAMPLES / "leads_example.csv"),
                         "--market", "generic",
                         "--format", "csv", "--out", out_file])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            lines = Path(out_file).read_text(
                encoding="utf-8-sig").splitlines()
            self.assertTrue(lines[0].startswith("tier,offset"))
            self.assertEqual(len(lines) - 1, 15)

    def test_lead_score_country_filter_and_csv_out(self):
        # --country filter and --format csv never run as CLI flags;
        # Saudi-only must be 5 leads, all Saudi.
        # lead_score 的 --country 筛选和 --format csv 一次没跑过；
        # 只筛沙特必须是 5 条，而且全是沙特。
        proc = _run("lead_score",
                    [str(EXAMPLES / "leads_example.csv"),
                     "--country", "Saudi", "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["total"], 5)
        self.assertTrue(
            all(lead["country"] == "Saudi Arabia"
                for lead in data["leads"]))
        with tempfile.TemporaryDirectory() as tmp:
            out_file = str(Path(tmp) / "saudi.csv")
            proc = _run("lead_score",
                        [str(EXAMPLES / "leads_example.csv"),
                         "--country", "Saudi", "--format", "csv",
                         "--out", out_file])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            lines = Path(out_file).read_text(
                encoding="utf-8-sig").splitlines()
            self.assertTrue(lines[0].startswith("tier,company"))
            self.assertEqual(len(lines) - 1, 5)

    def test_lead_score_detail_format_runs(self):
        # --format detail never runs as a CLI flag; it must print the
        # per-lead score breakdown.
        # lead_score 的 --format detail 一次没跑过；必须打出逐条分数来源。
        proc = _run("lead_score",
                    [str(EXAMPLES / "leads_example.csv"),
                     "--format", "detail"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("【示例】海湾轮胎贸易", proc.stdout)
        self.assertIn("95", proc.stdout)
        self.assertIn("联系方式", proc.stdout)

    def test_market_rules_brazil_and_mexico_cli(self):
        # Only Turkey ever runs as a CLI flag; Brazil and Mexico take
        # different verdict paths and must be exercised end to end.
        # market_rules 的 CLI 只跑过土耳其；巴西和墨西哥走不同的裁决，
        # 必须端到端跑一次。
        brazil = _run("market_rules", ["--country", "Brazil"])
        mexico = _run("market_rules", ["--country", "Mexico"])
        self.assertEqual(brazil.returncode, 0, brazil.stdout + brazil.stderr)
        self.assertEqual(mexico.returncode, 0, mexico.stdout + mexico.stderr)
        self.assertIn("反倾销税", brazil.stdout)
        self.assertIn("先确认转口", brazil.stdout)
        self.assertIn("市场排除", mexico.stdout)
        self.assertIn("别打", mexico.stdout)

    def test_nudge_company_contact_product_overrides(self):
        # --company / --contact / --product never run as CLI flags for
        # nudge; the overrides must show up in the copy.
        # nudge 的 --company/--contact/--product 一次没跑过；换了客户
        # 名、联系人、产品，话术里必须跟着换。
        proc = _run("nudge",
                    ["--day", "D3", "--scenario", "quoted",
                     "--company", "【示例】尼罗河商贸",
                     "--contact", "Sara",
                     "--product", "TBR 11.00R20",
                     "--channel", "email"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("【示例】尼罗河商贸", proc.stdout)
        self.assertIn("Sara", proc.stdout)
        self.assertIn("TBR 11.00R20", proc.stdout)
        self.assertIn("邮件长版", proc.stdout)
        self.assertNotIn("WhatsApp", proc.stdout)

    def test_outreach_sender_replaces_placeholder(self):
        # --sender never runs as a CLI flag; the signature must stop
        # being the [Your Name] placeholder.
        # --sender 一次没跑过；给了落款，签名档不能再是占位符。
        proc = _run("outreach_gen",
                    [str(EXAMPLES / "leads_example.csv"),
                     "--tier", "T0", "--sender", "Jason"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("落款: Jason", proc.stdout)
        self.assertNotIn("[Your Name]", proc.stdout)

    def test_outreach_out_writes_file(self):
        # --out never runs for outreach_gen.
        # outreach_gen 的 --out 一次没跑过。
        with tempfile.TemporaryDirectory() as tmp:
            out_file = str(Path(tmp) / "drafts.md")
            proc = _run("outreach_gen",
                        [str(EXAMPLES / "leads_example.csv"),
                         "--tier", "T0", "--out", out_file])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            text = Path(out_file).read_text(encoding="utf-8")
            self.assertIn("建联文案草稿", text)
            self.assertIn("【示例】海湾轮胎贸易", text)

    def test_tire_pack_out_writes_file(self):
        # --out never runs for tire_pack.
        # tire_pack 的 --out 一次没跑过。
        with tempfile.TemporaryDirectory() as tmp:
            out_file = str(Path(tmp) / "pack.txt")
            proc = _run("tire_pack",
                        ["--size", "11.00R20", "--market", "nigeria",
                         "--out", out_file])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            text = Path(out_file).read_text(encoding="utf-8")
            self.assertIn("轮胎行业包", text)
            self.assertIn("SONCAP", text)


if __name__ == "__main__":
    unittest.main()
