#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for the 5 vulnerabilities fixed on 2026-11-21.
2026-11-21 修掉的 5 个漏洞的回归测试。

Run: python3 -m unittest discover -s tests -v   (from the repo root)
     python3 -m pytest tests/test_vuln_fixes.py -q

Each test pins the fixed behaviour (the lane report that first recorded
each bug is cited in the test docstring). All fixtures are synthetic
and fictional; nothing is sent anywhere.
只用 Python 标准库；全部数据均为 synthetic 虚构数据。
"""

import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import lead_score as ls  # noqa: E402
import outreach_gen as og  # noqa: E402


def _write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def _make_lead(**over):
    lead = {"tier": "T1", "score": 77, "company": "Synthetic Oman Trading Co",
            "country": "Oman", "product": "TBR 12.00R20",
            "email": "demo01@sample.example", "contact": "Alex",
            "why_them": ("your note mentioned: tender invitation RFQ",
                         "贵司备注提到：tender invitation RFQ", False),
            "why_them_i18n": {"es": "su nota menciona: tender invitation RFQ",
                              "pt": "sua nota menciona: tender invitation RFQ",
                              "ar": "ذكرت ملاحظتك: tender invitation RFQ"}}
    lead.update(over)
    return lead


class TestCheckPrivateDataScope(unittest.TestCase):
    """F01 (lane 29-cli-usability): privacy scan must not silently pass."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.copy = Path(self._tmp.name) / "repo"
        shutil.copytree(REPO_ROOT, self.copy, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(
                            ".git", "__pycache__", "logs", ".pytest_cache"))

    def tearDown(self):
        self._tmp.cleanup()

    def test_refuses_outside_repo_root(self):
        """F01a: running from scripts/ must not silently pass.
        在 scripts/ 里跑，不许悄悄报“过了”：必须非 0 退出并点名不在根目录。"""
        proc = subprocess.run([sys.executable, "check_private_data.py"],
                              capture_output=True, text=True, timeout=60,
                              cwd=str(self.copy / "scripts"))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("不在仓库根目录", proc.stdout + proc.stderr)

    def test_scans_subdirectories(self):
        """F01b: a real-looking email in docs/advanced/ must be flagged.
        docs/ 子目录里的疑似真人邮箱也必须被扫出来。"""
        target = self.copy / "docs" / "advanced"
        target.mkdir(parents=True, exist_ok=True)
        (target / "dirty_probe_vuln.md").write_text(
            "# probe\ncontact: someone@realmail.org\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "scripts/check_private_data.py"],
            capture_output=True, text=True, timeout=60, cwd=str(self.copy))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("dirty_probe_vuln.md", proc.stdout + proc.stderr)


class TestChineseHeaders(unittest.TestCase):
    """Chinese column names (lane 26-dirty-csv-tests, file 05)."""

    def test_partial_chinese_headers_keep_email_and_tier(self):
        """Lane 26 file 05: company in English, 产品/邮箱 in Chinese.
        The email must be recognised (contact 40, tier T0) instead of
        silently dropped (was: email lost, 40 -> 22, T0 -> T1, no warning).
        部分中文列名：邮箱必须认出来（联系方式 40 分、T0），不能静默丢掉。"""
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "partial_cn.csv")
            _write_csv(path,
                       ["company", "country", "产品", "source", "邮箱", "phone",
                        "years", "contact", "note"],
                       [["Synthetic Mu Trading", "Saudi Arabia", "TBR",
                         "referral", "mu@sample.example", "+000 00 000 0020",
                         "18", "buyer", "note"]])
            rows = ls.read_leads(path)
            results, _ = ls.analyze(rows)
            row = results[0]
            self.assertEqual(row["email"], "mu@sample.example")
            self.assertEqual(row["score"], 83)
            self.assertEqual(row["tier"], "T0")

    def test_fully_chinese_headers_still_fail_loudly(self):
        """Lane 26 file 04: an all-Chinese header (公司/产品/邮箱) still
        fails loudly with '缺少 company 列' -- the company column stays
        English-only on purpose, so this guard is not lost by the alias fix.
        全中文列名仍大声报错：公司列故意不映射，这层保护不能丢。"""
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "all_cn.csv")
            _write_csv(path,
                       ["公司", "country", "产品", "source", "邮箱", "phone",
                        "years", "contact", "note"],
                       [["Synthetic Alpha Trading", "Saudi Arabia", "TBR",
                         "referral", "alpha@sample.example",
                         "+000 00 000 0001", "18", "purchasing manager",
                         "note"]])
            with self.assertRaises(ls.LeadDataError) as ctx:
                ls.read_leads(path)
            self.assertIn("缺少 company", str(ctx.exception))


class TestTableRender(unittest.TestCase):
    """F-04 / F-05 (lane 25-edge-fuzz-tests): table/detail rendering."""

    def _scored(self, company):
        res, _ = ls.analyze([{"company": company, "country": "Oman",
                              "product": "tyres", "email": "a@b.co",
                              "phone": "+1234567", "source": "referral",
                              "years": "12", "note": "RFQ"}])
        return res

    def test_folds_company_newline(self):
        """F-04: a newline inside a company name must not break the table
        rows -- it is folded to a space in table output.
        公司名里的换行不能打断表格：表格里折成空格。"""
        table = ls.render_table(self._scored("Acme\nLtd"))
        self.assertNotIn("Acme\nLtd", table)
        self.assertIn("Acme Ltd", table)

    def test_no_nul_in_table_or_detail(self):
        """F-05: a NUL byte from a CSV cell must not reach table or detail
        output (JSON/CSV keep the raw value -- they escape it).
        公司名里的 NUL 不能进表格/明细输出。"""
        res = self._scored("Acme\x00Ltd")
        self.assertNotIn("\x00", ls.render_table(res))
        self.assertNotIn("\x00", ls.render_detail(res))

    def test_json_and_csv_keep_raw_newline(self):
        """Guard: JSON/CSV still preserve the raw newline (they escape it,
        so they stay valid) -- the F-04 fold applies to table/detail only.
        反向 guard：JSON/CSV 仍保留原值换行，折叠只发生在表格/明细。"""
        res = self._scored("Acme\nLtd")
        self.assertEqual(
            json.loads(ls.render_json(res, "synthetic.csv"))["leads"][0]["company"],
            "Acme\nLtd")
        self.assertIn('"Acme\nLtd', ls.render_csv(res))


class TestPlaceholderCheck(unittest.TestCase):
    """F-06 (lane 25-edge-fuzz-tests): placeholder false positive."""

    def test_note_placeholder_text_not_flagged(self):
        """A note literally containing '{product}' is quoted user content,
        not a leaked template placeholder -- the checklist must not flag
        it. A real leftover (e.g. via the sender line) is still caught.
        备注里写着 {product} 是用户原文，不是模板残留：自查不许误报；
        真残留仍要报。"""
        row = {"note": "{product} RFQ", "source": "search",
               "country": "Oman", "product": "TBR 12.00R20"}
        why = og.build_why_them(row, "TBR 12.00R20")
        out = og.render(_make_lead(why_them=why), "Sender", "en")
        self.assertFalse(any("leftover placeholder" in ln and "✗" in ln
                             for ln in out.splitlines()))
        # Control: a genuine leftover placeholder is still flagged.
        out2 = og.render(_make_lead(), "{company}", "en")
        self.assertTrue(any("leftover placeholder" in ln and "✗" in ln
                            for ln in out2.splitlines()))


if __name__ == "__main__":
    unittest.main()
