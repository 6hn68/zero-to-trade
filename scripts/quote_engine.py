#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算报价的。给你成本、运费、想要的加成，它吐出 FOB / CIF 报价和底价，
外加一套三档让步阶梯——每降一档都得从客户那儿换回点东西，空手降的价等于白送。

只用了标准库，Python 3.8 往上都能直接跑，不联网。

用法:
    python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
    python scripts/quote_engine.py --cost 28 --freight 6 --margin 15 --anchor 42 --format json
    python scripts/quote_engine.py --cost 200 --currency CNY --fx 0.14 --freight 6
    python scripts/quote_engine.py --cost 28 --freight 6 --audience client --out quote.txt

参数:
    --cost          单位成本（工厂/EXW 价），必填，币种由 --currency/--fx 决定
    --freight       到目的港海运费（每单位），默认 0
    --margin        成本加成百分比（报价 = 成本基数 ×(1+margin)），默认 15
    --insurance     保险费率（占 CIF 货值的百分比 %），默认 0.15（海运险通常 0.1%–0.3%）
    --insurance-rate  高级入口：保险费率（比率），如 0.0015 = 0.15%，可覆盖 --insurance
    --local         本地费用（报关/拖车/港杂，每单位），默认 0
    --contingency   不可预见费比例，默认 0.03
    --anchor        竞品锚价（报价币种，可选），给了就多一句定位建议
    --fx            汇率：1 单位「成本币种」= fx 「报价币种」（成本 CNY、报价 USD 时填 0.14）。
                    换算只在最开头做一次，之后全程不再碰汇率，绝不重复乘 margin。
    --currency      报价币种符号，默认 USD
    --unit          计价单位，默认 件
    --moq           最小起订量（报价单必带字段，可选）
    --lead-time     交货期（如 "25天"，可选）
    --validity      报价有效期天数，默认 30
    --audience      internal(默认，含成本与底价) / client(客户视图，底价打死不出现)
    --out           同时写入文件（UTF-8），不指定则只打印
    --format        table(默认) / json

两条规矩：
    底价只在 internal 视图里露脸，发客户记得加 --audience client，别把底价寄出去。
    让步必须换条件，量 / 账期 / 排他 / 长约换一样都行，就是不能白降。
