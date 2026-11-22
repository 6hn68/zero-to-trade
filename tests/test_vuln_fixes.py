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
import check_private_data as cpd  # noqa: E402


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


    def test_clean_repo_still_passes(self):
        """Guard (route 07, 2026-11-22): after narrowing the SAFE_HINT
        line skip, the repo's own files must still scan clean -- the
        scanner must not start flagging docs that only mention the
        words "fake" / "placeholder".
        反向 guard：收窄豁免后，仓库自己的文件仍须扫过——只提到
        "fake"/"placeholder" 这些词的文档不能被误报。"""
        proc = subprocess.run(
            [sys.executable, "scripts/check_private_data.py"],
            capture_output=True, text=True, timeout=60, cwd=str(self.copy))
        self.assertEqual(proc.returncode, 0)
        self.assertIn("没查到真实客户数据", proc.stdout)


class TestCheckPrivateDataBoundaries(unittest.TestCase):
    """Route 07 (2026-11-22): boundary-case regressions for the privacy
    scan -- the 2026-11-21 fix stopped the silent pass, these cases
    stop the quieter false negatives (and one false positive) around it.
    All fixtures are synthetic and fictional; .example / .test domains
    are RFC 2606 reserved, phone digits are sequential patterns.
    隐私扫描边界 case 回归：2026-11-21 修了静默假通过，这批补更安静的
    漏报（和一处误报）。全部数据均为虚构，域名用 RFC 2606 保留域，
    电话用顺序号段。"""

    def _scan(self, text):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "probe.md")
            Path(path).write_text(text, encoding="utf-8")
            return cpd.scan_file(path)

    def test_test_at_hint_no_longer_hides_real_email(self):
        """A "test@" note on the same line must not hide a real email
        next to it -- the old whole-line SAFE_HINT skip let it through.
        同行写了 test@ 也不能藏住旁边的真邮箱。"""
        hits = self._scan("contact: buyer@customer-mail.example  # test@sample\n")
        self.assertTrue(any("customer-mail.example" in why for _, why in hits))

    def test_fake_word_no_longer_hides_real_phone(self):
        """The word "fake" on a line must not hide a real phone number.
        同行写了 fake 也不能藏住真电话。"""
        hits = self._scan("fake entry, call +966 55 123 4567\n")
        self.assertTrue(any("手机" in why for _, why in hits))

    def test_phone_with_zero_group_still_flagged(self):
        """+966 50 000 1234 is a real-looking number -- the old
        line-level "000" placeholder check wrongly let it through.
        带 000 组的真号不能再被放过。"""
        hits = self._scan("phone: +966 50 000 1234\n")
        self.assertTrue(any("手机" in why for _, why in hits))

    def test_spaces_around_at_flagged(self):
        """Spaces around @ do not make an address fake.
        @ 前后加空格仍是邮箱。"""
        hits = self._scan("reach me at buyer @ customer-mail.example\n")
        self.assertTrue(any("customer-mail.example" in why for _, why in hits))

    def test_at_word_obfuscation_flagged(self):
        """someone [at] domain is still a real address.
        [at] 写法仍是真邮箱。"""
        hits = self._scan("email me at buyer [at] customer-mail.example\n")
        self.assertTrue(any("customer-mail.example" in why for _, why in hits))

    def test_fullwidth_email_and_phone_flagged(self):
        """Full-width digits / @ pasted from a chat app are still
        a real phone / email. 全角数字、全角 @ 也要认出来。"""
        self.assertTrue(self._scan("电话：１３８１２３４５６７８\n"))
        hits = self._scan("邮箱：buyer＠customer-mail.example\n")
        self.assertTrue(any("customer-mail.example" in why for _, why in hits))

    def test_dotted_phone_flagged(self):
        """138.1234.5678 is a phone, not a version number.
        点分隔的号码也是电话。"""
        hits = self._scan("call 138.1234.5678\n")
        self.assertTrue(any("手机" in why for _, why in hits))

    def test_email_in_code_comment_flagged(self):
        """An address hiding in a code comment is still a leak.
        藏在代码注释里的邮箱也是泄漏。"""
        hits = self._scan("# TODO: send quote to buyer@customer-mail.example\n")
        self.assertTrue(any("customer-mail.example" in why for _, why in hits))

    def test_long_line_email_flagged_fast(self):
        """A real email at the end of a 100k-char line must be found,
        and fast -- the old EMAIL regex backtracked quadratically
        here and the scan hung instead of finishing.
        10 万字符长行末尾的邮箱必须被找到，而且要快——旧正则在这里
        平方级回溯，扫描直接挂住。"""
        import time
        text = "x" * 100000 + " buyer@customer-mail.example\n"
        started = time.monotonic()
        hits = self._scan(text)
        self.assertLess(time.monotonic() - started, 5)
        self.assertTrue(any("customer-mail.example" in why for _, why in hits))

    def test_long_digit_run_finishes_fast(self):
        """A 50k-digit run must not hang the phone regex either.
        5 万位纯数字串也不能挂住电话正则。"""
        import time
        text = "1" * 50000 + "\n"
        started = time.monotonic()
        hits = self._scan(text)
        self.assertLess(time.monotonic() - started, 5)
        self.assertEqual(hits, [])

    def test_empty_file_clean(self):
        """An empty file scans clean, no crash. 空文件干净、不报错。"""
        self.assertEqual(self._scan(""), [])

    def test_placeholder_phone_still_clean(self):
        """+000 00 000 0000 stays a placeholder, not a leak.
        +000 占位号仍不算泄漏。"""
        self.assertEqual(self._scan("phone: +000 00 000 0000\n"), [])

    def test_sample_domain_still_clean(self):
        """sample.example addresses stay clean, including subdomains.
        sample.example 邮箱仍干净，子域名也一样。"""
        self.assertEqual(self._scan("mail: demo01@sample.example\n"), [])
        self.assertEqual(self._scan("mail: info@mail.example.com\n"), [])

    def test_example_marker_line_still_exempt(self):
        """A line explicitly marked 【示例】 is still exempt.
        明确标了【示例】的行仍豁免。"""
        self.assertEqual(
            self._scan("【示例】 buyer@customer-mail.example\n"), [])

    def test_timestamp_and_version_not_flagged(self):
        """A date+time and a version number are not phone numbers.
        日期时间和版本号不是电话。"""
        self.assertEqual(self._scan("updated 2026-11-21 10:30:45\n"), [])
        self.assertEqual(self._scan("requires python 3.11.2 or later\n"), [])

    def test_ipv4_not_flagged_as_phone(self):
        """192.168.1.100 is an IP address, not a phone number.
        IPv4 地址不是电话。"""
        self.assertEqual(self._scan("server 192.168.1.100\n"), [])

    def test_real_us_style_number_not_eaten_by_date_guard(self):
        """Guard check: the date guard must not swallow a real number
        that starts with 202 (a DC area code, fictional 555 exchange).
        反向 guard：日期保护不能把 202 开头的真号也吞掉。"""
        hits = self._scan("call 202-555-0147\n")
        self.assertTrue(any("手机" in why for _, why in hits))
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
