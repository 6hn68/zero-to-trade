#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/landed_cost.py — CIF/DDP landed cost + profit room.

Run: python3 -m unittest discover -s tests -v   (from the repo root)
Only the standard library is used, same rule as the scripts themselves.

Hand-checked numbers (Decimal, ROUND_HALF_UP):
  Group 1: FOB 30, freight 5, rate 0.15%, duty 10%, port 2, qty 1
    denom = 1 - 1.10*0.0015 = 0.99835
    CIF = 35 / 0.99835 = 35.0578... -> 35.06
    insurance = 35.0578*1.10*0.0015 = 0.0578... -> 0.06
    duty = 35.0578*0.10 = 3.5058 -> 3.51
    DDP = 35.0578+3.5058+2 = 40.5636 -> 40.56
  Group 2: FOB 100, freight 12, rate 0.3%, duty 0%, port 0, qty 10
    denom = 1 - 1.10*0.003 = 0.9967
    CIF = 112 / 0.9967 = 112.3707... -> 112.37
    insurance = 112.3707*1.10*0.003 = 0.3708... -> 0.37
    DDP unit = 112.37, CIF/DDP total = 1123.71
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import landed_cost as lc  # noqa: E402
import quote_engine as qe  # noqa: E402


def run_landed(*args):
    """Run the landed_cost CLI; return (exit_code, stdout+stderr)."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "landed_cost.py"), *args],
        capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout + proc.stderr


class TestArithmeticGroup1(unittest.TestCase):
    def test_group1_itemised(self):
        r = lc.build_landed_cost(30, 5, 0.0015, 10, port_charges=2, qty=1)
        self.assertEqual(r["cif_unit"], 35.06)
        self.assertEqual(r["insurance_unit"], 0.06)
        self.assertEqual(r["duty_unit"], 3.51)
        self.assertEqual(r["ddp_unit"], 40.56)
        self.assertEqual(r["cif_total"], 35.06)
        self.assertEqual(r["ddp_total"], 40.56)

    def test_group1_cif_identity(self):
        # CIF must equal FOB + freight + insurance (same self-check as the script).
        r = lc.build_landed_cost(30, 5, 0.0015, 10, port_charges=2, qty=1)
        self.assertAlmostEqual(r["cif_unit"],
                               r["fob_unit"] + r["freight_unit"] + r["insurance_unit"],
                               places=2)


class TestArithmeticGroup2(unittest.TestCase):
    def test_group2_itemised(self):
        r = lc.build_landed_cost(100, 12, 0.003, 0, port_charges=0, qty=10)
        self.assertEqual(r["cif_unit"], 112.37)
        self.assertEqual(r["insurance_unit"], 0.37)
        self.assertEqual(r["duty_unit"], 0.0)
        self.assertEqual(r["ddp_unit"], 112.37)
        self.assertEqual(r["cif_total"], 1123.71)
        self.assertEqual(r["ddp_total"], 1123.71)

    def test_group2_profit_room(self):
        # sell 130/bar on group-2 numbers: profit 130-112.37 = 17.63, margin 13.56%
        r = lc.build_landed_cost(100, 12, 0.003, 0, port_charges=0, qty=10,
                                 sell_price=130)
        self.assertEqual(r["profit_unit"], 17.63)
        self.assertEqual(r["profit_total"], 176.29)
        self.assertEqual(r["profit_margin_pct"], 13.56)


class TestProfitAndBoundaries(unittest.TestCase):
    def test_group1_profit_with_qty(self):
        r = lc.build_landed_cost(30, 5, 0.0015, 10, port_charges=2, qty=100,
                                 sell_price=48)
        self.assertEqual(r["profit_unit"], 7.44)
        self.assertEqual(r["profit_total"], 743.64)
        self.assertEqual(r["profit_margin_pct"], 15.49)
        self.assertEqual(r["ddp_total"], 4056.36)

    def test_no_sell_price_means_no_profit_fields(self):
        r = lc.build_landed_cost(30, 5, 0.0015, 10, port_charges=2)
        self.assertNotIn("sell_price", r)
        self.assertNotIn("profit_unit", r)
        self.assertNotIn("profit_total", r)
        self.assertNotIn("profit_margin_pct", r)

    def test_zero_duty_boundary(self):
        r = lc.build_landed_cost(30, 5, 0.0015, 0, port_charges=2)
        self.assertEqual(r["duty_unit"], 0.0)
        self.assertEqual(r["ddp_unit"], 37.06)  # 35.06 + 0 + 2

    def test_zero_freight_boundary(self):
        # CIF = 30 / 0.99835 = 30.0496 -> 30.05; insurance 0.05
        r = lc.build_landed_cost(30, 0, 0.0015, 10, port_charges=2)
        self.assertEqual(r["cif_unit"], 30.05)
        self.assertEqual(r["insurance_unit"], 0.05)
        self.assertEqual(r["ddp_unit"], 35.05)  # 30.05 + 3.00 + 2

    def test_loss_makes_negative_profit_and_warns(self):
        r = lc.build_landed_cost(30, 5, 0.0015, 10, port_charges=2, sell_price=30)
        self.assertLess(r["profit_unit"], 0)
        self.assertTrue(any("亏" in w for w in r["warnings"]))


class TestCifCrossCheckWithQuoteEngine(unittest.TestCase):
    def test_same_cif_as_quote_engine(self):
        # quote_engine baseline: cost 28, freight 6, margin 15, rate 0.15%
        # -> FOB 33.17, CIF 39.23. Feed that FOB back into landed_cost:
        # the CIF must come out identical — one formula, two scripts.
        q = qe.build_quote(28, 6, 15, 0.0015)
        self.assertEqual(q["fob_list"], 33.17)
        self.assertEqual(q["cif_list"], 39.23)
        r = lc.build_landed_cost(q["fob_list"], 6, 0.0015, 0)
        self.assertEqual(r["cif_unit"], q["cif_list"])
        self.assertEqual(r["insurance_unit"], q["insurance"])

    def test_cli_cross_check(self):
        code, out = run_landed("--fob", "33.17", "--freight", "6",
                               "--duty", "0", "--port-charges", "0")
        self.assertEqual(code, 0)
        self.assertIn("39.23", out)


class TestOutputFormats(unittest.TestCase):
    def test_json_internal_has_cost_and_profit(self):
        code, out = run_landed("--fob", "30", "--freight", "5", "--duty", "10",
                               "--port-charges", "2", "--sell-price", "48",
                               "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        r = payload["landed_cost"]
        self.assertEqual(r["fob_unit"], 30.0)
        self.assertEqual(r["cif_unit"], 35.06)
        self.assertEqual(r["ddp_total"], 40.56)
        self.assertEqual(r["profit_unit"], 7.44)

    def test_json_client_hides_cost_rate_profit(self):
        code, out = run_landed("--fob", "30", "--freight", "5", "--duty", "10",
                               "--port-charges", "2", "--sell-price", "48",
                               "--audience", "client", "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        r = payload["landed_cost"]
        for hidden in ("fob_unit", "freight_unit", "insurance_unit",
                       "insurance_rate", "sell_price", "profit_unit",
                       "profit_total", "profit_margin_pct"):
            self.assertNotIn(hidden, r)
        for shown in ("cif_unit", "cif_total", "duty_unit", "duty_total",
                      "port_charges_unit", "ddp_unit", "ddp_total"):
            self.assertIn(shown, r)
        self.assertNotIn("inputs", payload["meta"])

    def test_table_client_hides_cost_and_profit_words(self):
        code, out = run_landed("--fob", "30", "--freight", "5", "--duty", "10",
                               "--port-charges", "2", "--sell-price", "48",
                               "--audience", "client")
        self.assertEqual(code, 0)
        # 术语表里讲 CIF 公式时仍会出现 FOB 这个词（跟 quote_engine 客户视图一样），
        # 漏的不是词，是数：FOB 单价行与 FOB 数值 30.00 必须一个都不出现。
        self.assertNotIn("FOB 单价", out)
        self.assertNotIn("30.00", out)
        self.assertNotIn("利润", out)
        # 同上：术语表讲 CIF 构成时会提「保险费」这个词，漏的不是词，是保险费金额行。
        self.assertNotIn("其中保险费", out)
        self.assertNotIn("0.06", out)
        self.assertIn("CIF", out)
        self.assertIn("DDP", out)
        self.assertIn("40.56", out)


class TestValidationAndHelp(unittest.TestCase):
    def test_missing_fob_is_human_error_not_traceback(self):
        code, out = run_landed("--freight", "5")
        self.assertNotEqual(code, 0)
        self.assertIn("fob", out.lower())
        self.assertNotIn("Traceback", out)

    def test_bad_inputs_rejected(self):
        for args in (["--fob", "0"], ["--fob", "-5"], ["--fob", "30", "--freight", "-1"],
                     ["--fob", "30", "--duty", "-5"], ["--fob", "30", "--qty", "0"],
                     ["--fob", "30", "--sell-price", "0"],
                     ["--fob", "30", "--insurance", "30"]):
            with self.subTest(args=args):
                code, out = run_landed(*args)
                self.assertNotEqual(code, 0)
                self.assertNotIn("Traceback", out)

    def test_help_has_real_examples(self):
        code, out = run_landed("--help")
        self.assertEqual(code, 0)
        self.assertIn("--fob 30 --freight 5 --duty 10 --port-charges 2", out)
        self.assertIn("--audience client", out)


class TestImportVat(unittest.TestCase):
    def test_group1_vat_13_numbers(self):
        # 【示例】税率虚构：group 1 + import VAT 13%.
        # CIF 35.0578, duty 3.5058 -> VAT (35.0578+3.5058) x 0.13 = 5.0133 -> 5.01
        # DDP 40.5636 + 5.0133 = 45.5769 -> 45.58; sell 48 -> profit 2.42, margin 5.05%.
        r = lc.build_landed_cost(30, 5, 0.0015, 10, port_charges=2, qty=1,
                                 sell_price=48, vat_rate_pct=13.0)
        self.assertEqual(r["vat_rate_pct"], 13.0)
        self.assertEqual(r["vat_unit"], 5.01)
        self.assertEqual(r["vat_total"], 5.01)
        self.assertEqual(r["ddp_unit"], 45.58)
        self.assertEqual(r["ddp_total"], 45.58)
        self.assertEqual(r["profit_unit"], 2.42)
        self.assertEqual(r["profit_margin_pct"], 5.05)

    def test_vat_totals_scale_with_qty(self):
        r = lc.build_landed_cost(30, 5, 0.0015, 10, port_charges=2, qty=100,
                                 vat_rate_pct=13.0)
        self.assertEqual(r["vat_total"], 501.33)
        self.assertEqual(r["ddp_total"], 4557.69)

    def test_no_vat_by_default(self):
        r = lc.build_landed_cost(30, 5, 0.0015, 10, port_charges=2)
        for key in ("vat_rate_pct", "vat_unit", "vat_total"):
            self.assertNotIn(key, r)
        self.assertEqual(r["ddp_unit"], 40.56)

    def test_bad_vat_rate_rejected(self):
        for rate in (-1, 150):
            with self.subTest(rate=rate):
                with self.assertRaises(ValueError):
                    lc.build_landed_cost(30, 5, 0.0015, 10, vat_rate_pct=rate)

    def test_cli_vat_shows_tax_inclusive_ddp(self):
        code, out = run_landed("--fob", "30", "--freight", "5", "--duty", "10",
                               "--port-charges", "2", "--vat-rate", "13")
        self.assertEqual(code, 0)
        self.assertIn("5.01", out)
        self.assertIn("45.58", out)
        self.assertIn("含进口增值税", out)

    def test_cli_json_client_keeps_vat_visible(self):
        # VAT is derived from CIF+duty, which the client already sees — no leak.
        code, out = run_landed("--fob", "30", "--freight", "5", "--duty", "10",
                               "--port-charges", "2", "--vat-rate", "13",
                               "--audience", "client", "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        r = payload["landed_cost"]
        self.assertEqual(r["vat_unit"], 5.01)
        self.assertEqual(r["ddp_unit"], 45.58)
        self.assertNotIn("fob_unit", r)


if __name__ == "__main__":
    unittest.main()
