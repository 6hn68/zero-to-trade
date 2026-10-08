#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lead_score.py — 客户线索 T0-T3 自动分级

给一批外贸线索，按「多快能成交」排优先级，并给出每一级的下一步动作。
只用标准库，Python 3.8+ 可直接跑。

用法:
    python scripts/lead_score.py examples/leads_example.csv
    python scripts/lead_score.py my_leads.csv --format json
    python scripts/lead_score.py my_leads.csv --country Saudi --product tyres

输入 CSV 必备列（表头名不区分大小写、多余列会被忽略）:
    company       公司名（必填）
    country       国家（必填，可留空不影响运行）
    product       主营产品（可选）
    source        线索来源：referral / trade_show / linkedin / customs / search
    email         邮箱（可选，有则加分）
    phone         电话（可选）
    contact       对接人/角色（可选，参与采购信号关键词命中）
    years         成立年数（可选）
    note          备注（可选，会被关键词命中影响分级）

分级逻辑（满分 100，四项加权）:
    联系方式完整度40 / 来源可信度 30 / 采购信号 20 / 公司成熟度 10

分级含义:
    T0 立刻打（当天）· T1 本周 · T2 排期 · T3 养着，先补信息
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime

# ---------------------------------------------------------------- 分级规则

TIER_RULES = {
    "T0": (80, "立刻打（当天）", "今天就发首触，别等"),
    "T1": (60, "本周打", "排进本周，今天准备文案"),
    "T2": (40, "排期打", "进 B 池，每天固定时段扫一遍"),
    "T3": (0,  "先养后打", "信息不足，先补联系方式/需求再打"),
}

# 来源可信度打分
SOURCE_SCORE = {
    "referral":   30,   # 客户转介绍 —— 最强的信任背书
    "trade_show": 26,   # 展会名录 —— 见过面/留过名片
    "customs":    22,   # 海关数据 —— 有真实进口记录
    "linkedin":   16,   # 领英 —— 身份可验证但采购意图弱
    "search":     10,   # 搜索引擎 —— 最泛
}

# 联系方式完整度打分（最多 40）
CONTACT_POINTS = [
    (40, "email+phone",  lambda r: bool(_get(r, "email")) and bool(_get(r, "phone"))),
    (28, "email",        lambda r: bool(_get(r, "email"))),
    (10, "wa",           lambda r: "wa" in str(_get(r, "phone", "")).lower()
                                     or "whatsapp" in str(_get(r, "phone", "")).lower()),
    (22, "phone",        lambda r: bool(_get(r, "phone"))),
    (0,  "none",         lambda r: True),
]

# 采购信号关键词（命中越多分越高，上限 20）
BUYING_SIGNALS = [
    (5, "采购/求购信号", ["rfq", "quotation request", "request for quote", "sourcing",
                          "looking for supplier", "tender", "enquiry", "inquiry",
                          "采购", "求购", "招标", "询价"]),
    (4, "明确品类词",   ["tyre", "tire", "tube", "rim", "truck", "bus", "radial",
                          "轮胎", "钢圈", "内胎"]),
    (3, "量级词",       ["container", "40hq", "20gp", "fcl", "lcl", "bulk",
                          "ton", "pallet", "柜", "吨"]),
    (3, "决策角色",     ["purchasing manager", "procurement", "buyer", "sourcing manager",
                          "采购经理", "总经理", "负责人"]),
]

# 成熟度打分（上限 10）
MATURITY_RULES = [
    (10, "成立 10 年以上", lambda r: _num(r, "years") >= 10),
    (7,  "成立 3-10 年",   lambda r: _num(r, "years") >= 3),
    (4,  "成立 1-3 年",    lambda r: _num(r, "years") >= 1),
    (0,  "成立不足 1 年/未知", lambda r: True),
]

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")


# ---------------------------------------------------------------- 小工具

def _get(row, key, default=""):
    """不区分大小写取列值。"""
    for k, v in row.items():
        if k and k.strip().lower() == key.lower():
            return (v or default) if v is not None else default
    return default


def _num(row, key):
    raw = _get(row, key, "")
    try:
        return float(str(raw).strip())
    except (TypeError, ValueError):
        return 0.0


def score_lead(row):
    """给一条线索打分，返回 (总分, 各分项明细)。"""
    contact = 0
    contact_label = "none"
    for pts, label, test in CONTACT_POINTS:
        if test(row):
            contact, contact_label = pts, label
            break

    source_raw = _get(row, "source", "search").strip().lower()
    source = SOURCE_SCORE.get(source_raw, 10)

    note_blob = " ".join([
        _get(row, "note", ""), _get(row, "product", ""),
        _get(row, "company", ""), _get(row, "contact", ""),
    ]).lower()

    buying = 0
    buying_hits = []
    for pts, label, kws in BUYING_SIGNALS:
        if any(k in note_blob for k in kws):
            buying += pts
            buying_hits.append(label)
    buying = min(buying, 20)

    maturity = 0
    maturity_label = "未知"
    for pts, label, test in MATURITY_RULES:
        if test(row):
            maturity, maturity_label = pts, label
            break

    # 邮箱格式校验：写错的邮箱不算联系方式
    email = _get(row, "email", "").strip()
    email_ok = bool(EMAIL_RE.match(email))
    if email and not email_ok and contact_label in ("email", "email+phone"):
        contact = max(0, contact - 18)
        contact_label += "(格式存疑)"

    total = contact + source + buying + maturity
    detail = {
        "联系方式": "%s/%d" % (contact_label, contact),
        "来源": "%s/%d" % (source_raw or "search", source),
        "采购信号": ("%s/%d" % ("+".join(buying_hits) or "无", buying)),
        "公司成熟度": "%s/%d" % (maturity_label, maturity),
    }
    return total, detail


