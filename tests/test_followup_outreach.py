#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/followup_plan.py, scripts/outreach_gen.py and
scripts/check_private_data.py.

Run: python3 -m unittest discover -s tests -v   (from the repo root)
"""

import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_private_data as cpd  # noqa: E402
import followup_plan as fp  # noqa: E402


def run_script(name, *args):
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / name), *args],
        capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout + proc.stderr


class TestFollowupPlan(unittest.TestCase):
    def test_cadence_is_d0_d2_d5_three_touches(self):
        rows = fp.build_plan("T0", "2026-10-08")
        self.assertEqual(len(rows), 3)
        self.assertEqual([r["offset"] for r in rows], ["D0", "D2", "D5"])
        self.assertEqual([r["date"] for r in rows],
                         ["2026-10-08", "2026-10-10", "2026-10-13"])

    def test_bad_tier_and_bad_date_raise_value_error(self):
        with self.assertRaises(ValueError):
            fp.build_plan("T9", "2026-10-08")
        with self.assertRaises(ValueError):
            fp.build_plan("T0", "2026-13-40")
        with self.assertRaises(ValueError):
            fp.build_plan("T0", "10/08/2026")

    def test_cli_rejects_bad_date_with_words_not_traceback(self):
        code, out = run_script("followup_plan.py", "--tier", "T0",
                               "--start", "2026-13-40",
                               "--csv", "examples/leads_example.csv")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)

    def test_cli_plan_matches_library(self):
        code, out = run_script("followup_plan.py", "--tier", "T0",
                               "--start", "2026-10-08",
                               "--csv", "examples/leads_example.csv")
        self.assertEqual(code, 0)
        for date in ("2026-10-08", "2026-10-10", "2026-10-13"):
            self.assertIn(date, out)

    def test_printed_commands_use_python3_not_bare_python(self):
        # 2026-11-26 route-12: the demo table prints a copy-paste outreach
        # command; bare `python` does not exist on stock Linux (only
        # `python3`), so the printed command must say python3.
        code, out = run_script("followup_plan.py", "--tier", "T0",
                               "--start", "2026-11-24",
                               "--csv", "examples/leads_example.csv")
        self.assertEqual(code, 0)
        self.assertIn("python3 scripts/outreach_gen.py", out)
        self.assertNotIn("python scripts/", out)

    def test_start_date_alias_matches_start(self):
        code, out = run_script("followup_plan.py", "--tier", "T0",
                               "--start-date", "2026-10-08",
                               "--csv", "examples/leads_example.csv")
        self.assertEqual(code, 0)
        for date in ("2026-10-08", "2026-10-10", "2026-10-13"):
            self.assertIn(date, out)

    def test_run_log_written(self):
        run_script("followup_plan.py", "--tier", "T0",
                   "--start", "2026-10-08",
                   "--csv", "examples/leads_example.csv")
        log_path = REPO_ROOT / "logs" / "followup_plan.log"
        self.assertTrue(log_path.exists())
        text = log_path.read_text(encoding="utf-8")
        self.assertIn("RUN argv=", text)
        self.assertIn("RESULT tier=T0", text)


class TestFollowupRhythmAndRefusal(unittest.TestCase):
    """7-day 3-touch rhythm (Day1/Day4/Day7) + stop at once on refusal."""

    def test_t1_is_day1_day4_day7(self):
        rows = fp.build_plan("T1", "2026-10-08")
        self.assertEqual([r["offset"] for r in rows], ["D0", "D3", "D6"])
        self.assertEqual([r["date"] for r in rows],
                         ["2026-10-08", "2026-10-11", "2026-10-14"])

    def test_t0_stays_inside_seven_day_envelope(self):
        rows = fp.build_plan("T0", "2026-10-08")
        self.assertEqual(len(rows), 3)
        offsets = [fp._day_offset(r["offset"]) for r in rows]
        self.assertLessEqual(offsets[-1], 6)
        gaps = [b - a for a, b in zip(offsets, offsets[1:])]
        self.assertTrue(all(g >= fp.MIN_GAP_DAYS for g in gaps))

    def test_check_cadence_all_tiers_clean(self):
        for tier in ("T0", "T1", "T2", "T3"):
            self.assertEqual(fp.check_cadence(tier), [], tier)
            fp.validate_cadence(tier)  # must not raise

    def test_validate_standard_rhythm_accepts_only_d0_d3_d6(self):
        fp.validate_standard_rhythm((0, 3, 6))
        for bad in ((0, 2, 5), (0, 3), (0, 3, 6, 9), (1, 4, 7), (0, 3, 7)):
            with self.assertRaises(ValueError, msg=str(bad)):
                fp.validate_standard_rhythm(bad)

    def test_build_plan_rejects_tampered_cadence(self):
        # Break T1's rhythm on purpose: build_plan must refuse, not silently
        # schedule wrong dates.
        saved = fp.CADENCE["T1"]
        try:
            fp.CADENCE["T1"] = saved[:2] + [("D5",) + saved[2][1:]]
            with self.assertRaises(ValueError):
                fp.build_plan("T1", "2026-10-08")
        finally:
            fp.CADENCE["T1"] = saved

    def test_refused_stops_all_remaining_touches(self):
        rows = fp.build_plan("T1", "2026-10-08")
        self.assertEqual(fp.remaining_touches(rows, "refused"), [])
        self.assertEqual(fp.remaining_touches(rows, "replied"), [])
        self.assertEqual(fp.remaining_touches(rows, "not_now"), [])
        self.assertEqual(fp.remaining_touches(rows, "no_reply"), rows)
        self.assertEqual(len(rows), 3)  # input list untouched

    def test_refusal_mid_cadence_cancels_later_touches(self):
        # D0 already sent, refusal arrives before D3: D3 and D6 are gone.
        rows = fp.build_plan("T1", "2026-10-08")
        self.assertEqual(fp.remaining_touches(rows[1:], "refused"), [])

    def test_stop_after_reply(self):
        self.assertFalse(fp.stop_after_reply("no_reply"))
        for status in ("replied", "refused", "not_now"):
            self.assertTrue(fp.stop_after_reply(status))
        with self.assertRaises(ValueError):
            fp.stop_after_reply("maybe")
        with self.assertRaises(ValueError):
            fp.remaining_touches([], "maybe")

    def test_refusal_cooldown_is_30_days(self):
        self.assertEqual(fp.refusal_cooldown_until("2026-10-10"), "2026-11-09")
        with self.assertRaises(ValueError):
            fp.refusal_cooldown_until("10/10/2026")

    def test_plan_with_reply_refused(self):
        rows, note = fp.plan_with_reply("T1", "2026-10-08", reply="refused",
                                        reply_date="2026-10-10")
        self.assertEqual(rows, [])
        self.assertIn("2026-11-09", note)
        self.assertIn("停", note)

    def test_plan_with_reply_no_reply_is_plain_plan(self):
        rows, note = fp.plan_with_reply("T1", "2026-10-08")
        self.assertEqual(len(rows), 3)
        self.assertEqual(note, "")

    def test_cli_reply_refused_prints_stop_not_plan(self):
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08", "--reply", "refused",
                               "--reply-date", "2026-10-10")
        self.assertEqual(code, 0)
        self.assertIn("2026-11-09", out)
        self.assertNotIn("2026-10-11", out)  # no D3 date in a stopped plan
        self.assertNotIn("Traceback", out)

    def test_cli_reply_replied_stops_without_traceback(self):
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08", "--reply", "replied")
        self.assertEqual(code, 0)
        self.assertNotIn("2026-10-11", out)
        self.assertNotIn("Traceback", out)

    def test_cli_reply_bad_value_is_argparse_error(self):
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08", "--reply", "maybe")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)

    def test_cli_reply_bad_date_is_words_not_traceback(self):
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08", "--reply", "refused",
                               "--reply-date", "10/10/2026")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)


class TestTodayList(unittest.TestCase):
    """--today morning list: overdue first, then due today, then next.

    T1 plan is D0 2026-10-08 / D3 2026-10-11 / D6 2026-10-14.
    """

    def _t1(self):
        return fp.build_plan("T1", "2026-10-08")

    def test_parse_today_explicit_and_default(self):
        self.assertEqual(fp.parse_today("2026-10-11"), date(2026, 10, 11))
        self.assertEqual(fp.parse_today(None), date.today())
        self.assertEqual(fp.parse_today(fp.TODAY_SENTINEL), date.today())
        with self.assertRaises(ValueError):
            fp.parse_today("2026/10/11")

    def test_parse_sent(self):
        self.assertEqual(fp.parse_sent("D0,D2"), ("D0", "D2"))
        self.assertEqual(fp.parse_sent(""), ())
        self.assertEqual(fp.parse_sent(None), ())
        self.assertEqual(fp.parse_sent("d3"), ("D3",))
        with self.assertRaises(ValueError):
            fp.parse_sent("tomorrow")

    def test_due_today_and_upcoming(self):
        result = fp.todays_followups(self._t1(), "2026-10-08")
        self.assertEqual([r["offset"] for r in result["due"]], ["D0"])
        self.assertEqual(result["overdue"], [])
        self.assertEqual(result["upcoming"]["offset"], "D3")
        self.assertEqual(result["upcoming_in_days"], 3)
        self.assertFalse(result["all_done"])
        self.assertEqual(result["today"], "2026-10-08")

    def test_overdue_most_overdue_first(self):
        result = fp.todays_followups(self._t1(), "2026-10-12")
        self.assertEqual([r["offset"] for r in result["overdue"]], ["D0", "D3"])
        self.assertEqual(result["due"], [])
        self.assertEqual(result["upcoming"]["offset"], "D6")
        self.assertEqual(result["upcoming_in_days"], 2)

    def test_sent_marks_hide_touches(self):
        result = fp.todays_followups(self._t1(), "2026-10-12", sent=("D0",))
        self.assertEqual([r["offset"] for r in result["overdue"]], ["D3"])
        result = fp.todays_followups(self._t1(), "2026-10-20",
                                     sent=("D0", "D3", "D6"))
        self.assertTrue(result["all_done"])
        self.assertIsNone(result["upcoming"])
        self.assertIsNone(result["upcoming_in_days"])

    def test_unknown_sent_label_raises(self):
        with self.assertRaises(ValueError):
            fp.todays_followups(self._t1(), "2026-10-12", sent=("D9",))

    def test_today_before_start_all_upcoming(self):
        result = fp.todays_followups(self._t1(), "2026-10-05")
        self.assertEqual(result["overdue"], [])
        self.assertEqual(result["due"], [])
        self.assertEqual(result["upcoming"]["offset"], "D0")
        self.assertEqual(result["upcoming_in_days"], 3)

    def test_cli_today_shows_due_not_full_plan(self):
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08",
                               "--csv", "examples/leads_example.csv",
                               "--today", "2026-10-11", "--sent", "D0")
        self.assertEqual(code, 0)
        self.assertIn("今日跟进", out)
        self.assertIn("DUE TODAY", out)
        self.assertIn("2026-10-11", out)
        self.assertIn("OVERDUE 0", out)
        self.assertNotIn("跟进计划（", out)
        self.assertNotIn("Traceback", out)

    def test_cli_today_overdue_pinned_first(self):
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08",
                               "--today", "2026-10-12")
        self.assertEqual(code, 0)
        self.assertIn("OVERDUE", out)
        self.assertIn("2026-10-08", out)  # the overdue D0 touch
        self.assertIn("2026-10-14", out)  # the upcoming D6 touch
        self.assertLess(out.index("OVERDUE"), out.index("NOT YET"))
        self.assertNotIn("Traceback", out)

    def test_cli_today_bare_flag_means_today(self):
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08", "--today")
        self.assertEqual(code, 0)
        self.assertIn("今日跟进", out)
        self.assertIn(date.today().isoformat(), out)
        self.assertNotIn("Traceback", out)

    def test_cli_today_bad_date_and_bad_sent_are_words_not_traceback(self):
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08",
                               "--today", "2026/10/12")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08",
                               "--today", "2026-10-12", "--sent", "D9")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        self.assertIn("D9", out)

    def test_cli_today_with_reply_refused_still_stops(self):
        code, out = run_script("followup_plan.py", "--tier", "T1",
                               "--start", "2026-10-08",
                               "--today", "2026-10-12",
                               "--reply", "refused",
                               "--reply-date", "2026-10-10")
        self.assertEqual(code, 0)
        self.assertIn("2026-11-09", out)
        self.assertNotIn("DUE TODAY", out)
        self.assertNotIn("Traceback", out)

    def test_cli_today_t3_has_nothing_to_send(self):
        code, out = run_script("followup_plan.py", "--tier", "T3",
                               "--start", "2026-10-08",
                               "--today", "2026-10-12")
        self.assertEqual(code, 0)
        self.assertNotIn("Traceback", out)


class TestOutreachGen(unittest.TestCase):
    def test_cli_t0_output_is_bilingual(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T0")
        self.assertEqual(code, 0)
        self.assertIn("[EN", out)
        self.assertIn("中文", out)

    def test_cli_bad_tier_is_argparse_error(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T9")
        self.assertNotEqual(code, 0)
        self.assertIn("T0", out)
        self.assertNotIn("Traceback", out)


class TestBadCsvFriendlyErrors(unittest.TestCase):
    """坏 CSV 要给人话报错，不许直接 traceback 糊脸。"""

    def _write(self, content):
        tmp = tempfile.NamedTemporaryFile(
            "w", suffix=".csv", delete=False, encoding="utf-8")
        tmp.write(content)
        tmp.close()
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return tmp.name

    def test_outreach_missing_company_column(self):
        path = self._write("country,product\nNigeria,tyres\n")
        code, out = run_script("outreach_gen.py", path)
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        self.assertIn("缺少 company 列", out)

    def test_outreach_empty_file(self):
        path = self._write("")
        code, out = run_script("outreach_gen.py", path)
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        self.assertIn("空的", out)

    def test_outreach_missing_file(self):
        code, out = run_script("outreach_gen.py", "no_such_file.csv")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        self.assertIn("找不到文件", out)

    def test_outreach_unwritable_out_path(self):
        bad_out = str(Path(tempfile.gettempdir()) / "不存在的目录" / "drafts.md")
        code, out = run_script(
            "outreach_gen.py", "examples/leads_example.csv",
            "--tier", "T1", "--out", bad_out)
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        self.assertIn("写不进", out)

    def test_followup_missing_company_column(self):
        path = self._write("country,product\nNigeria,tyres\n")
        code, out = run_script("followup_plan.py", "--tier", "T0",
                               "--start", "2026-10-08", "--csv", path)
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        self.assertIn("缺少 company 列", out)

    def test_followup_empty_file(self):
        path = self._write("")
        code, out = run_script("followup_plan.py", "--tier", "T0",
                               "--start", "2026-10-08", "--csv", path)
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        self.assertIn("空的", out)


class TestCheckPrivateData(unittest.TestCase):
    def test_placeholder_phone_is_not_flagged(self):
        self.assertFalse(cpd.looks_like_real_phone("电话 +000 00 000 0000（占位符）"))
        self.assertFalse(cpd.looks_like_real_phone("contact: demo01@sample.example"))

    def test_real_looking_phone_is_flagged(self):
        self.assertTrue(cpd.looks_like_real_phone("call me at +1 555 010 1234"))  # 555-01XX is the fictional range, never a real number

    def test_scan_file_flags_real_email_but_not_reserved_domain(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                         encoding="utf-8") as fh:
            fh.write("contact the buyer at boss@realcompany.com\n")
            real_path = fh.name
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                         encoding="utf-8") as fh:
            fh.write("contact: demo01@sample.example\n")
            clean_path = fh.name
        self.assertTrue(cpd.scan_file(real_path))
        self.assertEqual(cpd.scan_file(clean_path), [])

    def test_scan_file_skips_lines_marked_as_example(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                         encoding="utf-8") as fh:
            fh.write("【示例】海湾轮胎贸易 boss@realcompany.com\n")
            path = fh.name
        self.assertEqual(cpd.scan_file(path), [])


class TestCLISmoke(unittest.TestCase):
    """Every script must answer --help and run its happy path with exit 0."""

    def test_all_scripts_help(self):
        for name in ("lead_score.py", "outreach_gen.py", "followup_plan.py",
                     "quote_engine.py", "check_private_data.py"):
            code, _out = run_script(name, "--help")
            self.assertEqual(code, 0, name)

    def test_all_scripts_run(self):
        cases = [
            ("lead_score.py", "examples/leads_example.csv"),
            ("outreach_gen.py", "examples/leads_example.csv", "--tier", "T0"),
            ("followup_plan.py", "--tier", "T0", "--start", "2026-10-08",
             "--csv", "examples/leads_example.csv"),
            ("quote_engine.py", "--cost", "28", "--freight", "6",
             "--margin", "15"),
            ("check_private_data.py",),
        ]
        for case in cases:
            code, out = run_script(*case)
            self.assertEqual(code, 0, case)
            self.assertNotIn("Traceback", out, case)


if __name__ == "__main__":
    unittest.main()
