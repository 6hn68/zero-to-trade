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
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
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


class TestXlsxPrivacyScan(unittest.TestCase):
    """Route 04 (2026-11-24): .xlsx files are parsed as zip/XML now.
    Route 07 left them as plain text, so an address inside a
    spreadsheet was only caught if it happened to show up in the
    raw bytes -- a real email in sharedStrings.xml scanned clean.
    All fixtures are synthetic and fictional; phone digits are
    sequential patterns, domains are .example.
    .xlsx 按 zip/XML 解析的回归：上轮仍按文本读，表格里的地址
    未必扫得到。全部数据虚构，电话用顺序号段。"""

    def _scan_xlsx(self, shared_strings, rows, comments=None, threaded=None):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "probe.xlsx")
            _make_xlsx(path, shared_strings, rows,
                       comments=comments, threaded=threaded)
            return cpd.scan_file(path)

    def test_shared_string_email_flagged(self):
        """An email sitting in sharedStrings.xml must be caught.
        共享字符串里的邮箱必须被抓住。"""
        hits = self._scan_xlsx(
            ["Contact", "buyer@customer-mail.example"],
            [(1, [("A1", "s", 0), ("B1", "s", 1)])])
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_shared_string_phone_flagged(self):
        """A phone sitting in sharedStrings.xml must be caught.
        共享字符串里的电话必须被抓住。"""
        hits = self._scan_xlsx(
            ["phone", "+86 139 1234 5678"],
            [(1, [("A1", "s", 0), ("B1", "s", 1)])])
        self.assertTrue(any("手机" in why for _, why in hits))

    def test_inline_string_email_flagged(self):
        """An inline-string cell (no sharedStrings entry) is still
        an email. 内联字符串单元格里的邮箱也是泄漏。"""
        hits = self._scan_xlsx(
            [], [(2, [("A2", "inline", "buyer@customer-mail.example")])])
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_numeric_phone_cell_flagged(self):
        """A bare 11-digit number cell is a phone, not just a number.
        纯数字单元格里的 11 位号也是电话。"""
        hits = self._scan_xlsx(
            [], [(2, [("B2", "n", "13912345678")])])
        self.assertTrue(any("手机" in why for _, why in hits))

    def test_clean_xlsx_passes(self):
        """sample.example mail + placeholder phone stay clean.
        示例域名 + 占位电话的表格干净。"""
        hits = self._scan_xlsx(
            ["demo01@sample.example", "+000 00 000 0000"],
            [(1, [("A1", "s", 0), ("B1", "s", 1)])])
        self.assertEqual(hits, [])

    def test_example_marked_cell_exempt(self):
        """A cell marked 【示例】 is still exempt.
        标了【示例】的单元格仍豁免。"""
        hits = self._scan_xlsx(
            ["【示例】 buyer@customer-mail.example"],
            [(1, [("A1", "s", 0)])])
        self.assertEqual(hits, [])

    def test_xlsx_without_shared_strings(self):
        """A workbook with no sharedStrings.xml at all (inline
        strings only) must still be scanned, not crash.
        没有 sharedStrings.xml 的工作簿（只有内联字符串）也要
        扫得到，不能报错。"""
        hits = self._scan_xlsx(
            None, [(1, [("A1", "inline", "buyer@customer-mail.example")])])
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_unreferenced_shared_string_flagged(self):
        """A shared string no cell references must still be scanned
        -- a value hiding only in sharedStrings.xml cannot slip
        through. 没被任何单元格引用的共享字符串也要扫。"""
        hits = self._scan_xlsx(
            ["note", "buyer@customer-mail.example"],
            [(1, [("A1", "s", 0)])])
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_no_double_report(self):
        """A shared string referenced by one cell is reported once,
        not once for the cell and once for sharedStrings.xml.
        同一个值只报一次，不重复。"""
        hits = self._scan_xlsx(
            ["buyer@customer-mail.example"],
            [(1, [("A1", "s", 0)])])
        flagged = [h for h in hits if "customer-mail.example" in h[1]]
        self.assertEqual(len(flagged), 1)

    def test_subdomain_of_example_domain_clean(self):
        """info@mail.example.com in a cell stays clean, like in text.
        白名单子域名在单元格里也干净。"""
        hits = self._scan_xlsx(
            ["info@mail.example.com"],
            [(1, [("A1", "s", 0)])])
        self.assertEqual(hits, [])

    def test_corrupt_xlsx_falls_back_to_text(self):
        """A .xlsx that is not a zip at all falls back to the plain
        text scan instead of crashing or silently passing.
        根本不是 zip 的 .xlsx 回退到纯文本扫描，不报错、不放过。"""
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "probe.xlsx")
            Path(path).write_text(
                "contact buyer@customer-mail.example\n", encoding="utf-8")
            hits = cpd.scan_file(path)
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_comment_email_flagged(self):
        """Route 05 (2026-11-26): an email in a cell comment
        (xl/comments*.xml) must be caught -- it is not a cell value,
        so the worksheet scan never sees it.
        单元格批注里的邮箱必须被抓住（它不是单元格值，工作表扫描看不到）。"""
        hits = self._scan_xlsx(
            ["Contact"], [(1, [("A1", "s", 0)])],
            comments=[("B2", "Alex", "call buyer@customer-mail.example")])
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_comment_row_reported(self):
        """A comment's hit reports the row of the cell it is anchored
        to (ref="B2" -> row 2), not row 0.
        批注命中的行号是它挂的单元格的行号。"""
        hits = self._scan_xlsx(
            [], [], comments=[("B2", "Alex", "buyer@customer-mail.example")])
        flagged = [no for no, why in hits
                   if "customer-mail.example" in why]
        self.assertEqual(flagged, [2])

    def test_threaded_comment_phone_flagged(self):
        """Route 05 (2026-11-26): a phone in a threaded comment
        (xl/threadedComments/*.xml) must be caught too.
        threaded 批注里的电话也要抓住。"""
        hits = self._scan_xlsx(
            [], [], threaded=[("C3", "phone +86 139 1234 5678")])
        flagged = [no for no, why in hits if "手机" in why]
        self.assertEqual(flagged, [3])

    def test_comment_clean_passes(self):
        """sample.example mail in a comment stays clean, like in a cell.
        批注里的示例域名干净。"""
        hits = self._scan_xlsx(
            [], [], comments=[("B2", "Alex", "demo01@sample.example")])
        self.assertEqual(hits, [])

    def test_comment_example_marked_exempt(self):
        """A comment marked 【示例】 is still exempt.
        标了【示例】的批注仍豁免。"""
        hits = self._scan_xlsx(
            [], [],
            comments=[("B2", "Alex", "【示例】 buyer@customer-mail.example")])
        self.assertEqual(hits, [])

    def test_corrupt_xlsx_no_text_explicit_hit(self):
        """Route 05 (2026-11-26): a corrupt .xlsx with nothing
        visible in a text scan must NOT pass silently -- it reports
        an explicit whole-file warning instead.
        损坏又扫不出东西的 .xlsx 不能静默放过，要明确报请人工复核。"""
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "probe.xlsx")
            Path(path).write_bytes(b"\x00\x01\x02garbage, no text here\n")
            hits = cpd.scan_file(path)
        self.assertTrue(any("人工复核" in why for _, why in hits))


