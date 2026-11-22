#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/quote_engine.py — FOB/CIF quote + concession ladder.

Run: python3 -m unittest discover -s tests -v   (from the repo root)
Only the standard library is used, same rule as the scripts themselves.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import quote_engine as qe  # noqa: E402


def run_quote(*args):
    """Run the quote CLI; return (exit_code, stdout+stderr)."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "quote_engine.py"), *args],
        capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout + proc.stderr


class TestBuildQuoteBaseline(unittest.TestCase):
    def test_baseline_numbers_never_drift(self):
        # The numbers README and --help promise. If this moves, docs must move too.
        q = qe.build_quote(28, 6, 15, 0.0015)
        self.assertEqual(q["fob_list"], 33.17)
        self.assertEqual(q["cif_list"], 39.23)
        self.assertEqual(q["fob_floor"], 31.18)
        self.assertEqual(q["cif_floor"], 37.24)
        self.assertEqual(q["cost_base"], 28.84)

    def test_cif_identity_holds(self):
        q = qe.build_quote(28, 6, 15, 0.0015)
        self.assertAlmostEqual(q["cif_list"],
                               q["fob_list"] + 6 + q["insurance"], places=2)

    def test_ladder_is_three_steps_and_never_below_floor(self):
        q = qe.build_quote(28, 6, 15, 0.0015)
        self.assertEqual(len(q["ladder"]), 3)
        self.assertEqual([s["cum_pct"] for s in q["ladder"]], [2.5, 4.0, 5.0])
        for step in q["ladder"]:
            self.assertGreaterEqual(step["new_fob"], q["fob_floor"])
            self.assertTrue(step["condition"])  # every cut buys something back

    def test_tiny_margin_locks_floor_to_cost_base(self):
        q = qe.build_quote(28, 6, 1, 0.0015)
        self.assertEqual(q["fob_floor"], q["cost_base"])
        self.assertTrue(any("没有让步空间" in w for w in q["warnings"]))


class TestClientViewIsolation(unittest.TestCase):
    def test_table_client_view_hides_floor_numbers(self):
        code, out = run_quote("--cost", "28", "--freight", "6", "--margin", "15",
                              "--audience", "client", "--anchor", "42")
        self.assertEqual(code, 0)
        for leaked in ("31.18", "37.24", "28.84", "锚价定位"):
            self.assertNotIn(leaked, out)

    def test_json_client_view_hides_inputs_and_margin(self):
        code, out = run_quote("--cost", "28", "--freight", "6", "--margin", "15",
                              "--audience", "client", "--anchor", "42",
                              "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertNotIn("inputs", payload["meta"])
        quote = payload["quote"]
        for key in ("cost_base", "fob_floor", "cif_floor", "warnings",
                    "positioning", "contingency", "margin_mode"):
            self.assertNotIn(key, quote)
        # The quotes themselves must still be there.
        self.assertEqual(quote["fob_list"], 33.17)
        self.assertEqual(quote["cif_list"], 39.23)

    def test_json_internal_view_still_has_everything(self):
        code, out = run_quote("--cost", "28", "--freight", "6", "--margin", "15",
                              "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertIn("inputs", payload["meta"])
        self.assertEqual(payload["meta"]["inputs"]["cost"], 28.0)
        self.assertIn("fob_floor", payload["quote"])


class TestBoundaries(unittest.TestCase):
    def test_bad_inputs_raise_value_error(self):
        cases = [
            dict(cost=0, freight=6, margin=15, insurance_rate=0.0015),
            dict(cost=-5, freight=6, margin=15, insurance_rate=0.0015),
            dict(cost=20_000_000, freight=6, margin=15, insurance_rate=0.0015),
            dict(cost=28, freight=6, margin=1500, insurance_rate=0.0015),
            dict(cost=28, freight=6, margin=15, insurance_rate=0.0015,
                 contingency=5),
            dict(cost=28, freight=-1, margin=15, insurance_rate=0.0015),
            dict(cost=28, freight=6, margin=15, insurance_rate=0.09),
        ]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    qe.build_quote(**kwargs)

    def test_cli_rejects_bad_moq_and_validity_with_words_not_traceback(self):
        for args in (("--cost", "28", "--moq", "-5"),
                     ("--cost", "28", "--validity", "0"),
                     ("--cost", "28", "--validity", "400")):
            code, out = run_quote(*args)
            self.assertNotEqual(code, 0)
            self.assertIn("✗", out)
            self.assertNotIn("Traceback", out)

    def test_missing_cost_is_argparse_error_not_crash(self):
        code, out = run_quote()
        self.assertNotEqual(code, 0)
        self.assertIn("--cost", out)
        self.assertNotIn("Traceback", out)


class TestQuoteSheetValidation(unittest.TestCase):
    def test_bare_run_missing_five_names_them(self):
        # Price, currency and validity have values; the other five must be filled in.
        v = qe.validate_quote_sheet(currency="USD", validity_days=30)
        self.assertFalse(v["ok"])
        self.assertEqual(v["missing_keys"],
                         ["incoterm", "spec", "moq", "lead_time", "payment"])
        self.assertEqual(v["missing"],
                         ["贸易术语与港口", "规格型号", "最小起订量", "交货期", "付款条件"])
        self.assertEqual(len(v["items"]), 8)

    def test_full_sheet_passes(self):
        v = qe.validate_quote_sheet(
            currency="CNY", incoterm="FOB Yantian", spec="示例型号-A",
            moq=300, lead_time="25天",
            payment_terms="T/T 30% 定金 + 70% 见提单副本", validity_days=30)
        self.assertTrue(v["ok"])
        self.assertEqual(v["missing"], [])
        self.assertTrue(all(i["present"] for i in v["items"]))

    def test_cli_strict_fails_and_names_missing(self):
        code, out = run_quote("--cost", "28", "--freight", "6", "--margin", "15",
                              "--strict")
        self.assertEqual(code, 2)
        for label in ("贸易术语与港口", "规格型号", "最小起订量", "交货期", "付款条件"):
            self.assertIn(label, out)
        self.assertIn("8 要素", out)
        self.assertNotIn("Traceback", out)

    def test_cli_strict_passes_when_complete(self):
        code, out = run_quote("--cost", "28", "--freight", "6", "--margin", "15",
                              "--incoterm", "FOB Yantian", "--spec", "示例型号-A",
                              "--moq", "300", "--lead-time", "25天",
                              "--payment", "T/T 30% 定金 + 70% 见提单副本",
                              "--strict")
        self.assertEqual(code, 0)
        self.assertIn("8 要素齐了", out)

    def test_table_shows_eight_elements_with_marks(self):
        code, out = run_quote("--cost", "28", "--freight", "6", "--margin", "15")
        self.assertEqual(code, 0)
        self.assertIn("报价单 8 要素校验", out)
        for label in ("单价", "币种", "贸易术语与港口", "规格型号",
                      "最小起订量", "交货期", "付款条件", "报价有效期"):
            self.assertIn(label, out)

    def test_json_carries_validation_object(self):
        code, out = run_quote("--cost", "28", "--freight", "6", "--margin", "15",
                              "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        v = payload["meta"]["validation"]
        self.assertFalse(v["ok"])
        self.assertEqual(v["missing_keys"],
                         ["incoterm", "spec", "moq", "lead_time", "payment"])


class TestTaxInclusiveCNY(unittest.TestCase):
    def test_cny_tax_inclusive_numbers(self):
        # 【示例】价格虚构：cost 200 CNY, freight 6, margin 15%, VAT 13% inclusive.
        # cost_base 206.00, FOB 236.90, CIF 243.30; excl = incl / 1.13.
        q = qe.build_quote(200, 6, 15, 0.0015,
                           tax_rate_pct=13.0, tax_inclusive=True)
        self.assertEqual(q["fob_list"], 236.90)
        self.assertEqual(q["cif_list"], 243.30)
        self.assertEqual(q["tax_mode"], "inclusive")
        self.assertEqual(q["tax_rate_pct"], 13.0)
        self.assertEqual(q["fob_list_vat_excl"], 209.65)
        self.assertEqual(q["cif_list_vat_excl"], 215.31)
        self.assertEqual(q["fob_list_vat_incl"], 236.90)
        self.assertEqual(q["vat_on_fob_unit"], 27.25)
        self.assertEqual(q["vat_on_cif_unit"], 27.99)

    def test_tax_exclusive_numbers(self):
        # Same chain, quoted price is VAT-exclusive: incl = excl x 1.13.
        q = qe.build_quote(200, 6, 15, 0.0015,
                           tax_rate_pct=13.0, tax_inclusive=False)
        self.assertEqual(q["tax_mode"], "exclusive")
        self.assertEqual(q["fob_list_vat_incl"], 267.70)
        self.assertEqual(q["cif_list_vat_incl"], 274.93)
        self.assertEqual(q["vat_on_fob_unit"], 30.80)
        self.assertEqual(q["vat_on_cif_unit"], 31.63)

    def test_no_tax_rate_means_no_tax_keys(self):
        q = qe.build_quote(28, 6, 15, 0.0015)
        for key in ("tax_rate_pct", "tax_mode", "fob_list_vat_incl",
                    "fob_list_vat_excl", "vat_on_fob_unit"):
            self.assertNotIn(key, q)

    def test_bad_tax_rate_rejected(self):
        for rate in (-1, 150):
            with self.subTest(rate=rate):
                with self.assertRaises(ValueError):
                    qe.build_quote(28, 6, 15, 0.0015, tax_rate_pct=rate)

    def test_cli_cny_tax_inclusive_marks_basis(self):
        code, out = run_quote("--cost", "200", "--currency", "CNY",
                              "--tax-inclusive", "--tax-rate", "13",
                              "--freight", "6")
        self.assertEqual(code, 0)
        self.assertIn("236.90", out)
        self.assertIn("209.65", out)
        self.assertIn("人民币含税价", out)


if __name__ == "__main__":
    unittest.main()
