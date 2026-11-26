#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trade_show.py — 展会实战：名片收进来，会后 24 小时跟进计划排出去

展会结束不是结束，是 24 小时倒计时开始。展会上换的名片，拖过三天再联系，
对方连你长什么样都忘了——所以这个脚本只干一件事：把展会上收到的展商按
「兴趣度」排好队，每家给一张会后 24 小时跟进表（2 小时感谢 + 12 小时报价
线索 + 24 小时电话追一次），并按 outreach_gen 的首触模板把第一封消息的
草稿写出来。

只用标准库，Python 3.10+ 可直接跑，不联网。

两种录入方式（可以混着用：先读 CSV，再用 --add 补一家）：
    命令行逐条加：--add 公司 --country 国家 --product 产品 --interest 高
                  --email/--phone/--whatsapp 任选其一（至少留一个），
                  一次命令加一家；多家用 --csv 批量读
    CSV 批量读：--csv 文件，列名 company/country/product/contact/interest，
                  与 examples/leads_example.csv 的 9 列口径对齐（email/phone
                  列也认；contact 列只有长得像邮箱/电话时才当联系方式，
                  写职位如 purchasing manager 的不算）。

时间点只写相对时间（会后 2/12/24 小时），不编具体日期——展会哪天结束，
你哪天跑脚本，T+0 就是那一天。

兴趣度 → outreach_gen 分级（首触模板按这个走）：
    高 → T0（立即建联）· 中 → T1（本周首触）· 低 → T2（低频培育）

没填兴趣度的一律按「低」处理（宁可排后，不硬抬优先级）；填了认不出的
词（比如「很高」「urgent」）会直接报错，让你当场改，别悄悄排错队。

官方展商名录批量处理 (Official exhibitor directory batch mode, --backcheck)：
    Official directories list every exhibitor, and most rows have no contact
    info yet — that is exactly what the backcheck is for. So --backcheck
    keeps those rows as 待核实 (pending verification) placeholders instead
    of rejecting them, and only skips rows that cannot be backchecked at all
    (empty company name, or a duplicate of an earlier row), each with an
    explicit reason. Output is a backcheck worksheet: one placeholder row per
    exhibitor (官网 / 决策人 / 进口记录 all marked 没核实 until verified),
    plus a progress summary （已处理 / 待核实 / 跳过）.
    官方名录里大半展商本来就没留联系方式——背调就是去补这些的。所以
    --backcheck 模式不扔这些行，而是留成「待核实」占位行；只跳过实在没法
    背调的行（公司名为空、或与前面某行重名），每行都写清跳过原因。产出是
    一张背调工作表：每家一行占位行（官网/决策人/进口记录先标「没核实」），
    外加一份进度汇总（已处理/待核实/跳过）。

