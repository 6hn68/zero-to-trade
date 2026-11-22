#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/lead_score.py - T0-T3 lead scoring.

Run: python3 -m unittest discover -s tests -v   (from the repo root)
"""

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import lead_score as ls  # noqa: E402

HEADER = ["company", "country", "product", "source", "email", "phone",
          "years", "contact", "note"]


def row(**overrides):
    """A complete, high-signal lead; override fields to lower the score."""
    base = {"company": "【示例】海湾轮胎贸易", "country": "Saudi Arabia",
            "product": "TBR 12.00R20", "source": "referral",
            "email": "demo01@sample.example", "phone": "+000 00 000 0000",
            "years": "12", "contact": "采购经理",
            "note": "Annual RFQ for truck tyres, looking for supplier, 40HQ container regular"}
    base.update(overrides)
    return base


def write_csv(rows):
    tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                      encoding="utf-8", newline="")
    writer = csv.DictWriter(tmp, fieldnames=HEADER)
    writer.writeheader()
    writer.writerows(rows)
    tmp.close()
    return tmp.name


class TestScoring(unittest.TestCase):
    def test_full_signal_lead_is_t0(self):
        total, _detail = ls.score_lead(row())
        self.assertEqual(ls.grade(total), "T0")
        self.assertEqual(total, 95)

    def test_missing_everything_is_t3_not_a_crash(self):
        # A CSV row with only a company name: no traceback, just the lowest tier.
        total, _detail = ls.score_lead({"company": "Acme"})
        self.assertEqual(total, 10)
        self.assertEqual(ls.grade(total), "T3")

    def test_grade_boundaries(self):
        self.assertEqual(ls.grade(90), "T0")
        self.assertEqual(ls.grade(60), "T1")
        self.assertEqual(ls.grade(40), "T2")
        self.assertEqual(ls.grade(39), "T3")

    def test_example_file_counts_never_drift(self):
        rows = ls.read_leads(str(REPO_ROOT / "examples" / "leads_example.csv"))
        results, duplicates = ls.analyze(rows)
        counts = {}
        for item in results:
            counts[item["tier"]] = counts.get(item["tier"], 0) + 1
        self.assertEqual(len(results), 10)
        self.assertEqual(duplicates, 0)
        self.assertEqual(counts, {"T0": 2, "T1": 5, "T2": 1, "T3": 2})

    def test_duplicate_leads_merge(self):
        path = write_csv([row(), row()])
        results, duplicates = ls.analyze(ls.read_leads(path))
        self.assertEqual(len(results), 1)
        self.assertEqual(duplicates, 1)

    def test_empty_csv_raises_a_readable_error(self):
        # Header-only CSV: the script refuses with words, it does not silently
        # return an empty list (an empty list would look like "no leads today").
        path = write_csv([])
        with self.assertRaises(ls.LeadDataError):
            ls.read_leads(path)


class TestLeadScoreCLI(unittest.TestCase):
    def test_cli_runs_on_example_file(self):
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "lead_score.py"),
             str(REPO_ROOT / "examples" / "leads_example.csv")],
            capture_output=True, text=True, cwd=REPO_ROOT)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("T0:2 / T1:5 / T2:1 / T3:2", proc.stdout)

    def test_cli_json_format_is_parseable(self):
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "lead_score.py"),
             str(REPO_ROOT / "examples" / "leads_example.csv"),
             "--format", "json"],
            capture_output=True, text=True, cwd=REPO_ROOT)
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        items = payload["leads"] if isinstance(payload, dict) else payload
        self.assertEqual(len(items), 10)

    def test_run_log_written(self):
        subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "lead_score.py"),
             str(REPO_ROOT / "examples" / "leads_example.csv")],
            capture_output=True, text=True, cwd=REPO_ROOT)
        log_path = REPO_ROOT / "logs" / "lead_score.log"
        self.assertTrue(log_path.exists())
        text = log_path.read_text(encoding="utf-8")
        self.assertIn("RUN argv=", text)
        self.assertIn("RESULT total=10", text)

    def test_lighting_example_scores_eight_rows(self):
        # 非轮胎示例：LED 灯具 8 条，同一张表头；品类词只认轮胎词，
        # 所以 LED 行拿不到那 4 分，分布是 T0:0/T1:2/T2:2/T3:4。
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "lead_score.py"),
             str(REPO_ROOT / "examples" / "leads_example_lighting.csv"),
             "--format", "json"],
            capture_output=True, text=True, cwd=REPO_ROOT)
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        items = payload["leads"] if isinstance(payload, dict) else payload
        self.assertEqual(len(items), 8)
        counts = {}
        for item in items:
            counts[item["tier"]] = counts.get(item["tier"], 0) + 1
        self.assertEqual(counts, {"T1": 2, "T2": 2, "T3": 4})

    def test_unclosed_quote_errors_in_words(self):
        with tempfile.NamedTemporaryFile(
                "w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
            tmp.write('company,country\n"unclosed quote,Nigeria\n')
            path = tmp.name
        try:
            with self.assertRaises(ls.LeadDataError) as ctx:
                ls.read_leads(path)
            self.assertIn("引号没闭合", str(ctx.exception))
        finally:
            Path(path).unlink(missing_ok=True)

    def test_cli_unclosed_quote_no_traceback(self):
        with tempfile.NamedTemporaryFile(
                "w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
            tmp.write('company,country\n"unclosed quote,Nigeria\n')
            path = tmp.name
        try:
            proc = subprocess.run(
                [sys.executable, str(REPO_ROOT / "scripts" / "lead_score.py"),
                 path],
                capture_output=True, text=True, cwd=REPO_ROOT)
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn("Traceback", proc.stdout + proc.stderr)
            self.assertIn("引号没闭合", proc.stdout + proc.stderr)
        finally:
            Path(path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
