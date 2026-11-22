#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scripts/tire_pack.py — tire industry pack.

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

import tire_pack as tp  # noqa: E402


def run_pack(*args):
    """Run the tire-pack CLI; return (exit_code, stdout+stderr)."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "tire_pack.py"), *args],
        capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout + proc.stderr


FOUR_SIZES = ["11.00R20", "12.00R20", "295/80R22.5", "315/80R22.5"]
COMMON_DOCS = ["原产地证", "商业发票", "装箱单", "提单"]


class TestFourSizes(unittest.TestCase):
    def test_each_size_builds_with_its_common_li_and_speed(self):
        expected = {
            "11.00R20": ("150/147", "K"),
            "12.00R20": ("154/151", "K"),
            "295/80R22.5": ("152/148", "M"),
            "315/80R22.5": ("156/150", "L"),
        }
        for size in FOUR_SIZES:
            with self.subTest(size=size):
                pack = tp.build_tire_pack(size, "nigeria")
                self.assertEqual(pack["size"], size)
                self.assertEqual(pack["load_index"], expected[size][0])
                self.assertIn(expected[size][1], pack["speed_rating"])
                self.assertEqual(pack["kind"], "全钢子午线 TBR")

    def test_li_and_speed_overrides_are_honoured(self):
        pack = tp.build_tire_pack("315/80R22.5", "uae", li="156/150", speed="L")
        self.assertEqual(pack["load_index"], "156/150")
        self.assertIn("L", pack["speed_rating"])
        pack = tp.build_tire_pack("11.00R20", "nigeria", li="152/148", speed="M")
        self.assertEqual(pack["load_index"], "152/148")
        self.assertIn("M", pack["speed_rating"])

    def test_size_normalisation_tolerates_spaces_and_case(self):
        pack = tp.build_tire_pack(" 295/80r22.5 ", "nigeria")
        self.assertEqual(pack["size"], "295/80R22.5")


class TestMarkets(unittest.TestCase):
    def test_gcc_applies_only_to_gulf_markets(self):
        for market in ("saudi", "uae"):
            with self.subTest(market=market):
                pack = tp.build_tire_pack("11.00R20", market)
                self.assertTrue(pack["gcc_applies"])
                self.assertTrue(any("GSO" in p for p in pack["gcc_points"]))
                self.assertTrue(any("检测报告" in p for p in pack["gcc_points"]))
                self.assertTrue(any("GCC 符合性证书" in d for d in pack["docs"]))
        for market in ("nigeria", "ghana", "kenya", "tanzania",
                       "colombia", "brazil"):
            with self.subTest(market=market):
                pack = tp.build_tire_pack("11.00R20", market)
                self.assertFalse(pack["gcc_applies"])
                self.assertTrue(any("不适用" in p for p in pack["gcc_points"]))
                self.assertFalse(any("GCC 符合性证书" in d for d in pack["docs"]))

    def test_all_eight_markets_build(self):
        for market in ("nigeria", "ghana", "kenya", "tanzania",
                       "colombia", "brazil", "saudi", "uae"):
            with self.subTest(market=market):
                pack = tp.build_tire_pack("295/80R22.5", market)
                self.assertTrue(pack["port"])
                self.assertTrue(pack["notes"])
                self.assertEqual(len(pack["docs"]), 5)

    def test_market_aliases_chinese_and_english(self):
        self.assertEqual(tp.build_tire_pack("11.00R20", "尼日利亚")["market"], "尼日利亚")
        self.assertEqual(tp.build_tire_pack("11.00R20", "沙特")["market"], "沙特")
        self.assertEqual(tp.build_tire_pack("11.00R20", "UAE")["market"], "阿联酋")
        self.assertEqual(tp.build_tire_pack("11.00R20", "br")["market"], "巴西")

    def test_nigeria_soncap_and_saudi_saso_are_named(self):
        ng = tp.build_tire_pack("11.00R20", "nigeria")
        self.assertTrue(any("SONCAP" in d for d in ng["docs"]))
        self.assertTrue(any("SONCAP" in n for n in ng["notes"]))
        sa = tp.build_tire_pack("11.00R20", "saudi")
        self.assertTrue(any("SASO" in n or "SABER" in n for n in sa["notes"]))
        self.assertEqual(sa["program"], "SASO / SABER")

    def test_every_pack_carries_the_disclaimer(self):
        for market in ("nigeria", "ghana", "kenya", "tanzania",
                       "colombia", "brazil", "saudi", "uae"):
            with self.subTest(market=market):
                pack = tp.build_tire_pack("12.00R20", market)
                self.assertIn("须以官方最新要求为准、发货前复核", pack["disclaimer"])

    def test_common_docs_present_everywhere(self):
        for market in ("nigeria", "saudi", "brazil"):
            with self.subTest(market=market):
                pack = tp.build_tire_pack("11.00R20", market)
                joined = "\n".join(pack["docs"])
                for doc in COMMON_DOCS:
                    self.assertIn(doc, joined)


class TestErrors(unittest.TestCase):
    def test_unknown_size_raises_with_words(self):
        with self.assertRaises(ValueError) as cm:
            tp.build_tire_pack("13.00R24", "nigeria")
        self.assertIn("11.00R20", str(cm.exception))

    def test_unknown_market_raises_with_words(self):
        with self.assertRaises(ValueError) as cm:
            tp.build_tire_pack("11.00R20", "mexico")
        self.assertIn("尼日利亚", str(cm.exception))

    def test_bad_li_and_speed_raise(self):
        with self.assertRaises(ValueError):
            tp.build_tire_pack("11.00R20", "nigeria", li="abc")
        with self.assertRaises(ValueError):
            tp.build_tire_pack("11.00R20", "nigeria", li="99")
        with self.assertRaises(ValueError):
            tp.build_tire_pack("11.00R20", "nigeria", speed="KK")

    def test_cli_rejects_bad_inputs_with_words_not_traceback(self):
        for args in (("--size", "13.00R24", "--market", "nigeria"),
                     ("--size", "11.00R20", "--market", "mexico"),
                     ("--size", "11.00R20", "--market", "nigeria", "--li", "abc")):
            code, out = run_pack(*args)
            self.assertNotEqual(code, 0)
            self.assertIn("✗", out)
            self.assertNotIn("Traceback", out)

    def test_cli_missing_required_args_is_argparse_error(self):
        code, out = run_pack("--size", "11.00R20")
        self.assertNotEqual(code, 0)
        self.assertIn("--market", out)
        self.assertNotIn("Traceback", out)


class TestOutputFormats(unittest.TestCase):
    def test_json_output_parses_and_matches_table(self):
        code, out = run_pack("--size", "295/80R22.5", "--market", "saudi",
                             "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        pack = payload["pack"]
        self.assertEqual(pack["size"], "295/80R22.5")
        self.assertEqual(pack["market"], "沙特")
        self.assertTrue(pack["gcc_applies"])
        self.assertEqual(pack["load_index"], "152/148")
        self.assertEqual(len(pack["docs"]), 5)
        self.assertIn("须以官方最新要求为准、发货前复核", pack["disclaimer"])

    def test_table_output_has_all_three_sections(self):
        code, out = run_pack("--size", "11.00R20", "--market", "nigeria")
        self.assertEqual(code, 0)
        for section in ("GCC 认证要点", "目的港清关单证清单", "该市场注意事项",
                        "SONCAP", "须以官方最新要求为准、发货前复核"):
            self.assertIn(section, out)


class TestCheckSpec(unittest.TestCase):
    def test_all_given_is_ready_but_still_unverified(self):
        # 全给了也能出包，但自己填的值仍没按厂家数据表核实——要明说。
        check = tp.check_spec("11.00R20", "nigeria", li="150/147", speed="K")
        self.assertTrue(check["ready"])
        self.assertEqual(check["missing"], [])
        self.assertEqual(check["errors"], [])
        self.assertEqual(check["assumed"], [])
        self.assertEqual(len(check["unverified"]), 2)
        self.assertTrue(any("150/147" in g for g in check["unverified"]))

    def test_nothing_given_names_both_missing(self):
        check = tp.check_spec()
        self.assertFalse(check["ready"])
        self.assertEqual(len(check["missing"]), 2)
        self.assertTrue(any("11.00R20" in m for m in check["missing"]))
        self.assertTrue(any("Nigeria" in m for m in check["missing"]))

    def test_size_only_assumes_common_li_and_speed(self):
        check = tp.check_spec("11.00R20", "nigeria")
        self.assertTrue(check["ready"])
        self.assertEqual(len(check["assumed"]), 2)
        self.assertTrue(any("150/147" in g for g in check["assumed"]))
        self.assertTrue(any(" K" in g or " K（" in g or "value K" in g
                            for g in check["assumed"]))

    def test_bad_size_and_bad_li_are_errors_not_missing(self):
        check = tp.check_spec("13.00R24", "nigeria", li="abc")
        self.assertFalse(check["ready"])
        self.assertEqual(check["missing"], [])
        self.assertEqual(len(check["errors"]), 2)

    def test_unknown_size_means_common_value_unknown(self):
        check = tp.check_spec("13.00R24", "nigeria")
        self.assertTrue(any("unknown" in g for g in check["assumed"]))


class TestPackGaps(unittest.TestCase):
    def test_defaults_produce_two_gaps_naming_common_values(self):
        pack = tp.build_tire_pack("11.00R20", "nigeria")
        self.assertEqual(len(pack["gaps"]), 2)
        self.assertTrue(any("150/147" in g for g in pack["gaps"]))

    def test_user_supplied_values_are_gaps_too_until_verified(self):
        pack = tp.build_tire_pack("315/80R22.5", "uae", li="156/150", speed="L")
        self.assertEqual(len(pack["gaps"]), 2)
        self.assertTrue(any("156/150" in g for g in pack["gaps"]))
        self.assertTrue(any(" L " in g for g in pack["gaps"]))

    def test_table_shows_the_to_verify_section(self):
        pack = tp.build_tire_pack("11.00R20", "nigeria")
        text = tp.render_table(pack)
        self.assertIn("报价前先核实", text)
        self.assertIn("150/147", text)


class TestCheckCLI(unittest.TestCase):
    def test_check_with_defaults_exits_zero_and_names_gaps(self):
        code, out = run_pack("--check", "--size", "11.00R20",
                             "--market", "nigeria")
        self.assertEqual(code, 0)
        self.assertIn("150/147", out)
        self.assertIn("常见值", out)

    def test_check_missing_size_exits_two(self):
        code, out = run_pack("--check", "--market", "nigeria")
        self.assertEqual(code, 2)
        self.assertIn("轮胎规格", out)
        self.assertNotIn("Traceback", out)

    def test_check_json_parses(self):
        code, out = run_pack("--check", "--size", "295/80R22.5",
                             "--market", "saudi", "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertTrue(payload["check"]["ready"])
        self.assertEqual(len(payload["check"]["assumed"]), 2)


if __name__ == "__main__":
    unittest.main()
