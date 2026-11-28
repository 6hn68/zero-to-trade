"""README i18n consistency checks (V20).

V20 merges the local increments and hardens them in 10 rounds; V19 adds the interactive 7-day fast path; V18 added competitor anchor pricing; V17 added full Portuguese (README_PT.md, Brazilian Portuguese) and Arabic
(README_AR.md, RTL) translations, aligned with README_EN.md. These tests
check the five README versions agree on version, script count, test count
and prompt count, and that PT/AR carry the key chapters.
"""

import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = {
    "zh": "README.md",
    "en": "README_EN.md",
    "es": "README_ES.md",
    "pt": "README_PT.md",
    "ar": "README_AR.md",
}

# (scripts, tests, prompts) wording each version must carry.
EXPECTED_NUMBERS = {
    "zh": ("15 \u4e2a\u811a\u672c\u6587\u4ef6", "680 \u4e2a\u6807\u51c6\u5e93\u6d4b\u8bd5", "\u63d0\u793a\u8bcd 40 \u6761"),
    "en": ("15 script files", "680 stdlib tests", "40 prompts"),
    "es": ("15 scripts", "680 pruebas", "40 prompts"),
    "pt": ("15 arquivos de script", "680 testes", "40 prompts"),
    "ar": ("15 \u0645\u0644\u0641\u0627\u062a", "680 \u0627\u062e\u062a\u0628\u0627\u0631", "40 \u0645\u0648\u062c\u0651\u0647"),
}

CURRENT_MARKER = {
    "zh": "\u2705 \u5f53\u524d\u7248",
    "en": "\u2705 Current",
    "es": "\u2705 Actual",
    "pt": "\u2705 Atual",
    "ar": "\u2705 \u0627\u0644\u062d\u0627\u0644\u064a\u0629",
}

PT_HEADINGS = [
    "## In\u00edcio r\u00e1pido em 30 segundos",
    "## As sete etapas",
    "## Estrutura do reposit\u00f3rio",
    "## Perguntas frequentes",
]

AR_HEADINGS = [
    "## \u0627\u0644\u0628\u062f\u0621 \u0627\u0644\u0633\u0631\u064a\u0639 \u0641\u064a 30 \u062b\u0627\u0646\u064a\u0629",
    "## \u0627\u0644\u0645\u0631\u0627\u062d\u0644 \u0627\u0644\u0633\u0628\u0639",
    "## \u0628\u0646\u064a\u0629 \u0627\u0644\u0645\u0633\u062a\u0648\u062f\u0639",
    "## \u0627\u0644\u0623\u0633\u0626\u0644\u0629 \u0627\u0644\u0634\u0627\u0626\u0639\u0629",
]


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


class TestReadmeI18n(unittest.TestCase):
    def test_all_five_files_exist(self):
        for name in FILES.values():
            self.assertTrue(
                os.path.isfile(os.path.join(ROOT, name)), "%s missing" % name
            )

    def test_version_v20_present_in_all_five(self):
        for lang, name in FILES.items():
            self.assertIn("V20", read(name), "%s has no V20" % lang)

    def test_v20_is_current_row_in_all_five(self):
        for lang, name in FILES.items():
            text = read(name)
            rows = [ln for ln in text.splitlines() if "**V20**" in ln]
            self.assertTrue(rows, "%s has no V20 roadmap row" % lang)
            self.assertTrue(
                any(CURRENT_MARKER[lang] in ln for ln in rows),
                "%s V20 row is not marked current" % lang,
            )

    def test_script_count_15_in_all_five(self):
        for lang, name in FILES.items():
            self.assertIn(
                EXPECTED_NUMBERS[lang][0], read(name),
                "%s does not say 15 scripts" % lang,
            )

    def test_test_count_680_in_all_five(self):
        for lang, name in FILES.items():
            self.assertIn(
                EXPECTED_NUMBERS[lang][1], read(name),
                "%s does not say 680 tests" % lang,
            )

    def test_prompt_count_40_in_all_five(self):
        for lang, name in FILES.items():
            self.assertIn(
                EXPECTED_NUMBERS[lang][2], read(name),
                "%s does not say 40 prompts" % lang,
            )

    def test_pt_key_headings(self):
        text = read(FILES["pt"])
        for heading in PT_HEADINGS:
            self.assertIn(heading, text, "PT missing heading: %s" % heading)

    def test_ar_key_headings(self):
        text = read(FILES["ar"])
        for heading in AR_HEADINGS:
            self.assertIn(heading, text, "AR missing heading: %s" % heading)

    def test_ar_rtl_marker(self):
        text = read(FILES["ar"])
        self.assertIn('dir="rtl"', text, "AR has no RTL marker")

    def test_pt_ar_sample_markers(self):
        for lang in ("pt", "ar"):
            text = read(FILES[lang])
            self.assertIn("\u3010\u793a\u4f8b\u3011", text, "%s lacks sample marker" % lang)
            self.assertIn("sample.example", text, "%s lacks sample.example" % lang)

    def test_pt_ar_script_names(self):
        for lang in ("pt", "ar"):
            text = read(FILES[lang])
            for script in ("lead_score.py", "outreach_gen.py", "followup_plan.py",
                           "quote_engine.py", "due_diligence.py", "tire_pack.py",
                           "landed_cost.py", "trade_show.py", "nudge.py",
                           "anchor_price.py", "fast_path.py",
                           "check_private_data.py"):
                self.assertIn(script, text, "%s lacks %s" % (lang, script))

    def test_readme_nav_lists_pt_and_ar(self):
        text = read(FILES["zh"])
        self.assertIn("README_PT.md", text, "README.md nav lacks PT")
        self.assertIn("README_AR.md", text, "README.md nav lacks AR")

    def test_pt_mentions_brazilian_portuguese(self):
        self.assertIn("Brasil", read(FILES["pt"]))

    def test_en_headings_mirrored(self):
        text = read(FILES["en"])
        for heading in ("## 30-second quickstart", "## The seven stages",
                        "## Repository layout"):
            self.assertIn(heading, text)

    def test_pt_ar_roadmap_rows_mention_new_files(self):
        self.assertIn("README_PT.md", read(FILES["pt"]))
        self.assertIn("README_AR.md", read(FILES["ar"]))


if __name__ == "__main__":
    unittest.main()
