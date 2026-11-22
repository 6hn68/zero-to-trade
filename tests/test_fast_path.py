#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/fast_path.py — 7-day fast path, interactive edition.

Run: python3 -m unittest discover -s tests -v   (from the repo root)
Only the standard library is used, same rule as the scripts themselves.

Content is aligned day by day with docs/fast-path.md (not a second list):
  Day 1 market + 10-15 leads, Day 2 due diligence + lead_score.py,
  Day 3 first touch (hard deadline, outreach_gen.py), Day 4 channel probe
  + more leads, no formal message (followup_plan.py), Day 5 second touch D2,
  Day 6 draft the 3rd letter + review, Day 7 third touch D5 + archive.
State files in these tests always live in a temp dir, never in the repo.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import fast_path as fp  # noqa: E402


def run_fp(*args, cwd=None):
    """Run the fast_path CLI; return (exit_code, stdout+stderr)."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "fast_path.py"), *args],
        capture_output=True, text=True, cwd=cwd or str(REPO_ROOT))
    return proc.returncode, proc.stdout + proc.stderr


def tmp_state(testcase):
    """A fresh state path inside a temp dir owned by this test."""
    tmpdir = tempfile.mkdtemp(prefix="fast_path_")
    testcase.addCleanup(lambda: _rmtree(tmpdir))
    return os.path.join(tmpdir, "state.json"), tmpdir


def _rmtree(path):
    import shutil
    shutil.rmtree(path, ignore_errors=True)


class TestDayOutputs(unittest.TestCase):
    def test_day1_tasks(self):
        rc, out = run_fp("--day", "1")
        self.assertEqual(rc, 0)
        self.assertIn("Day 1", out)
        self.assertIn("定 1 个市场", out)
        self.assertIn("10-15", out)
        self.assertIn("my_leads.csv", out)
        self.assertIn("docs/01-market-selection.md", out)
        self.assertIn("docs/02-find-leads.md", out)
        self.assertIn("未打卡", out)

    def test_day2_tasks(self):
        rc, out = run_fp("--day", "2")
        self.assertEqual(rc, 0)
        self.assertIn("背调", out)
        self.assertIn("docs/03-due-diligence.md", out)
        self.assertIn("scripts/lead_score.py", out)
        self.assertIn("T0", out)

    def test_day3_tasks_hard_deadline(self):
        rc, out = run_fp("--day", "3")
        self.assertEqual(rc, 0)
        self.assertIn("首触", out)
        self.assertIn("硬底线", out)
        self.assertIn("scripts/outreach_gen.py", out)
        self.assertIn("drafts_day3.md", out)
        self.assertIn("没有出现价格", out)

    def test_day4_no_formal_message(self):
        rc, out = run_fp("--day", "4")
        self.assertEqual(rc, 0)
        self.assertIn("探渠道", out)
        self.assertIn("不发正式消息", out)
        self.assertIn("scripts/followup_plan.py", out)
        self.assertIn("Day 5", out)

    def test_day5_second_touch_d2(self):
        rc, out = run_fp("--day", "5")
        self.assertEqual(rc, 0)
        self.assertIn("第 2 次触达", out)
        self.assertIn("D2", out)
        self.assertIn("scripts/lead_score.py", out)
        self.assertIn("新信息", out)

    def test_day6_draft_third_letter_and_review(self):
        rc, out = run_fp("--day", "6")
        self.assertEqual(rc, 0)
        self.assertIn("第 3 封信", out)
        self.assertIn("发出 / 回复 / 回复率", out)
        self.assertIn("复盘", out)

    def test_day7_third_touch_d5_and_archive(self):
        rc, out = run_fp("--day", "7")
        self.assertEqual(rc, 0)
        self.assertIn("第 3 次触达", out)
        self.assertIn("D5", out)
        self.assertIn("存成档案", out)
        self.assertIn("不要发第 4 次", out)

    def test_each_day_prints_its_own_title_not_others(self):
        titles = {n: fp.DAYS[n]["title"] for n in range(1, 8)}
        self.assertEqual(len(set(titles.values())), 7)
        for n in range(1, 8):
            rc, out = run_fp("--day", str(n))
            self.assertEqual(rc, 0)
            self.assertIn(titles[n], out)
            for m, title in titles.items():
                if m != n:
                    self.assertNotIn(title, out,
                                     "Day %d output leaked Day %d title" % (n, m))

    def test_day_output_lists_tool_or_doc_per_task(self):
        for n in range(1, 8):
            rc, out = run_fp("--day", str(n))
            self.assertEqual(rc, 0)
            self.assertIn("用哪处：", out)
            self.assertIn("产出：", out)
            self.assertIn("过关标准：", out)


class TestInvalidInput(unittest.TestCase):
    def test_invalid_day_zero(self):
        rc, out = run_fp("--day", "0")
        self.assertNotEqual(rc, 0)
        self.assertIn("第 0 天不存在", out)
        self.assertIn("Day 1 到 Day 7", out)

    def test_invalid_day_eight(self):
        rc, out = run_fp("--day", "8")
        self.assertNotEqual(rc, 0)
        self.assertIn("第 8 天不存在", out)

    def test_invalid_day_non_numeric(self):
        rc, out = run_fp("--day", "abc")
        self.assertNotEqual(rc, 0)
        self.assertIn("不是数字", out)

    def test_invalid_done_day(self):
        state, _ = tmp_state(self)
        rc, out = run_fp("--done", "9", "--state", state)
        self.assertNotEqual(rc, 0)
        self.assertIn("第 9 天不存在", out)
        self.assertFalse(os.path.exists(state))

    def test_invalid_start_month(self):
        state, _ = tmp_state(self)
        rc, out = run_fp("--start", "2026-13-01", "--state", state)
        self.assertNotEqual(rc, 0)
        self.assertIn("YYYY-MM-DD", out)

    def test_invalid_start_day(self):
        state, _ = tmp_state(self)
        rc, out = run_fp("--start", "2026-11-31", "--state", state)
        self.assertNotEqual(rc, 0)
        self.assertIn("YYYY-MM-DD", out)

    def test_invalid_start_free_text(self):
        state, _ = tmp_state(self)
        rc, out = run_fp("--start", "下周一", "--state", state)
        self.assertNotEqual(rc, 0)
        self.assertIn("YYYY-MM-DD", out)

    def test_no_args_is_human_error_not_traceback(self):
        rc, out = run_fp()
        self.assertNotEqual(rc, 0)
        self.assertIn("--day", out)
        self.assertNotIn("Traceback", out)


class TestCheckIn(unittest.TestCase):
    def test_done_writes_state_with_timestamp(self):
        state, _ = tmp_state(self)
        rc, out = run_fp("--done", "1", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("已打卡", out)
        self.assertIn("第 1 天", out)
        with open(state, encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("1", data["done"])
        self.assertTrue(data["done"]["1"].startswith(str(date.today())))

    def test_done_duplicate_prompts_and_keeps_first_stamp(self):
        state, _ = tmp_state(self)
        run_fp("--done", "3", "--state", state)
        with open(state, encoding="utf-8") as f:
            first = json.load(f)["done"]["3"]
        rc, out = run_fp("--done", "3", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("已打卡过", out)
        self.assertIn("不重复记", out)
        with open(state, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["done"]["3"], first)
        self.assertEqual(len(data["done"]), 1)

    def test_day_shows_done_status_after_checkin(self):
        state, _ = tmp_state(self)
        run_fp("--done", "2", "--state", state)
        rc, out = run_fp("--day", "2", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("已打卡", out)

    def test_day_does_not_create_state_file(self):
        state, tmpdir = tmp_state(self)
        rc, out = run_fp("--day", "1", "--state", state, cwd=tmpdir)
        self.assertEqual(rc, 0)
        self.assertFalse(os.path.exists(state))

    def test_start_alone_only_saves_date(self):
        state, _ = tmp_state(self)
        rc, out = run_fp("--start", "2026-11-09", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("2026-11-09", out)
        with open(state, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["start"], "2026-11-09")
        self.assertEqual(data["done"], {})


class TestProgress(unittest.TestCase):
    def test_progress_no_start_says_so_and_no_overdue(self):
        state, _ = tmp_state(self)
        run_fp("--done", "1", "--state", state)
        rc, out = run_fp("--progress", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("未设开始日期", out)
        self.assertIn("已完成 1 天 / 待完成 6 天 / 逾期 0 天", out)

    def test_progress_counts_three_numbers(self):
        state, _ = tmp_state(self)
        run_fp("--done", "1", "--state", state)
        run_fp("--done", "2", "--state", state)
        rc, out = run_fp("--progress", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("已完成 2 天 / 待完成 5 天 / 逾期 0 天", out)

    def test_progress_missing_state_file_is_zero_not_crash(self):
        state, _ = tmp_state(self)
        rc, out = run_fp("--progress", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("已完成 0 天 / 待完成 7 天 / 逾期 0 天", out)

    def test_progress_overdue_with_past_start(self):
        state, _ = tmp_state(self)
        start = date.today() - timedelta(days=9)
        run_fp("--start", str(start), "--done", "1", "--state", state)
        rc, out = run_fp("--progress", "--state", state)
        self.assertEqual(rc, 0)
        # Day 1 planned start (9 days ago), Days 2-7 planned 8..3 days ago:
        # all past, only Day 1 done -> 6 overdue.
        self.assertIn("已完成 1 天 / 待完成 6 天 / 逾期 6 天", out)
        self.assertIn("Day 2", out)

    def test_progress_no_overdue_when_start_is_today(self):
        state, _ = tmp_state(self)
        run_fp("--start", str(date.today()), "--state", state)
        rc, out = run_fp("--progress", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("已完成 0 天 / 待完成 7 天 / 逾期 0 天", out)

    def test_progress_all_done(self):
        state, _ = tmp_state(self)
        for n in range(1, 8):
            run_fp("--done", str(n), "--state", state)
        rc, out = run_fp("--progress", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("已完成 7 天 / 待完成 0 天 / 逾期 0 天", out)
        self.assertIn("全部打卡完成", out)

    def test_compute_progress_unit_level(self):
        state = {"start": str(date.today() - timedelta(days=3)), "done": {"1": "x"}}
        p = fp.compute_progress(state)
        self.assertEqual(p["done_count"], 1)
        self.assertEqual(p["remaining_count"], 6)
        # Day 2 planned 2 days ago, Day 3 planned 1 day ago, Day 4 planned today:
        # only Days 2-3 overdue.
        self.assertEqual(p["overdue_count"], 2)
        self.assertEqual([n for n, _ in p["overdue"]], [2, 3])


class TestListAndHelp(unittest.TestCase):
    def test_list_overview_covers_all_seven_days(self):
        state, _ = tmp_state(self)
        rc, out = run_fp("--list", "--state", state)
        self.assertEqual(rc, 0)
        for n in range(1, 8):
            self.assertIn("Day %d" % n, out)
            self.assertIn(fp.DAYS[n]["title"], out)
        self.assertIn("待完成", out)

    def test_list_shows_done_status(self):
        state, _ = tmp_state(self)
        run_fp("--done", "1", "--state", state)
        rc, out = run_fp("--list", "--state", state)
        self.assertEqual(rc, 0)
        self.assertIn("已打卡", out)

    def test_help_has_real_examples(self):
        rc, out = run_fp("--help")
        self.assertEqual(rc, 0)
        for example in ("--day 1", "--done 3", "--progress",
                        "--start 2026-11-09", "--list"):
            self.assertIn(example, out)


class TestSevenDayWordingLocked(unittest.TestCase):
    """7 天口径防回退：代码常量、任务表、五版 README 的目录树行必须一致说 7 天。

    2026-11-22 核对发现：英文/葡语/阿语版 README 的目录树注释行还写着 5 天
    （"5 days" / "5 dias" / "5 أيام"），其余文件早已是 7 天。改回 7 天后，
    用这组测试锁住：以后谁再把 5 天写回来，测试立刻变红。
    """

    STALE_FIVE_DAY = ("5 days", "5 day", "5 dias", "5 días", "5 أيام",
                      "5 天", "five days", "cinco dias", "cinco días")

    def test_total_days_constant_is_seven(self):
        self.assertEqual(fp.TOTAL_DAYS, 7)
        self.assertEqual(sorted(fp.DAYS), [1, 2, 3, 4, 5, 6, 7])

    def test_readme_tree_lines_say_seven_days_not_five(self):
        # 只查目录树行（以 │ 开头的那行注释）：这就是 2026-11-22 发现残留 5 天的地方。
        # 正文里 "seven days" / "七天" / "siete días" 这类文字写法不在此列，不误报。
        for name in ("README.md", "README_EN.md", "README_ES.md",
                     "README_PT.md", "README_AR.md"):
            with open(REPO_ROOT / name, encoding="utf-8") as f:
                lines = [ln for ln in f
                         if "├── fast-path.md" in ln and ln.lstrip().startswith("│")]
            self.assertEqual(len(lines), 1,
                             "%s 的目录树里应恰好有一行 fast-path.md，实际 %d 行"
                             % (name, len(lines)))
            line = lines[0]
            for stale in self.STALE_FIVE_DAY:
                self.assertNotIn(
                    stale, line,
                    "%s 目录树行还写着 5 天口径：%s" % (name, line.strip()))
            self.assertIn("7", line,
                          "%s 目录树行没写 7 天：%s" % (name, line.strip()))

    def test_doc_and_interactive_doc_say_seven_days(self):
        for name in ("docs/fast-path.md", "docs/fast-path-interactive.md"):
            with open(REPO_ROOT / name, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("7 天", text, "%s 里找不到“7 天”" % name)
            self.assertNotIn("5 天快路径", text, "%s 里还写着“5 天快路径”" % name)
            self.assertNotIn("5 天从零", text, "%s 里还写着“5 天从零”" % name)


if __name__ == "__main__":
    unittest.main()
