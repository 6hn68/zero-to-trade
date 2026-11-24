"""Tests for the --review self-check in scripts/outreach_gen.py.

Route 09, round 2026-11-24: review_email_draft() / subject_alternatives()
/ count_body_sentences() / the --review CLI flag, plus the spam_scan fix
(a tyre size like 12.00R20 must not count as shouting). The review is
report-only: it lists flags, it never rewrites a draft.
"""

import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "scripts"))
import outreach_gen as og  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _body(tier, **kw):
    """Format one real BODY template with fixture values."""
    vals = {"subject": "TBR supply — Sample Co",
            "greeting": "Hi Adaeze,",
            "company": "Sample Co",
            "product": "TBR 315/80R22.5",
            "country": "Nigeria",
            "sender": "Jason | Sample Tyre",
            "why_them": "A client who knows the Nigeria market recommended your company to us"}
    vals.update(kw)
    return og.BODY[tier]["en"].format(**vals)


def _subject(tier="T0"):
    en, _zh, _fits = og.fit_subject(tier, "TBR 315/80R22.5",
                                    "TBR 315/80R22.5", "Sample Co")
    return en


class TestSentenceCounter(unittest.TestCase):
    def test_real_templates_sentence_counts(self):
        # T0: why(2) + We make(1) + lead-in(1) + bullets(2) + question(1) = 7
        self.assertEqual(og.count_body_sentences(_body("T0")), 7)
        # T1: why(2) + We make(1) + question(1) + reply(2) = 6
        self.assertEqual(og.count_body_sentences(_body("T1")), 6)
        # T2: updating(1) + question(2) = 3 — lightest touch by design
        self.assertEqual(og.count_body_sentences(_body("T2")), 3)

    def test_skips_subject_greeting_and_signoff(self):
        text = ("Subject: hello\n\nHi Adaeze,\n\nOne sentence here.\n\n"
                "Best regards,\nJason")
        self.assertEqual(og.count_body_sentences(text), 1)

    def test_bullet_counts_as_one(self):
        text = "Hi,\n\nIntro line:\n- First point\n- Second point\n\nBest regards,\nMe"
        self.assertEqual(og.count_body_sentences(text), 3)

    def test_question_counter(self):
        self.assertEqual(og.count_body_questions(_body("T0")), 1)
        self.assertEqual(og.count_body_questions("A? B? C."), 2)
        self.assertEqual(og.count_body_questions("No question here."), 0)


class TestReviewEmailDraft(unittest.TestCase):
    def test_real_templates_pass_review(self):
        for tier in ("T0", "T1", "T2"):
            flags = og.review_email_draft(_subject(tier), _body(tier),
                                          False, tier)
            self.assertEqual(flags, [], "%s template flagged: %s" % (tier, flags))

    def test_subject_too_long_flagged(self):
        flags = og.review_email_draft("X" * 45, _body("T0"), False, "T0")
        self.assertTrue(any("主题行 45 字符" in f for f in flags))

    def test_body_too_short_flagged(self):
        short = "Hi Adaeze,\n\nOne sentence here.\n\nBest regards,\nMe"
        flags = og.review_email_draft(_subject(), short, False, "T0")
        self.assertTrue(any("正文 1 句" in f for f in flags))

    def test_body_too_long_flagged(self):
        long_body = "Hi Adaeze,\n\n" + "\n".join(
            "Sentence %d here." % i for i in range(9)) + "\n\nBest regards,\nMe"
        flags = og.review_email_draft(_subject(), long_body, False, "T0")
        self.assertTrue(any("正文 9 句" in f for f in flags))

    def test_preview_too_long_flagged(self):
        body = ("Hi Adaeze,\n\n" + "A very long first sentence " * 6 +
                "that keeps going.\n\nBest regards,\nMe")
        flags = og.review_email_draft(_subject(), body, False, "T0")
        self.assertTrue(any("预览首句" in f for f in flags))

    def test_price_leak_flagged(self):
        body = _body("T0").replace("within 48 hours", "for $29 within 48 hours")
        flags = og.review_email_draft(_subject(), body, False, "T0")
        self.assertTrue(any("价格" in f for f in flags))

    def test_spam_word_flagged(self):
        body = _body("T0").replace("Best regards,", "Act now! Best regards,")
        flags = og.review_email_draft(_subject(), body, False, "T0")
        self.assertTrue(any("act now" in f for f in flags))

    def test_leftover_placeholder_flagged(self):
        body = _body("T0") + "\nP.S. {company} again."
        flags = og.review_email_draft(_subject(), body, False, "T0")
        self.assertTrue(any("{company}" in f for f in flags))

    def test_quoted_placeholder_in_why_them_is_not_leftover(self):
        body = _body("T0")
        flags = og.review_email_draft(_subject(), body, False, "T0",
                                      why_texts=('note says "{product}" here',))
        self.assertEqual(flags, [])

    def test_two_questions_flagged(self):
        body = _body("T2").replace("this year?",
                                    "this year? Or next year?")
        flags = og.review_email_draft(_subject("T2"), body, False, "T2")
        self.assertTrue(any("2 个问句" in f for f in flags))

    def test_generic_why_them_flagged(self):
        flags = og.review_email_draft(_subject(), _body("T0"), True, "T0")
        self.assertTrue(any("why them" in f for f in flags))


