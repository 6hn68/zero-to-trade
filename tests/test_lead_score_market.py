#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the market layer in lead_score.py (market_rules.py tables).

Market rules cap the tier, never the score: a perfect-contact lead from an
excluded market keeps its points but can only ever be T3; a barrier-market
lead stops at T1 until re-export / bonded zone is confirmed in the note.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import lead_score as ls  # noqa: E402
import market_rules as mr  # noqa: E402


def row(**overrides):
    """A complete, high-signal lead (95 points before any market cap)."""
    base = {"company": "Acme Fictional Trading", "country": "Saudi Arabia",
            "product": "TBR 12.00R20", "source": "referral",
            "email": "demo01@sample.example", "phone": "+000 00 000 0000",
            "years": "12", "contact": "purchasing manager",
            "note": "Annual RFQ for truck tyres, looking for supplier, 40HQ container regular"}
    base.update(overrides)
    return base


def analyze_one(r):
    results, duplicates = ls.analyze([r])
    assert len(results) == 1 and duplicates == 0
    return results[0]


class TestBarrierMarkets(unittest.TestCase):
    def test_turkey_full_signal_capped_at_t1(self):
        # 95 points, but Turkey has a 60% anti-dumping duty on Chinese TBR
        # until 2029: not a "call today" T0 until re-export is confirmed.
        item = analyze_one(row(country="Turkey"))
        self.assertEqual(item["score"], 95)
        self.assertEqual(item["tier"], "T1")
        self.assertEqual(item["next"], "先确认转口/保税区")
        self.assertIn("60%", item["detail"]["市场"])
        self.assertIn("转口", item["action"])

    def test_turkey_aliases_hit_the_same_rule(self):
        for name in ("Türkiye", "Turkiye", "土耳其", "TR", " turkey "):
            item = analyze_one(row(country=name))
            self.assertEqual(item["tier"], "T1", name)
            self.assertIn("60%", item["detail"]["市场"], name)

    def test_turkey_reexport_note_lifts_the_cap(self):
        # The note says the buyer does re-export via a bonded zone:
        # cap lifted, the 95 points stand as T0.
        item = analyze_one(row(
            country="Turkey",
            note="Annual RFQ for truck tyres, 40HQ container regular, "
                 "做转口贸易，走保税区"))
        self.assertEqual(item["score"], 95)
        self.assertEqual(item["tier"], "T0")
        self.assertIn("已确认转口/保税区", item["detail"]["市场"])

    def test_brazil_full_signal_capped_at_t1_rate_unverified(self):
        # Brazil has an anti-dumping duty on Chinese truck/bus tyres, but
        # the rate was never written down in this repo: the label must say
        # so (没核实) instead of inventing a number.
        item = analyze_one(row(country="Brazil"))
        self.assertEqual(item["score"], 95)
        self.assertEqual(item["tier"], "T1")
        self.assertIn("没核实", item["detail"]["市场"])
        self.assertNotIn("%", item["detail"]["市场"])


class TestExcludedMarkets(unittest.TestCase):
    def test_mexico_full_signal_capped_at_t3(self):
        item = analyze_one(row(country="Mexico"))
        self.assertEqual(item["score"], 95)  # score kept, tier capped
        self.assertEqual(item["tier"], "T3")
        self.assertEqual(item["next"], "别打（市场排除）")
        self.assertIn("市场排除", item["action"])

    def test_usa_full_signal_capped_at_t3(self):
        for name in ("United States", "USA", "U.S.A.", "美国", "US"):
            item = analyze_one(row(country=name))
            self.assertEqual(item["tier"], "T3", name)
            self.assertEqual(item["next"], "别打（市场排除）", name)

    def test_eu_members_capped_at_t3(self):
        for name in ("Germany", "France", "法国", "Netherlands", "EU",
                     "European Union", "欧盟", "Spain", "西班牙"):
            item = analyze_one(row(country=name))
            self.assertEqual(item["tier"], "T3", name)
            self.assertIn("市场排除", item["detail"]["市场"], name)

    def test_uk_is_not_eu(self):
        # The UK left the EU: no rule for it, so no cap — it stays "other".
        item = analyze_one(row(country="United Kingdom"))
        self.assertEqual(item["tier"], "T0")


class TestNoCapCases(unittest.TestCase):
    def test_target_market_unchanged(self):
        for name in ("Saudi Arabia", "Nigeria", "UAE", "Kenya"):
            item = analyze_one(row(country=name))
            self.assertEqual(item["score"], 95, name)
            self.assertEqual(item["tier"], "T0", name)
            self.assertIn("目标市场", item["detail"]["市场"], name)

    def test_unlisted_country_not_punished(self):
        # No rule for Qatar: no cap, just a "not verified" market note.
        item = analyze_one(row(country="Qatar"))
        self.assertEqual(item["tier"], "T0")
        self.assertIn("没核实", item["detail"]["市场"])

    def test_blank_country_unchanged(self):
        total, detail = ls.score_lead({"company": "Acme"})
        self.assertEqual(total, 10)
        self.assertEqual(ls.grade(total), "T3")
        self.assertIn("没核实", detail["市场"])


class TestMarketRulesTable(unittest.TestCase):
    def test_verdict_statuses(self):
        self.assertEqual(mr.verdict("Saudi Arabia")["status"], "target")
        self.assertEqual(mr.verdict("Turkey")["status"], "barrier")
        self.assertEqual(mr.verdict("Mexico")["status"], "excluded")
        self.assertEqual(mr.verdict("Germany")["status"], "excluded")
        self.assertEqual(mr.verdict("Qatar")["status"], "other")
        self.assertEqual(mr.verdict("")["status"], "other")
        self.assertEqual(
            mr.verdict("Turkey", "走保税区转口")["status"], "barrier-cleared")

    def test_target_markets_match_tire_pack(self):
        # The 8 target markets must stay in sync with tire_pack.py MARKETS.
        import tire_pack as tp  # noqa: E402
        self.assertEqual(set(mr.TARGET_MARKETS), set(tp.MARKETS))

    def test_barrier_rates_are_not_invented(self):
        # Brazil's rate is None on purpose: the repo never recorded one.
        self.assertIsNone(mr.BARRIERS["brazil"]["rate_pct"])
        self.assertFalse(mr.BARRIERS["brazil"]["rate_verified"])
        # Turkey's 60% verified 2026-11-24 against the official gazette
        # (Resmî Gazete 2024/1, Art. 4 table, 60% of CIF; Art. 5(4):
        # lapses 2029-02-06) — flag flipped at merge time with this test.
        self.assertEqual(mr.BARRIERS["turkey"]["rate_pct"], 60)
        self.assertTrue(mr.BARRIERS["turkey"]["rate_verified"])

    def test_eu_has_27_members(self):
        self.assertEqual(len(mr.EU_MEMBERS), 27)
        self.assertNotIn("united kingdom", mr.EU_MEMBERS)
        self.assertNotIn("uk", mr.EU_MEMBERS)


if __name__ == "__main__":
    unittest.main()
