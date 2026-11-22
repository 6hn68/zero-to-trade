#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for index.html staying in sync with the repo.

- The two embedded example fallbacks (file:// open, fetch fails) must stay
  byte-identical to the CSV data rows they mirror.
- The "more scripts" card must name all 12 scripts.

Run: python3 -m unittest discover -s tests -v   (from the repo root)
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SCRIPTS = [
    "lead_score.py", "outreach_gen.py", "followup_plan.py",
    "quote_engine.py", "due_diligence.py", "tire_pack.py",
    "landed_cost.py", "trade_show.py", "nudge.py", "anchor_price.py",
    "fast_path.py", "check_private_data.py",
]


def csv_data_lines(path):
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    return [line for line in lines if line.strip() and not line.startswith("#")]


class TestDemoPageSync(unittest.TestCase):
    def test_example_fallbacks_match_csvs(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        blocks = re.findall(
            r"document\.getElementById\(\"csv\"\)\.value=\n`(.*?)`;",
            html, re.S)
        self.assertEqual(len(blocks), 2, "expect tire + lighting fallbacks")
        tire_csv = csv_data_lines(REPO_ROOT / "examples" / "leads_example.csv")
        led_csv = csv_data_lines(
            REPO_ROOT / "examples" / "leads_example_lighting.csv")
        self.assertEqual(blocks[0].split("\n"), tire_csv,
                         "tire fallback drifted from leads_example.csv")
        self.assertEqual(blocks[1].split("\n"), led_csv,
                         "lighting fallback drifted from "
                         "leads_example_lighting.csv")

    def test_all_twelve_scripts_named(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        for name in SCRIPTS:
            self.assertIn(name, html, "index.html does not mention %s" % name)

    def test_fast_path_v19_feature_named(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("fast_path.py", html)
        self.assertIn("七天快路径", html)


if __name__ == "__main__":
    unittest.main()
