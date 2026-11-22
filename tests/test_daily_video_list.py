#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/daily_video_list.py — daily 5-video shooting list.

Run: python3 -m pytest tests/test_daily_video_list.py -q   (from the repo root)
Only the standard library is used, same rule as the scripts themselves.
"""

import json
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import daily_video_list as dvl  # noqa: E402
import tire_pack as tp  # noqa: E402


def run_cli(*args):
    """Run the daily-video-list CLI; return (exit_code, stdout+stderr)."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "daily_video_list.py"),
         *args],
        capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout + proc.stderr


class TestBuildDailyList(unittest.TestCase):
    def test_five_items_every_day(self):
        items = dvl.build_daily_list(day=date(2026, 11, 22))
        self.assertEqual(len(items), 5)

    def test_slots_and_time_blocks(self):
        items = dvl.build_daily_list(day=date(2026, 11, 22))
        self.assertEqual([it["slot"] for it in items], [1, 2, 3, 4, 5])
        self.assertEqual([it["time_block_zh"] for it in items],
                         ["上午", "上午", "上午", "下午", "下午"])
        # 5 different angles, one per slot.
        self.assertEqual(len({it["angle"] for it in items}), 5)

    def test_every_item_has_size_market_point_and_checks(self):
        items = dvl.build_daily_list(day=date(2026, 11, 22))
        for it in items:
            self.assertIn(it["size"], tp.TIRE_SIZES)
            self.assertIn(it["market_en"],
                          [m["name_en"] for m in tp.MARKETS.values()])
            self.assertTrue(it["selling_point"].strip())
            self.assertIn(it["size"], it["selling_point"])
            self.assertEqual(len(it["checklist"]), 3)
            self.assertEqual(len(it["checklist_zh"]), 3)
            self.assertTrue(it["pack_hint"].startswith(
                "python scripts/tire_pack.py --size "))

    def test_deterministic_same_day_same_list(self):
        day = date(2026, 11, 22)
        self.assertEqual(dvl.build_daily_list(day=day),
                         dvl.build_daily_list(day=day))

    def test_rotation_changes_day_to_day(self):
        first = dvl.build_daily_list(day=date(2026, 11, 22))
        second = dvl.build_daily_list(day=date(2026, 11, 23))
        self.assertNotEqual(
            [(it["size"], it["market_en"]) for it in first],
            [(it["size"], it["market_en"]) for it in second])

    def test_markets_do_not_repeat_within_a_day(self):
        # Step 3 through 8 markets keeps all 5 markets different.
        items = dvl.build_daily_list(day=date(2026, 11, 22))
        self.assertEqual(len({it["market_en"] for it in items}), 5)

    def test_all_sizes_appear_over_a_week(self):
        seen = set()
        for offset in range(7):
            day = date(2026, 11, 22 + offset) if 22 + offset <= 30 \
                else date(2026, 12, 22 + offset - 30)
            for it in dvl.build_daily_list(day=day):
                seen.add(it["size"])
        self.assertEqual(seen, set(tp.TIRE_SIZES.keys()))

    def test_seed_pins_rotation(self):
        first = dvl.build_daily_list(day=date(2026, 11, 22), seed=7)
        second = dvl.build_daily_list(day=date(2026, 12, 25), seed=7)
        self.assertEqual(first, second)

    def test_market_pin_applies_to_all_five(self):
        items = dvl.build_daily_list(day=date(2026, 11, 22),
                                     market="nigeria")
        self.assertEqual({it["market"] for it in items}, {"尼日利亚"})
        self.assertEqual({it["market_en"] for it in items}, {"Nigeria"})

    def test_market_aliases_accepted(self):
        items = dvl.build_daily_list(day=date(2026, 11, 22),
                                     market="沙特")
        self.assertEqual({it["market_en"] for it in items},
                         {"Saudi Arabia"})

    def test_unknown_market_raises(self):
        with self.assertRaises(ValueError):
            dvl.build_daily_list(day=date(2026, 11, 22), market="atlantis")

    def test_selling_points_come_from_tire_pack_data(self):
        # The cert angle must name the market's real program, not a
        # made-up one; the load angle must use the real common values.
        items = dvl.build_daily_list(day=date(2026, 11, 22))
        cert = items[2]
        self.assertIn(tp.MARKETS[
            [k for k, v in tp.MARKETS.items()
             if v["name_en"] == cert["market_en"]][0]]["program"],
            cert["selling_point"])
        load = items[1]
        self.assertIn(tp.TIRE_SIZES[load["size"]]["common_li"],
                      load["selling_point"])


class TestParseDate(unittest.TestCase):
    def test_none_and_empty_mean_today(self):
        self.assertEqual(dvl.parse_date(None), date.today())
        self.assertEqual(dvl.parse_date(""), date.today())
        self.assertEqual(dvl.parse_date("   "), date.today())

    def test_valid_date_parses(self):
        self.assertEqual(dvl.parse_date("2026-11-22"), date(2026, 11, 22))

    def test_bad_date_raises(self):
        for bad in ["2026-13-01", "2026-02-30", "22/11/2026",
                    "tomorrow", "2026-11"]:
            with self.assertRaises(ValueError, msg=bad):
                dvl.parse_date(bad)


class TestRendering(unittest.TestCase):
    def test_table_rendering_has_all_five_and_disclaimer(self):
        items = dvl.build_daily_list(day=date(2026, 11, 22))
        text = dvl.render_table(items, date(2026, 11, 22))
        for it in items:
            self.assertIn(it["size"], text)
            self.assertIn(it["selling_point"], text)
        self.assertIn("2026-11-22", text)
        self.assertIn("厂家数据表", text)  # disclaimer, no invented numbers

    def test_json_rendering_round_trips(self):
        items = dvl.build_daily_list(day=date(2026, 11, 22))
        data = json.loads(dvl.render_json(items, date(2026, 11, 22)))
        self.assertEqual(data["date"], "2026-11-22")
        self.assertEqual(len(data["videos"]), 5)
        self.assertEqual(data["videos"][0]["slot"], 1)


class TestCli(unittest.TestCase):
    def test_cli_default_runs(self):
        code, out = run_cli("--date", "2026-11-22")
        self.assertEqual(code, 0)
        self.assertIn("每日 5 条视频清单", out)
        self.assertIn("11.00R20", out)  # first slot on this date

    def test_cli_json_and_seed(self):
        code, out = run_cli("--seed", "7", "--format", "json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(len(data["videos"]), 5)

    def test_cli_market_pin(self):
        code, out = run_cli("--date", "2026-11-22", "--market", "ghana")
        self.assertEqual(code, 0)
        self.assertIn("加纳", out)
        self.assertNotIn("尼日利亚", out)

    def test_cli_bad_date_exits_nonzero(self):
        code, out = run_cli("--date", "2026-13-40")
        self.assertNotEqual(code, 0)
        self.assertIn("Bad date", out)

    def test_cli_unknown_market_exits_nonzero(self):
        code, out = run_cli("--date", "2026-11-22", "--market", "atlantis")
        self.assertNotEqual(code, 0)

    def test_cli_out_writes_file(self, tmp_path=None):
        out_file = REPO_ROOT / "tests" / "_tmp_daily_video_out.txt"
        try:
            code, out = run_cli("--date", "2026-11-22", "--out",
                                str(out_file))
            self.assertEqual(code, 0)
            self.assertTrue(out_file.exists())
            self.assertIn("每日 5 条视频清单", out_file.read_text(
                encoding="utf-8"))
        finally:
            if out_file.exists():
                out_file.unlink()


if __name__ == "__main__":
    unittest.main()
