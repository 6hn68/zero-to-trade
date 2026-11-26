#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提交前自查：扫一遍你要提交的东西里有没有真实客户数据。

为什么需要这个：
    `.gitignore` 只对「还没被 git 记住」的文件有效。
    `examples/leads_example.csv` 是仓库自带的，早就被 git 记住了——
    你往里面填真客户，再一个 `git add -A + git commit`，它就上去了，
    .gitignore 一声不吭。这个脚本就是补那个洞。

用法（在你打算提交之前）：
    python scripts/check_private_data.py

有真数据就打印文件名和第几行，并退出码1（挡住提交）。
干净就打印一行「没查到真实客户数据」，退出码 0。

`.xlsx` 按 zip/XML 解析（共享字符串 + 工作表单元格 + 单元格批注），
不是按文本读——表格里的邮箱/电话也能扫到。`.xls` 是 OLE2 二进制
格式，也用标准库解析：先读复合文件里的 Workbook 流，再走 BIFF
记录（共享字符串、单元格字符串、数字、批注作者 NOTE、批注文本
TXO），外加全流可打印字符串兜底扫。解析不了的表格（损坏、加密、
改名）不静默放过：先回退纯文本扫，没扫到就明确报“请人工复核”。
没扫到的部分：批注文本只从 TXO 记录体里抽字符串，没做完整 MSO
图形对象解析，极个别特殊编码的批注可能漏网——兜底扫是补网，
不是保证；加密工作簿（FILEPASS）读不出内容，直接报，不放过。

