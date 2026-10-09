#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lead_score.py — 客户线索 T0-T3 自动分级

给一批外贸线索，按「多快能成交」排优先级，并给出每一级的下一步动作。
只用标准库，Python 3.8+ 可直接跑。

用法见 --help（里面的例子都能直接复制）。

输入 CSV：company 这一列必须有，其余 country/product/source/email/phone/contact/
years/note 有就加分，没有也能跑。表头大小写、前后空格你随便写，脚本都认。
（邮箱格式不对就不算数；years 里填 2010 这种年份，会自动当成成立年份折算成年数。）

分级（满分 100）：联系方式 40 / 来源 30 / 采购信号 20 / 成熟度 10。权重集中在
CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W 四个常量里，想调只改那一块。
T0 立刻打（当天）· T1 本周 · T2 排期 · T3 养着，先补信息。
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import unicodedata
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# ================================================================ 权重总表
# 想改评分口径，只改这一块，改完务必跑一次：
#   python scripts/lead_score.py examples/leads_example.csv
# 改完跑一次：分布要是变了，说明你动到了业务口径，提 PR 时顺手写句理由就行。

# 联系方式 CONTACT_W（满分 40）：外贸第一问是「今天能不能联系上这个人」，
# 联系不上后面全是空的，所以权重最高。邮箱能发报价单留痕，电话能立刻确认需求。
CONTACT_W = {
    "email_phone": 40,  # 邮箱+电话：双通道，随时能推进
    "email_only": 28,   # 只有邮箱：能发开发信，等多久看运气
    "phone_only": 22,   # 只有电话：能打通，但发不了图文报价单
    # WhatsApp 加成：中东/非洲客户在 WA 上回消息比固话快得多，还能直发图片报价单。
    # 它是「加成」不是「档位」——以前 WA 被单独算作 10 分档，留了 WhatsApp 的客户
    # 反而不如留个固话的分高，那是错的。
    "wa_bonus": 4,
    "cap": 40,          # 封顶，防止这一项一家独大
}

# 来源可信度 SOURCE_W（满分 30）：有人背书 > 见过面 > 有真实进口记录 > 网上搜的。
SOURCE_W = {
    "referral": 30,    # 转介绍：有人替你背书，成交周期通常最短
    "trade_show": 26,  # 展会：见过面/换过名片，至少记得你是谁
    "customs": 22,     # 海关数据：真金白银进过货，需求和量级都可查
    "linkedin": 16,    # 领英：身份能验证，但采购意图弱
    "search": 10,      # 搜索：最泛，同行也都能搜到
    "unknown": 10,     # 填了没见过的词：按 search 记分，并在明细里标出来提醒你
}

# 采购信号 SIGNAL_W（满分 20，四组叠加后封顶）：光说要买，但不知道买什么、买多少、
# 谁说了算，都不算完整采购信号，所以这四件事分别给分。
SIGNAL_W = {
    "采购/求购信号": 5,  # 明确说要买：RFQ、询价、招标
    "明确品类词": 4,     # 提到具体品类：说明做的真是你这行
    "量级词": 3,         # 提到柜/吨：说明有真实走量需求
    "决策角色": 3,       # 对接人是采购/老板：能拍板，不用层层传话
    "cap": 20,
}
BUYING_SIGNALS = [
    ("采购/求购信号", ["rfq", "quotation request", "request for quote", "sourcing",
                       "looking for supplier", "tender", "enquiry", "inquiry",
                       "采购", "求购", "招标", "询价"]),
    ("明确品类词", ["tyre", "tire", "tube", "rim", "truck", "bus", "radial",
                    "轮胎", "钢圈", "内胎"]),
    ("量级词", ["container", "40hq", "20gp", "fcl", "lcl", "bulk",
                "ton", "pallet", "柜", "吨"]),
    ("决策角色", ["purchasing manager", "procurement", "buyer", "sourcing manager",
                  "采购经理", "总经理", "负责人"]),
]

