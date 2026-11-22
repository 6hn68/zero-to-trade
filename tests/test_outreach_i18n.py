#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the V13 multilingual outreach (--lang es/pt/ar).

Run: python3 -m unittest discover -s tests -v   (from the repo root)
"""

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import outreach_gen as og  # noqa: E402


def run_script(name, *args):
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / name), *args],
        capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout + proc.stderr


def make_lead(**over):
    lead = {
        "tier": "T1",
        "score": 77,
        "company": "【示例】阿曼蓝海",
        "country": "Oman",
        "product": "TBR 12.00R20",
        "email": "demo01@sample.example",
        "contact": "purchasing manager",
        "why_them": ("your note mentioned: Tender invitation issued by Oman municipality",
                     "贵司备注提到：Tender invitation issued by Oman municipality", False),
        "why_them_i18n": {
            "es": "su nota menciona: Tender invitation issued by Oman municipality",
            "pt": "sua nota menciona: Tender invitation issued by Oman municipality",
            "ar": "ذكرت ملاحظتك: Tender invitation issued by Oman municipality",
        },
    }
    lead.update(over)
    return lead


class TestI18nRender(unittest.TestCase):
    def test_es_t0_full_message(self):
        out = og.render(make_lead(tier="T0", score=95), "[Your Name] | [Company]", "es")
        self.assertIn("[Español — send this]", out)
        self.assertIn("Por eso le escribo directamente", out)
        self.assertIn("Saludos cordiales,", out)
        self.assertIn("[EN — English original, for approval]", out)
        self.assertIn("That is why I am writing to you", out)

    def test_pt_t1_full_message(self):
        out = og.render(make_lead(), "[Your Name] | [Company]", "pt")
        self.assertIn("[Português — send this]", out)
        self.assertIn("Só uma pergunta", out)
        self.assertIn("Atenciosamente,", out)
        self.assertIn("[EN — English original, for approval]", out)

    def test_ar_t2_full_message(self):
        out = og.render(make_lead(tier="T2", score=50), "[Your Name] | [Company]", "ar")
        self.assertIn("[العربية — send this]", out)
        self.assertIn("أحدّث ملاحظاتي", out)
        self.assertIn("مع أطيب التحيات،", out)
        self.assertIn("[EN — English original, for approval]", out)

    def test_every_lang_output_carries_english_reference(self):
        for lang in ("es", "pt", "ar"):
            out = og.render(make_lead(), "[Your Name] | [Company]", lang)
            self.assertIn("[EN — English original, for approval]", out, lang)
            self.assertIn("Best regards,", out, lang)

    def test_no_leftover_placeholders_in_any_lang(self):
        for lang in ("es", "pt", "ar"):
            out = og.render(make_lead(), "[Your Name] | [Company]", lang)
            for ph in ("{product}", "{company}", "{country}", "{subject}",
                       "{greeting}", "{why_them}", "{sender}"):
                self.assertNotIn(ph, out, (lang, ph))

    def test_role_contact_falls_back_to_bare_greeting(self):
        for lang, bare in (("es", "Hola,"), ("pt", "Olá,"), ("ar", "مرحباً،")):
            out = og.render(make_lead(), "[Your Name] | [Company]", lang)
            self.assertIn(bare, out, lang)
            self.assertNotIn("purchasing manager", out, lang)

    def test_why_them_i18n_source_fallback(self):
        # note 为空时走来源模板（search 之外的来源也有对应句）
        row = {"source": "customs", "country": "Oman",
               "product": "TBR 12.00R20", "note": ""}
        self.assertIn("historial de importación",
                      og.build_why_them_i18n(row, "TBR 12.00R20", "es"))
        self.assertIn("histórico de importação",
                      og.build_why_them_i18n(row, "TBR 12.00R20", "pt"))
        self.assertIn("سجل استيراد",
                      og.build_why_them_i18n(row, "TBR 12.00R20", "ar"))


class TestI18nCLI(unittest.TestCase):
    def test_cli_es_pt_ar_each_run(self):
        for lang, marker in (("es", "Saludos cordiales,"),
                             ("pt", "Atenciosamente,"),
                             ("ar", "مع أطيب التحيات،")):
            code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                                   "--tier", "T0", "--lang", lang)
            self.assertEqual(code, 0, lang)
            self.assertIn(marker, out, lang)
            self.assertIn("[EN — English original, for approval]", out, lang)

    def test_cli_bad_lang_is_argparse_error(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T0", "--lang", "fr")
        self.assertNotEqual(code, 0)
        self.assertIn("es", out)
        self.assertNotIn("Traceback", out)

    def test_cli_english_output_has_no_i18n_markers(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T0", "--lang", "en")
        self.assertEqual(code, 0)
        self.assertIn("[EN — send this]", out)
        for marker in ("Saludos cordiales,", "Atenciosamente,", "مع أطيب التحيات،"):
            self.assertNotIn(marker, out)

    def test_cli_help_lists_real_i18n_examples(self):
        code, out = run_script("outreach_gen.py", "--help")
        self.assertEqual(code, 0)
        self.assertIn("--lang es", out)
        self.assertIn("--lang pt", out)
        self.assertIn("--lang ar", out)

    def test_cli_t3_i18n_needs_no_copy(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T3", "--lang", "es")
        self.assertEqual(code, 0)
        self.assertIn("no first-touch copy needed", out)
        self.assertNotIn("Traceback", out)


class TestSingleMode(unittest.TestCase):
    """单条模式（--company，不读 CSV）是合并刚恢复的本地用法。"""

    def test_single_mode_writes_one_draft_with_given_tier(self):
        code, out = run_script(
            "outreach_gen.py", "--company", "【示例】海湾轮胎贸易",
            "--country", "Saudi Arabia", "--contact", "Alex",
            "--product", "TBR 12.00R20", "--tier", "T1")
        self.assertEqual(code, 0)
        self.assertIn("【示例】海湾轮胎贸易", out)
        self.assertIn("分级: T1", out)
        self.assertNotIn("Traceback", out)

    def test_single_mode_tier_all_keeps_scored_tier(self):
        code, out = run_script(
            "outreach_gen.py", "--company", "【示例】海湾轮胎贸易",
            "--country", "Saudi Arabia", "--contact", "Alex",
            "--product", "TBR 12.00R20", "--tier", "all")
        self.assertEqual(code, 0)
        self.assertIn("【示例】海湾轮胎贸易", out)

    def test_single_mode_without_company_errors_in_words(self):
        code, out = run_script("outreach_gen.py")
        self.assertNotEqual(code, 0)
        self.assertNotIn("Traceback", out)
        self.assertIn("请给一个线索 CSV 路径", out)

    def test_run_log_written(self):
        run_script("outreach_gen.py", "--company", "【示例】海湾轮胎贸易",
                   "--country", "Saudi Arabia", "--tier", "T1")
        log_path = REPO_ROOT / "logs" / "outreach_gen.log"
        self.assertTrue(log_path.exists())
        text = log_path.read_text(encoding="utf-8")
        self.assertIn("RUN argv=", text)
        self.assertIn("RESULT drafts=", text)


if __name__ == "__main__":
    unittest.main()
