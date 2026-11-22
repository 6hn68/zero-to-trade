#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/anchor_price.py — competitor anchor pricing, three tiers.

Run: python3 -m unittest discover -s tests -v   (from the repo root)
Only the standard library is used, same rule as the scripts themselves.

Hand-checked numbers (Decimal, ROUND_HALF_UP; profit/margin/markup are
computed from unrounded values, then rounded — same rule as landed_cost):
  Group 1: comp 38/46/42, cost 28, freight 6, duty 10%, rate 0.15%
    cost_base = 28 x 1.03 = 28.84
    denom = 1 - 1.10 x 0.0015 = 0.99835
    cif_floor = (28.84 + 6) / 0.99835 = 34.8976... -> 34.90
    ddp_floor = 34.8976 x 1.10 = 38.3874... -> 38.39
    aggressive 42 x 0.97 = 40.74: profit 5.84, margin 14.34%, FOB 34.67, markup 20.22%
    median     42.00: profit 7.10, margin 16.91%, FOB 35.93, markup 24.59%
    conservative 42 x 1.03 = 43.26: profit 8.36, margin 19.33%, FOB 37.19, markup 28.95%
    DDP tiers: 44.81 / 46.20 / 47.59
  Group 2 (no median given): comp 44/56, cost 30, freight 5, duty 0%
    median estimated = (44 + 56) / 2 = 50.00
    cost_base = 30 x 1.03 = 30.90; cif_floor = 35.90 / 0.99835 = 35.9593... -> 35.96
    aggressive 48.50: profit 12.54, margin 25.86%, FOB 43.42, markup 40.52%
    median     50.00: profit 14.04, margin 28.08%, FOB 44.92, markup 45.36%
    conservative 51.50: profit 15.54, margin 30.18%, FOB 46.42, markup 50.21%
  Below-cost group: comp 30/36/33, cost 28, freight 6
    cif_floor 34.90; all three tiers (32.01 / 33.00 / 33.99) below it.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import anchor_price as ap  # noqa: E402
import landed_cost as lc  # noqa: E402
import quote_engine as qe  # noqa: E402


