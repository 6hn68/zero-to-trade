#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/nudge.py — 催单话术库 (D3/D7/D14/D30 × 3 场景).

Run: python3 -m unittest discover -s tests -v   (from the repo root)
Only the standard library is used, same rule as the scripts themselves.

All company names in this file are fictional: 【示例】 prefix.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import nudge  # noqa: E402


def run_cli(*args):
    """Run the nudge CLI; return (exit_code, stdout+stderr)."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "nudge.py"), *args],
        capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout + proc.stderr


DAYS = ("D3", "D7", "D14", "D30")
SCENARIOS = ("quoted", "sampled", "negotiating")

# D3 轻提醒：这些施压词一律不许出现（英文/中文各查一遍）。
D3_PRESSURE_EN = ("urgent", "deadline", "final", "last chance", "must", "asap")
D3_PRESSURE_ZH = ("最后", "催", "必须", "赶紧", "截止", "通牒")


class TestAllCombos(unittest.TestCase):
    def test_12_combos_exist(self):
        self.assertEqual(len(nudge._DRAFTS), 12)
        for day in DAYS:
            for scenario in SCENARIOS:
                self.assertIn((day, scenario), nudge._DRAFTS,
                              "缺了 %s × %s 这一条" % (day, scenario))

    def test_every_combo_both_channels_bilingual(self):
        # 4 天数 × 3 场景，WhatsApp + 邮件各一版，每版中英对照齐全。
        for day in DAYS:
            for scenario in SCENARIOS:
                n = nudge.get_nudge(day, scenario)
                for channel in ("whatsapp", "email"):
                    for lang in ("en", "zh"):
                        text = n[channel][lang]
                        self.assertTrue(text.strip(),
                                        "%s/%s/%s/%s 是空的"
                                        % (day, scenario, channel, lang))
                        self.assertNotIn("{contact}", text)
                        self.assertNotIn("{company}", text)
                        self.assertNotIn("{product}", text)
                    self.assertNotEqual(n[channel]["en"], n[channel]["zh"],
                                        "%s/%s/%s 中英文一模一样？"
                                        % (day, scenario, channel))
                self.assertTrue(n["email"]["subject_en"].strip())
                self.assertTrue(n["email"]["subject_zh"].strip())

    def test_product_and_company_interpolated(self):
        n = nudge.get_nudge("D7", "sampled", company="【示例】尼罗河商贸",
                            contact="Sara", product="TBR 11.00R20")
        self.assertIn("TBR 11.00R20", n["whatsapp"]["en"])
        self.assertIn("TBR 11.00R20", n["whatsapp"]["zh"])
        self.assertIn("Sara", n["email"]["en"])
        # D7 版主题行只带产品不带公司名；公司名进 D3 报价版主题行。
        q = nudge.get_nudge("D3", "quoted", company="【示例】尼罗河商贸",
                            contact="Sara", product="TBR 11.00R20")
        self.assertIn("【示例】尼罗河商贸", q["email"]["subject_en"])

    def test_each_day_has_its_own_tone_label(self):
        self.assertEqual(len(set(nudge.TONE[d] for d in DAYS)), 4)
        self.assertEqual(nudge.get_nudge("D3", "quoted")["tone"], "轻提醒")
        self.assertEqual(nudge.get_nudge("D7", "quoted")["tone"], "问进度")
        self.assertIn("三选一", nudge.get_nudge("D14", "quoted")["tone"])
        self.assertIn("留后路", nudge.get_nudge("D30", "quoted")["tone"])


class TestToneLadder(unittest.TestCase):
    def test_d3_has_no_pressure_words(self):
        for scenario in SCENARIOS:
            n = nudge.get_nudge("D3", scenario)
            for channel in ("whatsapp", "email"):
                en = n[channel]["en"].lower()
                for word in D3_PRESSURE_EN:
                    self.assertNotIn(word, en,
                                     "D3/%s/%s 英文里冒出施压词 %r"
                                     % (scenario, channel, word))
                for word in D3_PRESSURE_ZH:
                    self.assertNotIn(word, n[channel]["zh"],
                                     "D3/%s/%s 中文里冒出施压词 %r"
                                     % (scenario, channel, word))

    def test_d30_is_final_but_leaves_the_door_open(self):
        for scenario in SCENARIOS:
            n = nudge.get_nudge("D30", scenario)
            for channel in ("whatsapp", "email"):
                self.assertIn("last", n[channel]["en"].lower(),
                              "D30/%s/%s 英文没写明是最后一封"
                              % (scenario, channel))
                self.assertIn("最后一封", n[channel]["zh"],
                              "D30/%s/%s 中文没写明是最后一封"
                              % (scenario, channel))
                self.assertIn("reach out any time", n[channel]["en"],
                              "D30/%s/%s 英文没留后路句"
                              % (scenario, channel))
                self.assertIn("以后有需要随时找我", n[channel]["zh"],
                              "D30/%s/%s 中文没留后路句"
                              % (scenario, channel))

    def test_d14_offers_three_options_in_both_channels(self):
        # 给台阶三选一：降价 / 换规格 / 延账期，WhatsApp 和邮件两版都得齐。
        for scenario in SCENARIOS:
            n = nudge.get_nudge("D14", scenario)
            for channel in ("whatsapp", "email"):
                en = n[channel]["en"].lower()
                for word in ("price", "spec", "payment terms"):
                    self.assertIn(word, en,
                                  "D14/%s/%s 英文缺了 %r 这一档"
                                  % (scenario, channel, word))
                zh = n[channel]["zh"]
                self.assertIn("降", zh, "D14/%s/%s 中文缺了降价这一档"
                              % (scenario, channel))
                self.assertIn("换规格", zh, "D14/%s/%s 中文缺了换规格这一档"
                              % (scenario, channel))
                self.assertIn("账期", zh, "D14/%s/%s 中文缺了延账期这一档"
                              % (scenario, channel))

    def test_d7_asks_for_progress_not_a_decision(self):
        n = nudge.get_nudge("D7", "quoted")
        self.assertIn("week", n["email"]["en"].lower())
        self.assertIn("一周", n["email"]["zh"])


class TestNormalize(unittest.TestCase):
    def test_day_forms(self):
        self.assertEqual(nudge.normalize_day("D3"), "D3")
        self.assertEqual(nudge.normalize_day("3"), "D3")
        self.assertEqual(nudge.normalize_day("d30"), "D30")

    def test_scenario_aliases(self):
        self.assertEqual(nudge.normalize_scenario("quote"), "quoted")
        self.assertEqual(nudge.normalize_scenario("sample"), "sampled")
        self.assertEqual(nudge.normalize_scenario("price"), "negotiating")
        self.assertEqual(nudge.normalize_scenario("谈价"), "negotiating")

    def test_invalid_day_and_scenario_raise(self):
        with self.assertRaises(ValueError):
            nudge.normalize_day("D5")
        with self.assertRaises(ValueError):
            nudge.normalize_day("tomorrow")
        with self.assertRaises(ValueError):
            nudge.normalize_scenario("ghosted")
        with self.assertRaises(ValueError):
            nudge.get_nudge("D3", "ghosted")

    def test_defaults_are_fictional(self):
        n = nudge.get_nudge("D3", "quoted")
        self.assertTrue(n["company"].startswith("【示例】"))
        self.assertEqual(n["contact"], "Alex")


class TestJsonAndRender(unittest.TestCase):
    def test_json_parses_and_matches_table(self):
        n = nudge.get_nudge("D14", "negotiating")
        payload = json.loads(nudge.render_json(n))
        self.assertEqual(payload["day"], "D14")
        self.assertEqual(payload["scenario"], "negotiating")
        self.assertEqual(payload["tone"], n["tone"])
        self.assertEqual(payload["whatsapp"]["en"], n["whatsapp"]["en"])
        self.assertEqual(payload["email"]["zh"], n["email"]["zh"])
        self.assertIn("stop_rule", payload)
        self.assertIn("followup_plan", payload["followup_plan_note"])

    def test_json_channel_filter(self):
        n = nudge.get_nudge("D7", "sampled")
        payload = json.loads(nudge.render_json(n, channels=("whatsapp",)))
        self.assertIn("whatsapp", payload)
        self.assertNotIn("email", payload)

    def test_table_contains_both_languages_and_stop_rule(self):
        text = nudge.render_table(nudge.get_nudge("D30", "quoted"))
        self.assertIn("D30", text)
        self.assertIn("最后一封", text)
        self.assertIn("以后有需要随时找我", text)
        self.assertIn("reach out any time", text)
        self.assertIn("止损线", text)
        self.assertIn("followup_plan", text)

    def test_get_nudge_is_pure_no_file_written(self):
        import os
        before = set(os.listdir("."))
        nudge.get_nudge("D3", "quoted")
        nudge.render_json(nudge.get_nudge("D7", "sampled"))
        self.assertEqual(before, set(os.listdir(".")))


class TestCLI(unittest.TestCase):
    def test_cli_d3_quoted(self):
        code, out = run_cli("--day", "D3", "--scenario", "quoted")
        self.assertEqual(code, 0)
        self.assertIn("轻提醒", out)
        self.assertIn("did the quote for", out)
        self.assertIn("报价收到没有", out)

    def test_cli_d7_sampled_whatsapp_only(self):
        code, out = run_cli("--day", "D7", "--scenario", "sampled",
                            "--channel", "whatsapp")
        self.assertEqual(code, 0)
        self.assertIn("WhatsApp", out)
        self.assertNotIn("Subject:", out)

    def test_cli_d14_negotiating_json(self):
        code, out = run_cli("--day", "D14", "--scenario", "negotiating",
                            "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["day"], "D14")
        self.assertIn("payment terms", payload["email"]["en"].lower())
        self.assertIn("换规格", payload["whatsapp"]["zh"])

    def test_cli_d30_quoted(self):
        code, out = run_cli("--day", "D30", "--scenario", "quoted")
        self.assertEqual(code, 0)
        self.assertIn("最后一封", out)
        self.assertIn("以后有需要随时找我", out)

    def test_cli_out_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "nudge.json")
            code, out = run_cli("--day", "D3", "--scenario", "quoted",
                                "--format", "json", "--out", path)
            self.assertEqual(code, 0)
            self.assertIn("已写入", out)
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
            self.assertEqual(payload["scenario"], "quoted")

    def test_cli_missing_args_human_error(self):
        code, out = run_cli("--day", "D3")
        self.assertNotEqual(code, 0)
        self.assertIn("--help", out)
        code, out = run_cli()
        self.assertNotEqual(code, 0)
        self.assertIn("--help", out)

    def test_cli_invalid_day_human_error(self):
        code, out = run_cli("--day", "D5", "--scenario", "quoted")
        self.assertNotEqual(code, 0)
        self.assertIn("D3 / D7 / D14 / D30", out)

    def test_cli_invalid_scenario_human_error(self):
        code, out = run_cli("--day", "D3", "--scenario", "ghosted")
        self.assertNotEqual(code, 0)
        self.assertIn("quoted", out)

    def test_cli_help_has_real_examples(self):
        code, out = run_cli("--help")
        self.assertEqual(code, 0)
        self.assertIn("--day D3 --scenario quoted", out)
        self.assertIn("--day D30 --scenario quoted", out)

    def test_reproduce_line_uses_python3_not_bare_python(self):
        # 2026-11-26 route-12: the demo's step-7 output prints a
        # copy-paste reproduce command; bare `python` does not exist on
        # stock Linux (only `python3`), so it must say python3.
        code, out = run_cli("--day", "D7", "--scenario", "quoted")
        self.assertEqual(code, 0)
        self.assertIn("python3 scripts/nudge.py --day D7 --scenario quoted",
                      out)
        self.assertNotIn("python scripts/", out)


class TestDailyList(unittest.TestCase):
    TODAY = "2026-11-22"

    def _rows(self):
        # Overdue, due today, upcoming, stopped — one of each, all fictional.
        return [
            {"company": "【示例】海湾轮胎贸易", "contact": "Alex",
             "product": "TBR 12.00R20", "scenario": "quoted",
             "day0": "2026-11-10", "sent": ["D3"],
             "size": "12.00R20", "market": "saudi"},
            {"company": "【示例】尼罗河商贸", "contact": "Sara",
             "product": "TBR 11.00R20", "scenario": "sampled",
             "day0": "2026-11-19", "sent": []},
            {"company": "【示例】大西洋轮胎", "contact": "Tom",
             "product": "TBR 315/80R22.5", "scenario": "negotiating",
             "day0": "2026-11-21", "sent": []},
            {"company": "【示例】撒哈拉商贸", "contact": "Musa",
             "product": "TBR 295/80R22.5", "scenario": "quoted",
             "day0": "2026-10-15", "sent": ["D3", "D7", "D14", "D30"]},
        ]

    def test_next_nudge_rungs(self):
        self.assertEqual(nudge.next_nudge(2, []), ("D3", "upcoming", 0, 1))
        self.assertEqual(nudge.next_nudge(3, []), ("D3", "due_today", 0, 0))
        self.assertEqual(nudge.next_nudge(5, []), ("D3", "overdue", 2, 0))
        self.assertEqual(nudge.next_nudge(8, ["D3"]), ("D7", "overdue", 1, 0))
        self.assertEqual(nudge.next_nudge(7, ["D3"]), ("D7", "due_today", 0, 0))
        # Nothing sent yet at day 31: the ladder starts at D3, 28 days overdue —
        # it does not jump straight to the D30 last note.
        self.assertEqual(nudge.next_nudge(31, []), ("D3", "overdue", 28, 0))
        self.assertEqual(nudge.next_nudge(31, ["D3", "D7", "D14"]),
                         ("D30", "overdue", 1, 0))
        self.assertEqual(nudge.next_nudge(40, ["D3", "D7", "D14", "D30"]),
                         (None, "stopped", 0, 0))

    def test_parse_date_strict(self):
        self.assertEqual(str(nudge.parse_date("2026-11-10")), "2026-11-10")
        with self.assertRaises(ValueError):
            nudge.parse_date("11/10/2026")
        with self.assertRaises(ValueError):
            nudge.parse_date("tomorrow")

    def test_daily_list_sorts_overdue_first_then_due_upcoming_stopped(self):
        daily = nudge.build_daily_list(self._rows(), today=self.TODAY)
        self.assertEqual([it["company"] for it in daily["items"]],
                         ["【示例】海湾轮胎贸易", "【示例】尼罗河商贸",
                          "【示例】大西洋轮胎", "【示例】撒哈拉商贸"])
        self.assertEqual([it["status"] for it in daily["items"]],
                         ["overdue", "due_today", "upcoming", "stopped"])
        self.assertEqual(daily["counts"],
                         {"due_today": 1, "overdue": 1,
                          "upcoming": 1, "stopped": 1})

    def test_daily_list_rows_carry_who_why_what(self):
        daily = nudge.build_daily_list(self._rows(), today=self.TODAY)
        overdue = daily["items"][0]
        self.assertEqual(overdue["next_day"], "D7")
        self.assertEqual(overdue["overdue_days"], 5)
        self.assertIn("12 days", overdue["why"])
        self.assertIn("12 天", overdue["why"])
        self.assertIn("TBR 12.00R20", overdue["nudge"]["whatsapp"]["en"])
        self.assertIn("TBR 12.00R20", overdue["nudge"]["whatsapp"]["zh"])
        stopped = daily["items"][3]
        self.assertIsNone(stopped["next_day"])
        self.assertIsNone(stopped["nudge"])
        self.assertEqual(stopped["status"], "stopped")

    def test_daily_list_chains_tire_pack(self):
        daily = nudge.build_daily_list(self._rows(), today=self.TODAY)
        overdue = daily["items"][0]
        self.assertIn("12.00R20", overdue["pack_summary"])
        self.assertIn("沙特", overdue["pack_summary"])
        self.assertIn("SASO", overdue["pack_summary"])
        # li/speed not given in the row → pack gaps name the common values.
        self.assertTrue(any("154/151" in g for g in overdue["pack_gaps"]))
        # Row without size/market has no pack at all, not an error.
        self.assertIsNone(daily["items"][1]["pack_summary"])
        self.assertIsNone(daily["items"][1]["pack_error"])

    def test_daily_list_bad_pack_does_not_kill_the_list(self):
        rows = [{"company": "【示例】错规格公司", "contact": "Pat",
                 "product": "TBR 13.00R24", "scenario": "quoted",
                 "day0": "2026-11-19", "sent": [],
                 "size": "13.00R24", "market": "nigeria"}]
        daily = nudge.build_daily_list(rows, today=self.TODAY)
        self.assertEqual(len(daily["items"]), 1)
        self.assertIsNotNone(daily["items"][0]["pack_error"])
        self.assertIsNotNone(daily["items"][0]["nudge"])

    def test_daily_list_bad_rows_go_to_errors_not_exceptions(self):
        rows = [
            {"contact": "No Company", "scenario": "quoted",
             "day0": "2026-11-19"},
            {"company": "【示例】缺日子", "scenario": "quoted"},
            {"company": "【示例】未来日子", "scenario": "quoted",
             "day0": "2026-12-01"},
            {"company": "【示例】错场景", "scenario": "ghosted",
             "day0": "2026-11-19"},
            {"company": "【示例】错日期", "scenario": "quoted",
             "day0": "11/19/2026"},
            {"company": "【示例】好行", "contact": "Sara",
             "product": "TBR 11.00R20", "scenario": "quoted",
             "day0": "2026-11-19", "sent": []},
        ]
        daily = nudge.build_daily_list(rows, today=self.TODAY)
        self.assertEqual(len(daily["items"]), 1)
        self.assertEqual(len(daily["errors"]), 5)

    def test_daily_list_empty_and_example_defaults_flagged(self):
        daily = nudge.build_daily_list([], today=self.TODAY)
        self.assertEqual(daily["items"], [])
        self.assertEqual(daily["counts"],
                         {"due_today": 0, "overdue": 0,
                          "upcoming": 0, "stopped": 0})
        rows = [{"company": "【示例】没填联系人", "scenario": "quoted",
                 "day0": "2026-11-19", "sent": []}]
        item = nudge.build_daily_list(rows, today=self.TODAY)["items"][0]
        self.assertTrue(item["uses_example_defaults"])
        self.assertTrue(item["company"].startswith("【示例】"))

    def test_render_daily_list_flags_overdue_loud(self):
        daily = nudge.build_daily_list(self._rows(), today=self.TODAY)
        text = nudge.render_daily_list(daily)
        self.assertIn("⚠", text)
        self.assertIn("OVERDUE 5 days", text)
        self.assertIn("过期了 5 天", text)
        self.assertIn("停手", text)
        self.assertIn("12.00R20", text)
        # Overdue row comes before the due-today row in the text.
        self.assertLess(text.index("海湾轮胎贸易"), text.index("尼罗河商贸"))

    def test_render_daily_list_json_round_trips(self):
        daily = nudge.build_daily_list(self._rows(), today=self.TODAY)
        payload = json.loads(nudge.render_daily_list_json(daily))
        self.assertEqual(payload["today"], self.TODAY)
        self.assertEqual(payload["counts"]["overdue"], 1)
        self.assertEqual(payload["items"][0]["status"], "overdue")
        self.assertEqual(payload["items"][0]["nudge"]["day"], "D7")


class TestDailyListCLI(unittest.TestCase):
    def _write_list(self, tmp, rows):
        path = Path(tmp) / "followups.json"
        path.write_text(json.dumps({"followups": rows}, ensure_ascii=False),
                        encoding="utf-8")
        return str(path)

    def test_cli_list_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_list(tmp, [
                {"company": "【示例】海湾轮胎贸易", "contact": "Alex",
                 "product": "TBR 12.00R20", "scenario": "quoted",
                 "day0": "2026-11-10", "sent": ["D3"],
                 "size": "12.00R20", "market": "saudi"},
                {"company": "【示例】尼罗河商贸", "contact": "Sara",
                 "product": "TBR 11.00R20", "scenario": "sampled",
                 "day0": "2026-11-19", "sent": []},
            ])
            code, out = run_cli("--list", path, "--today", "2026-11-22")
            self.assertEqual(code, 0)
            self.assertIn("OVERDUE", out)
            self.assertIn("⚠", out)
            self.assertIn("海湾轮胎贸易", out)
            self.assertIn("SASO", out)
            self.assertIn("今天该跟谁", out)

    def test_cli_list_json_and_email_channel(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_list(tmp, [
                {"company": "【示例】尼罗河商贸", "contact": "Sara",
                 "product": "TBR 11.00R20", "scenario": "sampled",
                 "day0": "2026-11-19", "sent": []},
            ])
            code, out = run_cli("--list", path, "--today", "2026-11-22",
                                "--format", "json")
            self.assertEqual(code, 0)
            payload = json.loads(out)
            self.assertEqual(payload["items"][0]["status"], "due_today")
            self.assertEqual(payload["items"][0]["nudge"]["day"], "D3")
            code, out = run_cli("--list", path, "--today", "2026-11-22",
                                "--channel", "email")
            self.assertEqual(code, 0)
            self.assertIn("Subject:", out)
            self.assertNotIn("WhatsApp 这样发", out)

    def test_cli_list_missing_file_and_bad_json_are_human_errors(self):
        code, out = run_cli("--list", "/tmp/does-not-exist-xyz.json")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text("{not json", encoding="utf-8")
            code, out = run_cli("--list", str(bad))
            self.assertNotEqual(code, 0)
            self.assertNotIn("Traceback", out)
            empty = Path(tmp) / "empty.json"
            empty.write_text("{}", encoding="utf-8")
            code, out = run_cli("--list", str(empty))
            self.assertNotEqual(code, 0)
            self.assertIn("followups", out)

    def test_cli_list_bad_rows_do_not_fail_the_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_list(tmp, [
                {"company": "【示例】好行", "contact": "Sara",
                 "product": "TBR 11.00R20", "scenario": "quoted",
                 "day0": "2026-11-19", "sent": []},
                {"company": "【示例】未来日子", "scenario": "quoted",
                 "day0": "2026-12-01"},
            ])
            code, out = run_cli("--list", path, "--today", "2026-11-22")
            self.assertEqual(code, 0)
            self.assertIn("跳过的行", out)
            self.assertIn("好行", out)

    def test_cli_day_without_scenario_is_human_error(self):
        code, out = run_cli("--day", "D3")
        self.assertNotEqual(code, 0)
        self.assertIn("--help", out)
        self.assertNotIn("Traceback", out)


class TestSince(unittest.TestCase):
    """--since: 只给 Day 0，脚本自己算过去了几天、该发哪档。

    2026-11-28 route-11：单条模式原来只认 --day D3/D7/D14/D30，每次都要
    手算报价发出几天了。--since 是纯加法：--day 的行为、输出一个字都不变。
    """

    TODAY = "2026-11-28"

    def test_pick_day_boundaries(self):
        # 档位边界：3/7/14/30 当天就进档，前一天还是上一档。
        self.assertEqual(nudge.pick_day_since("2026-11-25", self.TODAY), ("D3", 3))
        self.assertEqual(nudge.pick_day_since("2026-11-22", self.TODAY), ("D3", 6))
        self.assertEqual(nudge.pick_day_since("2026-11-21", self.TODAY), ("D7", 7))
        self.assertEqual(nudge.pick_day_since("2026-11-15", self.TODAY), ("D7", 13))
        self.assertEqual(nudge.pick_day_since("2026-11-14", self.TODAY), ("D14", 14))
        self.assertEqual(nudge.pick_day_since("2026-10-30", self.TODAY), ("D14", 29))
        self.assertEqual(nudge.pick_day_since("2026-10-29", self.TODAY), ("D30", 30))
        self.assertEqual(nudge.pick_day_since("2026-09-01", self.TODAY), ("D30", 88))

    def test_pick_day_not_yet(self):
        # 不到 3 天：还没到发的时候，档是 None，不是报错。
        self.assertEqual(nudge.pick_day_since("2026-11-28", self.TODAY), (None, 0))
        self.assertEqual(nudge.pick_day_since("2026-11-26", self.TODAY), (None, 2))

    def test_pick_day_bad_and_future_date_raise(self):
        with self.assertRaises(ValueError):
            nudge.pick_day_since("2026/11/20", self.TODAY)
        with self.assertRaises(ValueError):
            nudge.pick_day_since("下周", self.TODAY)
        with self.assertRaises(ValueError):
            nudge.pick_day_since("2026-11-29", self.TODAY)

    def test_cli_since_picks_d7_and_shows_day0_line(self):
        code, out = run_cli("--since", "2026-11-20", "--scenario", "quoted",
                            "--today", self.TODAY)
        self.assertEqual(code, 0)
        self.assertIn("D7", out)
        self.assertIn("问进度", out)
        self.assertIn("Day 0：2026-11-20（已过 8 天）→ 该发 D7 这档", out)
        self.assertIn("python3 scripts/nudge.py --since 2026-11-20 "
                      "--scenario quoted", out)

    def test_cli_since_json_carries_day0(self):
        code, out = run_cli("--since", "2026-11-14", "--scenario", "sampled",
                            "--today", self.TODAY, "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["day"], "D14")
        self.assertEqual(payload["day0"], "2026-11-14")
        self.assertEqual(payload["days_elapsed"], 14)
        self.assertIn("--since 2026-11-14", payload["reproduce"])

    def test_cli_since_not_yet_is_plain_words_not_error(self):
        code, out = run_cli("--since", "2026-11-27", "--scenario", "quoted",
                            "--today", self.TODAY)
        self.assertEqual(code, 0)
        self.assertIn("还没到发的时候", out)
        self.assertIn("D3 还要 2 天", out)
        self.assertNotIn("Traceback", out)

    def test_cli_since_and_day_together_is_human_error(self):
        code, out = run_cli("--since", "2026-11-20", "--day", "D7",
                            "--scenario", "quoted")
        self.assertNotEqual(code, 0)
        self.assertIn("二选一", out)
        self.assertNotIn("Traceback", out)

    def test_cli_since_without_scenario_is_human_error(self):
        code, out = run_cli("--since", "2026-11-20")
        self.assertNotEqual(code, 0)
        self.assertIn("--help", out)
        self.assertNotIn("Traceback", out)

    def test_cli_since_bad_and_future_date_are_human_errors(self):
        code, out = run_cli("--since", "2026/11/20", "--scenario", "quoted")
        self.assertNotEqual(code, 0)
        self.assertIn("YYYY-MM-DD", out)
        self.assertNotIn("Traceback", out)
        code, out = run_cli("--since", "2026-11-29", "--scenario", "quoted",
                            "--today", self.TODAY)
        self.assertNotEqual(code, 0)
        self.assertIn("还没到", out)
        self.assertNotIn("Traceback", out)

    def test_cli_day_output_has_no_day0_line(self):
        # --day 模式的输出一个字都不变：没有 Day 0 那一行，没有多余的键。
        code, out = run_cli("--day", "D7", "--scenario", "quoted")
        self.assertEqual(code, 0)
        self.assertNotIn("Day 0：", out)
        code, out = run_cli("--day", "D7", "--scenario", "quoted",
                            "--format", "json")
        payload = json.loads(out)
        self.assertNotIn("day0", payload)
        self.assertNotIn("days_elapsed", payload)

    def test_cli_help_mentions_since(self):
        code, out = run_cli("--help")
        self.assertEqual(code, 0)
        self.assertIn("--since 2026-11-20 --scenario quoted", out)


if __name__ == "__main__":
    unittest.main()
