#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the three-channel outreach (V14): email / LinkedIn note / web form
share one pitch, and the LinkedIn connection note is capped at 200 chars.

Run: python3 -m pytest tests/test_outreach_channels.py -q   (from the repo root)
"""

import subprocess
import sys
import tempfile
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


class TestLinkedInNote(unittest.TestCase):
    def test_note_within_200_chars_all_tiers(self):
        for tier, score in (("T0", 95), ("T1", 77), ("T2", 50)):
            note = og.build_linkedin_note(make_lead(tier=tier, score=score))
            self.assertLessEqual(len(note), og.LINKEDIN_NOTE_LIMIT, tier)
        # T0/T1 carry the why-them sentence; T2's note is the
        # confirm-sourcing question only (same as its email body).
        self.assertIn("Tender invitation issued by Oman municipality",
                      og.build_linkedin_note(make_lead(tier="T0", score=95)))
        self.assertIn("Updating my notes",
                      og.build_linkedin_note(make_lead(tier="T2", score=50)))

    def test_note_carries_same_cta_as_email(self):
        # T0 asks sizes + volume, T1/T2 ask to confirm sourcing — same CTA
        # as the email body for that tier, only shorter.
        note_t0 = og.build_linkedin_note(make_lead(tier="T0", score=95))
        self.assertIn("sizes and monthly volume", note_t0)
        note_t1 = og.build_linkedin_note(make_lead())
        self.assertIn("still something you source from Asia", note_t1)
        note_t2 = og.build_linkedin_note(make_lead(tier="T2", score=50))
        self.assertIn("still sourcing from Asia this year", note_t2)

    def test_note_too_long_raises_instead_of_truncating(self):
        # A long note column (95 chars, the preview budget) + T0's longer
        # CTA pushes the note over 200 — it must raise, not silently cut.
        long_why = ("your note mentioned: " + "x" * 95,
                    "贵司备注提到：" + "x" * 95, False)
        lead = make_lead(tier="T0", score=95, why_them=long_why,
                         product="TBR 12.00R20, PCR tubes, OTR tyres")
        with self.assertRaises(og.LinkedInNoteTooLongError) as cm:
            og.build_linkedin_note(lead)
        self.assertIn("200", str(cm.exception))
        # The message says how long it actually is, so the fix is obvious.
        self.assertRegex(str(cm.exception), r"\d+ chars")

    def test_render_linkedin_raises_on_long_note(self):
        long_why = ("your note mentioned: " + "x" * 95,
                    "贵司备注提到：" + "x" * 95, False)
        lead = make_lead(tier="T0", score=95, why_them=long_why)
        with self.assertRaises(og.LinkedInNoteTooLongError):
            og.render(lead, "Sender", "en", channel="linkedin")

    def test_note_is_english_even_when_lang_is_es(self):
        out = og.render(make_lead(), "[Your Name] | [Company]", "es",
                        channel="linkedin")
        self.assertIn("[LinkedIn note — paste into the connection request]", out)
        self.assertIn("Quick question", out)
        self.assertNotIn("Saludos cordiales", out)

    def test_note_checklist_reports_length(self):
        out = og.render(make_lead(), "[Your Name] | [Company]", "en",
                        channel="linkedin")
        self.assertIn("LinkedIn note checklist:", out)
        self.assertIn("Note 144 chars (<=200", out)

    def test_t3_linkedin_needs_no_copy(self):
        self.assertIsNone(og.build_linkedin_note(make_lead(tier="T3", score=20)))
        self.assertIsNone(og.render(make_lead(tier="T3", score=20),
                                    "Sender", "en", channel="linkedin"))


class TestWebFormChannel(unittest.TestCase):
    def test_webform_has_form_subject_but_no_subject_line(self):
        out = og.render(make_lead(tier="T0", score=95),
                        "[Your Name] | [Company]", "both", channel="webform")
        self.assertIn("[Form subject — put this in the form's subject field]", out)
        self.assertIn("[Message — paste into the form's message box]", out)
        self.assertNotIn("\nSubject: ", out)
        # Same CTA as the email body for T0.
        self.assertIn("What sizes and monthly volume are you running", out)

    def test_webform_carries_zh_reference_for_approval(self):
        out = og.render(make_lead(), "[Your Name] | [Company]", "both",
                        channel="webform")
        self.assertIn("[ZH — 中文对照，仅供你审批，客户不收]", out)


class TestChannelConsistency(unittest.TestCase):
    def test_three_channels_agree_on_fixture_leads(self):
        for tier, score in (("T0", 95), ("T1", 77), ("T2", 50)):
            ok, problems = og.check_channel_consistency(
                make_lead(tier=tier, score=score), "Sender")
            self.assertTrue(ok, (tier, problems))
            self.assertEqual(problems, [])

    def test_consistency_flags_price_in_why_them(self):
        # A price smuggled in through the note column shows up in all three
        # channels — the check must catch it instead of passing quietly.
        priced = ("your note mentioned: quoted USD 500 per unit last month",
                  "贵司备注提到：上月报过 USD 500 一件", False)
        ok, problems = og.check_channel_consistency(
            make_lead(why_them=priced), "Sender")
        self.assertFalse(ok)
        self.assertTrue(any("price" in p for p in problems), problems)

    def test_consistency_flags_linkedin_note_too_long(self):
        long_why = ("your note mentioned: " + "x" * 95,
                    "贵司备注提到：" + "x" * 95, False)
        ok, problems = og.check_channel_consistency(
            make_lead(tier="T0", score=95, why_them=long_why), "Sender")
        self.assertFalse(ok)
        self.assertTrue(any("200" in p for p in problems), problems)

    def test_consistency_t3_is_vacuously_ok(self):
        ok, problems = og.check_channel_consistency(
            make_lead(tier="T3", score=20), "Sender")
        self.assertTrue(ok)
        self.assertEqual(problems, [])


class TestChannelCLI(unittest.TestCase):
    def test_cli_linkedin_channel(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T1", "--channel", "linkedin")
        self.assertEqual(code, 0)
        self.assertIn("[LinkedIn note — paste into the connection request]", out)
        self.assertIn("LinkedIn note checklist:", out)
        self.assertNotIn("Traceback", out)

    def test_cli_webform_channel(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T0", "--channel", "webform")
        self.assertEqual(code, 0)
        self.assertIn("[Message — paste into the form's message box]", out)
        self.assertNotIn("Traceback", out)

    def test_cli_channel_all_emits_three_blocks_per_lead(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T1", "--channel", "all")
        self.assertEqual(code, 0)
        self.assertIn("[EN — send this]", out)
        self.assertIn("[LinkedIn note — paste into the connection request]", out)
        self.assertIn("[Message — paste into the form's message box]", out)
        self.assertNotIn("Traceback", out)

    def test_cli_long_note_is_skipped_not_fatal(self):
        # One lead's note over 200 chars must not kill the whole batch:
        # its LinkedIn block becomes a plain-language skip note, the rest
        # still render. (Temp CSV: 95-char note column + T0 CTA > 200.)
        long_note = "x" * 95
        content = ("company,country,product,source,email,phone,years,contact,note\n"
                   "【示例】超长备注公司,Oman,TBR 12.00R20,referral,"
                   "demo01@sample.example,+000 00 000 0000,18,Alex,\"%s\"\n"
                   "【示例】海湾轮胎贸易,Saudi Arabia,\"TBR 12.00R20, PCR tubes\",referral,"
                   "demo02@sample.example,+000 00 000 0000,18,purchasing manager,"
                   "\"Annual RFQ for truck tyres, looking for supplier\"\n" % long_note)
        tmp = tempfile.NamedTemporaryFile(
            "w", suffix=".csv", delete=False, encoding="utf-8")
        tmp.write(content)
        tmp.close()
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        code, out = run_script("outreach_gen.py", tmp.name,
                               "--tier", "T0", "--channel", "linkedin")
        self.assertEqual(code, 0, out)
        self.assertNotIn("Traceback", out)
        self.assertIn("LinkedIn note is", out)
        self.assertIn("200", out)
        # The other lead's note still renders.
        self.assertIn("[LinkedIn note — paste into the connection request]", out)

    def test_cli_bad_channel_is_argparse_error(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T0", "--channel", "fax")
        self.assertNotEqual(code, 0)
        self.assertIn("linkedin", out)
        self.assertNotIn("Traceback", out)

    def test_cli_help_lists_channel_examples(self):
        code, out = run_script("outreach_gen.py", "--help")
        self.assertEqual(code, 0)
        self.assertIn("--channel linkedin", out)
        self.assertIn("--channel all", out)

    def test_cli_default_channel_is_still_email(self):
        code, out = run_script("outreach_gen.py", "examples/leads_example.csv",
                               "--tier", "T0")
        self.assertEqual(code, 0)
        self.assertIn("[EN — send this]", out)
        self.assertNotIn("[LinkedIn note — paste", out)


if __name__ == "__main__":
    unittest.main()
