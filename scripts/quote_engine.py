#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quote_engine.py — v0.2 报价引擎 (alpha)
外贸 FOB / CIF 报价区间 + 三档让步阶梯（每步必须换条件）。

只用标准库，Python 3.8+ 可直接跑。

用法:
    python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
    python scripts/quote_engine.py --cost 28 --freight 6 --margin 15 --anchor 42 --format json

参数:
    --cost        单位成本（工厂/EXW 价，USD/件或 USD/套），必填
    --freight     到目的港海运费（USD/件），默认 0
    --margin      目标毛利百分比，默认 15
    --insurance   保险费率（占CIF货值百分比%），默认 0.15（即 0.15%；海运险通常 0.1%–0.3%）
    --insurance-rate  高级入口：保险费率(比率)，如 0.0015=0.15%，可覆盖 --insurance
    --local       本地费用（报关/拖车/港杂，USD/件），默认 0
    --contingency 不可预见费比例，默认 0.03
    --anchor      竞品锚价（USD/件，可选）—— 有则给定位建议
    --format      table(默认) / json

报价纪律（项目核心）:
    让步必须换条件。每降一点价，都要从客户那里换回一样东西（量 / 账期 / 排他 / 长约）。
    不换条件的让步 = 送钱。
"""

import argparse
import json
from datetime import datetime


def build_quote(cost, freight, margin, insurance_rate, local, contingency, anchor=None):
    # 输入校验：防止静默错价 / 亏本报价
    if cost <= 0:
        raise ValueError("成本必须 > 0")
    if margin < 0:
        raise ValueError("毛利率不能为负（负毛利=亏本报价）")
    # 不可预见费先叠进成本
    landed_cost = cost * (1 + contingency) + local
    # FOB = 成本 + 毛利（海运费不进 FOB）
    fob = landed_cost * (1 + margin / 100.0)
    # CIF 标准公式：保险按 CIF 货值 110% 投保，故 CIF = (FOB+运费) / (1 - 1.10×费率)
    rate = insurance_rate
    denom = 1 - 1.10 * rate
    if denom <= 0:
        # 费率 ≥ 90.9% 时分母非正，CIF 无定义，必须明确报错而非静默回退
        raise ValueError("保险费率过高(≥90.9%%)导致 CIF 分母非正，请检查 --insurance")
    cif = (fob + freight) / denom
    insurance = cif * 1.10 * rate

    # 报价格子：给客户一个区间而不是死价，留出谈判空间
    fob_list = round(fob, 2)
    fob_floor = round(fob * 0.94, 2)          # 底价（再低不接）
    cif_list = round(cif, 2)
    cif_floor = round(cif * 0.95, 2)

    # 三档让步阶梯：每一步都绑定一个条件
    ladder = [
        {"step": 1, "cut_pct": 2, "new_fob": round(fob * 0.98, 2),
         "condition": "客户确认首单 ≥ 1 个柜（20GP/40HQ）"},
        {"step": 2, "cut_pct": 4, "new_fob": round(fob * 0.96, 2),
         "condition": "由试订单升级为年度框架 / 量翻倍以上"},
        {"step": 3, "cut_pct": 6, "new_fob": round(fob * 0.94, 2),
         "condition": "签 1–3 年排他或独家代理（区域保护换低价）"},
    ]

    positioning = None
    if anchor is not None and anchor > 0:
        gap = round(fob_list - anchor, 2)
        if gap > 0:
            positioning = ("你的 FOB 报价高于竞品锚价 %s。要么用 T0/T1 客户分级筛掉价格敏感户，"
                           "要么用'更长账期/更快交期/认证(SASO等)'补差价，别直接降价。" % gap)
        else:
            positioning = ("你的 FOB 报价低于竞品锚价 %s，有价格优势。先确认锚价是否含认证/售后，"
                           "避免拿裸价撞带证价。" % abs(gap))

    return {
        "landed_cost": round(landed_cost, 2),
        "fob_list": fob_list,
        "fob_floor": fob_floor,
        "cif_list": cif_list,
        "cif_floor": cif_floor,
        "insurance": round(insurance, 2),
        "contingency": contingency,
        "ladder": ladder,
        "positioning": positioning,
    }


def render_table(q):
    s = []
    s.append("")
    s.append("=" * 60)
    s.append("  报价引擎 (alpha) 结果")
    s.append("=" * 60)
    s.append("  落地成本(含不可预见) : %s" % q["landed_cost"])
    s.append("  FOB 报价区间        : 底价 %s ~ 报价 %s (USD/件)" % (q["fob_floor"], q["fob_list"]))
    s.append("  CIF 报价区间        : 底价 %s ~ 报价 %s (USD/件)" % (q["cif_floor"], q["cif_list"]))
    s.append("  保险费              : %s USD/件 (按 CIF 110%% 投保)" % q["insurance"])
    s.append("-" * 60)
    s.append("  三档让步阶梯（每一步必须换条件）:")
    for st in q["ladder"]:
        s.append("   第%s步  -%s%%  → FOB %s  | 条件: %s" % (st["step"], st["cut_pct"], st["new_fob"], st["condition"]))
    if q["positioning"]:
        s.append("-" * 60)
        s.append("  竞品锚价定位: %s" % q["positioning"])
    s.append("=" * 60)
    s.append("")
    return "\n".join(s)


def main():
    p = argparse.ArgumentParser(
        description="v0.2 报价引擎(alpha)：FOB/CIF 区间 + 三档让步阶梯",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python scripts/quote_engine.py --cost 28 --freight 6 --margin 15")
    p.add_argument("--cost", type=float, required=True, help="单位成本(EXW/工厂价, USD)")
    p.add_argument("--freight", type=float, default=0.0, help="到港海运费(USD/件)")
    p.add_argument("--margin", type=float, default=15.0, help="目标毛利%%, 默认 15")
    p.add_argument("--insurance", type=float, default=0.15,
                   help="保险费率(占CIF货值%%, 默认 0.15%%)")
    p.add_argument("--insurance-rate", type=float, default=None,
                   help="高级入口：保险费率(比率, 如 0.0015=0.15%%)，覆盖 --insurance")
    p.add_argument("--local", type=float, default=0.0, help="本地费用(报关/拖车/港杂, USD/件)")
    p.add_argument("--contingency", type=float, default=0.03, help="不可预见费比例, 默认 0.03")
    p.add_argument("--anchor", type=float, default=None, help="竞品锚价(USD/件, 可选)")
    p.add_argument("--format", choices=["table", "json"], default="table")
    args = p.parse_args()

    # 保险费率：默认收「百分比」，内部换算为比率；--insurance-rate 为高级比率入口
    if args.insurance_rate is not None:
        rate = args.insurance_rate
    else:
        rate = args.insurance / 100.0
    if rate > 0.05:
        raise SystemExit("✗ 保险费率 %.2f%% 异常(>5%%)? 新手常把 0.3%%输成0.3。请确认单位。" % (rate * 100))

    q = build_quote(args.cost, args.freight, args.margin,
                   rate, args.local, args.contingency, args.anchor)

    if args.format == "json":
        print(json.dumps({"generated_at": datetime.now().isoformat(timespec="seconds"),
                          **q}, ensure_ascii=False, indent=2))
    else:
        print(render_table(q))


if __name__ == "__main__":
    main()