# 公司成熟度 MATURITY_W（满分 10）：只代表「稳不稳」，不代表「要不要打」，所以权重
# 最低——一家开了 20 年但联系不上的公司，依然只能排 T3。
MATURITY_W = {"成立 10 年以上": 10, "成立 3-10 年": 7, "成立 1-3 年": 4,
              "成立不足 1 年/未知": 0}
MATURITY_STEPS = ((10, "成立 10 年以上"), (3, "成立 3-10 年"), (1, "成立 1-3 年"))

# 分级门槛：T0=80 意味着「联系方式拿满 + 来源靠谱 + 至少一条采购信号」才够格今天打。
# 只靠来源和信号堆不出 T0——联系不上的人不配占你今天的第一个小时。
TIER_RULES = {
    "T0": (80, "立刻打（当天）", "今天就发首触，别等"),
    "T1": (60, "本周打", "排进本周，今天准备文案"),
    "T2": (40, "排期打", "进 B 池，每天固定时段扫一遍"),
    "T3": (0, "先养后打", "信息不足，先补联系方式/需求再打"),
}
TIER_ORDER = ("T0", "T1", "T2", "T3")

# ================================================================ 校验用常量

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
# 只认整词的 wa/whatsapp。不能写 "wa" in phone——"+886 2 2758 xxxx" 里 Tai*wa*n
# 会命中，台湾客户会被误判成留了 WhatsApp。
WHATSAPP_RE = re.compile(r"(whats\s?app|\bwa\b|\bwm\b)", re.I)
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
PHONE_MIN_DIGITS = 7        # 有效电话至少 7 位数字，少于一律当没填
YEARS_AS_YEAR_ABOVE = 100   # years 填了比 100 还大的数，当成成立年份换算（如 2010）
MAX_CELL_CHARS = 2000       # 超长字段截断，防止一个巨长备注拖垮扫描
# 这些值都等于「没填」，不能因为格子里有字就算有联系方式
PLACEHOLDERS = {"", "-", "--", "---", "/", "n/a", "na", "n.a.", "none", "null",
                "nil", "unknown", "tbd", "?", "??", "待定", "待补", "暂无",
                "未知", "无", "不知道", "未填写"}
# 读不懂的编码就按这个顺序回退，最后一项 latin-1 永不失败，用来兜底不崩
FALLBACK_ENCODINGS = ("utf-8-sig", "gb18030", "utf-8", "big5", "latin-1")


# ---------------------------------------------------------------- 小工具
def _get(row: Dict[str, Any], key: str, default: str = "") -> str:
    """不区分大小写、忽略前后空格地取列值（写 ' Company ' 也认）；列不存在返回 default。"""
    target = key.strip().lower()
    for col, value in row.items():
        if col is not None and str(col).strip().lower() == target:
            return _clean(value)
    return default

def _clean(value: Any) -> str:
    """单元格内容 -> 去掉首尾空白的字符串。None 变空串，超长字段截断。"""
    if value is None:
        return ""
    text = str(value).strip()
    return text[:MAX_CELL_CHARS] if len(text) > MAX_CELL_CHARS else text

def _is_filled(value: str) -> bool:
    """格子里有字不等于真填了：「-」「n/a」「待补」这类占位符一律算没填。"""
    return value.strip().lower() not in PLACEHOLDERS

def _has_email(row: Dict[str, Any]) -> bool:
    """邮箱既要填了，也要格式对。写错的邮箱等于没有邮箱，不能白送分。"""
    email = _get(row, "email")
    return _is_filled(email) and bool(EMAIL_RE.match(email))

def _has_phone(row: Dict[str, Any]) -> bool:
    """电话至少要有 7 位数字，否则当成没填。"""
    phone = _get(row, "phone")
    return _is_filled(phone) and sum(c.isdigit() for c in phone) >= PHONE_MIN_DIGITS

