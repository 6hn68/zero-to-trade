#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Web score sync: index.html must score exactly like the Python scripts.

网页打分同步：index.html 里的 JS 打分必须和 Python 脚本逐条一致。
The page already ports market_rules.py + lead_score.py into its ZTT rule
block (round 1 merged it); this test locks the sync in two ways:
1. Static: the JS tables (targets, barriers, exclusions, EU members,
   re-export keywords, tier thresholds, country aliases) match the
   Python tables exactly — catches "edited market_rules.py, forgot
   index.html" drift without needing a browser or Node.
2. Live (needs `node` on PATH, skipped otherwise): the same fictional
   CSV matrix is scored by Python lead_score.analyze() and by the JS
   ZTT block extracted from index.html, and every lead must agree on
   tier, score, next step, action and market label, in the same order.

Run: python3 -m unittest discover -s tests   (from the repo root)
"""

import csv
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import lead_score as ls  # noqa: E402
import market_rules as mr  # noqa: E402

# ---------------------------------------------------------------- ZTT block
_ZTT_RE = re.compile(
    r"<script>\n/\* zero-to-trade core rules[\s\S]*?\n</script>")


def ztt_js():
    """The JS rule block straight out of index.html (no copy, no cache
    file: if the page and the scripts disagree, this test must see it)."""
    html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
    match = _ZTT_RE.search(html)
    assert match, "ZTT rule block not found in index.html"
    code = match.group(0)
    assert "market_rules.py" in code, "ZTT block no longer cites market_rules.py"
    return code


def _block(js, name):
    match = re.search(r"var %s = \{(.*?)\n  \};" % re.escape(name), js, re.S)
    assert match, "JS table %s not found" % name
    return match.group(1)


# ---------------------------------------------------------------- Static sync
class TestWebTablesMatchPython(unittest.TestCase):
    """JS tables == Python tables. No Node needed."""

    def test_target_markets_match(self):
        js = ztt_js()
        keys = re.findall(r"(\w+): \[", _block(js, "TARGET_MARKETS"))
        self.assertEqual(sorted(keys), sorted(mr.TARGET_MARKETS))

    def test_barrier_rates_match(self):
        js = ztt_js()
        for code, rule in mr.BARRIERS.items():
            match = re.search(
                r"%s: \{[^}]*rate_pct: (null|\d+), until: (null|\"[^\"]+\")"
                % re.escape(code), _block(js, "BARRIERS"))
            self.assertIsNotNone(match, "JS barrier %s missing" % code)
            rate = None if match.group(1) == "null" else int(match.group(1))
            until = None if match.group(2) == "null" else match.group(2)[1:-1]
            self.assertEqual(rate, rule["rate_pct"], code)
            self.assertEqual(until, rule["until"], code)

    def test_barrier_specific_duty_match(self):
        # Brazil is a specific (per-kg) duty, not a %: the JS table must
        # carry the same per-kg range as Python, or the live diff drifts
        # the next time market_rules.py changes.
        js = ztt_js()
        for code, rule in mr.BARRIERS.items():
            match = re.search(
                r"%s: \{[^}]*rate_specific_usd_per_kg: \"([^\"]+)\""
                % re.escape(code), _block(js, "BARRIERS"))
            want = rule.get("rate_specific_usd_per_kg")
            if want is None:
                self.assertIsNone(
                    match, "JS barrier %s has a stray per-kg rate" % code)
            else:
                self.assertIsNotNone(
                    match, "JS barrier %s missing per-kg rate" % code)
                self.assertEqual(match.group(1), want, code)

    def test_excluded_markets_match(self):
        js = ztt_js()
        keys = re.findall(r"(\w+): \{ name:", _block(js, "EXCLUDED_MARKETS"))
        self.assertEqual(sorted(keys), sorted(mr.EXCLUDED_MARKETS))

    def test_eu_members_match(self):
        js = ztt_js()
        pairs = re.findall(r"(\w+): \"([^\"]+)\"", _block(js, "EU_MEMBERS"))
        self.assertEqual(dict(pairs), mr.EU_MEMBERS)
        self.assertEqual(len(pairs), 27, "EU has 27 members")

    def test_reexport_keywords_match(self):
        js = ztt_js()
        match = re.search(r"var REEXPORT_KEYWORDS = \[(.*?)\];", js, re.S)
        self.assertIsNotNone(match)
        words = re.findall(r"\"([^\"]+)\"", match.group(1))
        self.assertEqual(sorted(words), sorted(mr.REEXPORT_KEYWORDS))

    def test_tier_thresholds_match(self):
        js = ztt_js()
        for tier, rule in ls.TIER_RULES.items():
            match = re.search(r"%s: \[(\d+)," % re.escape(tier),
                              _block(js, "TIER_RULES"))
            self.assertIsNotNone(match, "JS tier %s missing" % tier)
            self.assertEqual(int(match.group(1)), rule[0], tier)

    def test_country_aliases_match(self):
        # The JS builds its alias map the same way Python does: a literal
        # plus the EU-member loop plus a few short forms. Replay those
        # steps on the JS literals and compare the finished maps.
        js = ztt_js()
        literal = dict(re.findall(
            r"\"([^\"]+)\": \"([^\"]+)\"", _block(js, "MARKET_ALIASES")))
        eu = dict(re.findall(
            r"(\w+): \"([^\"]+)\"", _block(js, "EU_MEMBERS")))
        for en, zh in eu.items():
            literal.setdefault(en, "eu")
            literal.setdefault(zh, "eu")
        literal.update({"czech": "eu", "czech republic": "eu",
                        "holland": "eu", "uk": "other", "英国": "other"})
        self.assertEqual(literal, mr.MARKET_ALIASES)


# ---------------------------------------------------------------- Live diff
NODE_DRIVER = r"""
"use strict";
var fs = require("fs");
var input = JSON.parse(fs.readFileSync(0, "utf-8"));
var html = fs.readFileSync(input.html, "utf-8");
var m = html.match(/<script>\n\/\* zero-to-trade core rules[\s\S]*?\n<\/script>/);
if (!m) { console.error("ZTT script block not found in index.html"); process.exit(2); }
var code = m[0].replace(/^<script>\n/, "").replace(/\n<\/script>$/, "");
var mod = { exports: {} };
new Function("module", "exports", code)(mod, mod.exports);
var Z = mod.exports;
var parsed = Z.readLeads(input.csv, ",");
var res = Z.analyze(parsed.rows);
console.log(JSON.stringify({ leads: res.leads.map(function (l) {
  return { company: l.company, country: l.country, tier: l.tier,
    score: l.score, next: l.next, action: l.action,
    market: l.detail["\u5e02\u573a"], capped: !!l._capped,
    dup_count: l.dup_count, status: l._verdict.status,
    cap_action_en: l._action_en };
}), duplicates: res.duplicates }));
"""

# (email, phone, source, signal-note, years) -> total before any cap.
RECIPES = {
    95: ("buyer@sample.example", "+000 00 000 0000", "referral",
         "RFQ for truck tyres, 40HQ container, purchasing manager", "18"),
    80: ("buyer@sample.example", "+000 00 000 0000", "referral", "", "18"),
    60: ("buyer@sample.example", "", "customs", "", "18"),
    40: ("buyer@sample.example", "", "search", "", ""),
    0: ("", "", "", "", ""),
}

COUNTRIES = [
    "Nigeria", "Ghana", "Kenya", "Tanzania", "Colombia", "Brazil",
    "Saudi Arabia", "UAE",
    "Turkey", "Türkiye", "Turkiye", "土耳其", " Turkey ", "TURKEY", "TR",
    "Mexico", "墨西哥", "USA", "U.S.A.", "US", "America",
    "United States of America", "Germany", "France", "德国",
    "Czech Republic", "Czech", "Holland", "EU", "European Union", "欧盟",
    "UK", "英国", "Japan", "Egypt", "", "  ",
]

NOTES = ["", "re-export confirmed", "保税区"]


def build_matrix_csv():
    """Fictional leads only: every company name carries 【示例】, every
    mailbox is sample.example. Rows span score levels x countries x notes
    so each market rule is hit above and below its cap line."""
    rows = [["company", "country", "email", "phone", "source", "product",
             "contact", "years", "note"]]
    n = 0
    for _total, (email, phone, source, sig, years) in RECIPES.items():
        for country in COUNTRIES:
            for note in NOTES:
                n += 1
                note_full = " ".join(x for x in (sig, note) if x)
                rows.append([
                    "【示例】WebSync %04d" % n, country, email, phone,
                    source, "TBR tyres", "【示例】Buyer", years, note_full,
                ])
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerows(rows)
    return buf.getvalue()


def run_js(csv_text):
    """Score csv_text with the JS block from index.html via node."""
    with tempfile.TemporaryDirectory() as tmp:
        driver = Path(tmp) / "ztt_driver.js"
        driver.write_text(NODE_DRIVER, encoding="utf-8")
        payload = json.dumps({"html": str(REPO_ROOT / "index.html"),
                              "csv": csv_text})
        proc = subprocess.run(["node", str(driver)], input=payload,
                              capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise AssertionError("node driver failed: %s" % proc.stderr)
    return json.loads(proc.stdout)


def run_python(csv_text):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "matrix.csv"
        path.write_text(csv_text, encoding="utf-8")
        rows = ls.read_leads(str(path))
        results, dups = ls.analyze(rows)
    return {"leads": [{
        "company": r["company"], "country": r["country"],
        "tier": r["tier"], "score": r["score"], "next": r["next"],
        "action": r["action"], "market": r["detail"]["市场"],
        "dup_count": r["dup_count"],
    } for r in results], "duplicates": dups}


@unittest.skipUnless(shutil.which("node"), "node not on PATH: live JS diff skipped")
class TestWebScoreMatchesPython(unittest.TestCase):
    """Same CSV in, same tiers out — JS and Python must agree lead by lead."""

    def assert_same_results(self, csv_text):
        py = run_python(csv_text)
        js = run_js(csv_text)
        self.assertEqual(len(js["leads"]), len(py["leads"]),
                         "lead count differs")
        self.assertEqual(js["duplicates"], py["duplicates"],
                         "duplicate count differs")
        self.assertEqual([r["company"] for r in js["leads"]],
                         [r["company"] for r in py["leads"]],
                         "sort order differs")
        by_company = {r["company"]: r for r in py["leads"]}
        for got in js["leads"]:
            want = by_company[got["company"]]
            for key in ("country", "tier", "score", "next", "action",
                        "market", "dup_count"):
                self.assertEqual(got[key], want[key],
                                 "%s [%s]" % (got["company"], key))
            # A capped lead must never reach T0, and must carry the
            # English cap wording the page shows in English mode.
            self.assertNotEqual((got["status"], got["tier"]),
                                ("barrier", "T0"))
            self.assertNotEqual((got["status"], got["tier"]),
                                ("excluded", "T0"))
            if got["capped"]:
                self.assertTrue(got["cap_action_en"],
                                "%s capped without English action"
                                % got["company"])

    def test_matrix_matches_python(self):
        self.assert_same_results(build_matrix_csv())

    def test_example_file_matches_python(self):
        csv_text = (REPO_ROOT / "examples" / "leads_example.csv").read_text(
            encoding="utf-8")
        self.assert_same_results(csv_text)
        from collections import Counter
        py = run_python(csv_text)
        self.assertEqual(Counter(r["tier"] for r in py["leads"]),
                         {"T0": 2, "T1": 5, "T2": 1, "T3": 2})


if __name__ == "__main__":
    unittest.main()
