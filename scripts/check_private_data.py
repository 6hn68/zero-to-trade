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

`.xlsx` 按 zip/XML 解析（共享字符串 + 工作表单元格），不是
按文本读——表格里的邮箱/电话也能扫到。`.xls` 是旧二进制格式，
标准库解析不了，仍按文本读，里面的内容要人工复核。

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


def _scan_xlsx(path):
    """Scan an .xlsx file cell by cell, with the same email/phone
    checks as the text scan. Returns [(row number, why)] -- the row
    number is the sheet row for cells, or the shared-string index
    for unreferenced shared strings. Returns None if the file is
    not a readable zip (the caller falls back to a text scan).
    按单元格扫 .xlsx，邮箱/电话检查和文本扫描同一套；返回
    [(行号, 原因)]。文件不是合法 zip 就返回 None（调用方回退）。"""
    parts = _xlsx_text_parts(path)
    if parts is None:
        return None
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


def scan_file(path):
    """返回 [(行号, 为什么中招)]，干净就返回空列表。"""
    if path.lower().endswith(".xlsx"):
        hits = _scan_xlsx(path)
        if hits is not None:
            return hits
        # Not a readable zip (corrupt or misnamed file): fall through
        # to the plain-text scan below, so anything visible in the
        # raw bytes is still caught instead of silently passed.
        # 不是合法 zip（损坏或改名文件）：往下走纯文本扫描，
        # 原始字节里看得见的东西照样能抓住，不静默放过。
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