class TestSpamScanTyreSize(unittest.TestCase):
    def test_tyre_size_is_not_shouting(self):
        # Regression: 12.00R20 used to trip the ALL-CAPS check ("00R20").
        self.assertEqual(og.spam_scan("TBR 12.00R20 supply"), [])
        self.assertEqual(og.spam_scan("We make TBR 315/80R22.5 and ship it."), [])

    def test_real_shouting_still_caught(self):
        hits = og.spam_scan("This is a FREE URGENT offer")
        self.assertTrue(any("free" in h for h in hits))
        self.assertTrue(any("URGENT" in h for h in hits))


class TestSubjectAlternatives(unittest.TestCase):
    def test_t0_lists_both_candidates(self):
        alts = og.subject_alternatives("T0", "TBR", "TBR", "Sample Co")
        self.assertEqual(len(alts), 2)
        self.assertTrue(all(fits for _e, _z, fits in alts))

    def test_long_product_falls_back_to_shorter(self):
        alts = og.subject_alternatives(
            "T0", "TBR 315/80R22.5 premium highway",
            "TBR 315/80R22.5 premium highway", "A Very Long Company Name Ltd")
        self.assertEqual(len(alts), 2)
        self.assertFalse(alts[0][2])  # long form over 40 chars
        self.assertTrue(alts[1][2])   # short form still fits


class TestReviewCLI(unittest.TestCase):
    def _run(self, *argv):
        proc = subprocess.run(
            [sys.executable, "scripts/outreach_gen.py"] + list(argv),
            cwd=ROOT, capture_output=True, text=True, timeout=120)
        return proc

    def test_review_flag_adds_block(self):
        proc = self._run("examples/leads_example.csv", "--tier", "T0",
                         "--lang", "en", "--review")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Review / 复核", proc.stdout)
        self.assertIn("主题备选", proc.stdout)

    def test_without_review_no_block(self):
        proc = self._run("examples/leads_example.csv", "--tier", "T0",
                         "--lang", "en")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("Review / 复核", proc.stdout)

    def test_review_does_not_change_drafts(self):
        with_review = self._run("examples/leads_example.csv", "--tier", "T0",
                                 "--lang", "en", "--review").stdout
        without = self._run("examples/leads_example.csv", "--tier", "T0",
                            "--lang", "en").stdout
        # Every non-review line of the --review run is in the plain run.
        # The review block runs from its header to the next blank line;
        # drop exactly that span (checklist "✗ FIX" lines look similar
        # but belong to the draft and must stay).
        kept = []
        in_review = False
        for ln in with_review.splitlines():
            if ln.startswith("Review / 复核"):
                in_review = True
                continue
            if in_review:
                if ln.strip() == "":
                    in_review = False
                    kept.append(ln)
                continue
            kept.append(ln)
        self.assertEqual("\n".join(kept).strip(), without.strip())


if __name__ == "__main__":
    unittest.main()