用法见 --help（里面的例子都能直接复制）。
"""

import argparse
import csv
import io
import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import _ZhArgumentParser, _clean, _is_filled  # noqa: E402

# ================================================================ 口径总表
# 想改跟进口径，只改这一块，改完务必跑一次：
#   python scripts/trade_show.py --csv examples/leads_example.csv

# 兴趣度：高在前、低在后；同级按录入顺序（Python 的 sort 本来就是稳定的，
# 不用再拼公司名——展会现场谁先聊的就是谁先记的，顺序本身就是信息）。
INTEREST_ORDER = {"高": 0, "中": 1, "低": 2}
INTEREST_ALIAS = {
    "高": "高", "high": "高", "h": "高",
    "中": "中", "medium": "中", "med": "中", "m": "中",
    "低": "低", "low": "低", "l": "低",
}
# 兴趣度 → outreach_gen 分级：首触模板的语气按这个走，高兴趣直接问规格用量，
# 低兴趣只求确认今年还采不采购。
TIER_FOR_INTEREST = {"高": "T0", "中": "T1", "低": "T2"}
TIER_LABEL = {"T0": "立即建联", "T1": "本周首触", "T2": "低频培育"}

# 会后 24 小时三档：时间点是相对时间（T+2h / T+12h / T+24h），不编具体日期。
# 三档缺一不可——只发感谢不跟报价等于白聊，只报价格不打电话等于等对方想起你。
STEPS = [
    {"window": "会后 2 小时内", "offset": "T+2h",
     "action": "发感谢 + 展会资料（产品单页/规格表）",
     "must": "一句话提展会上聊过的具体产品/规格，别群发同一版"},
    {"window": "会后 12 小时内", "offset": "T+12h",
     "action": "发报价线索：请对方确认规格与月用量，再给报价区间意向",
     "must": "只给「确认规格再报价」的口子，不报具体价格数字、不发价单"},
    {"window": "会后 24 小时内", "offset": "T+24h",
     "action": "电话/WhatsApp 追一次：只问一个 20 秒能答的问题（规格/用量/目的港）",
     "must": "对方明确说不需要就停手，别在 24 小时内连追两次"},
]

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
PHONE_MIN_DIGITS = 7        # 有效电话至少 7 位数字，少于一律当没填
MAX_CELL_CHARS = 2000       # 超长字段截断，防止一个巨长备注拖垮读取
# 这些值都等于「没填」，不能因为格子里有字就算有联系方式
PLACEHOLDERS = {"", "-", "--", "---", "/", "n/a", "na", "n.a.", "none", "null",
                "nil", "unknown", "tbd", "?", "??", "待定", "待补", "暂无",
                "未知", "无", "不知道", "未填写"}
FALLBACK_ENCODINGS = ("utf-8-sig", "gb18030", "utf-8", "big5", "latin-1")

# Real-directory column aliases (真实名录列名别名).
# Real exhibitor directories rarely use our tidy headers. Verified
# 2026-11-26 (route-07, re-check of the last round's conclusion):
#   - Current editions (2025/2026 Dubai) are a web search page only —
#     no official downloadable CSV/XLSX/PDF for the current edition.
#     Official 2026 list: automechanika-dubai.ae.messefrankfurt.com/
#     dubai/en/exhibitor-list.html (search by company / product group,
#     floor-plan view, no export link). Riyadh 2027 (21-23 June 2027,
#     official site automechanika-riyadh.ksa.messefrankfurt.com): no
#     official downloadable list found either.
#   - The only verified official downloadable file is the 2021 Dubai
#     exhibitor-list PDF on the organiser's own domain (opened firsthand):
#     .../2021/downloads/AMDU21 – Exhibitor List.pdf — exactly three
#     columns, "Company Name / Country / Booth Number", no product
#     section, no email, no website; some booths are "-" (missing) and
#     some rows carry two booths ("6-H22, 6-H20"). That shape already
#     runs through --backcheck (aliases below accept "Company Name" and
#     "Booth Number"; a missing booth is counted, not dropped) — but the
#     file is a PDF, so convert it to CSV first; --backcheck reads CSV.
#   - Everything else called a "downloadable list" is third-party, not
#     official: a free PDF compiled from the web list (dubaifastliving,
#     1,021 companies, 2026-11-02 snapshot), paid data-vendor CSVs
#     (VisitorsList / Lensmor), and paid scraper tools. None of these
#     is the organiser's file, so none of their formats is treated as
#     the official format here.
# So the directory reader accepts these aliases instead of failing on
# the header — a real export must run, not error out on "Exhibitor Name".
# 真实名录的表头很少是我们这套干净列名：现届迪拜展官方名录只有网页检索页，
# 没有官方可下载文件；唯一核实过的官方可下载文件是 2021 年迪拜展 PDF，
# 只有 Company Name / Country / Booth Number 三列，没有产品分区、没有联系
# 方式，部分展位号是 "-"，个别一行带两个展位号。这套表头 --backcheck 本来
# 就认（下面别名里有 Company Name 和 Booth Number），缺展位号只计数不丢行；
# 但那是 PDF，得先转成 CSV 再喂 --backcheck。市面上其余所谓“可下载名录”
# 全是第三方编译或付费卖的，不是官方文件，不当官方格式用。
COMPANY_ALIASES = ("company", "company name", "exhibitor",
                   "exhibitor name", "exhibitor company")
PRODUCT_ALIASES = ("product", "product section", "product category",
                   "product group", "category", "section")
BOOTH_ALIASES = ("booth", "booth number", "booth no", "booth no.",
                 "stand", "stand number", "stand no", "stand no.")
WEBSITE_ALIASES = ("website", "web site", "url", "homepage", "web")
EMAIL_ALIASES = ("email", "e-mail", "email address", "contact email")
PHONE_ALIASES = ("phone", "telephone", "tel", "phone number", "mobile")
WHATSAPP_ALIASES = ("whatsapp", "whats app", "wa")
LOCATION_ALIASES = ("location", "city, country", "city and country")


class TradeShowError(Exception):
    """名单读不出来、缺列、没数据、参数填错。main 会把它翻成人话再退出。"""


# ---------------------------------------------------------------- 小工具
def _get(row: Dict[str, Any], key: str, default: str = "") -> str:
    """不区分大小写、忽略前后空格地取列值；列不存在返回 default。"""
    target = key.strip().lower()
    for col, value in row.items():
        if col is not None and str(col).strip().lower() == target:
            return _clean(value)
    return default


def _get_first(row: Dict[str, Any], keys: Tuple[str, ...],
               default: str = "") -> str:
    """First filled value across alias keys (first alias wins).
    按别名顺序取第一个填了的值（排前面的别名优先）。"""
    for key in keys:
        value = _get(row, key)
        if _is_filled(value):
            return value
    return default


def _get_company(row: Dict[str, Any]) -> str:
    """Company name from any accepted alias (company / Company Name /
    Exhibitor Name / ...). Real exports rarely say plain "company".
    公司名：认 company / Company Name / Exhibitor Name 等别名，真实导出
    很少只写 company 一个词。"""
    return _get_first(row, COMPANY_ALIASES)


def _get_country(row: Dict[str, Any]) -> Tuple[str, str]:
    """Country -> (country, note). A "Location" column like
    "Sharjah, United Arab Emirates" yields the part after the last comma;
    a lone "City" column leaves country as 没核实 and notes the city.
    国家 -> (国家, 备注)：Location 列如 "Sharjah, United Arab Emirates"
    取最后一个逗号后面那段；只有 City 列时国家标「没核实」，城市写进备注。"""
    country = _get(row, "country")
    if _is_filled(country):
        return country, ""
    location = _get_first(row, LOCATION_ALIASES)
    if _is_filled(location) and "," in location:
        return location.rsplit(",", 1)[-1].strip(), ""
    city = _get(row, "city")
    if _is_filled(city):
        return NOT_VERIFIED, "城市：%s（国家没核实）" % city
    if _is_filled(location):
        return NOT_VERIFIED, "地点：%s（国家没核实）" % location
    return NOT_VERIFIED, ""






def _looks_like_contact(value: str) -> bool:
    """contact 列里的值像不像联系方式：含 @（邮箱）或至少 7 位数字（电话）。
    写职位（purchasing manager）的不算——那是角色，不是联系方式。"""
    if not _is_filled(value):
        return False
    if "@" in value:
        return True
    return sum(c.isdigit() for c in value) >= PHONE_MIN_DIGITS


def normalize_interest(raw: Any) -> str:
    """兴趣度 -> 高/中/低。空着按「低」处理；填了认不出的词直接报错。"""
    text = _clean(raw).lower()
    if not _is_filled(text):
        return "低"
    if text in INTEREST_ALIAS:
        return INTEREST_ALIAS[text]
    raise TradeShowError("兴趣度只能填 高/中/低（或 high/medium/low），收到的是 %r。"
                         % _clean(raw))


# ---------------------------------------------------------------- 录入
def parse_contact(email: str = "", phone: str = "", whatsapp: str = "",
                  contact: str = "") -> Tuple[str, str, str, str]:
    """四路联系方式 -> (渠道, 展示用的联系方式, 邮箱, 电话/WhatsApp)。

    渠道优先级：邮箱 > WhatsApp > 电话——第 1/2 步（发感谢、发报价线索）走
    邮箱最能留痕；只有电话时才走 WhatsApp/电话。contact 列只有长得像邮箱/
    电话时才认（见 _looks_like_contact），写职位的不算。
    邮箱格式不对、电话数字不够 7 位，当场报错，别等到跟进那步才发现联系不上。
    """
    email, phone, whatsapp, contact = (_clean(email), _clean(phone),
                                       _clean(whatsapp), _clean(contact))
    if _is_filled(email) and not EMAIL_RE.match(email):
        raise TradeShowError("邮箱格式不对：%r（应为 someone@sample.example 这种样子）"
                             % email)
    for label, number in (("电话", phone), ("WhatsApp", whatsapp)):
        if _is_filled(number) and sum(c.isdigit() for c in number) < PHONE_MIN_DIGITS:
            raise TradeShowError("%s数字不够 7 位：%r，少于 7 位当成没填。"
                                 % (label, number))
    if _is_filled(email):
        return "邮箱", email, email, whatsapp or phone
    if _is_filled(whatsapp):
        return "WhatsApp", whatsapp, "", whatsapp
    if _is_filled(phone):
        return "电话", phone, "", phone
    if _looks_like_contact(contact):
        if "@" in contact:
            return "邮箱", contact, contact, ""
        return "电话", contact, "", contact
    return "", "", "", ""


def make_exhibitor(company: str, country: str = "", product: str = "",
                   interest: Any = "", email: str = "", phone: str = "",
                   whatsapp: str = "", contact: str = "") -> Dict[str, Any]:
    """一条展商记录。纯函数：只校验、不读文件。没留任何联系方式的直接报错，
    因为排进跟进表也联系不上——展会现场就该当场补，回来再补就晚了。"""
    company = _clean(company)
    if not _is_filled(company):
        raise TradeShowError("公司名没填：--add 后面要跟公司名，CSV 里 company 列不能为空。")
    level = normalize_interest(interest)
    channel, shown, email_ok, phone_ok = parse_contact(email, phone, whatsapp, contact)
    if not channel:
        raise TradeShowError("「%s」没留任何联系方式（邮箱/电话/WhatsApp 至少留一个），"
                             "排不进跟进表——展会现场当场补一个再记。" % company)
    return {
        "company": company,
        "country": _clean(country) or "?",
        "product": _clean(product),
        "interest": level,
        "tier": TIER_FOR_INTEREST[level],
        "contact": shown,
        "channel": channel,
        "email": email_ok,
        "phone": phone_ok,
    }


def _decode(raw: bytes) -> Tuple[str, str]:
    """按 UTF-8 -> GB18030 -> ... 猜编码，返回 (文本, 实际编码名)。"""
    for encoding in FALLBACK_ENCODINGS:
        try:
            return raw.decode(encoding), encoding
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8(容错)"


def _read_csv_records(path: str) -> Tuple[List[str], List[Tuple[int, Dict[str, Any]]]]:
    """Read a CSV file and return (header, [(source_line_no, row_dict), ...]).
    从 CSV 读出 (表头, [(原文件行号, 行字典), ...])。

    Shared by the follow-up reader (read_exhibitors) and the directory
    reader (read_directory), so both tolerate the same messy input:
    encoding falls back from UTF-8 to GB18030 and others; header case and
    surrounding spaces are ignored; #-comment lines before the header are
    skipped; fully blank rows are skipped. Rows are never silently dropped
    later — the line number travels with each row so a skipped row can
    always be traced back to its source line.
    共用：跟进表读取 (read_exhibitors) 与名录读取 (read_directory) 走同一套
    容错——编码自动回退、表头大小写/空格都认、表头前的 # 行当免责声明跳过、
    全空行跳过。行号跟着每行走，之后哪行被跳过都能对回原文件第几行，不静默丢行。
    """
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except FileNotFoundError:
        raise TradeShowError("找不到文件「%s」。\n"
                             "  检查一下路径拼写。Windows 上可以直接把文件拖进终端，"
                             "路径会自动填好。" % path)
    except OSError as e:
        raise TradeShowError("打不开文件「%s」：%s\n"
                             "  文件可能正被 Excel 打开着，先关掉再试。"
                             % (path, e.strerror or e))
    if not raw.strip():
        raise TradeShowError("文件是空的：%s" % path)

    text, encoding = _decode(raw)
    if encoding not in ("utf-8-sig", "utf-8"):
        print("提示：这个 CSV 不是 UTF-8，已按 %s 读取。"
              "以后用 Excel 另存时选「CSV UTF-8」就不用猜了。" % encoding,
              file=sys.stderr)

    try:
        csv.field_size_limit(min(sys.maxsize, 10 ** 7))
    except (OverflowError, ValueError):
        pass

    # Delimiter sniffing (分隔符嗅探): real exports are not always comma —
    # European Excel writes ";" and some exports use tabs. Sniff the first
    # chunk; if sniffing fails or guesses something odd, fall back to ",".
    # 真实导出不一定是逗号分隔——欧洲版 Excel 写 ";"，有的导出用制表符。
    # 先嗅探一小段，嗅不出来或嗅出怪东西就回退到逗号。
    delimiter = ","
    try:
        sample = text[:2048]
        sniffed = csv.Sniffer().sniff(sample, delimiters=",;\t")
        if sniffed.delimiter in (",", ";", "\t"):
            delimiter = sniffed.delimiter
    except csv.Error:
        pass

    reader = csv.reader(io.StringIO(text, newline=""), delimiter=delimiter)
    header: Optional[List[str]] = None
    records: List[Tuple[int, Dict[str, Any]]] = []
    for row_values in reader:
        if not row_values or all((c or "").strip() == "" for c in row_values):
            continue
        if header is None:
            if (row_values[0] or "").lstrip().startswith("#"):
                continue
            header = [h.strip() or "第%d列" % (i + 1)
                      for i, h in enumerate(row_values)]
            continue
        record: Dict[str, Any] = {}
        for col, value in zip(header, row_values):
            if col not in record:
                record[col] = value
        records.append((reader.line_num, record))

    if header is None:
        raise TradeShowError("这个 CSV 没有表头行（第一行得是列名，比如 company,country）。")
    header_keys = [h.lower() for h in header]
    if not any(alias in header_keys for alias in COMPANY_ALIASES):
        raise TradeShowError("CSV 缺少公司名列（写 company / Company Name / "
                             "Exhibitor Name 都行，照 examples/leads_example.csv "
                             "抄表头最省事）。")

    rows = [(n, r) for n, r in records if any(_clean(v) for v in r.values())]
    if not rows:
        raise TradeShowError("表头读到了，但下面一行数据都没有。")
    return header, rows


def read_exhibitors(path: str) -> List[Dict[str, Any]]:
    """从 CSV 批量读展商。列名 company/country/product/contact/interest，
    与 examples/leads_example.csv 的 9 列口径对齐：email/phone 列也认，
    contact 列只有长得像邮箱/电话时才当联系方式。

    容错：编码自动回退 GB18030；表头大小写/空格都能处理；表头前以 # 开头
    的行当免责声明跳过；没填 interest 的行按「低」处理并在末尾数出来；
    没留联系方式的行跳过并报出来（不是悄悄丢掉）。
    """
    _header, rows = _read_csv_records(path)

    exhibitors: List[Dict[str, Any]] = []
    no_interest, skipped = 0, []
    for _line_no, row in rows:
        if not _is_filled(_get(row, "interest")):
            no_interest += 1
        try:
            exhibitors.append(make_exhibitor(
                _get_company(row), _get(row, "country"), _get(row, "product"),
                _get(row, "interest"), _get(row, "email"), _get(row, "phone"),
                _get(row, "whatsapp"), _get(row, "contact")))
        except TradeShowError as e:
            skipped.append(str(e))
    for msg in skipped:
        print("跳过一行：%s" % msg, file=sys.stderr)
    if no_interest:
        print("提示：%d 条没填 interest，按「低」处理（宁可排后，不硬抬优先级）。"
              % no_interest, file=sys.stderr)
    if not exhibitors:
        raise TradeShowError("CSV 里 %d 行全都排不进来（都没留联系方式），"
                             "跟进表是空的。" % len(rows))
    return exhibitors


# ---------------------------------------------------------------- 官方展商名录批量处理
# Official exhibitor directory batch mode: read a whole official directory
# (hundreds to ~1000+ rows), keep every row accounted for, and emit one
# backcheck placeholder row per exhibitor plus a progress summary.
# 官方展商名录批量处理：整份官方名录（几百到 1000+ 行）读进来，每行都有交代，
# 每家产出一行背调占位行，外加一份进度汇总。

# Backcheck worksheet columns (also the --format csv header, in this order).
# 背调工作表的列（也是 --format csv 的表头，按这个顺序）。
# booth (展位号) is carried over from the directory when present: on the
# show floor the stand number is how you find a company, and the official
# list's core fields are name / country / product section / stand number.
# 展位号从名录里原样带过来：展馆里找公司靠的就是展位号，官方名录的核心
# 字段本来就是公司名 / 国家 / 产品分区 / 展位号。
BACKCHECK_COLUMNS = ["seq", "company", "country", "product", "booth", "status",
                     "contact", "interest", "website", "decision_maker",
                     "import_record", "note"]

# Directory row statuses. A row is never dropped silently: skipped rows stay
# in the summary with their source line number and reason.
# 名录行的三种状态。行从不静默丢掉：被跳过的行留在汇总里，带原文件行号和原因。
DIR_STATUS_READY = "已处理"      # has a usable contact, ready for a follow-up plan
                                 # 留了可用联系方式，能直接排跟进表
DIR_STATUS_PENDING = "待核实"    # no usable contact yet — backcheck placeholder
                                 # 还没留可用联系方式，背调占位行，等背调补
DIR_STATUS_SKIPPED = "跳过"      # cannot be backchecked: empty name or duplicate
                                 # 没法背调：公司名为空，或与前面某行重名
NOT_VERIFIED = "没核实"          # placeholder for backcheck fields not yet verified
                                 # 背调字段还没核实，先这么标着，不编数


def _normalize_company_key(name: str) -> str:
    """Company name -> dedup key: strip whitespace, casefold Latin letters.
    公司名 -> 去重用的键：去首尾空白，拉丁字母统一小写（中文不受影响）。"""
    return " ".join(_clean(name).split()).casefold()


def _lenient_contact(email: str = "", phone: str = "", whatsapp: str = "",
                     contact: str = "") -> Tuple[str, str]:
    """Four contact inputs -> (channel, shown contact), never raises.
    四路联系方式 -> (渠道, 展示用的联系方式)，绝不报错。

    Same channel priority and validity rules as parse_contact (email >
    WhatsApp > phone; bad email / under-7-digit phone does not count), but
    an unusable value just means "no contact on file" here instead of an
    error — an official directory is a raw list, and a bad contact is a
    backcheck task, not a reason to stop the whole batch.
    渠道优先级和有效性判断与 parse_contact 一样（邮箱 > WhatsApp > 电话；
    格式不对的邮箱、不到 7 位的电话不算数），但这里不报错——官方名录本来
    就是原始名单，联系方式不对是背调要补的活，不是整批停下的理由。
    """
    email, phone, whatsapp, contact = (_clean(email), _clean(phone),
                                       _clean(whatsapp), _clean(contact))
    if _is_filled(email) and EMAIL_RE.match(email):
        return "邮箱", email
    if _is_filled(whatsapp) and sum(c.isdigit() for c in whatsapp) >= PHONE_MIN_DIGITS:
        return "WhatsApp", whatsapp
    if _is_filled(phone) and sum(c.isdigit() for c in phone) >= PHONE_MIN_DIGITS:
        return "电话", phone
    if _looks_like_contact(contact):
        if "@" in contact and EMAIL_RE.match(contact):
            return "邮箱", contact
        if "@" not in contact:
            return "电话", contact
    return "", ""


def read_directory(path: str) -> List[Dict[str, Any]]:
    """Read an official exhibitor directory CSV and account for every row.
    读一份官方展商名录 CSV，每行都有交代。

    Columns: company is required (aliases: Company Name / Exhibitor
    Name / Exhibitor); country / product / contact / interest / email /
    phone / whatsapp are optional and read when present. Real-format
    extras are carried over when present: booth / stand number, product
    section / category, website, and a combined Location ("City,
    Country") column. A website on file is used as-is instead of being
    marked 没核实 — the directory already gave it to us.
    列：company 必填（别名 Company Name / Exhibitor Name / Exhibitor）；
    country / product / contact / interest / email / phone / whatsapp
    有就认，没有也能跑。真实格式里常见的多余列有就带过来：展位号
    （booth / stand number）、产品分区（product section / category）、
    官网（website）、合并的地点列（Location 如 "City, Country"）。
    名录里给了官网就直接用，不标「没核实」——名录已经给了，没必要重标。

    Dirty data is handled out in the open, never silently:
    脏数据都摆在明面上处理，不静默丢行：
      - empty company name -> status 跳过 (skipped), reason recorded;
        公司名为空 -> 跳过，原因记下来；
      - duplicate company name (same name after trimming + casefolding,
        same booth) -> status 跳过 (skipped), reason names the earlier
        line. Same company at a DIFFERENT booth is kept (one company can
        hold two stands / two brands) and noted — a real directory lists
        stands, not just companies;
        重名（去空白、拉丁字母小写后相同，且展位号也相同）-> 跳过，原因
        写明与第几行重名；同一家公司、不同展位 -> 留着（一家公司可能
        占两个展位 / 挂两个品牌），备注写明——真实名录列的是展位，不
        只是公司；
      - missing country -> kept, country = 没核实 (not verified);
        国家没填 -> 留着，国家标「没核实」；
      - no usable contact -> kept as 待核实 (pending), a backcheck
        placeholder, NOT an error — most directory rows start this way;
        没留可用联系方式 -> 留着，状态「待核实」，是背调占位行不是报错——
        名录里大半行本来就是这个状态；
      - bad email / short phone / unrecognized interest -> treated as
        "not filled", noted in the row's note, batch keeps running.
        邮箱写错、电话太短、兴趣度认不出 -> 一律按「没填」处理，原因写进
        备注，整批继续跑，不停下。
    Returns one dict per source row (kept + skipped), in source order.
    返回每行一个字典（留下的 + 跳过的都有），按原文件顺序。
    """
    _header, rows = _read_csv_records(path)

    seen: Dict[Tuple[str, str], int] = {}
    company_booths: Dict[str, set] = {}
    directory: List[Dict[str, Any]] = []
    for line_no, row in rows:
        company = _clean(_get_company(row))
        booth = _clean(_get_first(row, BOOTH_ALIASES))
        website = _clean(_get_first(row, WEBSITE_ALIASES))
        notes: List[str] = []
        if not _is_filled(company):
            directory.append({
                "seq": None, "line": line_no, "company": company,
                "country": _get_country(row)[0],
                "product": _clean(_get_first(row, PRODUCT_ALIASES)),
                "booth": booth, "website": website,
                "interest": "", "contact": "", "channel": "",
                "status": DIR_STATUS_SKIPPED,
                "reason": "公司名为空 (empty company name)",
                "note": "",
            })
            continue
        key = (_normalize_company_key(company),
               " ".join(booth.split()).casefold())
        if key in seen:
            directory.append({
                "seq": None, "line": line_no, "company": company,
                "country": _get_country(row)[0],
                "product": _clean(_get_first(row, PRODUCT_ALIASES)),
                "booth": booth, "website": website,
                "interest": "", "contact": "", "channel": "",
                "status": DIR_STATUS_SKIPPED,
                "reason": "与第 %d 行重名 (duplicate of line %d)"
                          % (seen[key], seen[key]),
                "note": "",
            })
            continue
        seen[key] = line_no

        country, country_note = _get_country(row)
        if country == NOT_VERIFIED:
            notes.append("国家没核实 (country not verified)")
            if country_note:
                notes.append(country_note)
        interest_raw = _get(row, "interest")
        try:
            interest = normalize_interest(interest_raw) if _is_filled(interest_raw) else ""
        except TradeShowError:
            interest = ""
            notes.append("兴趣度「%s」无法识别，按未填处理 "
                         "(unrecognized interest, treated as blank)"
                         % _clean(interest_raw))
        channel, shown = _lenient_contact(
            _get_first(row, EMAIL_ALIASES), _get_first(row, PHONE_ALIASES),
            _get_first(row, WHATSAPP_ALIASES), _get(row, "contact"))
        if channel:
            status = DIR_STATUS_READY
        else:
            status = DIR_STATUS_PENDING
            notes.append("联系方式待核：名录里没留可用的邮箱/电话，背调时先补联系方式 "
                         "(no usable contact on file — find one during backcheck)")
        booths = company_booths.setdefault(
            _normalize_company_key(company), set())
        booth_key = " ".join(booth.split()).casefold()
        if booths and booth_key not in booths:
            notes.append("同一家公司、不同展位 (same company, different booth)")
        booths.add(booth_key)
        directory.append({
            "seq": None, "line": line_no, "company": company,
            "country": country,
            "product": _clean(_get_first(row, PRODUCT_ALIASES)),
            "booth": booth, "website": website,
            "interest": interest, "contact": shown, "channel": channel,
            "status": status, "reason": "", "note": "；".join(notes),
        })
    return directory


def summarize_directory(directory: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Progress summary for a directory read: total / ready / pending /
    skipped / missing-country / missing-booth, plus the skipped rows with
    line + reason.
    名录进度汇总：总数 / 已处理 / 待核实 / 跳过 / 缺国家的行数 / 缺展位号
    的行数，外加被跳过的行（带原文件行号和原因）。ready + pending +
    skipped == total.
    """
    skipped_rows = [{"line": d["line"], "company": d["company"],
                     "reason": d["reason"]}
                    for d in directory if d["status"] == DIR_STATUS_SKIPPED]
    return {
        "total": len(directory),
        "ready": sum(1 for d in directory if d["status"] == DIR_STATUS_READY),
        "pending": sum(1 for d in directory if d["status"] == DIR_STATUS_PENDING),
        "skipped": len(skipped_rows),
        "missing_country": sum(1 for d in directory
                               if d["status"] != DIR_STATUS_SKIPPED
                               and d["country"] == NOT_VERIFIED),
        "missing_booth": sum(1 for d in directory
                             if d["status"] != DIR_STATUS_SKIPPED
                             and not _is_filled(d.get("booth", ""))),
        "skipped_rows": skipped_rows,
    }


def build_backcheck_rows(directory: List[Dict[str, Any]],
                         pending_only: bool = False) -> List[Dict[str, Any]]:
    """One backcheck placeholder row per kept exhibitor (ready + pending),
    in source order, numbered from 1. Skipped rows get no row — they are
    already listed in the summary with their reason.
    每家留下的展商（已处理 + 待核实）产出一行背调占位行，按原文件顺序从 1
    编号。被跳过的行不出占位行——它们已经在汇总里带着原因列出来了。

    pending_only=True keeps only the 待核实 rows: that is the queue to
    work — the rows with no contact on file. The seq numbers stay the
    full-list numbers, so a pending-only export still lines up with the
    full worksheet row by row.
    pending_only=True 只留「待核实」的行：那就是要干的活——名录里没留
    联系方式的行。序号仍用全表的序号，待核实清单能跟全表逐行对上。

    Backcheck fields nobody has verified yet (decision maker / import
    record) are marked 没核实 (not verified), never invented. Booth and
    website are carried over from the directory when the directory gave
    them — a website on file is used as-is, not re-marked 没核实.
    还没人核实过的背调字段（决策人 / 进口记录）一律标「没核实」，不编数、
    不编案例。展位号和官网从名录里原样带过来——名录给了官网就直接用，
    不重标「没核实」。
    """
    rows: List[Dict[str, Any]] = []
    for d in directory:
        if d["status"] == DIR_STATUS_SKIPPED:
            continue
        rows.append({
            "seq": len(rows) + 1,
            "company": d["company"],
            "country": d["country"],
            "product": d["product"],
            "booth": d.get("booth", ""),
            "status": d["status"],
            "contact": d["contact"] or NOT_VERIFIED,
            "interest": d["interest"],
            "website": d.get("website") or NOT_VERIFIED,
            "decision_maker": NOT_VERIFIED,
            "import_record": NOT_VERIFIED,
            "note": d["note"],
        })
    if pending_only:
        rows = [r for r in rows if r["status"] == DIR_STATUS_PENDING]
    return rows


def render_backcheck_table(rows: List[Dict[str, Any]], summary: Dict[str, Any],
                           source: str, pending_only: bool = False) -> str:
    """Plain-text progress report: summary first, one compact line per
    exhibitor, then every skipped row with its reason.
    纯文本进度报告：先是汇总，每家一行，再是所有被跳过的行（带原因）。
    pending_only=True 只列待核实的行，汇总仍是全表的数（对得上总数）。"""
    lines = ["=" * 76,
             "  展商名录背调进度   来源：%s" % source,
             "  共 %d 家 · 已处理 %d 家（留了联系方式，能直接排跟进表）· "
             "待核实 %d 家（背调占位行，等补联系方式）· 跳过 %d 家"
             % (summary["total"], summary["ready"], summary["pending"],
                summary["skipped"]),
             "  缺国家的行：%d 家（国家标「没核实」，背调时补）· 缺展位号的行：%d 家"
             % (summary["missing_country"], summary["missing_booth"]),
             "=" * 76, ""]
    if pending_only:
        lines.append("  只列待核实 %d 家（--pending-only：没留联系方式的队列）。"
                     % len(rows))
        lines.append("")
    for r in rows:
        contact = r["contact"] if r["contact"] != NOT_VERIFIED else "联系方式没核实"
        interest = " · 兴趣度 %s" % r["interest"] if r["interest"] else ""
        booth = " · 展位 %s" % r["booth"] if r.get("booth") else ""
        lines.append("[%d] %s（%s）· %s · %s%s%s"
                     % (r["seq"], r["company"], r["country"], r["status"],
                        contact, booth, interest))
        if r["note"]:
            lines.append("    备注：%s" % r["note"])
    if summary["skipped_rows"]:
        lines.append("")
        lines.append("  跳过的行（没进背调表，原因如下）：")
        for s in summary["skipped_rows"]:
            lines.append("    第 %d 行 %s：%s"
                         % (s["line"], s["company"] or "（空公司名）", s["reason"]))
    lines += ["",
              "  下一步：拿这张表一家一家背调——先补官网和联系方式，再核决策人"
              "和进口记录；核实一项改一项，别把「没核实」当成核实过。",
              "  有联系方式的 %d 家可以直接排跟进表："
              "python scripts/trade_show.py --csv <名录>（只排留了联系方式的行）。"
              % summary["ready"],
              "=" * 76, ""]
    return "\n".join(lines)


def render_backcheck_json(rows: List[Dict[str, Any]], summary: Dict[str, Any],
                          source: str, pending_only: bool = False) -> str:
    """JSON payload: summary + skipped rows + one placeholder row per exhibitor.
    JSON 版：汇总 + 被跳过的行 + 每家一行占位行。pending_only 只列待核实行，
    汇总仍是全表的数。"""
    payload = {
        # 带时区，不然跨时区的同事对不上是哪一版
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": source,
        "mode": "backcheck",
        "pending_only": pending_only,
        "summary": summary,
        "rows": rows,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_backcheck_csv(rows: List[Dict[str, Any]]) -> str:
    """Backcheck worksheet as CSV text (BACKCHECK_COLUMNS header), ready to
    open in Excel and fill in row by row. Skipped rows are not in this file
    — they are listed in the summary (table / json) with their reason.
    背调工作表 CSV 文本（表头见 BACKCHECK_COLUMNS），Excel 打开就能一家一家
    往下填。被跳过的行不在这个文件里——它们在汇总（table / json）里带着
    原因列着。"""
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=BACKCHECK_COLUMNS,
                            extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return buf.getvalue()


# ---------------------------------------------------------------- 跟进计划
def draft_first_touch(ex: Dict[str, Any], csv_path: Optional[str] = None) -> Dict[str, str]:
    """按 outreach_gen 的首触模板口径，给这家写第一封消息的草稿。

    模板对应关系（跟 outreach_gen.py 的 BODY 一一对应，不另立一套话术）：
        高/T0：直接、具体，问规格和月用量
        中/T1：轻、短，只问一个问题（今年还采不采购）
        低/T2：更轻，只求确认信息，不求回复
    第一封不报具体价格数字（报价线索在 T+12h 那步，先确认规格再报价）。
    返回的 outreach_command 是拿完整中英对照版的命令：CSV 里 source 填
    trade_show，outreach_gen 会按同一分级出全文 + 发送前自查清单。
    """
    tier = ex["tier"]
    product = ex["product"] or "our products"
    company = ex["company"]
    country = ex["country"] if ex["country"] != "?" else "your market"
    subjects = {
        "T0": "%s supply — %s" % (product, company),
        "T1": "%s — one quick question" % product,
        "T2": "%s — %s sourcing check" % (company, product),
    }
    bodies_en = {
        "T0": ("Hello,\n\nWe met at the trade show and you asked about %s. "
               "We make %s and ship to %s on a regular basis.\n\n"
               "What sizes and monthly volume are you running on %s at the moment?"
               % (product, product, country, product)),
        "T1": ("Hello,\n\nWe met at the trade show and talked about %s. "
               "One quick question: is %s still something you source from Asia this year?"
               % (product, product)),
        "T2": ("Hello,\n\nWe met at the trade show. I am updating my notes on %s "
               "importers of %s — is %s still sourcing %s from Asia this year? "
               "One word is enough." % (country, product, company, product)),
    }
    bodies_zh = {
        "T0": ("您好，\n\n展会上见过面，贵司问过%s 的价格。我们做%s，长期发往%s。\n\n"
               "贵司目前在跑的规格和月用量大概是多少？" % (product, product, country)),
        "T1": ("您好，\n\n展会上聊过%s。就问一个问题：%s 贵司今年还在从亚洲采购吗？"
               % (product, product)),
        "T2": ("您好，\n\n展会上见过面。我在更新%s 的%s 进口商记录：%s 今年还在从亚洲采购%s 吗？"
               "回一个字就够了。" % (country, product, company, product)),
    }
    source = csv_path or "my_leads.csv"
    return {
        "tier": tier,
        "subject": subjects[tier],
        "en": bodies_en[tier],
        "zh": bodies_zh[tier],
        "draft_from": "outreach_gen.py --tier %s 的首触模板（高→T0 / 中→T1 / 低→T2）" % tier,
        "outreach_command": ("python scripts/outreach_gen.py %s --tier %s"
                             % (source, tier)),
    }


def _step_channel(ex: Dict[str, Any], step_idx: int) -> str:
    """这一步走哪个渠道：第 1/2 步（发消息）走邮箱最能留痕，没邮箱走 WhatsApp；
    第 3 步（追一次）优先电话/WhatsApp，没留电话只能邮件追一次。"""
    if step_idx < 2:
        if ex["email"]:
            return "邮箱"
        if ex["phone"]:
            return "WhatsApp" if "wa" in ex["phone"].lower() or ex["channel"] == "WhatsApp" else "电话/WhatsApp"
        return "邮箱"
    if ex["phone"]:
        return "电话/WhatsApp"
    return "邮箱（没留电话，只能邮件追一次）"


def build_plan(exhibitors: List[Dict[str, Any]],
               csv_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """按兴趣度排序（高→中→低，同级按录入顺序），每家排一张会后 24 小时表。
    纯函数，不读文件、不联网。空名单直接报错，别出个空表让人以为做完了。"""
    if not exhibitors:
        raise TradeShowError("名单是空的，排不出跟进表：加 --add 逐条录，"
                             "或用 --csv 批量读一个 CSV。")
    ranked = sorted(exhibitors, key=lambda e: INTEREST_ORDER[e["interest"]])
    plan: List[Dict[str, Any]] = []
    for rank, ex in enumerate(ranked, 1):
        draft = draft_first_touch(ex, csv_path)
        steps = []
        for i, s in enumerate(STEPS):
            steps.append({
                "window": s["window"],
                "offset": s["offset"],
                "channel": _step_channel(ex, i),
                "action": s["action"],
                "must_bring": s["must"],
            })
        plan.append({
            "rank": rank,
            "company": ex["company"],
            "country": ex["country"],
            "product": ex["product"],
            "interest": ex["interest"],
            "tier": ex["tier"],
            "contact": ex["contact"],
            "channel": ex["channel"],
            "steps": steps,
            "first_touch": draft,
        })
    return plan


# ---------------------------------------------------------------- 输出排版
def render_table(plan: List[Dict[str, Any]]) -> str:
    if not plan:
        return "\n名单是空的，排不出跟进表。\n"
    counts = {lv: sum(1 for p in plan if p["interest"] == lv)
              for lv in ("高", "中", "低")}
    lines = ["=" * 76,
             "  会后 24 小时跟进计划   共 %d 家 · 高 %d 家先打 · 中 %d 家本周内 · 低 %d 家只确认"
             % (len(plan), counts["高"], counts["中"], counts["低"]),
             "  时间点是相对时间（T+0 = 展会结束那一刻）：T+2h / T+12h / T+24h",
             "=" * 76, ""]
    for p in plan:
        lines.append("[%d] %s（%s）· 兴趣度 %s → %s（%s）· 联系：%s %s"
                     % (p["rank"], p["company"], p["country"], p["interest"],
                        p["tier"], TIER_LABEL[p["tier"]], p["channel"], p["contact"]))
        if p["product"]:
            lines.append("    产品：%s" % p["product"])
        for i, s in enumerate(p["steps"], 1):
            lines.append("    %s（%s）· %s：第 %d/3 步"
                         % (s["window"], s["offset"], s["channel"], i))
            lines.append("      做什么：%s" % s["action"])
            lines.append("      记住：%s" % s["must_bring"])
        d = p["first_touch"]
        lines.append("    首触草稿（%s）：Subject: %s" % (d["draft_from"], d["subject"]))
        for ln in d["en"].split("\n"):
            lines.append("      %s" % ln)
        lines.append("    完整中英对照版：%s（CSV 里 source 填 trade_show）"
                     % d["outreach_command"])
        lines.append("")
    lines += ["  止损线：第 3 步（T+24h）追完仍无任何回应 → 停手，进长名单，"
              "季度扫一次；同一家 24 小时内别追两次。",
              "  下一步：T+2h 那封发出去后，按 followup_plan.py 排 D0/D2/D5 的后续节奏。",
              "=" * 76, ""]
    return "\n".join(lines)


def render_json(plan: List[Dict[str, Any]], source: str) -> str:
    payload = {
        # 带时区，不然跨时区的同事对不上是哪一版
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": source,
        "total": len(plan),
        "interest_counts": {lv: sum(1 for p in plan if p["interest"] == lv)
                            for lv in ("高", "中", "低")},
        # 时间点只写相对时间，不编具体日期
        "windows": ["会后 2 小时内（T+2h）", "会后 12 小时内（T+12h）",
                    "会后 24 小时内（T+24h）"],
        "exhibitors": plan,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)




def build_parser() -> _ZhArgumentParser:
    p = _ZhArgumentParser(
        prog="trade_show.py",
        description="展会实战：把展会上收到的展商按兴趣度排成会后 24 小时跟进计划（只用标准库，不联网）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""可直接复制的例子:
  python scripts/trade_show.py --add "【示例】海湾轮胎贸易" --country "Saudi Arabia" --product "TBR 12.00R20" --interest 高 --email demo01@sample.example
  python scripts/trade_show.py --csv examples/trade_show_example.csv
  python scripts/trade_show.py --csv examples/leads_example.csv
  python scripts/trade_show.py --csv examples/trade_show_example.csv --format json --out plan.json

一次命令只加一家（--add 逐条加）；多家走 --csv 批量读。--csv 和 --add
可以混着用（先读 CSV 再加 --add 补一家）。兴趣度填 高/中/低（或
high/medium/low），不填按「低」处理。联系方式邮箱/电话/WhatsApp 至少留
一个，没留的排不进表。

官方名录批量背调（整份名录几百上千家都这么跑）：
  python scripts/trade_show.py --backcheck my_directory.csv --format csv --out backcheck_worksheet.csv
  python scripts/trade_show.py --backcheck my_directory.csv --format json
  python scripts/trade_show.py --backcheck my_directory.csv --format csv --pending-only --out pending_queue.csv
名录里没留联系方式的留成「待核实」占位行，不扔；只跳过公司名为空或重名
的行，每行都写清原因。背调字段（决策人/进口记录）没核实就标「没核实」；
名录里给了官网就直接用。--pending-only 只导出「待核实」队列（没留联系
方式、等背调补的行），序号仍用全表序号，能跟全表逐行对上。
表头认这些别名：公司名 company / Company Name / Exhibitor Name；产品
product / Product Section / Category；展位 booth / Stand Number；官网
website；地点 Location（"City, Country" 取逗号后一段当国家）。分隔符
逗号 / 分号 / 制表符都认。已核实（2026-11-26）：现届迪拜展官方名录只有
网页检索页，没有官方可下载的 CSV；唯一核实过的官方可下载文件是 2021 年
迪拜展 PDF（Company Name / Country / Booth Number 三列，无产品分区、无
联系方式），须先转成 CSV 再喂 --backcheck，这套表头本来就认。利雅得展
（2027-06-21–23）同样没找到官方可下载名录。先用 --backcheck 跑一遍看汇总再说。""")
    p.add_argument("--add", help="逐条加一家展商：--add 公司名（一次命令加一家）")
    p.add_argument("--country", help="国家（如 Saudi Arabia）")
    p.add_argument("--product", help="意向产品（如 TBR 12.00R20）")
    p.add_argument("--interest", help="兴趣度：高/中/低（或 high/medium/low），不填按「低」处理")
    p.add_argument("--email", help="邮箱")
    p.add_argument("--phone", help="电话")
    p.add_argument("--whatsapp", help="WhatsApp 号码")
    p.add_argument("--csv", help="展商 CSV（列名 company/country/product/contact/interest，"
                   "email/phone 列也认；照 examples/leads_example.csv 抄表头最省事）")
    p.add_argument("--backcheck", help="官方展商名录 CSV（official exhibitor directory)："
                   "整份名录批量读进来，每家产出一行背调占位行 + 进度汇总"
                   "（已处理/待核实/跳过）。没留联系方式的行留成「待核实」不扔掉；"
                   "只跳过公司名为空或重名的行，每行都写清原因。"
                   "Official exhibitor directory: batch-read the whole list, emit one"
                   " backcheck placeholder row per exhibitor plus a progress summary"
                   " (ready / pending / skipped).")
    p.add_argument("--pending-only", action="store_true",
                   help="只导出「待核实」队列（only the pending-verification rows: "
                   "no usable contact on file). Only with --backcheck; "
                   "seq numbers stay the full-list numbers so the queue "
                   "lines up with the full worksheet. 只在 --backcheck 下用；"
                   "序号仍用全表序号，能跟全表逐行对上。")
    p.add_argument("--format", choices=["table", "json", "csv"], default="table",
                   help="输出格式：table=跟进表/进度报告(默认) / json=给别的脚本用 / "
                   "csv=背调工作表（只在 --backcheck 下用）")
    p.add_argument("--out", help="把结果写到文件（两种格式都支持）")
    return p


def main() -> None:
    args = build_parser().parse_args()
    if args.pending_only and not args.backcheck:
        raise SystemExit("错误：--pending-only 只在 --backcheck 下用（待核实队列）。\n"
                         "  用法：python scripts/trade_show.py --backcheck "
                         "my_directory.csv --format csv --pending-only "
                         "--out pending_queue.csv")
    if args.backcheck:
        # Directory batch mode: --csv / --add do not mix with --backcheck —
        # the directory is a raw official list, the follow-up plan is built
        # from contacts on file, and mixing the two inputs in one run would
        # blur which rows came from where.
        # 名录批量模式：--csv / --add 不跟 --backcheck 混用——名录是原始官方
        # 名单，跟进表是按已有联系方式排的，一次命令混着跑就分不清行从哪来。
        if args.csv or args.add:
            raise SystemExit("错误：--backcheck 不跟 --csv / --add 混用。\n"
                             "  名录批量背调只用：python scripts/trade_show.py "
                             "--backcheck my_directory.csv\n"
                             "  排跟进表只用：python scripts/trade_show.py --csv my_leads.csv")
        try:
            directory = read_directory(args.backcheck)
        except TradeShowError as e:
            raise SystemExit("错误：%s" % e)
        summary = summarize_directory(directory)
        rows = build_backcheck_rows(directory, pending_only=args.pending_only)
        if args.format == "json":
            text = render_backcheck_json(rows, summary, args.backcheck,
                                         pending_only=args.pending_only)
        elif args.format == "csv":
            text = render_backcheck_csv(rows)
        else:
            text = render_backcheck_table(rows, summary, args.backcheck,
                                          pending_only=args.pending_only)
        if not text.endswith("\n"):
            text += "\n"
        sys.stdout.write(text)
        if args.out:
            try:
                with open(args.out, "w", encoding="utf-8", newline="") as f:
                    f.write(text)
            except OSError as e:
                raise SystemExit("错误：写不进「%s」：%s（换个目录，或先关掉打开它的 Excel）"
                                 % (args.out, e.strerror or e))
            print("已写入 %s" % args.out)
        return
    if not args.csv and not args.add:
        raise SystemExit("错误：名单是空的。\n"
                         "  逐条加一家：python scripts/trade_show.py --add \"【示例】海湾轮胎贸易\" "
                         "--country \"Saudi Arabia\" --product \"TBR 12.00R20\" --interest 高 "
                         "--email demo01@sample.example\n"
                         "  或批量读 CSV：python scripts/trade_show.py --csv my_exhibitors.csv\n"
                         "  或名录批量背调：python scripts/trade_show.py --backcheck my_directory.csv\n"
                         "  例子都在 --help 里，能直接复制。")
    exhibitors: List[Dict[str, Any]] = []
    csv_path = args.csv
    if args.format == "csv":
        # The csv worksheet only exists in --backcheck mode (it is a
        # backcheck worksheet, not a follow-up plan). Failing loudly here
        # beats silently printing a table the user did not ask for.
        # csv 工作表只在 --backcheck 模式下有（它是背调工作表，不是跟进表）：
        # 这里明确报错，比静默印一张没人要的表强。
        raise SystemExit("错误：--format csv 只在 --backcheck 下用（背调工作表）。\n"
                         "  排跟进表用 --format table 或 --format json；\n"
                         "  背调工作表用：python scripts/trade_show.py --backcheck "
                         "my_directory.csv --format csv --out backcheck_worksheet.csv")
    try:
        if csv_path:
            exhibitors.extend(read_exhibitors(csv_path))
        if args.add:
            exhibitors.append(make_exhibitor(
                args.add, args.country or "", args.product or "",
                args.interest or "", args.email or "", args.phone or "",
                args.whatsapp or ""))
    except TradeShowError as e:
        raise SystemExit("错误：%s" % e)

    try:
        plan = build_plan(exhibitors, csv_path)
    except TradeShowError as e:
        raise SystemExit("错误：%s" % e)

    text = render_json(plan, csv_path or "命令行 --add") if args.format == "json" \
        else render_table(plan)
    if not text.endswith("\n"):
        text += "\n"
    sys.stdout.write(text)

    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8", newline="") as f:
                f.write(text)
        except OSError as e:
            raise SystemExit("错误：写不进「%s」：%s（换个目录，或先关掉打开它的 Excel）"
                             % (args.out, e.strerror or e))
        print("已写入 %s" % args.out)


if __name__ == "__main__":
    main()
