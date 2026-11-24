#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/fulfillment_checklist.py / 订单交付核对清单测试.

All example data is fictional. / 示例数据全部虚构。
"""

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import fulfillment_checklist as fc  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts",
                      "fulfillment_checklist.py")


def base_order(**overrides):
    """A clean fictional order with every gate passing except the balance
    (not due yet — normal mid-order). / 一张关口全过（除未到期的尾款）的虚构订单。"""
    order = fc.demo_order()
    order.update(overrides)
    return order


class TestDepositMath(unittest.TestCase):
    """Deposit arithmetic / 定金算数."""

    def test_expected_is_total_times_rate(self):
        self.assertEqual(fc.deposit_expected(base_order()), 4032.0)

    def test_expected_follows_custom_rate(self):
        self.assertEqual(
            fc.deposit_expected(base_order(deposit_rate=50)), 6720.0)

    def test_expected_none_without_total(self):
        order = base_order()
        del order["total"]
        self.assertIsNone(fc.deposit_expected(order))

    def test_balance_due_is_total_minus_deposit(self):
        self.assertEqual(fc.balance_due(base_order()), 9408.0)

    def test_full_deposit_passes(self):
        check = fc.deposit_check(base_order())
        self.assertTrue(check["ok"])
        self.assertEqual(check["shortfall"], 0.0)
        self.assertEqual(check["notes"], [])

    def test_short_deposit_fails_with_shortfall(self):
        check = fc.deposit_check(base_order(deposit_received=1000.0))
        self.assertFalse(check["ok"])
        self.assertEqual(check["shortfall"], 3032.0)
        self.assertTrue(any("3032" in n for n in check["notes"]))

    def test_zero_deposit_fails(self):
        self.assertFalse(fc.deposit_check(
            base_order(deposit_received=0.0))["ok"])

    def test_below_floor_rate_fails_even_if_paid_in_full(self):
        # 20% of total paid in full is still below the 30% first-order floor.
        order = base_order(deposit_rate=20, deposit_received=2688.0)
        check = fc.deposit_check(order)
        self.assertFalse(check["ok"])
        self.assertTrue(any("30" in n for n in check["notes"]))

    def test_screenshot_only_fails(self):
        # Money received but never confirmed on your own bank statement.
        order = base_order(deposit_confirmed_by_bank=False)
        check = fc.deposit_check(order)
        self.assertFalse(check["ok"])
        self.assertTrue(any("screenshot" in n for n in check["notes"]))

    def test_overpayment_flagged(self):
        check = fc.deposit_check(base_order(deposit_received=20000.0))
        self.assertFalse(check["ok"])
        self.assertTrue(any("exceeds total" in n for n in check["notes"]))


class TestPaymentMethod(unittest.TestCase):
    """Payment-method risk / 付款方式风险."""

    def test_oa_refused_on_first_order(self):
        check = fc.deposit_check(base_order(payment_method="oa"))
        self.assertFalse(check["ok"])

    def test_western_union_refused_on_first_order(self):
        check = fc.deposit_check(base_order(payment_method="western_union"))
        self.assertFalse(check["ok"])

    def test_oa_allowed_on_repeat_order(self):
        # Repeat order: the method itself is no longer a hard block here
        # (risk is still HIGH — the checklist shows it, it just does not
        # refuse the deposit gate on amount grounds).
        order = base_order(payment_method="oa", first_order=False)
        check = fc.deposit_check(order)
        self.assertTrue(check["ok"])

    def test_unknown_method_rejected(self):
        with self.assertRaises(ValueError):
            fc.validate_order(base_order(payment_method="bitcoin"))


class TestValidateOrder(unittest.TestCase):
    """Input validation / 输入校验."""

    def test_total_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            fc.validate_order(base_order(total=9999.0))

    def test_negative_qty_rejected(self):
        with self.assertRaises(ValueError):
            fc.validate_order(base_order(qty=-5))

    def test_rate_over_100_rejected(self):
        with self.assertRaises(ValueError):
            fc.validate_order(base_order(deposit_rate=150))

    def test_negative_deposit_rejected(self):
        with self.assertRaises(ValueError):
            fc.validate_order(base_order(deposit_received=-1.0))

    def test_non_dict_rejected(self):
        with self.assertRaises(ValueError):
            fc.validate_order(["not", "an", "order"])


class TestPiBlThreeWay(unittest.TestCase):
    """PI / B/L / three-way checks / PI、提单、三单一致性."""

    def test_demo_pi_complete(self):
        self.assertEqual(fc.pi_check(base_order()), [])

    def test_missing_pi_fields_listed(self):
        order = base_order()
        del order["bank_details"]
        del order["validity_days"]
        missing = fc.pi_check(order)
        self.assertIn("bank_details", missing)
        self.assertIn("validity_days", missing)

    def test_demo_bl_complete(self):
        self.assertEqual(fc.bl_check(base_order()), [])

    def test_missing_bl_fields_listed(self):
        order = base_order()
        del order["bl"]["consignee"]
        del order["bl"]["gross_weight"]
        missing = fc.bl_check(order)
        self.assertIn("consignee", missing)
        self.assertIn("gross_weight", missing)

    def test_three_way_match(self):
        self.assertEqual(fc.three_way_check(base_order()), [])

    def test_three_way_mismatch_names_field(self):
        order = base_order()
        order["docs"]["packing_list"]["pieces"] = 470
        mismatches = fc.three_way_check(order)
        self.assertEqual(len(mismatches), 1)
        self.assertEqual(mismatches[0][0], "pieces")
        self.assertEqual(mismatches[0][1]["packing_list"], 470)


class TestChecklistAndGates(unittest.TestCase):
    """Full checklist build and money gates / 整张清单与钱的关口."""

    def test_demo_has_27_items(self):
        checklist = fc.build_checklist(base_order())
        self.assertEqual(checklist["summary"]["total"], 27)

    def test_demo_verdict_on_track(self):
        checklist = fc.build_checklist(base_order())
        self.assertTrue(checklist["verdict"].startswith("ON TRACK"))
        self.assertEqual(checklist["summary"]["blocked"], 0)

    def test_unpaid_deposit_blocks_verdict(self):
        checklist = fc.build_checklist(
            base_order(deposit_received=0.0))
        self.assertTrue(checklist["verdict"].startswith("BLOCKED"))
        self.assertGreater(checklist["summary"]["blocked"], 0)

    def test_production_gate_go_with_deposit(self):
        gates = fc.build_checklist(base_order())["gates"]
        self.assertTrue(gates["production"]["go"])

    def test_production_gate_no_go_without_pi_confirmation(self):
        gates = fc.build_checklist(
            base_order(pi_confirmed=False))["gates"]
        self.assertFalse(gates["production"]["go"])

    def test_release_gate_no_go_until_balance_clears(self):
        gates = fc.build_checklist(base_order())["gates"]
        self.assertFalse(gates["release"]["go"])

    def test_release_gate_go_when_balance_paid(self):
        order = base_order(balance_received=9408.0)
        gates = fc.build_checklist(order)["gates"]
        self.assertTrue(gates["release"]["go"])

    def test_ship_gate_needs_inspection_signoff(self):
        gates = fc.build_checklist(base_order())["gates"]
        self.assertFalse(gates["ship"]["go"])
        gates = fc.build_checklist(
            base_order(), done={"inspection": "2026-11-24T10:00:00"})["gates"]
        self.assertTrue(gates["ship"]["go"])

    def test_done_stage_marks_its_items(self):
        checklist = fc.build_checklist(
            base_order(), done={"production": "2026-11-24T10:00:00"})
        prod = [i for i in checklist["items"]
                if i["stage"] == "production"]
        self.assertTrue(all(i["status"] == "done" for i in prod))

    def test_gate_for_done_refuses_production_without_deposit(self):
        allowed, reason = fc.gate_for_done(
            "production", base_order(deposit_received=0.0), {})
        self.assertFalse(allowed)
        self.assertIn("production gate", reason)

    def test_gate_for_done_allows_production_with_deposit(self):
        allowed, _ = fc.gate_for_done("production", base_order(), {})
        self.assertTrue(allowed)

    def test_gate_for_done_refuses_balance_without_payment(self):
        allowed, _ = fc.gate_for_done("balance", base_order(), {})
        self.assertFalse(allowed)

    def test_gate_for_done_refuses_docs_on_mismatch(self):
        order = base_order()
        order["docs"]["invoice"]["gross_weight"] = 1
        allowed, reason = fc.gate_for_done("docs", order, {})
        self.assertFalse(allowed)
        self.assertIn("gross_weight", reason)


class TestCli(unittest.TestCase):
    """CLI smoke tests / 命令行冒烟."""

    def run_cli(self, *argv):
        return subprocess.run(
            [sys.executable, SCRIPT, *argv],
            capture_output=True, text=True, timeout=30)

    def test_demo_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("--demo", "--state",
                                  os.path.join(tmp, "state.json"))
            self.assertEqual(result.returncode, 0)
            self.assertIn("Order fulfillment checklist", result.stdout)
            self.assertIn("4032.00", result.stdout)

    def test_json_format_parses(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("--demo", "--format", "json", "--state",
                                  os.path.join(tmp, "state.json"))
            self.assertEqual(result.returncode, 0)
            data = json.loads(result.stdout)
            self.assertEqual(data["summary"]["total"], 27)
            self.assertIn("production", data["gates"])

    def test_status_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("--demo", "--status", "--state",
                                  os.path.join(tmp, "state.json"))
            self.assertEqual(result.returncode, 0)
            self.assertIn("Progress", result.stdout)

    def test_done_production_writes_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = os.path.join(tmp, "state.json")
            result = self.run_cli("--demo", "--done", "production",
                                  "--state", state)
            self.assertEqual(result.returncode, 0)
            saved = json.load(open(state, encoding="utf-8"))
            self.assertIn("production", saved["done"])
            again = self.run_cli("--demo", "--status", "--state", state)
            # demo already has 7 done; signing off production adds its 3 items.
            self.assertIn("10/27 done", again.stdout)

    def test_done_production_refused_without_deposit(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("--demo", "--deposit-received", "0",
                                  "--done", "production", "--state",
                                  os.path.join(tmp, "state.json"))
            self.assertEqual(result.returncode, 2)
            self.assertIn("refused", result.stderr)

    def test_missing_order_file_exits_two(self):
        result = self.run_cli("--order", "/nonexistent/order.json")
        self.assertEqual(result.returncode, 2)

    def test_demo_and_order_conflict(self):
        result = self.run_cli("--demo", "--order", "order.json")
        self.assertEqual(result.returncode, 2)

    def test_no_input_flag_exits_two(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)

    def test_order_file_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "order.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(base_order(), f, ensure_ascii=False)
            result = self.run_cli("--order", path, "--state",
                                  os.path.join(tmp, "state.json"))
            self.assertEqual(result.returncode, 0)
            self.assertIn("【示例】", result.stdout)

    def test_out_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "checklist.txt")
            result = self.run_cli("--demo", "--out", out, "--state",
                                  os.path.join(tmp, "state.json"))
            self.assertEqual(result.returncode, 0)
            self.assertIn("Order fulfillment checklist",
                          open(out, encoding="utf-8").read())


if __name__ == "__main__":
    unittest.main()