def grade(total):
    for tier in ("T0", "T1", "T2", "T3"):
        floor = TIER_RULES[tier][0]
        if total >= floor:
            return tier
    return "T3"


# ---------------------------------------------------------------- 主流程

def read_leads(path):
    """读 CSV。表头（第一行有效数据）之前以 # 开头的行视为免责声明注释并跳过；
    表头确定后，即使某条数据公司名以 # 开头也照常读入，不会被静默吞掉。
    用 csv 模块逐行解析，支持带引号字段与多行字段。"""
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = None
        records = []
        for raw in reader:
            # 跳过完全空白的行（表头前后都跳）
            if not raw or all((c or "").strip() == "" for c in raw):
                continue
            # 表头尚未确定时，# 开头的行当作免责声明注释跳过
            if header is None:
                if (raw[0] or "").lstrip().startswith("#"):
                    continue
                header = [h.strip() for h in raw]
                continue
            records.append(dict(zip(header, raw)))

    if header is None:
        raise SystemExit("错误：CSV 为空或没有表头行，无法读取数据。")
    if "company" not in [h.lower() for h in header]:
        raise SystemExit("错误：CSV 缺少 company 列。表头示例见 examples/leads_example.csv")

    rows = [r for r in records if any((v or "").strip() for v in r.values())]
    if not rows:
        raise SystemExit("错误：CSV 里没有读到任何有效数据行。")
    return rows


def analyze(rows, country=None, product=None):
    out = []
    for row in rows:
        if country and country.lower() not in _get(row, "country", "").lower():
            continue
        if product and product.lower() not in _get(row, "product", "").lower():
            continue
        total, detail = score_lead(row)
        tier = grade(total)
        out.append({
            "company": _get(row, "company", "(未命名)"),
            "country": _get(row, "country", "?"),
            "product": _get(row, "product", ""),
            "email": _get(row, "email", ""),
            "tier": tier,
            "score": total,
            "next": TIER_RULES[tier][1],
            "action": TIER_RULES[tier][2],
            "detail": detail,
        })
    out.sort(key=lambda x: (-x["score"], x["company"]))
    return out


def print_table(results):
    if not results:
        print("没有符合条件的线索。")
        return

    counts = {"T0": 0, "T1": 0, "T2": 0, "T3": 0}
    for r in results:
        counts[r["tier"]] += 1

    print("")
    print("=" * 74)
    print("  线索分级结果  共 %d 条" % len(results))
    print("=" * 74)
    print("%-4s %-26s %-14s %5s  %s" % ("分级", "公司", "国家", "得分", "下一步"))
    print("-" * 74)
    for r in results:
        name = r["company"][:24] + ("…" if len(r["company"]) > 24 else "")
        print("%-4s %-26s %-14s %5d  %s" % (
            r["tier"], name, r["country"][:12], r["score"], r["action"]))
    print("-" * 74)
    print("汇总: T0:%d / T1:%d / T2:%d / T3:%d" % (
        counts["T0"], counts["T1"], counts["T2"], counts["T3"]))
    print("")
    print("先回谁: " + "、".join(r["company"] for r in results if r["tier"] == "T0") or "无")
    print("先打谁: " + "、".join(r["company"] for r in results if r["tier"] == "T1") or "无")
    print("")
    print("下一步: 用 outreach_gen.py 按这份分级生成建联文案。")
    print("=" * 74)
    print("")


def print_detail(results):
    for r in results:
        print("[%s] %s  (%s, %d 分)" % (r["tier"], r["company"], r["country"], r["score"]))
        for k, v in r["detail"].items():
            print("     %-8s %s" % (k, v))
        print("     %-8s %s" % ("下一步", r["action"]))
        print("")


def main():
    p = argparse.ArgumentParser(
        description="客户线索 T0-T3 自动分级（只用标准库）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python scripts/lead_score.py examples/leads_example.csv")
    p.add_argument("csv_path", help="线索 CSV 路径")
    p.add_argument("--country", help="只筛某个国家（子串匹配，忽略大小写）")
    p.add_argument("--product", help="只筛某类产品（子串匹配，忽略大小写）")
    p.add_argument("--format", choices=["table", "json", "detail"], default="table",
                   help="输出格式，默认 table")
    p.add_argument("--out", help="把 JSON 结果写到文件")
    args = p.parse_args()

    if args.out and args.format != "json":
        print("提示：--out 仅对 --format json 生效，本次未写入文件。")

    try:
        rows = read_leads(args.csv_path)
    except OSError as e:
        raise SystemExit("错误：无法读取文件 %s\n  %s" % (args.csv_path, e))

    results = analyze(rows, args.country, args.product)

    if args.format == "json":
        payload = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "source_file": args.csv_path,
            "total": len(results),
            "tier_counts": {t: sum(1 for r in results if r["tier"] == t)
                            for t in ("T0", "T1", "T2", "T3")},
            "leads": results,
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2)
        print(text)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(text)
            print("\n已写入 %s" % args.out)
    elif args.format == "detail":
        print_detail(results)
    else:
        print_table(results)


if __name__ == "__main__":
    main()