"""

import argparse
import json
import unicodedata
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# 可调常量：要改默认数值就动这边
DEFAULT_MARGIN_PCT = 15.0        # 默认成本加成 %
DEFAULT_INSURANCE_PCT = 0.15     # 默认保险费率（占 CIF 货值的百分比）
INSURANCE_COVER_FACTOR = 1.10    # 投保加成：按 CIF 货值 110% 投保（行业惯例 110%）
DEFAULT_CONTINGENCY = 0.03       # 不可预见费比例（叠在成本上）
MAX_INSURANCE_RATE = 0.05        # 费率 >5% 判定为「单位输错」，直接报错
MAX_CONCESSION_PCT = 6.0         # 底价 = 报价 ×(1-6%)，且永不低于成本基数
LADDER_CUTS = (2.5, 1.5, 1.0)    # 三档让步的「增量」，递减节奏；累计 5% < 底价 6%
QUOTE_VALIDITY_DAYS = 30         # 报价有效期默认天数
DEFAULT_PAYMENT_TERMS = "T/T 30% 定金 + 70% 见提单副本；或即期 L/C"
DEFAULT_CURRENCY = "USD"         # 输出币种符号（所有金额都带，不让新人猜）
DEFAULT_UNIT = "件"              # 计价单位

LADDER_CONDITIONS = (
    "首单 ≥ 1 个柜（20GP/40HQ）且接受 30% 定金",
    "由试订单升级为年度框架 / 量翻倍以上",
    "签 1–3 年排他或独家代理（区域保护换低价）",
)


def money(x):
    """金额统一「四舍五入到分」。用 Decimal 而非 round()：
    round() 是银行家舍入（round(2.675, 2) == 2.67），还会留下 31.179999 这类浮点尾巴。"""
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def fmt(x):
    """金额显示：固定两位小数（31.1 不会被打印成 31.1，避免列错位）。"""
    return "%.2f" % money(x)


def _width(s):
    """终端显示宽度：中文/全角按 2 计，否则按 1 计。"""
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)


def _pad(s, width):
    return s + " " * max(0, width - _width(s))


def build_quote(cost, freight, margin, insurance_rate, local=0.0,
                contingency=DEFAULT_CONTINGENCY, anchor=None,
                cover_factor=INSURANCE_COVER_FACTOR,
                max_concession=MAX_CONCESSION_PCT,
                ladder_cuts=LADDER_CUTS):
    """算 FOB / CIF 报价与底价 + 三档让步阶梯。

    计价链路（严格按顺序，每步只做一次）:
        cost ──×fx(调用方已换算)──> 成本 ──×(1+不可预见)+本地费──> 成本基数
             ──×(1+加成%)──> FOB ──(FOB+运费)/(1-投保加成×费率)──> CIF
    汇率只在最开头介入一次，之后不再参与，因此不存在「换算后重复乘 margin」。
    """
    # 输入校验：错了就直接报错，绝不悄悄塞个错报价出去
    if cost <= 0:
        raise ValueError("成本必须 > 0")
    if freight < 0:
        raise ValueError("海运费不能为负（负数会让 CIF 低于 FOB）")
    if local < 0:
        raise ValueError("本地费用不能为负")
    if margin < 0:
        raise ValueError("成本加成不能为负（负加成 = 亏本报价）")
    if contingency < 0:
        raise ValueError("不可预见费比例不能为负")
    if insurance_rate < 0:
        raise ValueError("保险费率不能为负")
    if insurance_rate > MAX_INSURANCE_RATE:
        raise ValueError("保险费率 %.3f%% 异常(>%.0f%%)？新手常把 0.3%% 输成 0.3。"
                         " --insurance 收的是百分比数值。" % (insurance_rate * 100,
                                                         MAX_INSURANCE_RATE * 100))

    # ---- 成本基数：不可预见费 + 本地费先叠进成本（海运费不进 FOB）
    cost_base = cost * (1 + contingency) + local
    # ---- FOB：成本加成(markup)，不是毛利率(gross margin)，见下方 margin_mode 说明
    fob = cost_base * (1 + margin / 100.0)
    # ---- CIF：保险按 CIF 货值的 110% 投保 → CIF = (FOB+运费) / (1 - 投保加成×费率)
    denom = 1 - cover_factor * insurance_rate
    if denom <= 0:
        # 费率太高时分母变负，CIF 没法算，直接报错，不当老好人硬给个结果
        raise ValueError("保险费率过高(≥ %.1f%%)导致 CIF 分母非正，请检查 --insurance 单位"
                         % (100.0 / cover_factor))
    cif = (fob + freight) / denom
    insurance = cif * cover_factor * insurance_rate
    # 自检：CIF 必须等于 FOB+运费+保险费（防止公式写错却看不出来）
    if abs(cif - (fob + freight + insurance)) > 0.005:
        raise ValueError("CIF 恒等式校验失败，请检查投保加成参数")

    warnings = []

    # ---- 底价：报价 ×(1-最大让步)，且永不低于成本基数（宁可没空间，也不报亏本价）
    fob_floor_raw = fob * (1 - max_concession / 100.0)
    fob_floor = money(max(fob_floor_raw, cost_base))
    if fob_floor_raw < cost_base:
        warnings.append("加成只有 %.2f%%，撑不住 %.1f%% 的底价空间：底价已按「不亏本」"
                        "锁到成本基数 %s，本单实际没有让步空间。"
                        % (margin, max_concession, fmt(cost_base)))
    # CIF 底价用「FOB 底价」重算，而不是 CIF 直接打折 —— 否则连运费一起打了折
    cif_floor = money((fob_floor + freight) / denom)

    # ---- 三档让步阶梯：增量递减(2.5→1.5→1.0)，累计 5% < 底价 6%，永远留一手
    ladder = []
    cum = 0.0
    for i, cut in enumerate(ladder_cuts):
        cum += cut
        new_fob_raw = fob * (1 - cum / 100.0)
        new_fob = money(max(new_fob_raw, cost_base))
        if new_fob_raw < cost_base:
            warnings.append("第 %d 档让步(-%.1f%%) 已跌破成本，已锁到成本基数 %s。"
                            % (i + 1, cum, fmt(cost_base)))
        ladder.append({
            "step": i + 1,
            "cut_pct": cut,                    # 本档增量（递减）
            "cum_pct": money(cum),             # 累计降幅
            "new_fob": new_fob,
            "new_cif": money((new_fob + freight) / denom),
            "condition": LADDER_CONDITIONS[i] if i < len(LADDER_CONDITIONS) else "换一个条件",
        })
    if cum >= max_concession:
        warnings.append("让步阶梯累计 %.1f%% 已触及底价(%.1f%%)，客户会看穿底线；"
                        "调小 LADDER_CUTS 或调大 MAX_CONCESSION_PCT。" % (cum, max_concession))

    if margin > 100:
        warnings.append("加成 %.1f%% 罕见，确认 --margin 单位：这里填百分比(15 表示 15%%)。" % margin)
    if money(fob) < 0.05:
        warnings.append("单价四舍五入后失真(%s)，建议改按 100 件 / 1000 件为一档报价。" % fmt(fob))

    positioning = None
    if anchor is not None:
        if anchor <= 0:
            warnings.append("竞品锚价 %s 非正，已忽略定位建议。" % anchor)
        else:
            gap = money(fob - anchor)
            if gap > 0:
                positioning = ("你的 FOB 报价高于竞品锚价 %s %s/%s。要么用 T0/T1 分级筛掉价格敏感户，"
                               "要么用'更长账期/更快交期/认证'补差价，别直接降价。"
                               % (fmt(gap), DEFAULT_CURRENCY, DEFAULT_UNIT))
            else:
                positioning = ("你的 FOB 报价低于竞品锚价 %s %s/%s，有价格优势。先确认锚价是否含认证/售后，"
                               "避免拿裸价撞带证价。" % (fmt(abs(gap)), DEFAULT_CURRENCY, DEFAULT_UNIT))

    return {
        "cost_base": money(cost_base),
        "fob_list": money(fob),
        "fob_floor": fob_floor,
        "cif_list": money(cif),
        "cif_floor": cif_floor,
        "insurance": money(insurance),
        "insurance_cover_factor": cover_factor,
        "contingency": contingency,
        "margin_mode": "markup_on_cost",       # 成本加成，不是毛利率倒推
        "ladder": ladder,
        "positioning": positioning,
        "warnings": warnings,
    }


def client_view(q):
    """客户视图：把成本、底价、内部提醒全砍了，这些发客户那边等于把底牌亮出去。"""
    return {k: v for k, v in q.items()
            if k not in ("cost_base", "fob_floor", "cif_floor", "warnings")}


def render_table(q, currency=DEFAULT_CURRENCY, unit=DEFAULT_UNIT,
                 audience="internal", meta=None):
    meta = meta or {}
    per = "%s/%s" % (currency, unit)          # 每张表都带币种+单位，不让新人猜
    W = 66
    is_client = audience == "client"
    s = []
    s.append("=" * W)
    s.append("  报价单（客户视图，成本底价都不带）" if is_client
             else "  内部视图（含成本与底价，这版别发客户）")
    s.append("  币种: %s · 计价单位: %s · 生成时间: %s"
             % (currency, unit, meta.get("generated_at", "-")))
    s.append("=" * W)

    rows = []
    if not is_client:
        rows.append(("成本基数(含不可预见+本地费)", fmt(q["cost_base"])))
    rows.append(("FOB 报价: 离岸价，不含运费保险", fmt(q["fob_list"])))
    if not is_client:
        rows.append(("FOB 底价: 内部，再低不接", fmt(q["fob_floor"])))
    rows.append(("CIF 报价: 到岸价，含运费+保险", fmt(q["cif_list"])))
    if not is_client:
        rows.append(("CIF 底价: 内部，再低不接", fmt(q["cif_floor"])))
    rows.append(("其中保险费 = CIF*%.0f%%*费率" % (q["insurance_cover_factor"] * 100),
                 fmt(q["insurance"])))
    label_w = max(_width(l) for l, _ in rows)
    for label, val in rows:
        s.append("  %s │ %10s %s" % (_pad(label, label_w), val, per))

    s.append("-" * W)
    s.append("  三档让步阶梯（每降一档换回个条件，增量递减，底线自己留着）")
    for st in q["ladder"]:
        s.append("   第%s步  本档 -%s%%  累计 -%s%%   → FOB %s │ CIF %s %s"
                 % (st["step"], st["cut_pct"], st["cum_pct"],
                    fmt(st["new_fob"]), fmt(st["new_cif"]), per))
        s.append("          换回: %s" % st["condition"])

    s.append("-" * W)
    s.append("  报价单这几样得补齐（发出前挨个对，漏了客户正好拿缺的来压价）")
    s.append("    [ ] 报价有效期 : %s 天（海运费/汇率波动大时缩到 7–15 天）"
             % meta.get("quote_validity_days", QUOTE_VALIDITY_DAYS))
    s.append("    [ ] 付款方式   : %s" % DEFAULT_PAYMENT_TERMS)
    s.append("    [ ] 最小起订量 : %s"
             % ("%s %s" % (meta["moq"], unit) if meta.get("moq") else "未填 —— 用 --moq 300 之类补上"))
    s.append("    [ ] 交货期     : %s"
             % (meta.get("lead_time") or "未填 —— 用 --lead-time \"25天\" 补上"))
    s.append("    [ ] 贸易术语   : 写明 Incoterms 2020 + 港口，如 FOB <装运港> / CIF <目的港>")

    s.append("-" * W)
    s.append("  顺手记几个词（完整版去翻 GLOSSARY.md）")
    s.append("   · FOB 离岸价：卖方的钱只花到货物装上船，不含海运费与保险。")
    s.append("   · CIF 到岸价：FOB + 海运费 + 保险费，卖方付到目的港。")
    s.append("   · 投保加成 %.0f%%：保险按 CIF 货值的 %.0f%% 投保，所以 "
             "CIF = (FOB+运费) ÷ (1 − %.2f×费率)，不是 FOB+运费 再乘个费率。"
             % (q["insurance_cover_factor"] * 100, q["insurance_cover_factor"] * 100,
                q["insurance_cover_factor"]))
    s.append("   · 让步阶梯：降一档价必换回一样东西（量/账期/排他/长约），不换条件的让步=送钱。")
    s.append("   · 计价口径：报价 = 成本基数 *(1+加成%)，这是成本加成(markup)；"
             "若按毛利率倒推，报价 = 成本 /(1-毛利率)，15% 毛利率约等于 17.6% 加成。")

    if q.get("positioning"):
        s.append("-" * W)
        s.append("  竞品锚价定位: %s" % q["positioning"])
    if not is_client and q.get("warnings"):
        s.append("-" * W)
        s.append("  内部提醒（这截别贴进发给客户的文件）:")
        for w in q["warnings"]:
            s.append("    - %s" % w)
    s.append("=" * W)
    return "\n".join(s)


def main():
    p = argparse.ArgumentParser(
        description="算 FOB/CIF 报价和底价，再给一套三档让步阶梯",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python scripts/quote_engine.py --cost 28 --freight 6 --margin 15\n"
               "  python scripts/quote_engine.py --cost 28 --freight 6 --audience client")
    p.add_argument("--cost", type=float, required=True, help="单位成本(EXW/工厂价)")
    p.add_argument("--freight", type=float, default=0.0, help="到港海运费（每单位）")
    p.add_argument("--margin", type=float, default=DEFAULT_MARGIN_PCT,
                   help="成本加成%%，默认 %(default)s")
    p.add_argument("--insurance", type=float, default=DEFAULT_INSURANCE_PCT,
                   help="保险费率(占 CIF 货值的百分比%%，默认 %(default)s)")
    p.add_argument("--insurance-rate", type=float, default=None,
                   help="高级入口：保险费率(比率，如 0.0015=0.15%%)，覆盖 --insurance")
    p.add_argument("--local", type=float, default=0.0, help="本地费用(报关/拖车/港杂)")
    p.add_argument("--contingency", type=float, default=DEFAULT_CONTINGENCY,
                   help="不可预见费比例，默认 %(default)s")
    p.add_argument("--anchor", type=float, default=None, help="竞品锚价(报价币种, 可选)")
    p.add_argument("--fx", type=float, default=1.0,
                   help="汇率: 1 成本币种 = fx 报价币种(成本 CNY/报价 USD 时填 0.14)，只换算一次")
    p.add_argument("--currency", default=DEFAULT_CURRENCY, help="报价币种符号, 默认 USD")
    p.add_argument("--unit", default=DEFAULT_UNIT, help="计价单位, 默认 件")
    p.add_argument("--moq", type=int, default=None, help="最小起订量(报价单必带字段)")
    p.add_argument("--lead-time", default=None, help="交货期, 如 \"25天\"")
    p.add_argument("--validity", type=int, default=QUOTE_VALIDITY_DAYS,
                   help="报价有效期天数，默认 %(default)s")
    p.add_argument("--audience", choices=["internal", "client"], default="internal",
                   help="internal=含成本与底价(默认) / client=客户视图，绝不泄露底价")
    p.add_argument("--out", default=None, help="把结果写入文件(UTF-8)")
    p.add_argument("--format", choices=["table", "json"], default="table")
    args = p.parse_args()

    # 保险费率：默认收「百分比」，内部换算为比率；--insurance-rate 为高级比率入口
    rate = args.insurance_rate if args.insurance_rate is not None else args.insurance / 100.0

    if args.fx <= 0:
        raise SystemExit("✗ --fx 必须 > 0（1 成本币种 = fx 报价币种）")

    # 汇率只在这里介入一次：成本/运费/本地费统一换成报价币种，之后不再碰汇率
    try:
        q = build_quote(args.cost * args.fx, args.freight * args.fx, args.margin,
                        rate, args.local * args.fx, args.contingency, args.anchor)
    except ValueError as e:
        raise SystemExit("✗ %s" % e)

    meta = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "currency": args.currency,
        "unit": args.unit,
        "audience": args.audience,
        "quote_validity_days": args.validity,
        "payment_terms": DEFAULT_PAYMENT_TERMS,
        "moq": args.moq,
        "lead_time": args.lead_time,
        "inputs": {"cost": args.cost, "freight": args.freight, "margin_pct": args.margin,
                   "insurance_rate": rate, "local": args.local,
                   "contingency": args.contingency, "anchor": args.anchor, "fx": args.fx},
    }

    if args.format == "json":
        payload_q = client_view(q) if args.audience == "client" else q
        out = json.dumps({"meta": meta, "quote": payload_q},
                         ensure_ascii=False, indent=2)
    else:
        out = render_table(q, args.currency, args.unit, args.audience, meta)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
    print(out)


if __name__ == "__main__":
    main()