零依赖，跟仓库里其他脚本一个规矩。
"""
from __future__ import print_function

import argparse
import os
import re
import string
import sys
import xml.etree.ElementTree as ET
import zipfile

# Allowed email domains: RFC 2606 reserved domains + the example domain
# this project agreed on. Subdomains of these count as allowed too
# (mail.example.com is still an example address).
# 允许出现的邮箱域名：RFC 2606 保留域名 + 本项目约定的示例域名；
# 这些域名的子域名也算允许（mail.example.com 仍是示例地址）。
OK_DOMAINS = {
    "sample.example", "example.com", "example.org", "example.net",
    "localhost", "test", "invalid",
}

# NOTE (why no EMAIL regex here): a pattern like
# `[A-Za-z0-9._%+-]+@...` backtracks quadratically on one very long
# line with no "@" (a minified blob, a base64 dump) -- the scan hangs
# instead of finishing. Email addresses are found with a linear walk
# in _find_email_domains() below, so a 100k-char line stays fast.
# 注意：这里故意不用 EMAIL 正则——`[...]+@` 在超长行上会平方级回溯，
# 扫描直接挂住；下面 _find_email_domains() 用线性走查，10 万字符的行也很快。

# A phone-looking digit run: 9-15 digits, separators may be space, dash
# or dot (a dotted mobile still counts). An IPv4 address has the
# same shape, so it is filtered out separately.
# 看着像电话的数字串：9–15 位数字，分隔符可以是空格、横杠或点
# （带点的手机号也算）；IPv4 地址形状一样，另外单独排除。
PHONE = re.compile(r"(?<!\d)(?:\+?\d{1,3}[\s\-.]?)?(?:\d[\s\-.]?){8,13}\d(?!\d)")
_DIGIT = re.compile(r"\d")
_IPV4 = re.compile(r"\d{1,3}(?:\.\d{1,3}){3}")
# A digit run that is really a date plus a time: the phone pattern
# would happily eat the date and the first bit of the time as one
# long number. Skip matches that start like a date, in either order,
# and compact YYYYMMDD digit runs too.
# 看着像日期加时间的数字串：电话 pattern 会把日期和时间开头
# 当成一个长号码吃掉。日期形状的开头直接跳过，
# 紧凑的 YYYYMMDD 数字串也一样。
_DATE_LIKE = re.compile(
    r"^(?:\d{4}[-./]\d{1,2}[-./]\d{1,2}|\d{1,2}[-./]\d{1,2}[-./]\d{4})")
_COMPACT_DATE = re.compile(r"20\d\d(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])")

# Full-width characters that sneak in when contact lines are pasted
# from chat apps: full-width digits, @, dot, brackets, plus/minus,
# ideographic space. They are translated to ASCII before scanning.
# 从聊天软件粘贴联系方式时常带的全角字符：全角数字、@、点、括号、
# 加减号、全角空格，扫描前先转成半角。
_FULLWIDTH = str.maketrans({
    "０": "0", "１": "1", "２": "2", "３": "3", "４": "4",
    "５": "5", "６": "6", "７": "7", "８": "8", "９": "9",
    "＠": "@", "．": ".", "　": " ",
    "（": "(", "）": ")", "＋": "+", "－": "-",
})

# Obfuscated spellings people use to dodge scrapers -- still a real
# address, so normalise them before scanning: [at] / (at) / {at} -> @,
# [dot] / (dot) / {dot} -> ., and spaces around @ and dots are dropped.
# 为躲爬虫写的变形写法仍是真地址，扫描前先还原：[at]/(at)/{at} -> @、
# [dot]/(dot)/{dot} -> .，@ 和点前后的空格去掉。
_AT_WORD = re.compile(r"\s*[\[({]at[\])}]\s*", re.IGNORECASE)
_DOT_WORD = re.compile(r"\s*[\[({]dot[\])}]\s*", re.IGNORECASE)
_AT_SPACE = re.compile(r"\s*@\s*")
_DOT_SPACE = re.compile(r"(?<=[A-Za-z0-9])\s*\.\s*(?=[A-Za-z0-9])")

# Characters allowed in the local part of an email address.
# (Built from string.digits so the source line itself does not
# contain a 10-digit run that looks like a phone number.)
# 邮箱 @ 前面本地部分允许的字符。（用 string.digits 拼，
# 免得源码行里出现 10 位连号、被自己当成电话。)
_EMAIL_LOCAL_CHARS = set(string.ascii_letters + string.digits + "._%+-")
_DOMAIN_SHAPE = re.compile(r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# Lines explicitly marked as an example are exempt -- the whole line is
# a placeholder, not a leak. Weak hints ("fake", "dummy", "test@" ...)
# used to exempt the whole line too, which hid real data sitting on
# the same line (e.g. a real phone next to "test@sample"); they no
# longer skip anything -- the domain allow-list and the per-number
# placeholder check below are the only exemptions now.
# 只有明确标了示例的行才豁免——整行是占位符，不是泄漏。以前 "fake"、
# "dummy"、"test@" 这类弱提示也会豁免整行，结果同一行里的真数据
# （比如 test@sample 旁边的真电话）也被藏住了；现在弱提示不再豁免任何
# 东西，只有域名白名单和下面按号码算的占位判断才豁免。
EXAMPLE_MARKERS = ("【示例】", "[示例]", "占位", "placeholder")

SCAN_EXT = (
    ".md", ".csv", ".txt", ".json", ".html", ".py", ".yml", ".yaml",
    ".tsv", ".xlsx", ".xls",
)
SKIP_DIR = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def _normalize(line):
    """Normalise a line for scanning only (line numbers are untouched):
    full-width chars -> ASCII, [at]/[dot] spellings -> @ / .,
    spaces around @ and dots dropped, so a spaced-out address
    is seen as the address it is.
    只为扫描做归一化（行号不动）：全角转半角、[at]/[dot] 还原成 @ / .、
    @ 和点前后的空格去掉，这样带空格的邮箱也会被认出来。"""
    line = line.translate(_FULLWIDTH)
    line = _AT_WORD.sub("@", line)
    line = _DOT_WORD.sub(".", line)
    line = _AT_SPACE.sub("@", line)
    line = _DOT_SPACE.sub(".", line)
    return line


def _find_email_domains(line):
    """Linear scan for email domains in a line (no regex backtracking):
    for each "@", walk back over the local part and forward over the
    domain, and keep the domain if it looks like a real one.
    线性走查一行里的邮箱域名（不用正则、不回溯）：每个 @ 往前走本地部分、
    往后走域名，域名像真的就留下。"""
    domains = []
    start = 0
    while True:
        at = line.find("@", start)
        if at < 0:
            break
        i = at - 1
        while i >= 0 and line[i] in _EMAIL_LOCAL_CHARS:
            i -= 1
        local = line[i + 1:at]
        j = at + 1
        while j < len(line) and (line[j].isalnum() or line[j] in ".-"):
            j += 1
        domain = line[at + 1:j].rstrip(".")
        if local and _DOMAIN_SHAPE.fullmatch(domain or ""):
            domains.append(domain)
        start = at + 1
    return domains


def _is_ok_domain(domain):
    """An allowed domain, or a subdomain of one (mail.example.com)."""
    d = domain.lower()
    return d in OK_DOMAINS or any(
        d.endswith("." + ok) for ok in OK_DOMAINS)


def _is_placeholder_number(digits):
    """Is this digit run a placeholder, not a real number?
    All the same digit (+000 00 000 0000), or mostly zeros.
    A real number that happens to contain a 000 group is only
    about a third zeros, so it is NOT a placeholder -- the old
    line-level check wrongly let it through because it saw
    "000" anywhere on the line.
    这串数字是不是占位符：全是同一个数字（+000 00 000 0000），或
    大半是 0。真号里带个 000 组只占三分之一左右，不算占位——
    旧的行级检查因为行里出现 "000" 就放过，是错的。"""
    if len(set(digits)) <= 1:
        return True
    return digits.count("0") * 10 >= len(digits) * 6


def looks_like_real_phone(line):
    """这行里的号码是不是看着像真电话（不是 +000 00 000 0000 这种占位）。

    Is a number on this line a real-looking phone, not a placeholder?
    Each candidate is judged on its own digits (see
    _is_placeholder_number); an IPv4 address is not a phone.
    每个候选号码按自己的数字单独判断（见 _is_placeholder_number）；
    IPv4 地址不是电话。"""
    if not _DIGIT.search(line):
        return False
    for m in PHONE.finditer(line):
        text = m.group()
        if _IPV4.fullmatch(text):
            continue
        if _DATE_LIKE.match(text):
            continue
        digits = re.sub(r"\D", "", text)
        if len(digits) < 9:
            continue
        if _COMPACT_DATE.match(digits):
            continue
        if _is_placeholder_number(digits):
            continue
        return True
    return False


def _local(tag):
    """Tag name without its XML namespace ({...}sheet -> sheet).
    去掉 XML 标签的命名空间前缀。"""
    return tag.rsplit("}", 1)[-1]


def _ref_row(ref):
    """Cell ref ("B2", "AA12") -> 1-based row number; 0 if unparsable.
    单元格引用转行号，解析不出记 0。"""
    m = re.match(r"^[A-Za-z]+(\d+)", ref or "")
    return int(m.group(1)) if m else 0


def _xlsx_text_parts(path):
    """Extract scannable text from an .xlsx file (stdlib zipfile + XML):
    every worksheet cell (shared strings resolved, inline strings and
    plain numbers kept as-is), plus any shared string no scanned cell
    references, so a value hiding only in sharedStrings.xml cannot
    slip through. Returns a list of (part, row, text); row is the
    sheet row number, or the shared-string index for unreferenced
    strings. Returns None if the file is not a readable zip at all
    (corrupt or misnamed -- the caller falls back to a plain-text scan).
    从 .xlsx 里抽出可扫描的文本（标准库 zipfile + XML）：每个工作表
    单元格（共享字符串已还原、内联字符串和纯数字原样保留），外加
    没被任何单元格引用的共享字符串——只藏在 sharedStrings.xml 里
    的值也跑不掉。返回 [(部位, 行号, 文本)]；文件根本不是 zip
    就返回 None（调用方回退到纯文本扫描）。"""
    try:
        zf = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError, IOError):
        return None
    shared = []
    parts = []
    used = set()
    try:
        try:
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root:
                shared.append("".join(
                    t.text or "" for t in si.iter()
                    if _local(t.tag) == "t"))
        except (KeyError, ET.ParseError):
            shared = []
        for name in sorted(zf.namelist()):
            if not (name.startswith("xl/worksheets/")
                    and name.endswith(".xml")):
                continue
            try:
                root = ET.fromstring(zf.read(name))
            except (ET.ParseError, zipfile.BadZipFile, KeyError):
                continue
            seq = 0
            for row in root.iter():
                if _local(row.tag) != "row":
                    continue
                seq += 1
                r = row.get("r") or ""
                row_no = int(r) if r.isdigit() else seq
                for cell in row:
                    if _local(cell.tag) != "c":
                        continue
                    ctype = cell.get("t")
                    value = None
                    for child in cell:
                        tag = _local(child.tag)
                        if tag == "v":
                            value = child.text or ""
                        elif tag == "is":
                            value = "".join(
                                x.text or "" for x in child.iter()
                                if _local(x.tag) == "t")
                    if value is None:
                        continue
                    if ctype == "s":
                        try:
                            idx = int(value)
                        except ValueError:
                            continue
                        used.add(idx)
                        if 0 <= idx < len(shared):
                            value = shared[idx]
                        else:
                            continue
                    parts.append((name, row_no, value))
        # Cell comments (xl/comments*.xml) and threaded comments
        # (xl/threadedComments/*.xml): the note text and the author
        # names. A comment is not a cell, so the row is the cell the
        # comment is anchored to (from its ref="B2"); authors have
        # no cell and report row 0. xl/persons/person.xml holds the
        # display names threaded comments point at -- scanned too.
        # 单元格批注和 threaded 批注：批注文本和作者名也扫；行号取
        # 批注挂的单元格，作者没有单元格、行号记 0。
        for name in sorted(zf.namelist()):
            if not (name.endswith(".xml") and (
                    name.startswith("xl/comments") or
                    name.startswith("xl/threadedComments/") or
                    name == "xl/persons/person.xml")):
                continue
            try:
                root = ET.fromstring(zf.read(name))
            except (ET.ParseError, zipfile.BadZipFile, KeyError):
                continue
            for el in root.iter():
                tag = _local(el.tag)
                if tag in ("author", "displayName"):
                    if el.text:
                        parts.append((name, 0, el.text))
                elif tag in ("comment", "threadedComment"):
                    text = "".join(
                        t.text or "" for t in el.iter()
                        if _local(t.tag) == "t")
                    if text:
                        parts.append((name, _ref_row(el.get("ref")), text))
        # Shared strings never referenced by a scanned cell are still
        # scanned on their own; referenced ones are skipped here so
        # the same value is not reported twice.
        # 没被任何单元格引用的共享字符串单独再扫一遍；已被引用的
        # 在上面扫过，这里跳过，免得同一个值报两次。
        for i, text in enumerate(shared):
            if i not in used:
                parts.append(("xl/sharedStrings.xml", i + 1, text))
    finally:
        zf.close()
    return parts


def _scan_parts(parts):
    """Run the email/phone checks over [(part, row, text)] -- the
    same checks as the text scan, with the part name attached to
    each hit so the report says where the value hid.
    对 [(部位, 行号, 文本)] 跑同一套邮箱/电话检查，命中里带部位名。"""
    hits = []
    for part, no, text in parts:
        low = text.lower()
        if any(h in text for h in ("【示例】", "[示例]")) or \
           any(h in low for h in ("占位", "placeholder")):
            continue
        norm = _normalize(text)

        for domain in _find_email_domains(norm):
            if not _is_ok_domain(domain):
                hits.append((no, "邮箱域名 %s（不是保留域名，像是真人邮箱）[%s]"
                             % (domain, part)))
                break

        if looks_like_real_phone(norm):
            hits.append((no, "手机号/座机号（看着像真号码）[%s]" % part))
    return hits


def _scan_xlsx(path):
    """Scan an .xlsx file cell by cell, with the same email/phone
    checks as the text scan. Returns [(row number, why)] -- the row
    number is the sheet row for cells, or the shared-string index
    for unreferenced shared strings. Returns None if the file is
    not a readable zip (the caller falls back to a text scan, then
    to an explicit warning).
    按单元格扫 .xlsx，邮箱/电话检查和文本扫描同一套；返回
    [(行号, 原因)]。文件不是合法 zip 就返回 None（调用方回退）。"""
    parts = _xlsx_text_parts(path)
    if parts is None:
        return None
    return _scan_parts(parts)


# ---------------------------------------------------------------------------
# .xls (OLE2 / BIFF) -- stdlib only, and no new imports at all: every
# integer is read with int.from_bytes, so ci.yml's ALLOWED list needs
# no new entry (no struct, no extra module).
# .xls（OLE2 / BIFF）——只用标准库，而且一个新 import 都没加：
# 整数全用 int.from_bytes 读，ci.yml 白名单不用动。
# ---------------------------------------------------------------------------

_OLE_SIGNATURE = bytes([0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1])
_ENDOFCHAIN = 0xFFFFFFFE
_FREESECT = 0xFFFFFFFF


def _u16(data, off):
    return int.from_bytes(data[off:off + 2], "little")


def _u32(data, off):
    return int.from_bytes(data[off:off + 4], "little")


def _ieee754_double(raw8):
    """Decode 8 little-endian bytes as an IEEE 754 double, without
    struct (not in ci.yml's ALLOWED list -- int.from_bytes is enough).
    8 字节小端解成双精度浮点，不用 struct（它不在 ci 白名单里）。"""
    bits = int.from_bytes(raw8, "little")
    sign = -1.0 if bits >> 63 else 1.0
    exp = (bits >> 52) & 0x7FF
    mant = bits & ((1 << 52) - 1)
    if exp == 0:
        if mant == 0:
            return 0.0
        return sign * mant * 2.0 ** -1074
    if exp == 0x7FF:
        if mant == 0:
            return sign * float("inf")
        return float("nan")
    return sign * (1.0 + mant / 2.0 ** 52) * 2.0 ** (exp - 1023)


def _rk_value(raw4):
    """Decode a BIFF RK value (a 4-byte packed number) to float.
    RK 是 BIFF 里 4 字节打包的数字，解成浮点。"""
    v = int.from_bytes(raw4, "little")
    if v & 2:
        n = v >> 2
        if n & (1 << 29):
            n -= 1 << 30
        num = float(n)
    else:
        num = _ieee754_double(((v & 0xFFFFFFFC) << 32).to_bytes(8, "little"))
    if v & 1:
        num /= 100.0
    return num


def _format_number(num):
    """A cell number as scannable text: a whole number stored as a
    float prints with a trailing .0 -- drop it, so the phone check
    sees the digits it would see in the sheet.
    单元格数字转成可扫描文本：整数去掉 .0，电话检查才能认出来。"""
    if num != num or num in (float("inf"), float("-inf")):
        return ""
    if num == int(num) and abs(num) < 10 ** 16:
        return str(int(num))
    return repr(num)


def _cfb_read_stream(data):
    """Read the Workbook/Book stream out of an OLE2 compound file
    (the .xls container), stdlib only. Returns (bytes, None) on
    success, or (None, reason) with reason in "not-ole" (not an
    OLE2 file at all), "damaged" (signature OK but FAT/directory
    broken) or "no-workbook" (OLE2 file, no Workbook/Book stream).
    只用标准库读 OLE2 复合文件里的 Workbook 流。"""
    if len(data) < 512 or data[:8] != _OLE_SIGNATURE:
        return None, "not-ole"
    try:
        sector_shift = _u16(data, 30)
        if sector_shift not in (9, 12):
            return None, "damaged"
        if _u16(data, 32) != 6:
            return None, "damaged"
        ss = 1 << sector_shift
        num_fat = _u32(data, 40)
        first_dir = _u32(data, 44)
        mini_cutoff = _u32(data, 52)
        first_minifat = _u32(data, 56)
        num_minifat = _u32(data, 60)
        first_difat = _u32(data, 64)
        num_difat = _u32(data, 68)

        def sector(n):
            start = (n + 1) * ss
            if n < 0 or start + ss > len(data):
                return None
            return data[start:start + ss]

        # DIFAT: 109 entries in the header, then DIFAT sectors chained
        # through their last slot.
        difat = [_u32(data, 72 + 4 * i) for i in range(109)]
        difat = [d for d in difat if d != _FREESECT]
        nxt = first_difat
        guard = 0
        while nxt != _ENDOFCHAIN and nxt != _FREESECT \
                and guard <= num_difat + 1:
            guard += 1
            sec = sector(nxt)
            if sec is None:
                return None, "damaged"
            per = ss // 4
            difat.extend(_u32(sec, 4 * i) for i in range(per - 1))
            nxt = _u32(sec, 4 * (per - 1))
        difat = [d for d in difat if d != _FREESECT]

        fat = []
        for fsec in difat:
            sec = sector(fsec)
            if sec is None:
                return None, "damaged"
            fat.extend(_u32(sec, 4 * i) for i in range(ss // 4))
        if len(fat) < num_fat:
            return None, "damaged"

        def chain(start):
            out = []
            seen = set()
            cur = start
            while cur != _ENDOFCHAIN and cur != _FREESECT:
                if cur in seen or cur >= len(fat):
                    return None
                seen.add(cur)
                out.append(cur)
                cur = fat[cur]
            return out

        def read_chain(start, size):
            secs = chain(start)
            if secs is None:
                return None
            buf = bytearray()
            for s in secs:
                sec = sector(s)
                if sec is None:
                    return None
                buf += sec
            if len(buf) < size:
                return None
            return bytes(buf[:size])

        dir_secs = chain(first_dir)
        if dir_secs is None:
            return None, "damaged"
        directory = bytearray()
        for s in dir_secs:
            sec = sector(s)
            if sec is None:
                return None, "damaged"
            directory += sec
        entries = []
        for off in range(0, len(directory) - 127, 128):
            ent = directory[off:off + 128]
            name_len = _u16(ent, 64)
            if name_len < 2 or name_len > 64:
                name = ""
            else:
                name = ent[:name_len - 2].decode("utf-16-le", "replace")
            entries.append({
                "name": name,
                "type": ent[66],
                "start": _u32(ent, 116),
                "size": _u32(ent, 120),
            })
        if not entries:
            return None, "damaged"
        root = None
        target = None
        for ent in entries:
            if ent["type"] == 5 and root is None:
                root = ent
            if ent["type"] == 2 and ent["name"].lower() in ("workbook", "book"):
                target = ent
        if target is None:
            return None, "no-workbook"
        if root is None:
            return None, "damaged"

        size = target["size"]
        if size >= mini_cutoff:
            blob = read_chain(target["start"], size)
            if blob is None:
                return None, "damaged"
            return blob, None
        # Small stream: lives inside the root entry's mini stream,
        # addressed through the MiniFAT (64-byte mini sectors).
        if root["start"] in (_ENDOFCHAIN, _FREESECT):
            return None, "damaged"
        mini_stream = read_chain(root["start"], root["size"])
        if mini_stream is None:
            return None, "damaged"
        minifat = []
        secs = chain(first_minifat)
        if secs is None:
            return None, "damaged"
        for s in secs:
            sec = sector(s)
            if sec is None:
                return None, "damaged"
            minifat.extend(_u32(sec, 4 * i) for i in range(ss // 4))
        out = bytearray()
        cur = target["start"]
        seen = set()
        while cur != _ENDOFCHAIN and cur != _FREESECT:
            if cur in seen or cur >= len(minifat):
                return None, "damaged"
            seen.add(cur)
            start = cur * 64
            out += mini_stream[start:start + 64]
            cur = minifat[cur]
        if len(out) < size:
            return None, "damaged"
        return bytes(out[:size]), None
    except (IndexError, ValueError, OverflowError):
        return None, "damaged"


def _string_runs(payload):
    """Printable string runs inside a raw BIFF payload, both
    encodings: plain ASCII runs and UTF-16LE runs (every second byte
    0x00). Yields each run of >= 4 characters. Used for NOTE authors
    and TXO comment text, where the exact field layout varies
    between BIFF versions -- the runs are the text, whatever wraps
    them -- and as the safety-net sweep over the whole stream.
    从原始记录体里抽可打印字符串：ASCII 和 UTF-16LE 两种，>=4 字符。"""
    runs = []
    buf = []
    for b in payload:
        if 0x20 <= b <= 0x7E:
            buf.append(chr(b))
        else:
            if len(buf) >= 4:
                runs.append("".join(buf))
            buf = []
    if len(buf) >= 4:
        runs.append("".join(buf))
    buf = []
    i = 0
    while i + 1 < len(payload):
        b, z = payload[i], payload[i + 1]
        if z == 0 and 0x20 <= b <= 0x7E:
            buf.append(chr(b))
            i += 2
        else:
            if len(buf) >= 4:
                runs.append("".join(buf))
            buf = []
            i += 1
    if len(buf) >= 4:
        runs.append("".join(buf))
    return runs


class _SegReader(object):
    """Cursor over an SST record plus its CONTINUE segments.
    Reads across segment boundaries; when a string's character data
    is split across a CONTINUE, the new segment starts with a flag
    byte (bit 0 = 16-bit chars) that is skipped, not data.
    SST 记录 + CONTINUE 段上的游标：字符串被 CONTINUE 截断时，
    新段开头 1 字节是标志位，不是数据。"""

    def __init__(self, segments):
        self.segs = [s for s in segments if s]
        self.i = 0
        self.off = 0

    def _skip_empty(self):
        while self.i < len(self.segs) and self.off >= len(self.segs[self.i]):
            self.i += 1
            self.off = 0

    def has_data(self):
        self._skip_empty()
        return self.i < len(self.segs)

    def read(self, n):
        """Read n bytes across segments (no flag-byte handling:
        use only for record headers / run data, never for string
        characters)."""
        out = bytearray()
        while len(out) < n and self.has_data():
            seg = self.segs[self.i]
            take = min(n - len(out), len(seg) - self.off)
            out += seg[self.off:self.off + take]
            self.off += take
        return bytes(out)

    def read_chars(self, count, is_unicode):
        """Read `count` characters of a split-able SST string.
        The encoding may flip at a CONTINUE boundary; the flag byte
        there says which. Returns the text."""
        out = []
        remaining = count
        while remaining > 0:
            if not self.has_data():
                break
            seg = self.segs[self.i]
            avail = len(seg) - self.off
            bpc = 2 if is_unicode else 1
            n = min(remaining, avail // bpc)
            if n == 0:
                # A lone trailing byte (a 2-byte char split across
                # records -- not valid BIFF): stop, keep what we have.
                break
            raw = self.read(n * bpc)
            if is_unicode:
                out.append(raw.decode("utf-16-le", "replace"))
            else:
                out.append(raw.decode("latin-1"))
            remaining -= n
            if remaining > 0:
                cur = self.i
                if self.has_data() and self.i != cur:
                    # Entered a CONTINUE segment mid-string: its
                    # first byte is the continuation flag byte.
                    flag = self.read(1)
                    if flag:
                        is_unicode = bool(flag[0] & 1)
        return "".join(out)


def _parse_sst(segments):
    """Parse an SST record (+ its CONTINUE segments) into a list of
    strings. A malformed tail stops the parse; strings already read
    are kept -- a half-broken table still gets scanned, and the raw
    byte sweep below covers the rest.
    解析 SST（共享字符串表），尾部损坏就停，已读到的照样扫。"""
    r = _SegReader(segments)
    head = r.read(8)
    if len(head) < 8:
        return []
    unique = _u32(head, 4)
    strings = []
    for _ in range(unique):
        cch_b = r.read(2)
        flag_b = r.read(1)
        if len(cch_b) < 2 or len(flag_b) < 1:
            break
        cch = _u16(cch_b, 0)
        flags = flag_b[0]
        runs = 0
        ext_len = 0
        if flags & 0x08:
            rb = r.read(2)
            if len(rb) < 2:
                break
            runs = _u16(rb, 0)
        if flags & 0x04:
            eb = r.read(4)
            if len(eb) < 4:
                break
            ext_len = _u32(eb, 0)
        strings.append(r.read_chars(cch, bool(flags & 0x01)))
        # Formatting runs and extended data are skipped unread;
        # they carry no cell text.
        skip = runs * 4 + ext_len
        while skip > 0 and r.has_data():
            seg = r.segs[r.i]
            take = min(skip, len(seg) - r.off)
            r.off += take
            skip -= take
    return strings


def _biff_text_parts(stream):
    """Walk BIFF records in a Workbook stream and pull out every
    scannable string: shared strings (SST), cell strings (LABELSST /
    LABEL / formula STRING results), numbers (NUMBER / RK, formatted
    as text), comment authors (NOTE) and comment text (TXO).
    Returns (parts, encrypted): parts is [(part, row, text)] with
    1-based sheet rows (0 = no cell, e.g. the raw-byte sweep);
    encrypted is True if a FILEPASS record says the book is locked.
    遍历 Workbook 流里的 BIFF 记录，抽出所有可扫描字符串。"""
    # Split into records; CONTINUE payloads are kept as extra
    # segments of the previous record (SST/TXO strings can span them).
    records = []
    pos = 0
    while pos + 4 <= len(stream):
        op = _u16(stream, pos)
        ln = _u16(stream, pos + 2)
        data = stream[pos + 4:pos + 4 + ln]
        if op == 0x003C and records:
            records[-1][1].append(data)
        else:
            records.append((op, [data]))
        pos += 4 + ln

    version = 0x0600
    sst = []
    parts = []
    used_sst = set()
    last_formula_row = None
    encrypted = False
    for op, segments in records:
        data = segments[0]
        if op == 0x0809:  # BOF: version decides the LABEL layout
            if len(data) >= 2:
                version = _u16(data, 0)
        elif op == 0x002F:  # FILEPASS: encrypted book, unreadable
            encrypted = True
        elif op == 0x00FC:  # SST
            sst = _parse_sst(segments)
        elif op == 0x00FD:  # LABELSST
            if len(data) >= 10:
                row = _u16(data, 0)
                idx = _u32(data, 6)
                if 0 <= idx < len(sst):
                    used_sst.add(idx)
                    parts.append(("Workbook", row + 1, sst[idx]))
        elif op == 0x0204:  # LABEL
            if len(data) >= 8:
                row = _u16(data, 0)
                cch = _u16(data, 6)
                if version >= 0x0600:
                    flag = data[8] if len(data) > 8 else 0
                    raw = data[9:9 + cch * (2 if flag & 1 else 1)]
                    text = (raw.decode("utf-16-le", "replace") if flag & 1
                            else raw.decode("latin-1"))
                else:
                    text = data[8:8 + cch].decode("latin-1")
                parts.append(("Workbook", row + 1, text))
        elif op == 0x0203:  # NUMBER: row + col + xf + 8-byte double
            if len(data) >= 14:
                row = _u16(data, 0)
                parts.append(("Workbook", row + 1,
                              _format_number(_ieee754_double(data[6:14]))))
        elif op == 0x027E:  # RK: row + col + xf + 4-byte packed number
            if len(data) >= 10:
                row = _u16(data, 0)
                parts.append(("Workbook", row + 1,
                              _format_number(_rk_value(data[6:10]))))
        elif op == 0x0006:  # FORMULA: remember its row for STRING
            if len(data) >= 2:
                last_formula_row = _u16(data, 0)
        elif op == 0x0207:  # STRING: a formula's string result
            if len(data) >= 3:
                cch = _u16(data, 0)
                flag = data[2]
                raw = data[3:3 + cch * (2 if flag & 1 else 1)]
                text = (raw.decode("utf-16-le", "replace") if flag & 1
                        else raw.decode("latin-1"))
                row = (last_formula_row + 1
                       if last_formula_row is not None else 0)
                parts.append(("Workbook", row, text))
        elif op == 0x001C:  # NOTE: comment author
            if len(data) >= 6:
                row = _u16(data, 0)
                for run in _string_runs(data[6:]):
                    parts.append(("Workbook（批注作者）", row + 1, run))
        elif op == 0x01B6:  # TXO: comment text
            for run in _string_runs(data[16:]):
                parts.append(("Workbook（批注）", 0, run))
    # Shared strings no cell references are still scanned on their own.
    for i, text in enumerate(sst):
        if i not in used_sst:
            parts.append(("Workbook（共享字符串）", i + 1, text))
    # Safety net: printable runs over the whole stream, skipping
    # texts the record walk already found (same value, reported once
    # with its real row). This catches string payloads in records
    # the walk above does not know by opcode.
    # 兜底：全流可打印字符串，已从记录里找到的文本不再重复报。
    seen = set(text for _, _, text in parts)
    for run in _string_runs(stream):
        if run not in seen:
            parts.append(("Workbook（原始字节扫描）", 0, run))
            seen.add(run)
    return parts, encrypted


def _xls_text_parts(path):
    """Extract scannable text from a .xls file (OLE2 + BIFF, stdlib
    only). Returns (parts, None) on success, or (None, reason) when
    the file cannot be parsed at all -- reason is a short string for
    the "please review by hand" report, never a silent pass.
    What this does NOT cover (stated, not hidden): comment text in
    an MSO drawing object is recovered from the TXO record payload,
    not from a full MSO drawing parse, so a comment stored with an
    unusual encoding can still be missed by the record walk -- the
    raw-byte sweep is the net for that case. An encrypted (FILEPASS)
    workbook cannot be read at all and is reported as such.
    从 .xls 里抽可扫描文本（OLE2 + BIFF，只用标准库）。"""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except (OSError, IOError):
        return None, "读不到文件"
    blob, problem = _cfb_read_stream(data)
    if blob is None:
        return None, {
            "not-ole": "不是 OLE2 格式的 .xls 文件",
            "damaged": "OLE2 结构损坏，读不出 Workbook 流",
            "no-workbook": "OLE2 文件里找不到 Workbook/Book 流",
        }.get(problem, "无法解析")
    parts, encrypted = _biff_text_parts(blob)
    if encrypted:
        return None, "工作簿已加密（FILEPASS），读不出内容"
    return parts, None


def _scan_xls(path):
    """Scan a .xls file. Returns (hits, None) when parsed, or
    (None, reason) when unparsable (the caller falls back to a
    text scan, then to an explicit warning)."""
    parts, problem = _xls_text_parts(path)
    if parts is None:
        return None, problem
    return _scan_parts(parts), None


def _scan_text_file(path):
    """Plain-text scan: one line at a time, same email/phone checks.
    Returns [] when the file cannot be read (matches the old
    behaviour for unreadable files).
    纯文本扫描：一行一行，同一套邮箱/电话检查。"""
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except (OSError, IOError):
        return []

    hits = []
    for no, line in enumerate(lines, 1):
        low = line.lower()
        if any(h in line for h in ("【示例】", "[示例]")) or \
           any(h in low for h in ("占位", "placeholder")):
            continue
        norm = _normalize(line)

        for domain in _find_email_domains(norm):
            if not _is_ok_domain(domain):
                hits.append((no, "邮箱域名 %s（不是保留域名，像是真人邮箱）" % domain))
                break

        if looks_like_real_phone(norm):
            hits.append((no, "手机号/座机号（看着像真号码）"))

    return hits


def _scan_unparsable(path, kind, problem):
    """A spreadsheet that cannot be parsed at all: first a plain
    text scan (a misnamed text file still gets caught), and if that
    finds nothing, an explicit whole-file warning -- never a silent
    pass. Empty files are clean (there is nothing to leak) and never
    reach here.
    解析不了的表格：先纯文本扫一遍，没扫到东西就明确报“请人工复核”，
    不静默放过。空文件干净，不会走到这里。"""
    hits = _scan_text_file(path)
    if hits:
        return hits
    return [(0, "整个文件无法解析（%s：%s），内容没扫到，请人工复核后再提交"
            % (kind, problem))]


def scan_file(path):
    """返回 [(行号, 为什么中招)]，干净就返回空列表。"""
    low = path.lower()
    if low.endswith(".xlsx"):
        hits = _scan_xlsx(path)
        if hits is not None:
            return hits
        return _scan_unparsable(path, ".xlsx", "不是合法的 zip 文件")
    if low.endswith(".xls"):
        try:
            size = os.path.getsize(path)
        except OSError:
            size = 0
        if size == 0:
            return []
        hits, problem = _scan_xls(path)
        if hits is not None:
            return hits
        return _scan_unparsable(path, ".xls", problem or "无法解析")
    return _scan_text_file(path)


def _repo_root():
    """仓库根目录：从本文件位置推，不依赖当前工作目录。

    Repo root derived from this file's location, never from the cwd:
    running the script from scripts/ used to silently scan only that
    directory (13 files) and still report a pass.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    argparse.ArgumentParser(
        prog="check_private_data.py",
        description="扫一遍仓库，查有没有真实客户数据（真实公司名/电话/邮箱）混进示例和文档（只用标准库）",
        epilog="可直接复制的例子:\n  python scripts/check_private_data.py\n\n"
               "没参数就直接扫：通过会说扫了多少文件，没通过会逐条列出可疑位置。",
    ).parse_args()
    root = _repo_root()
    # 不在根目录就直接报错退出：换个目录跑会漏扫、报假通过，
    # 安全检查宁可拦住也不许悄悄放过。
    if os.path.abspath(os.getcwd()) != os.path.abspath(root):
        print("错误：不在仓库根目录（当前在 %s）。" % os.getcwd())
        print("  这个脚本只扫仓库根目录下的文件，换个目录跑会漏扫、报假通过。")
        print("  请先 cd 到 %s 再跑。" % root)
        return 2
    # 只扫要提交的目录，别把 node_modules、.venv 这些翻一遍
    roots = ["scripts", "docs", "examples", "prompts", ".github"]
    # 仓库根目录下的单文件（README / LICENSE 之类）
    root_files = []

    seen = set()
    files = []
    for fn in sorted(os.listdir(root)):
        p = os.path.join(root, fn)
        if fn.endswith(SCAN_EXT) and os.path.isfile(p):
            root_files.append(os.path.relpath(p, root))

    for sub in roots:
        base = os.path.join(root, sub)
        if not os.path.isdir(base):
            continue
        # 递归进子目录：以前只取顶层，docs/advanced/ 里的文件根本没扫过
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIR)
            for fn in sorted(filenames):
                if fn.endswith(SCAN_EXT):
                    files.append(os.path.relpath(
                        os.path.join(dirpath, fn), root))

    files = sorted(set(files) | set(root_files))
    files = [f.replace("\\", "/") for f in files]

    total_hits = 0
    report = []
    for path in files:
        if path in seen:
            continue
        seen.add(path)
        hits = scan_file(path)
        if hits:
            total_hits += len(hits)
            report.append((path, hits))

    print("仓库根目录：%s" % root)
    print("扫了 %d 个文件" % len(files))
    if not report:
        print("没查到真实客户数据，这一关过了。")
        return 0

    print("")
    print("下面这些地方看着像真客户数据，提交前先处理掉：")
    for path, hits in report:
        print("")
        print("  %s" % path)
        for no, why in hits[:8]:
            print("    第 %d 行 — %s" % (no, why))
        if len(hits) > 8:
            print("    ……还有 %d 处" % (len(hits) - 8))
    print("")
    print("怎么改（挑一个）：")
    print("  · 真客户挪到 my_leads.csv，别留在要提交的文件里")
    print("  · 邮箱换成 sample.example（保留域名，不会真的寄出去）")
    print("  · 电话换成 +000 00 000 0000（明显的假号）")
    print("  · 确实只是示例，就把公司名带上【示例】前缀")
    return 1


if __name__ == "__main__":
    sys.exit(main())