def _years(row: Dict[str, Any]) -> float:
    """取成立年数：填 '18年' / '18 years' 都能读；填年份（如 2010）自动换算。"""
    raw = _get(row, "years")
    if not _is_filled(raw):
        return 0.0
    match = NUMBER_RE.search(raw)
    if not match:
        return 0.0
    value = float(match.group())
    if value > YEARS_AS_YEAR_ABOVE:
        value = float(datetime.now().year) - value
    return max(0.0, value)


# ---------------------------------------------------------------- 四项打分

def score_contact(row: Dict[str, Any]) -> Tuple[int, str]:
    """联系方式（封顶 40）。决定「今天能不能联系上这个人」。"""
    email, phone = _has_email(row), _has_phone(row)
    if email and phone:
        pts, label = CONTACT_W["email_phone"], "邮箱+电话"
    elif email:
        pts, label = CONTACT_W["email_only"], "只有邮箱"
    elif phone:
        pts, label = CONTACT_W["phone_only"], "只有电话"
    else:
        return 0, "都联系不上"
    if WHATSAPP_RE.search(_get(row, "phone")):
        pts += CONTACT_W["wa_bonus"]
        label += "+WhatsApp"
    return min(pts, CONTACT_W["cap"]), label

def score_source(row: Dict[str, Any]) -> Tuple[int, str]:
    """来源可信度（最高 30）。没填按最泛的 search 记；填了不认识的词会标出来。"""
    raw = _get(row, "source").strip().lower()
    if not _is_filled(raw):
        raw = "search"
    if raw in SOURCE_W:
        return SOURCE_W[raw], raw
    return SOURCE_W["unknown"], "%s(未识别)" % raw

def score_buying(row: Dict[str, Any]) -> Tuple[int, List[str]]:
    """采购信号（封顶 20）。四组关键词各加各的分，命中越多说明越接近下单。"""
    # 故意不扫 company：公司名叫「XX轮胎」不代表它现在要买，
    # 把公司名算进采购信号，等于让线索自己给自己加分。
    blob = " ".join([_get(row, "note"), _get(row, "product"),
                     _get(row, "contact")]).lower()
    pts, hits = 0, []
    for label, keywords in BUYING_SIGNALS:
        if any(k in blob for k in keywords):
            pts += SIGNAL_W[label]
            hits.append(label)
    return min(pts, SIGNAL_W["cap"]), hits

def score_maturity(row: Dict[str, Any]) -> Tuple[int, str]:
    """公司成熟度（最高 10）。只影响「稳不稳」，不影响「打不打」。"""
    years = _years(row)
    for floor, label in MATURITY_STEPS:
        if years >= floor:
            return MATURITY_W[label], label
    return MATURITY_W["成立不足 1 年/未知"], "成立不足 1 年/未知"

def score_lead(row: Dict[str, Any]) -> Tuple[int, Dict[str, str]]:
    """给一条线索打分，返回 (总分, 各分项明细)。"""
    contact, contact_label = score_contact(row)
    source, source_label = score_source(row)
    buying, buying_hits = score_buying(row)
    maturity, maturity_label = score_maturity(row)

    total = contact + source + buying + maturity
    detail = {
        "联系方式": "%s/%d" % (contact_label, contact),
        "来源": "%s/%d" % (source_label, source),
        "采购信号": "%s/%d" % ("+".join(buying_hits) or "无", buying),
        "公司成熟度": "%s/%d" % (maturity_label, maturity),
    }
    return total, detail

def grade(total: int) -> str:
    """总分 -> T0-T3。从高到低比对门槛，够线就归这一级。"""
    for tier in TIER_ORDER:
        if total >= TIER_RULES[tier][0]:
            return tier
    return "T3"


# ---------------------------------------------------------------- 主流程
class LeadDataError(Exception):
    """CSV 读不出来、缺列、没数据。main 会把它翻成人话再退出。"""

def _decode(raw: bytes) -> Tuple[str, str]:
    """按 UTF-8 -> GB18030 -> ... 猜编码，返回 (文本, 实际编码名)。
    Excel 在中文 Windows 上另存的是 GBK，不回退的话新人只会看到看不懂的报错。"""
    for encoding in FALLBACK_ENCODINGS:
        try:
            return raw.decode(encoding), encoding
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8(容错)"

