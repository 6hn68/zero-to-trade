#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for index.html staying in sync with the repo.

- The two embedded example fallbacks (file:// open, fetch fails) must stay
  byte-identical to the CSV data rows they mirror.
- The "more scripts" card must name all 15 scripts.
- The 2-minute demo card (#demo) must keep its 7 clickable steps, with
  every step's data-target resolving to a real id and every shown string
  translated into all 12 languages.

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
    "market_rules.py", "daily_video_list.py", "fulfillment_checklist.py",
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

    def test_all_fifteen_scripts_named(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(len(SCRIPTS), 15,
                         "SCRIPTS drifted from the 15 scripts in scripts/")
        for name in SCRIPTS:
            self.assertIn(name, html, "index.html does not mention %s" % name)

    def test_fast_path_v19_feature_named(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("fast_path.py", html)
        self.assertIn("七天快路径", html)


LANGS_12 = ["es", "pt", "fr", "ar", "ru", "de", "ja", "ko", "tr", "id"]


def _load_i18n_dict(html):
    """Parse the ZI18N dict `D` out of index.html (brace matching)."""
    import json
    start = html.index("var D = {")
    i = html.index("{", start)
    depth = 0
    in_str = False
    esc = False
    j = i
    while j < len(html):
        c = html[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
        j += 1
    return json.loads(html[i:j + 1])


def _demo_section(html):
    start = html.index('<section id="demo">')
    end = html.index("</section>", start)
    return html[start:end]


class TestDemoCard(unittest.TestCase):
    def test_demo_card_present(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('<section id="demo">', html)
        self.assertIn('id="demosteps"', html)
        self.assertIn('id="demoprog"', html)
        sec = _demo_section(html)
        self.assertEqual(len(re.findall(r"<li[ >]", sec)), 7,
                         "demo card must have exactly 7 steps")
        self.assertEqual(sec.count('class="demo-t"'), 7)
        self.assertEqual(sec.count('class="demo-c"'), 10)
        # Nothing is pre-marked done: this page does not auto-load or
        # auto-score on open (the sample only loads on button click).
        self.assertNotIn('class="done"', sec)
        self.assertIn("已完成 0 / 7 步", sec)

    def test_demo_targets_resolve(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        sec = _demo_section(html)
        targets = re.findall(r'data-target="([^"]+)"', sec)
        self.assertTrue(targets, "demo steps carry no jump targets")
        for target in targets:
            self.assertTrue(target.startswith("#"), target)
            self.assertIn('id="%s"' % target[1:], html,
                          "demo step target %s has no such id" % target)

    def test_demo_steps_name_real_commands(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        sec = _demo_section(html)
        for name in ("lead_score.py", "due_diligence.py", "outreach_gen.py",
                     "followup_plan.py", "quote_engine.py", "nudge.py"):
            self.assertIn(name, sec, "demo card lost the %s step" % name)
        self.assertIn("docs/04-outreach.md", sec)

    def test_demo_twelve_languages(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        d = _load_i18n_dict(html)
        sec = _demo_section(html)
        en_texts = re.findall(r'<span class="en">(.*?)</span>', sec, re.S)
        self.assertEqual(
            len(re.findall(r'<span class="zh">', sec)),
            len(en_texts),
            "every demo zh span needs an en sibling")
        en_texts.append("Demo")  # nav link lives outside the section
        for text in en_texts:
            key = text.strip()
            entry = d["s"].get(key)
            self.assertIsNotNone(entry,
                                 "no i18n entry for demo string %r" % key)
            missing = [lang for lang in LANGS_12 if not entry.get(lang)]
            self.assertEqual(missing, [],
                             "demo string %r lacks %s" % (key, missing))
        pat = [pp for pp in d["p"] if pp[0] == "{0} of 7 steps done"]
        self.assertEqual(len(pat), 1, "progress pattern missing")
        missing = [lang for lang in LANGS_12 if not pat[0][1].get(lang)]
        self.assertEqual(missing, [], "progress pattern lacks %s" % missing)

    def test_demo_no_external_urls(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        sec = _demo_section(html)
        self.assertNotIn("http://", sec)
        self.assertNotIn("https://", sec)
        self.assertNotIn("<script", sec)

    def test_demo_handler_present(self):
        html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('getElementById("demosteps")', html)
        self.assertIn('getElementById("demoprog")', html)
        self.assertIn('document.addEventListener("ztt-lang", update)', html)


if __name__ == "__main__":
    unittest.main()