def run_anchor(*args):
    """Run the anchor_price CLI; return (exit_code, stdout+stderr)."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "anchor_price.py"), *args],
        capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout + proc.stderr


def group1(**over):
    kw = dict(comp_low=38, comp_high=46, comp_median=42, cost=28, freight=6,
              duty_pct=10, verified=frozenset({"cost", "freight", "fx", "payment", "validity"}))
    kw.update(over)
    return ap.build_anchor(**kw)


class TestArithmeticGroup1(unittest.TestCase):
    def test_group1_itemised(self):
        a = group1()
        self.assertEqual(a["cost_base"], 28.84)
        self.assertEqual(a["cif_floor"], 34.90)
        self.assertEqual(a["ddp_floor"], 38.39)
        self.assertFalse(a["median_estimated"])
        self.assertFalse(a["below_cost"])
        tiers = {t["key"]: t for t in a["tiers"]}
        self.assertEqual(tiers["aggressive"]["price_cif"], 40.74)
        self.assertEqual(tiers["median"]["price_cif"], 42.00)
        self.assertEqual(tiers["conservative"]["price_cif"], 43.26)
        self.assertEqual(tiers["aggressive"]["price_ddp"], 44.81)
        self.assertEqual(tiers["median"]["price_ddp"], 46.20)
        self.assertEqual(tiers["conservative"]["price_ddp"], 47.59)
        self.assertEqual(tiers["aggressive"]["profit_cif"], 5.84)
        self.assertEqual(tiers["median"]["profit_cif"], 7.10)
        self.assertEqual(tiers["conservative"]["profit_cif"], 8.36)
        self.assertEqual(tiers["aggressive"]["margin_pct"], 14.34)
        self.assertEqual(tiers["median"]["margin_pct"], 16.91)
        self.assertEqual(tiers["conservative"]["margin_pct"], 19.33)

    def test_group1_fob_equiv_and_markup(self):
        a = group1()
        tiers = {t["key"]: t for t in a["tiers"]}
        self.assertEqual(tiers["aggressive"]["fob_equiv"], 34.67)
        self.assertEqual(tiers["median"]["fob_equiv"], 35.93)
        self.assertEqual(tiers["conservative"]["fob_equiv"], 37.19)
        self.assertEqual(tiers["aggressive"]["implied_markup_pct"], 20.22)
        self.assertEqual(tiers["median"]["implied_markup_pct"], 24.59)
        self.assertEqual(tiers["conservative"]["implied_markup_pct"], 28.95)
        for t in a["tiers"]:
            self.assertFalse(t["below_cost"])
            self.assertTrue(t["scenario"])


class TestArithmeticGroup2NoMedian(unittest.TestCase):
    def test_group2_median_estimated(self):
        a = ap.build_anchor(44, 56, None, 30, 5)
        self.assertTrue(a["median_estimated"])
        self.assertEqual(a["comp_median"], 50.00)
        self.assertEqual(a["cost_base"], 30.90)
        self.assertEqual(a["cif_floor"], 35.96)
        self.assertTrue(any("估算" in w for w in a["warnings"]))
        tiers = {t["key"]: t for t in a["tiers"]}
        self.assertEqual(tiers["aggressive"]["price_cif"], 48.50)
        self.assertEqual(tiers["median"]["price_cif"], 50.00)
        self.assertEqual(tiers["conservative"]["price_cif"], 51.50)
        self.assertEqual(tiers["aggressive"]["profit_cif"], 12.54)
        self.assertEqual(tiers["median"]["profit_cif"], 14.04)
        self.assertEqual(tiers["conservative"]["profit_cif"], 15.54)

    def test_group2_margins_and_fob(self):
        a = ap.build_anchor(44, 56, None, 30, 5)
        tiers = {t["key"]: t for t in a["tiers"]}
        self.assertEqual(tiers["aggressive"]["margin_pct"], 25.86)
        self.assertEqual(tiers["median"]["margin_pct"], 28.08)
        self.assertEqual(tiers["conservative"]["margin_pct"], 30.18)
        self.assertEqual(tiers["aggressive"]["fob_equiv"], 43.42)
        self.assertEqual(tiers["median"]["fob_equiv"], 44.92)
        self.assertEqual(tiers["conservative"]["fob_equiv"], 46.42)
        self.assertEqual(tiers["aggressive"]["implied_markup_pct"], 40.52)
        self.assertEqual(tiers["median"]["implied_markup_pct"], 45.36)
        self.assertEqual(tiers["conservative"]["implied_markup_pct"], 50.21)


class TestBelowCost(unittest.TestCase):
    def test_all_three_tiers_below_cost(self):
        a = ap.build_anchor(30, 36, 33, 28, 6)
        self.assertTrue(a["below_cost"])
        self.assertTrue(a["median_below_cost"])
        tiers = {t["key"]: t for t in a["tiers"]}
        self.assertEqual(tiers["aggressive"]["price_cif"], 32.01)
        self.assertEqual(tiers["median"]["price_cif"], 33.00)
        self.assertEqual(tiers["conservative"]["price_cif"], 33.99)
        for t in a["tiers"]:
            self.assertTrue(t["below_cost"])
            self.assertLess(t["profit_cif"], 0)
            self.assertLess(t["margin_pct"], 0)
        self.assertTrue(any(ap.BELOW_COST_WARNING in w for w in a["warnings"]))

    def test_only_aggressive_below_cost(self):
        # median 35.50: aggressive 34.44 < floor 34.90, median 35.50 above it.
        a = ap.build_anchor(34, 37, 35.5, 28, 6)
        self.assertTrue(a["below_cost"])
        self.assertFalse(a["median_below_cost"])
        tiers = {t["key"]: t for t in a["tiers"]}
        self.assertTrue(tiers["aggressive"]["below_cost"])
        self.assertFalse(tiers["median"]["below_cost"])
        self.assertFalse(tiers["conservative"]["below_cost"])
        self.assertTrue(any(ap.BELOW_COST_WARNING in w for w in a["warnings"]))

    def test_below_cost_warning_on_cli(self):
        code, out = run_anchor("--comp-low", "30", "--comp-high", "36",
                               "--comp-median", "33", "--cost", "28",
                               "--freight", "6")
        self.assertEqual(code, 0)
        self.assertIn(ap.BELOW_COST_WARNING, out)
        self.assertIn("34.90", out)
        self.assertIn("低于成本", out)


class TestChecklist(unittest.TestCase):
    def test_checklist_has_all_five_items(self):
        a = ap.build_anchor(38, 46, 42, 28, 6)
        self.assertEqual([i["key"] for i in a["checklist"]],
                         ["cost", "freight", "fx", "payment", "validity"])
        self.assertEqual([i["label"] for i in a["checklist"]],
                         ["成本", "运费", "汇率", "付款条件", "有效期"])

    def test_default_all_pending(self):
        a = ap.build_anchor(38, 46, 42, 28, 6)
        self.assertEqual(a["pending_count"], 5)
        self.assertTrue(all(i["status"] == "待核" for i in a["checklist"]))
        self.assertTrue(any("待核" in w for w in a["warnings"]))

    def test_verified_subset_and_all(self):
        a = ap.build_anchor(38, 46, 42, 28, 6,
                            verified=frozenset({"cost", "freight"}))
        self.assertEqual(a["pending_count"], 3)
        by_key = {i["key"]: i["status"] for i in a["checklist"]}
        self.assertEqual(by_key["cost"], "已核")
        self.assertEqual(by_key["freight"], "已核")
        self.assertEqual(by_key["fx"], "待核")
        full = group1()
        self.assertEqual(full["pending_count"], 0)
        self.assertTrue(all(i["status"] == "已核" for i in full["checklist"]))

    def test_verified_chinese_aliases_and_bad_key(self):
        self.assertEqual(ap.normalize_verified("成本,运费,汇率,付款条件,有效期"),
                         frozenset({"cost", "freight", "fx", "payment", "validity"}))
        self.assertEqual(ap.normalize_verified("cost, freight"), frozenset({"cost", "freight"}))
        with self.assertRaises(ValueError):
            ap.normalize_verified("cost,boss")
        code, out = run_anchor("--comp-low", "38", "--comp-high", "46",
                               "--comp-median", "42", "--cost", "28",
                               "--freight", "6",
                               "--verified", "cost,boss")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)


class TestOutputFormats(unittest.TestCase):
    def test_json_internal_has_cost_margin_checklist(self):
        code, out = run_anchor("--comp-low", "38", "--comp-high", "46",
                               "--comp-median", "42", "--cost", "28",
                               "--freight", "6", "--duty", "10",
                               "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        a = payload["anchor_price"]
        self.assertEqual(a["cost_base"], 28.84)
        self.assertEqual(a["cif_floor"], 34.90)
        self.assertEqual(len(a["tiers"]), 3)
        self.assertEqual(len(a["checklist"]), 5)
        self.assertEqual(a["tiers"][1]["price_cif"], 42.00)
        self.assertEqual(a["tiers"][1]["margin_pct"], 16.91)
        self.assertIn("inputs", payload["meta"])

    def test_json_client_hides_cost_margin_checklist(self):
        code, out = run_anchor("--comp-low", "38", "--comp-high", "46",
                               "--comp-median", "42", "--cost", "28",
                               "--freight", "6", "--duty", "10",
                               "--audience", "client", "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        a = payload["anchor_price"]
        self.assertEqual(len(a["tiers"]), 3)
        self.assertEqual([t["price_cif"] for t in a["tiers"]],
                         [40.74, 42.00, 43.26])
        for hidden in ("cost", "cost_base", "cif_floor", "ddp_floor",
                       "comp_low", "comp_high", "comp_median",
                       "checklist", "warnings", "below_cost",
                       "insurance_rate", "contingency"):
            self.assertNotIn(hidden, a)
        for t in a["tiers"]:
            for hidden in ("profit_cif", "margin_pct", "fob_equiv",
                           "implied_markup_pct", "below_cost"):
                self.assertNotIn(hidden, t)
            self.assertIn("scenario", t)
        self.assertNotIn("inputs", payload["meta"])

    def test_table_client_hides_cost_margin_checklist(self):
        code, out = run_anchor("--comp-low", "38", "--comp-high", "46",
                               "--comp-median", "42", "--cost", "28",
                               "--freight", "6", "--duty", "10",
                               "--audience", "client")
        self.assertEqual(code, 0)
        for hidden in ("成本", "毛利", "复核", "保本", "28.84", "34.90", "待核"):
            self.assertNotIn(hidden, out)
        self.assertIn("40.74", out)
        self.assertIn("42.00", out)
        self.assertIn("43.26", out)

    def test_cli_out_writes_file(self):
        out_path = REPO_ROOT / "anchor_out_smoke.txt"
        try:
            code, out = run_anchor("--comp-low", "38", "--comp-high", "46",
                                   "--comp-median", "42", "--cost", "28",
                                   "--freight", "6", "--out", str(out_path))
            self.assertEqual(code, 0)
            self.assertTrue(out_path.is_file())
            self.assertIn("42.00", out_path.read_text(encoding="utf-8"))
        finally:
            if out_path.exists():
                out_path.unlink()


class TestCrossCheckWithQuoteAndLandedCost(unittest.TestCase):
    def test_tier_fob_reproduces_cif_in_landed_cost(self):
        # Median tier FOB 35.93 + freight 6 through landed_cost must give CIF 42.00.
        a = group1()
        median_tier = a["tiers"][1]
        r = lc.build_landed_cost(median_tier["fob_equiv"], 6, 0.0015, 0)
        self.assertEqual(r["cif_unit"], median_tier["price_cif"])
        self.assertEqual(r["cif_unit"], 42.00)
        r2 = lc.build_landed_cost(a["tiers"][0]["fob_equiv"], 6, 0.0015, 10)
        self.assertEqual(r2["cif_unit"], 40.74)
        self.assertEqual(r2["ddp_unit"], 44.81)

    def test_quote_engine_with_implied_markup_reproduces_tier(self):
        # quote_engine: cost 28, freight 6, margin = implied markup 24.59%
        # -> FOB 35.93, CIF 42.00, exactly the median tier.
        a = group1()
        median_tier = a["tiers"][1]
        q = qe.build_quote(28, 6, median_tier["implied_markup_pct"], 0.0015)
        self.assertEqual(q["fob_list"], median_tier["fob_equiv"])
        self.assertEqual(q["cif_list"], median_tier["price_cif"])
        self.assertEqual(q["cif_list"], 42.00)


class TestValidationAndHelp(unittest.TestCase):
    def test_bad_inputs_rejected(self):
        bad = [
            ["--comp-low", "46", "--comp-high", "38", "--cost", "28"],
            ["--comp-low", "38", "--comp-high", "46", "--comp-median", "50",
             "--cost", "28"],
            ["--comp-low", "38", "--comp-high", "46", "--comp-median", "42",
             "--cost", "0"],
            ["--comp-low", "38", "--comp-high", "46", "--comp-median", "42",
             "--cost", "28", "--freight", "-1"],
            ["--comp-low", "38", "--comp-high", "46", "--comp-median", "42",
             "--cost", "28", "--duty", "-5"],
            ["--comp-low", "38", "--comp-high", "46", "--comp-median", "42",
             "--cost", "28", "--insurance", "30"],
        ]
        for args in bad:
            with self.subTest(args=args):
                code, out = run_anchor(*args)
                self.assertNotEqual(code, 0)
                self.assertNotIn("Traceback", out)

    def test_missing_required_is_human_error_not_traceback(self):
        code, out = run_anchor("--comp-low", "38", "--comp-high", "46")
        self.assertNotEqual(code, 0)
        self.assertIn("cost", out.lower())
        self.assertNotIn("Traceback", out)

    def test_help_has_real_examples(self):
        code, out = run_anchor("--help")
        self.assertEqual(code, 0)
        self.assertIn("--comp-low 38 --comp-high 46 --comp-median 42 --cost 28 --freight 6 --duty 10", out)
        self.assertIn("--audience client", out)
        self.assertIn("40.74", out)


class TestLocalFeeChain(unittest.TestCase):
    def test_local_fee_matches_quote_engine_cost_base(self):
        # Chain consistency: anchor cost_base must equal quote_engine cost_base
        # for the same cost + local fee, and anchor cif_floor must equal the
        # landed_cost CIF for FOB = that cost_base (one formula, three scripts).
        a = ap.build_anchor(38, 46, 42, 28, 6, local=5.0)
        self.assertEqual(a["cost_base"], 33.84)   # 28 x 1.03 + 5
        self.assertEqual(a["cif_floor"], 39.91)   # (33.84 + 6) / 0.99835
        q = qe.build_quote(28, 6, 15, 0.0015, local=5.0)
        self.assertEqual(q["cost_base"], a["cost_base"])
        r = lc.build_landed_cost(a["cost_base"], 6, 0.0015, 0)
        self.assertEqual(r["cif_unit"], a["cif_floor"])

    def test_no_local_by_default(self):
        a = ap.build_anchor(38, 46, 42, 28, 6)
        self.assertEqual(a["local"], 0.0)
        self.assertEqual(a["cost_base"], 28.84)

    def test_bad_local_rejected(self):
        with self.assertRaises(ValueError):
            ap.build_anchor(38, 46, 42, 28, 6, local=-1)
        code, out = run_anchor("--comp-low", "38", "--comp-high", "46",
                               "--comp-median", "42", "--cost", "28",
                               "--freight", "6", "--local", "-1")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)


class TestTaxInclusiveTiers(unittest.TestCase):
    def test_tiers_tax_incl_13(self):
        # 【示例】税率虚构：group 1 tiers x 1.13 (from unrounded values).
        a = ap.build_anchor(38, 46, 42, 28, 6, duty_pct=10, tax_rate_pct=13.0)
        self.assertEqual(a["tax_rate_pct"], 13.0)
        tiers = {t["key"]: t for t in a["tiers"]}
        self.assertEqual(tiers["aggressive"]["price_cif_tax_incl"], 46.04)
        self.assertEqual(tiers["median"]["price_cif_tax_incl"], 47.46)
        self.assertEqual(tiers["conservative"]["price_cif_tax_incl"], 48.88)
        self.assertEqual(tiers["median"]["price_ddp_tax_incl"], 52.21)
        self.assertEqual(tiers["conservative"]["price_ddp_tax_incl"], 53.77)

    def test_no_tax_keys_by_default(self):
        a = ap.build_anchor(38, 46, 42, 28, 6)
        self.assertEqual(a["tax_rate_pct"], 0.0)
        for t in a["tiers"]:
            self.assertNotIn("price_cif_tax_incl", t)
            self.assertNotIn("price_ddp_tax_incl", t)

    def test_bad_tax_rate_rejected(self):
        with self.assertRaises(ValueError):
            ap.build_anchor(38, 46, 42, 28, 6, tax_rate_pct=150)

    def test_cli_client_view_keeps_tax_incl_prices(self):
        code, out = run_anchor("--comp-low", "38", "--comp-high", "46",
                               "--comp-median", "42", "--cost", "28",
                               "--freight", "6", "--duty", "10",
                               "--tax-rate", "13", "--audience", "client",
                               "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        tiers = {t["key"]: t for t in payload["anchor_price"]["tiers"]}
        self.assertEqual(tiers["median"]["price_cif_tax_incl"], 47.46)
        self.assertNotIn("cost_base", payload["anchor_price"])


if __name__ == "__main__":
    unittest.main()