def read_leads(path: str) -> List[Dict[str, Any]]:
    """读成「一行一个 dict」。容错：编码自动回退 GB18030；表头大小写/空格/空列名/
    重复列名都能处理；表头前以 # 开头的行当免责声明跳过；支持引号字段与超长字段。"""
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except FileNotFoundError:
        raise LeadDataError("找不到文件「%s」。\n"
                            "  检查一下路径拼写。Windows 上可以直接把文件拖进终端，"
                            "路径会自动填好。" % path)
    except OSError as e:
        raise LeadDataError("打不开文件「%s」：%s\n"
                            "  文件可能正被 Excel 打开着，先关掉再试。"
                            % (path, e.strerror or e))
    if not raw.strip():
        raise LeadDataError("文件是空的：%s" % path)

    text, encoding = _decode(raw)
    if encoding not in ("utf-8-sig", "utf-8"):
        print("提示：这个 CSV 不是 UTF-8，已按 %s 读取。"
              "以后用 Excel 另存时选「CSV UTF-8」就不用猜了。" % encoding)

    # 备注里可能贴了一整封邮件，把单字段上限抬高一档，别让 csv 直接抛错
    try:
        csv.field_size_limit(min(sys.maxsize, 10 ** 7))
    except (OverflowError, ValueError):
        pass

    reader = csv.reader(io.StringIO(text, newline=""))
    header: Optional[List[str]] = None
    records: List[Dict[str, Any]] = []
    for row_values in reader:
        # 跳过完全空白的行（表头前后都跳）
        if not row_values or all((c or "").strip() == "" for c in row_values):
            continue
        # 表头尚未确定时，# 开头的行当作免责声明注释跳过
        if header is None:
            if (row_values[0] or "").lstrip().startswith("#"):
                continue
            header = [h.strip() or "第%d列" % (i + 1)
                      for i, h in enumerate(row_values)]
            seen, dups = set(), []
            for name in header:  # 重名列只认第一列的值
                if name.lower() in seen:
                    dups.append(name)
                seen.add(name.lower())
            if dups:
                print("警告：表头有重复列名 %s，只保留第一列的值。" % "、".join(dups))
            continue
        record: Dict[str, Any] = {}
        for col, value in zip(header, row_values):
            if col not in record:
                record[col] = value
        records.append(record)

    if header is None:
        raise LeadDataError("这个 CSV 没有表头行（第一行得是列名，比如 company,country）。")
    if "company" not in [h.lower() for h in header]:
        raise LeadDataError("CSV 缺少 company 列（写 Company / COMPANY / ' company ' 都行，"
                            "照 examples/leads_example.csv 抄表头最省事）。")

    rows = [r for r in records if any(_clean(v) for v in r.values())]
    if not rows:
        raise LeadDataError("表头读到了，但下面一行数据都没有。")
    return rows