def _make_xlsx(path, shared_strings, rows, comments=None, threaded=None):
    """Build a minimal .xlsx with the stdlib only (zipfile).
    shared_strings is a list of strings (None omits
    xl/sharedStrings.xml); rows is a list of (row_no,
    [(ref, kind, value)]) with kind 's' (shared-string index),
    'inline' (inline string) or 'n' (plain number).
    comments is a list of (ref, author, text) written to
    xl/comments1.xml; threaded is a list of (ref, text) written to
    xl/threadedComments/threadedComment1.xml.
    只用标准库造一个最小 .xlsx；shared_strings 是字符串列表
    （None 表示不写 sharedStrings.xml），rows 是
    (行号, [(格子, 类型, 值)])，类型 s=共享字符串序号、
    inline=内联字符串、n=纯数字。comments 写进 xl/comments1.xml，
    threaded 写进 xl/threadedComments/threadedComment1.xml。"""
    def esc(s):
        return (s.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;"))

    parts = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
            '</Types>'),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>'),
        "xl/workbook.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>'),
        "xl/_rels/workbook.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
            '</Relationships>'),
    }
    if shared_strings is not None:
        items = "".join("<si><t>%s</t></si>" % esc(s)
                        for s in shared_strings)
        parts["xl/sharedStrings.xml"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'count="%d" uniqueCount="%d">%s</sst>'
            % (len(shared_strings), len(shared_strings), items))
    sheet_rows = []
    for row_no, cells in rows:
        rendered = []
        for ref, kind, value in cells:
            if kind == "s":
                rendered.append('<c r="%s" t="s"><v>%s</v></c>'
                                % (ref, value))
            elif kind == "inline":
                rendered.append('<c r="%s" t="inlineStr"><is><t>%s</t></is></c>'
                                % (ref, esc(value)))
            else:  # 'n'
                rendered.append('<c r="%s"><v>%s</v></c>' % (ref, value))
        sheet_rows.append('<row r="%d">%s</row>' % (row_no, "".join(rendered)))
    parts["xl/worksheets/sheet1.xml"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetData>%s</sheetData></worksheet>' % "".join(sheet_rows))
    if comments is not None:
        authors = sorted({a for _, a, _ in comments})
        items = "".join(
            '<comment ref="%s" authorId="%d"><text><t>%s</t></text></comment>'
            % (ref, authors.index(a), esc(t))
            for ref, a, t in comments)
        auth = "".join("<author>%s</author>" % esc(a) for a in authors)
        parts["xl/comments1.xml"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<comments xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            "<authors>%s</authors><commentList>%s</commentList></comments>"
            % (auth, items))
    if threaded is not None:
        items = "".join(
            '<threadedComment ref="%s"><text><t>%s</t></text></threadedComment>'
            % (ref, esc(t)) for ref, t in threaded)
        parts["xl/threadedComments/threadedComment1.xml"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<ThreadedComments xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            "%s</ThreadedComments>" % items)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in parts.items():
            zf.writestr(name, data)


def _biff_rec(opcode, data):
    """One BIFF record: opcode (2) + length (2) + payload."""
    return struct.pack("<HH", opcode, len(data)) + data


def _biff_bof(version=0x0600):
    """BOF: version 0x0600 = BIFF8, 0x0500 = BIFF5."""
    return _biff_rec(0x0809,
                     struct.pack("<HHHH", version, 0x0005, 0, 0) + b"\x00" * 8)


def _biff_eof():
    return _biff_rec(0x000A, b"")


def _biff_sst(strings):
    """SST record: total + unique counts, then each string as
    char-count (2) + flags (1, 0x01 = 16-bit) + UTF-16LE chars."""
    body = struct.pack("<II", len(strings), len(strings))
    for s in strings:
        body += struct.pack("<HB", len(s), 0x01) + s.encode("utf-16-le")
    return _biff_rec(0x00FC, body)


def _biff_labelsst(row, col, idx):
    return _biff_rec(0x00FD, struct.pack("<HHHI", row, col, 0, idx))


def _biff_label8(row, col, text):
    """BIFF8 LABEL: row + col + xf + char-count + flags + UTF-16LE."""
    raw = text.encode("utf-16-le")
    return _biff_rec(0x0204, struct.pack("<HHH", row, col, 0)
                     + struct.pack("<HB", len(text), 0x01) + raw)


def _biff_label5(row, col, text):
    """BIFF5 LABEL: row + col + xf + char-count + latin-1 bytes
    (no flags byte -- the BOF version decides the layout)."""
    raw = text.encode("latin-1")
    return _biff_rec(0x0204, struct.pack("<HHH", row, col, 0)
                     + struct.pack("<H", len(text)) + raw)


def _biff_number(row, col, value):
    return _biff_rec(0x0203, struct.pack("<HHH", row, col, 0)
                     + struct.pack("<d", value))


def _biff_note(row, col, author):
    """NOTE record: row + col + flags + author char-count + author."""
    raw = author.encode("latin-1")
    return _biff_rec(0x001C, struct.pack("<HHH", row, col, 0)
                     + struct.pack("<H", len(raw)) + raw)


def _biff_txo(text):
    """TXO record: grbit + rot + reserved + cchText + cbRuns +
    reserved + text bytes (latin-1 here; the scanner reads the
    payload's printable runs, either encoding)."""
    raw = text.encode("latin-1")
    return _biff_rec(0x01B6, struct.pack("<HH", 0, 0) + b"\x00" * 4
                     + struct.pack("<HH", len(text), 0) + b"\x00" * 4 + raw)


def _ole_dir_entry(name, obj_type, start, size, child=None):
    """One 128-byte OLE2 directory entry."""
    raw_name = name.encode("utf-16-le") + b"\x00\x00"
    raw_name = raw_name + b"\x00" * (64 - len(raw_name))
    return (raw_name
            + struct.pack("<H", len(name.encode("utf-16-le")) + 2)
            + bytes([obj_type, 0])
            + struct.pack("<III", 0xFFFFFFFF, 0xFFFFFFFF,
                          0xFFFFFFFF if child is None else child)
            + b"\x00" * 16
            + struct.pack("<I", 0)
            + b"\x00" * 16
            + struct.pack("<III", start, size, 0))


def _ole_header(first_dir=1, num_fat=1, first_minifat=0xFFFFFFFE,
                num_minifat=0):
    """A 512-byte OLE2 header for the layouts below."""
    header = bytearray(512)
    header[0:8] = bytes([0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1])
    struct.pack_into("<H", header, 24, 0x003E)  # minor version
    struct.pack_into("<H", header, 26, 3)       # major: 512-byte sectors
    struct.pack_into("<H", header, 28, 0xFFFE)  # byte order
    struct.pack_into("<H", header, 30, 9)       # sector shift: 512
    struct.pack_into("<H", header, 32, 6)       # mini sector shift: 64
    struct.pack_into("<I", header, 36, 1)       # num directory sectors
    struct.pack_into("<I", header, 40, num_fat)  # num FAT sectors
    struct.pack_into("<I", header, 44, first_dir)  # first dir sector
    struct.pack_into("<I", header, 52, 4096)    # mini stream cutoff
    struct.pack_into("<I", header, 56, first_minifat)
    struct.pack_into("<I", header, 60, num_minifat)
    struct.pack_into("<I", header, 64, 0xFFFFFFFE)  # first DIFAT: none
    struct.pack_into("<I", header, 68, 0)       # num DIFAT sectors
    struct.pack_into("<I", header, 72, 0)       # DIFAT[0]: FAT sector 0
    for i in range(1, 109):
        struct.pack_into("<I", header, 72 + 4 * i, 0xFFFFFFFF)
    return bytes(header)


def _make_xls_mini(path, stream):
    """Same minimal OLE2 .xls, but the Workbook stream is small
    (< 4096 bytes) so it legally lives in the mini stream: the root
    entry holds the mini stream, the MiniFAT chains its 64-byte
    mini sectors. Covers the scanner's MiniFAT path.
    Layout: sector 0 = FAT, 1 = directory, 2 = MiniFAT,
    sectors 3.. = the mini stream.
    小流版 .xls：Workbook 流 < 4096 字节，走 MiniFAT，覆盖扫描器的
    MiniFAT 分支。"""
    ss = 512
    mini = stream + b"\x00" * ((64 - len(stream) % 64) % 64)
    n_mini = len(mini) // 64
    n_mini_sectors = (len(mini) + ss - 1) // ss
    fat = [0xFFFFFFFF] * 128
    fat[0] = 0xFFFFFFFD
    fat[1] = 0xFFFFFFFE
    fat[2] = 0xFFFFFFFE
    for i in range(n_mini_sectors):
        s = 3 + i
        fat[s] = s + 1 if i + 1 < n_mini_sectors else 0xFFFFFFFE
    fat_sector = b"".join(struct.pack("<I", v) for v in fat)
    minifat = [0xFFFFFFFF] * 128
    for i in range(n_mini):
        minifat[i] = i + 1 if i + 1 < n_mini else 0xFFFFFFFE
    minifat_sector = b"".join(struct.pack("<I", v) for v in minifat)
    root = _ole_dir_entry("Root Entry", 5, 3, len(mini), child=1)
    book = _ole_dir_entry("Workbook", 2, 0, len(stream))
    directory = root + book + b"\x00" * (ss - 256)
    mini_stream = mini + b"\x00" * (n_mini_sectors * ss - len(mini))
    with open(path, "wb") as fh:
        fh.write(_ole_header(first_minifat=2, num_minifat=1))
        fh.write(fat_sector)
        fh.write(directory)
        fh.write(minifat_sector)
        fh.write(mini_stream)


def _make_xls(path, stream):
    """Build a minimal OLE2 .xls file (stdlib only) holding `stream`
    as the Workbook stream. The stream is padded to >= 4096 bytes
    so it goes through the regular FAT chain (no MiniFAT needed).
    Layout: sector 0 = FAT, sector 1 = directory (root + Workbook),
    sectors 2.. = the Workbook stream.
    只用标准库造一个最小 OLE2 .xls：stream 当 Workbook 流，补到
    4096 字节以上、走普通 FAT 链（不用 MiniFAT）。扇区 0=FAT、
    扇区 1=目录（根 + Workbook）、扇区 2 起是流数据。"""
    ss = 512
    n_sectors = max(8, (len(stream) + ss - 1) // ss)
    padded = stream + b"\x00" * (n_sectors * ss - len(stream))
    first_stream_sector = 2
    fat = [0xFFFFFFFF] * 128
    fat[0] = 0xFFFFFFFD  # this sector is a FAT sector
    fat[1] = 0xFFFFFFFE  # directory: single sector, end of chain
    for i in range(n_sectors):
        s = first_stream_sector + i
        fat[s] = s + 1 if i + 1 < n_sectors else 0xFFFFFFFE
    fat_sector = b"".join(struct.pack("<I", v) for v in fat)

    root = _ole_dir_entry("Root Entry", 5, 0xFFFFFFFE, 0, child=1)
    # NOTE: the entry size is the padded length (>= 4096), so the
    # stream goes through the regular FAT chain, not the MiniFAT.
    # (An entry smaller than the 4096 mini-stream cutoff would
    # legally belong in the mini stream instead.)
    book = _ole_dir_entry("Workbook", 2, first_stream_sector, len(padded))
    directory = root + book + b"\x00" * (ss - 256)
    header = bytearray(512)
    header[0:8] = bytes([0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1])
    struct.pack_into("<H", header, 24, 0x003E)  # minor version
    struct.pack_into("<H", header, 26, 3)       # major: 512-byte sectors
    struct.pack_into("<H", header, 28, 0xFFFE)  # byte order
    struct.pack_into("<H", header, 30, 9)       # sector shift: 512
    struct.pack_into("<H", header, 32, 6)       # mini sector shift: 64
    struct.pack_into("<I", header, 36, 1)       # num directory sectors
    struct.pack_into("<I", header, 40, 1)       # num FAT sectors
    struct.pack_into("<I", header, 44, 1)       # first directory sector
    struct.pack_into("<I", header, 52, 4096)    # mini stream cutoff
    struct.pack_into("<I", header, 56, 0xFFFFFFFE)  # first MiniFAT: none
    struct.pack_into("<I", header, 60, 0)       # num MiniFAT sectors
    struct.pack_into("<I", header, 64, 0xFFFFFFFE)  # first DIFAT: none
    struct.pack_into("<I", header, 68, 0)       # num DIFAT sectors
    struct.pack_into("<I", header, 72, 0)       # DIFAT[0]: FAT sector 0
    for i in range(1, 109):
        struct.pack_into("<I", header, 72 + 4 * i, 0xFFFFFFFF)
    with open(path, "wb") as fh:
        fh.write(bytes(header))
        fh.write(fat_sector)
        fh.write(directory)
        fh.write(padded)


class TestXlsPrivacyScan(unittest.TestCase):
    """Route 05 (2026-11-26): .xls files are parsed as OLE2/BIFF now.
    Route 04 left them as plain text, so a real address inside a
    binary .xls scanned clean unless it happened to show up in the
    raw bytes. All fixtures are synthetic and fictional; phone
    digits are sequential patterns, domains are .example.
    .xls 按 OLE2/BIFF 解析的回归：上轮仍按文本读，二进制表格里
    的地址扫不到。全部数据虚构，电话用顺序号段。"""

    def _scan_xls(self, stream_bytes):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "probe.xls")
            _make_xls(path, stream_bytes)
            return cpd.scan_file(path)

    def test_labelsst_email_flagged(self):
        """An email in SST, referenced by a LABELSST cell, is caught.
        SST 里的邮箱、被单元格引用，必须被抓住。"""
        hits = self._scan_xls(
            _biff_bof() + _biff_sst(["buyer@customer-mail.example"])
            + _biff_labelsst(0, 0, 0) + _biff_eof())
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_mini_stream_labelsst_flagged(self):
        """A small Workbook stream (< 4096 bytes) legally lives in
        the mini stream -- the MiniFAT path must find it too.
        小 Workbook 流走 MiniFAT，也要扫得到。"""
        stream = (_biff_bof()
                  + _biff_sst(["buyer@customer-mail.example"])
                  + _biff_labelsst(0, 0, 0) + _biff_eof())
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "probe.xls")
            _make_xls_mini(path, stream)
            hits = cpd.scan_file(path)
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_sst_unreferenced_flagged(self):
        """A shared string no cell references is still scanned.
        没被任何单元格引用的共享字符串也要扫。"""
        hits = self._scan_xls(
            _biff_bof() + _biff_sst(["buyer@customer-mail.example"])
            + _biff_eof())
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_label8_phone_flagged(self):
        """A BIFF8 LABEL cell holding a phone number is caught.
        BIFF8 LABEL 单元格里的电话必须被抓住。"""
        hits = self._scan_xls(
            _biff_bof() + _biff_label8(1, 0, "+86 139 1234 5678")
            + _biff_eof())
        self.assertTrue(any("手机" in why for _, why in hits))

    def test_label5_email_flagged(self):
        """A BIFF5 LABEL cell (no flags byte, latin-1) is caught too
        -- the BOF version decides the layout.
        BIFF5 LABEL（无标志位、latin-1）也要抓住。"""
        hits = self._scan_xls(
            _biff_bof(0x0500)
            + _biff_label5(0, 0, "buyer@customer-mail.example")
            + _biff_eof())
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_number_phone_flagged(self):
        """A bare 11-digit NUMBER cell is a phone, not just a number
        (same rule as the .xlsx numeric cell).
        纯数字 NUMBER 单元格里的 11 位号也是电话。"""
        hits = self._scan_xls(
            _biff_bof() + _biff_number(1, 1, 13912345678.0) + _biff_eof())
        self.assertTrue(any("手机" in why for _, why in hits))

    def test_comment_text_txo_flagged(self):
        """Comment text in a TXO record is caught -- a comment is
        not a cell value, so the cell scan never sees it.
        TXO 批注文本里的邮箱必须被抓住。"""
        hits = self._scan_xls(
            _biff_bof()
            + _biff_txo("call buyer@customer-mail.example")
            + _biff_eof())
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_comment_author_note_flagged(self):
        """A NOTE record's author holding an email is caught.
        NOTE 批注作者里的邮箱也要抓住。"""
        hits = self._scan_xls(
            _biff_bof()
            + _biff_note(2, 2, "buyer@customer-mail.example")
            + _biff_eof())
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_no_double_report(self):
        """An email reached through LABELSST is reported once, not
        once for the cell and once for the raw-byte sweep.
        同一个值只报一次，不重复。"""
        hits = self._scan_xls(
            _biff_bof() + _biff_sst(["buyer@customer-mail.example"])
            + _biff_labelsst(0, 0, 0) + _biff_eof())
        flagged = [h for h in hits if "customer-mail.example" in h[1]]
        self.assertEqual(len(flagged), 1)

    def test_clean_xls_passes(self):
        """sample.example mail + placeholder phone stay clean.
        示例域名 + 占位电话的表格干净。"""
        hits = self._scan_xls(
            _biff_bof()
            + _biff_sst(["demo01@sample.example", "+000 00 000 0000"])
            + _biff_labelsst(0, 0, 0) + _biff_labelsst(0, 1, 1)
            + _biff_eof())
        self.assertEqual(hits, [])

    def test_empty_xls_clean(self):
        """An empty .xls file scans clean, no crash.
        空 .xls 文件干净、不报错。"""
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "probe.xls")
            Path(path).write_bytes(b"")
            self.assertEqual(cpd.scan_file(path), [])

    def test_corrupt_xls_not_silently_passed(self):
        """A non-empty .xls that is not OLE2 at all must NOT pass
        silently -- it reports an explicit whole-file warning.
        根本不是 OLE2 的 .xls 不能静默放过，要明确报请人工复核。"""
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "probe.xls")
            Path(path).write_bytes(
                b"this is not an ole file, nothing sensitive here\n")
            hits = cpd.scan_file(path)
        self.assertTrue(any("人工复核" in why for _, why in hits))

    def test_corrupt_xls_text_fallback(self):
        """A .xls that is really a text file still gets its visible
        email caught by the text fallback.
        改名成 .xls 的文本文件，里面的邮箱仍被文本回退抓住。"""
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "probe.xls")
            Path(path).write_text(
                "contact buyer@customer-mail.example\n", encoding="utf-8")
            hits = cpd.scan_file(path)
        self.assertTrue(any("customer-mail.example" in why
                            for _, why in hits))

    def test_truncated_ole_not_silently_passed(self):
        """A .xls with a valid OLE2 signature but a broken body
        (truncated file) is reported, not passed.
        签名对但正文截断的 .xls 也要报出来，不能放过。"""
        with tempfile.TemporaryDirectory() as d:
            good = str(Path(d) / "good.xls")
            _make_xls(good, _biff_bof() + _biff_eof())
            raw = Path(good).read_bytes()[:600]
            path = str(Path(d) / "probe.xls")
            Path(path).write_bytes(raw)
            hits = cpd.scan_file(path)
        self.assertTrue(any("人工复核" in why for _, why in hits))

    def test_encrypted_xls_flagged(self):
        """A FILEPASS (encrypted) workbook cannot be read -- it is
        reported as encrypted, not passed.
        加密工作簿读不出来，要报“已加密”，不能放过。"""
        stream = (_biff_bof()
                  + _biff_rec(0x002F, struct.pack("<H", 1) + b"\x00" * 4)
                  + _biff_eof())
        hits = self._scan_xls(stream)
        self.assertTrue(any("加密" in why for _, why in hits))


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