def analyze(rows: List[Dict[str, Any]], country: Optional[str] = None,
            product: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
    """筛 -> 打分 -> 分级 -> 排序。返回 (结果列表, 被合并掉的重复条数)。"""
    results: List[Dict[str, Any]] = []
    seen: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    duplicates = 0

    for row in rows:
        if country and country.strip().lower() not in _get(row, "country").lower():
            continue
        if product and product.strip().lower() not in _get(row, "product").lower():
            continue

        # 公司名 + 邮箱 + 电话数字，三样都一样就是同一条线索重复录入了
        key = (_get(row, "company").strip().lower(), _get(row, "email").strip().lower(),
               "".join(c for c in _get(row, "phone") if c.isdigit()))
        if key in seen:
            # 只留第一条，记下重复次数，别让新人同一家打两遍
            seen[key]["dup_count"] += 1
            duplicates += 1
            continue

        total, detail = score_lead(row)
        tier = grade(total)
        item = {
            "company": _get(row, "company") or "(未填公司名)",
            "country": _get(row, "country") or "?",
            "product": _get(row, "product"),
            "source": score_source(row)[1],
            "email": _get(row, "email"),
            "tier": tier,
            "score": total,
            "next": TIER_RULES[tier][1],
            "action": TIER_RULES[tier][2],
            "dup_count": 1,
            "detail": detail,
        }
        results.append(item)
        seen[key] = item

    # 先按分数从高到低；同分再按公司名、国家排，保证每次跑出来的顺序一样，
    # 不会因为 CSV 里行的先后顺序变了就换一排（排得稳，才能跟上次对比）。
    results.sort(key=lambda x: (-x["score"], x["company"], x["country"]))
    return results, duplicates


# ---------------------------------------------------------------- 输出排版

def _wide(ch: str) -> bool:
    return unicodedata.east_asian_width(ch) in ("W", "F")

def _fit(text: str, width: int, right: bool = False) -> str:
    """按终端显示宽度补齐：中文占 2 列、英文占 1 列，所以用 %-26s 那种按字符数
    补齐的写法一定会歪。放不下的截断加省略号。"""
    if sum(2 if _wide(c) else 1 for c in text) > width:
        kept, used = "", 0
        for ch in text:
            used += 2 if _wide(ch) else 1
            if used > width - 1:
                break
            kept += ch
        text = kept + "…"
    pad = " " * (width - sum(2 if _wide(c) else 1 for c in text))
    return pad + text if right else text + pad

def _names_of(results: List[Dict[str, Any]], tier: str) -> str:
    """某一级的公司名用顿号串起来；一个都没有就写「无」。"""
    names = [r["company"] for r in results if r["tier"] == tier]
    return "、".join(names) if names else "无"

def render_table(results: List[Dict[str, Any]], duplicates: int = 0) -> str:
    if not results:
        return "\n没筛出线索。把 --country / --product 收一收，或者干脆不加这俩参数再跑一遍——筛太狠，一条都捞不着也正常。\n"

    total = len(results)
    counts = {t: sum(1 for r in results if r["tier"] == t) for t in TIER_ORDER}

    def row(idx, tier, company, country, score, action):
        return "  %s %s %s %s %s  %s" % (
            _fit(str(idx), 3), _fit(tier, 4), _fit(company, 28),
            _fit(country, 14), _fit(score, 5, right=True), action)

    lines = ["=" * 84,
             "  线索分级结果   共 %d 条 · 今天先打 %d 家 · 本周再加 %d 家"
             % (total, counts["T0"], counts["T1"]),
             "=" * 84,
             # 表头写「今天/本周该做什么」而不是「下一步」——新人要的是动作不是字段名
             row("#", "分级", "公司", "国家", "得分", "今天/本周该做什么"),
             "-" * 84]
    lines += [row(i, r["tier"], r["company"], r["country"], str(r["score"]),
                  r["action"]) for i, r in enumerate(results, 1)]
    lines += ["-" * 84,
              "  汇总: " + " / ".join("%s:%d" % (t, counts[t]) for t in TIER_ORDER)
              + "  （" + " · ".join("%s %.0f%%" % (t, counts[t] * 100.0 / total)
                                    for t in TIER_ORDER) + "）",
              "",
              "  今天先打: %s" % _names_of(results, "T0"),
              "  本周跟进: %s" % _names_of(results, "T1"),
              "  先别碰  : %s（信息不全，补完再说）" % _names_of(results, "T3")]
    if duplicates:
        lines += ["", "  注意：有 %d 条重复线索已自动合并（同一家公司 + 相同联系方式）。"
                  % duplicates]
    lines += ["", "  下一步: 用 outreach_gen.py 按这份分级生成建联文案。", "=" * 84, ""]
    return "\n".join(lines)

def render_detail(results: List[Dict[str, Any]], duplicates: int = 0) -> str:
    if not results:
        return "\n没筛出线索。把 --country / --product 收一收，或者干脆不加这俩参数再跑一遍——筛太狠，一条都捞不着也正常。\n"

    lines = []
    for r in results:
        lines.append("[%s] %s  (%s，%d 分)"
                     % (r["tier"], r["company"], r["country"], r["score"]))
        lines += ["     %s %s" % (_fit(k, 12), v) for k, v in r["detail"].items()]
        lines.append("     %s %s" % (_fit("下一步", 12), r["action"]))
        if r["dup_count"] > 1:
            lines.append("     %s 这条在 CSV 里重复了 %d 次"
                         % (_fit("提示", 12), r["dup_count"]))
        lines.append("")
    if duplicates:
        lines.append("共合并掉 %d 条重复线索。" % duplicates)
    return "\n".join(lines)

def render_csv(results: List[Dict[str, Any]], duplicates: int = 0) -> str:
    """导出成 CSV，方便丢回 Excel 排班。"""
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["tier", "company", "country", "product", "source",
                     "email", "score", "next", "action", "detail"])
    for r in results:
        writer.writerow([r["tier"], r["company"], r["country"], r["product"],
                         r["source"], r["email"], r["score"], r["next"],
                         r["action"],
                         " ; ".join("%s:%s" % (k, v) for k, v in r["detail"].items())])
    return buf.getvalue()

def render_json(results: List[Dict[str, Any]], source_file: str,
                duplicates: int = 0) -> str:
    payload = {
        # 带时区，不然跨时区的同事对不上是哪一版
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_file": source_file,
        "total": len(results),
        "duplicates_merged": duplicates,
        "tier_counts": {t: sum(1 for r in results if r["tier"] == t)
                        for t in TIER_ORDER},
        "leads": results,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)

class _ZhArgumentParser(argparse.ArgumentParser):
    """argparse 默认报错是英文，包一层，给新人一句能看懂的话。"""

    def error(self, message: str):  # type: ignore[override]
        self.print_usage(sys.stderr)
        raise SystemExit(
            "\n参数没写对：%s\n"
            "  不知道怎么填就跑：python %s --help（里面有能直接复制的例子）"
            % (message, os.path.basename(sys.argv[0]) or "lead_score.py"))

def build_parser() -> _ZhArgumentParser:
    p = _ZhArgumentParser(
        prog="lead_score.py",
        description="客户线索 T0-T3 自动分级（只用标准库，不联网）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""可直接复制的例子:
  python scripts/lead_score.py examples/leads_example.csv               # 今天该打谁
  python scripts/lead_score.py examples/leads_example.csv --format detail # 分数怎么来的
  python scripts/lead_score.py examples/leads_example.csv --format csv --out 待打清单.csv
  python scripts/lead_score.py examples/leads_example.csv --format json --out scored.json
  python scripts/lead_score.py my_leads.csv --country Saudi --product tyres

输入 CSV 至少要有一列叫 company，其余列（country/product/source/email/phone/
contact/years/note）有就加分、没有也能跑。照 examples/leads_example.csv 抄表头最省事。""")
    p.add_argument("csv_path", help="线索 CSV 的路径")
    p.add_argument("--country", help="只筛某个国家（子串匹配，忽略大小写，如 Saudi）")
    p.add_argument("--product", help="只筛某类产品（子串匹配，忽略大小写，如 tyres）")
    p.add_argument("--format", choices=["table", "detail", "csv", "json"],
                   default="table",
                   help="输出格式：table=表格(默认) / detail=逐条看分数来源 / "
                        "csv=导出 Excel / json=给别的脚本用")
    p.add_argument("--out", help="把结果写到文件（四种格式都支持，不只是 json）")
    return p

def main() -> None:
    args = build_parser().parse_args()
    try:
        rows = read_leads(args.csv_path)
    except LeadDataError as e:
        raise SystemExit("错误：%s" % e)

    results, duplicates = analyze(rows, args.country, args.product)
    if args.format == "json":
        text = render_json(results, args.csv_path, duplicates)
    elif args.format == "csv":
        text = render_csv(results, duplicates)
    elif args.format == "detail":
        text = render_detail(results, duplicates)
    else:
        text = render_table(results, duplicates)

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
