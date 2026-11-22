#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品锚价：海关数据里竞品卖多少钱，你该报多少钱。

报价之前先锚价：拿海关数据里的竞品价区间（最低/最高/中位），对照自家
成本，算出三档建议报价——进取价/中位价/保守价，每档写清毛利空间和
适用场景。报出去之前，再过一遍 5 项复核清单（成本、运费、汇率、付款
条件、有效期），有一项没打勾就标出来提醒你。

只用了标准库，Python 3.8 往上都能直接跑，不联网，不写文件（除非你加 --out）。

口径与 quote_engine.py / landed_cost.py 逐字同一套，不许第三套算法打架：
    成本基数 = FOB 成本 x (1 + 不可预见费 3%) + 本地费，与 quote_engine.build_quote() 相同
    保本 CIF = (成本基数 + 运费) / (1 - 1.10 x 保险费率)，保险按 CIF 货值 110% 投保
    CIF = (FOB + 运费) / (1 - 1.10 x 保险费率)，与两边同一条公式
    三档锚价是 CIF 价：进取价 = 中位价 x 97%，中位价 = 中位价，保守价 = 中位价 x 103%
    每档的 FOB 对等价 = 该档 CIF x (1 - 1.10 x 保险费率) - 运费（把 CIF 公式倒推回去）
    毛利 = 该档 CIF - 保本 CIF；毛利率 = 毛利 / 该档 CIF（按售价，与 landed_cost 同口径）
    关税给了才算 DDP：DDP 价 = CIF 价 x (1 + 关税税率)，关税按 CIF 计（与 landed_cost 相同）
    含税价（给了 --tax-rate 才算）：含税 CIF = CIF x (1 + 税率)，与 quote_engine 的含税拆分同口径

用法:
    python scripts/anchor_price.py --comp-low 38 --comp-high 46 --comp-median 42 --cost 28 --freight 6 --duty 10
    python scripts/anchor_price.py --comp-low 30 --comp-high 36 --comp-median 33 --cost 28 --freight 6
    python scripts/anchor_price.py --comp-low 38 --comp-high 46 --comp-median 42 --cost 28 --freight 6 --duty 10 --audience client
    python scripts/anchor_price.py --comp-low 44 --comp-high 56 --cost 30 --freight 5 --format json

参数:
    --comp-low      竞品价最低价（海关数据），必填
    --comp-high     竞品价最高价（海关数据），必填
    --comp-median   竞品价中位价（海关数据），可选；不给就按（最低+最高）/2 估算并注明
    --cost          自家 FOB 成本（工厂/EXW 价），必填，币种由 --currency 决定
    --freight       到目的港海运费（每单位），默认 0
    --local         本地费用（报关/拖车/港杂，每单位），默认 0；进了成本基数，与 quote_engine 相同
    --tax-rate      增值税率（%，默认 0 = 不算；给了三档价多一列含税价，与 quote_engine 同口径）
    --duty          关税税率（%），默认 0；给了才算 DDP 价
    --insurance     保险费率（占 CIF 货值的百分比 %），默认 0.15（海运险通常 0.1%-0.3%）
    --insurance-rate  高级入口：保险费率（比率），如 0.0015 = 0.15%，可覆盖 --insurance
    --contingency   不可预见费比例，默认 0.03（与 quote_engine.py 相同）
    --currency      币种符号，默认 USD
    --unit          计价单位，默认 条
    --validity      报价有效期天数，默认 30
    --payment       付款条件，默认 "T/T 30% 定金 + 70% 见提单副本；或即期 L/C"（与 quote_engine.py 相同）
    --verified      已复核的项，逗号分隔：cost,freight,fx,payment,validity（也可写中文：成本,运费,汇率,付款条件,有效期）；不写默认全是待核
    --audience      internal(默认，含成本、毛利与复核清单) / client(客户视图，只给三档报价)
    --out           同时写入文件（UTF-8），不指定则只打印
    --format        table(默认) / json

两条规矩：
    竞品价低于自家成本时，明确警告"低于成本，别接单或先谈量换价"，别硬接。
    客户版只给三档报价与适用场景，成本、毛利、复核清单一行都不露，发客户记得加 --audience client。
"""

import argparse
import json
import os
import sys
import unicodedata
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import _ZhArgumentParser, fmt, money  # noqa: E402

# 可调常量：要改默认数值就动这边（与 quote_engine.py / landed_cost.py 同值，改一处必须改另一处）
DEFAULT_INSURANCE_PCT = 0.15     # 默认保险费率（占 CIF 货值的百分比）
INSURANCE_COVER_FACTOR = 1.10    # 投保加成：按 CIF 货值 110% 投保（行业惯例 110%）
DEFAULT_CONTINGENCY = 0.03       # 不可预见费比例（叠在成本上，与 quote_engine.py 相同）
MAX_INSURANCE_RATE = 0.05        # 费率 >5% 判定为「单位输错」，直接报错
MAX_DUTY_PCT = 1000.0            # 关税税率上限 1000%（反倾销税可能很高，但 1000% 以上基本是单位错）
MAX_TAX_RATE_PCT = 100.0         # 增值税率上限 100%（超过基本是单位错）
AGGRESSIVE_CUT_PCT = 3.0         # 进取价 = 中位价 x (1 - 3%)
CONSERVATIVE_PREMIUM_PCT = 3.0   # 保守价 = 中位价 x (1 + 3%)
QUOTE_VALIDITY_DAYS = 30         # 报价有效期默认天数
DEFAULT_PAYMENT_TERMS = "T/T 30% 定金 + 70% 见提单副本；或即期 L/C"
DEFAULT_CURRENCY = "USD"         # 输出币种符号（所有金额都带，不让新人猜）
DEFAULT_UNIT = "条"              # 计价单位（轮胎按条计，与 landed_cost.py 相同）

BELOW_COST_WARNING = "低于成本，别接单或先谈量换价"

# 复核清单 5 项：顺序固定，成本、运费、汇率、付款条件、有效期
CHECKLIST_ITEMS = (
    ("cost", "成本"),
    ("freight", "运费"),
    ("fx", "汇率"),
    ("payment", "付款条件"),
    ("validity", "有效期"),
)
CHECKLIST_KEYS = tuple(k for k, _ in CHECKLIST_ITEMS)
CHECKLIST_LABELS = {k: label for k, label in CHECKLIST_ITEMS}
CHECKLIST_ALIASES = {"cost": "cost", "成本": "cost",
                     "freight": "freight", "运费": "freight",
                     "fx": "fx", "汇率": "fx",
                     "payment": "payment", "付款条件": "payment",
                     "validity": "validity", "有效期": "validity"}

TIER_SCENARIOS = {
    "aggressive": "抢单 / 进新市场 / 首单破冰：量大、长期合作、或客户明确比价时用",
    "median": "默认档：跟市场中位齐平，不拼低价也不高挂，多数情况先报这档",
    "conservative": "品牌、认证或交期有优势时用；小单、定制单、或客户不比价时优先",
}
TIER_NAMES = {
    "aggressive": "进取价",
    "median": "中位价",
    "conservative": "保守价",
}










def normalize_verified(raw):
    """--verified 的逗号清单归一成 key 集合；认不出的词直接报错，别悄悄吞掉。"""
    if raw is None:
        return frozenset()
    if isinstance(raw, (set, frozenset)):
        items = list(raw)
    elif isinstance(raw, (list, tuple)):
        items = list(raw)
    else:
        items = str(raw).split(",")
    out = set()
    for item in items:
        text = str(item).strip()
        if not text:
            continue
        if text not in CHECKLIST_ALIASES:
            raise ValueError("复核项只能是 cost/运费……这一组：%s，收到的是 %r"
                             % ("/".join(CHECKLIST_KEYS), item))
        out.add(CHECKLIST_ALIASES[text])
    return frozenset(out)


def build_anchor(comp_low, comp_high, comp_median, cost, freight,
                 duty_pct=0.0, insurance_rate=0.0015,
                 contingency=DEFAULT_CONTINGENCY, verified=frozenset(),
                 local=0.0, tax_rate_pct=0.0):
    """算三档锚价 + 毛利空间 + 5 项复核清单。

    计价链路（与 quote_engine.py / landed_cost.py 同一条公式，每步只做一次）:
        成本基数 = FOB 成本 x (1 + 不可预见费) + 本地费；保本 CIF = (成本基数 + 运费) / (1 - 1.10 x 保险费率)
        三档 CIF：进取价 = 中位价 x 97%，中位价 = 中位价，保守价 = 中位价 x 103%
        每档 FOB 对等价 = 该档 CIF x (1 - 1.10 x 保险费率) - 运费（CIF 公式倒推）
        毛利 = 该档 CIF - 保本 CIF；毛利率 = 毛利 / 该档 CIF（按售价）
        DDP 价 = CIF 价 x (1 + 关税税率)；关税按 CIF 计
        含税价（tax_rate_pct > 0 时才算）：含税 CIF = CIF x (1 + 税率)，含税 DDP 同理
    毛利/毛利率/加成按未四舍五入的原值算，再四舍五入到分（与 landed_cost 的总计口径相同）。
    """
    # 输入校验：错了就直接报错，绝不悄悄塞个错锚价出去
    if comp_low <= 0:
        raise ValueError("竞品最低价必须 > 0")
    if comp_low > 10_000_000:
        raise ValueError("竞品最低价 %s 大得离谱（上限 10,000,000）：是不是多输了几个 0，"
                         "或把整柜总价当成了单价？" % fmt(comp_low))
    if comp_high <= 0:
        raise ValueError("竞品最高价必须 > 0")
    if comp_high > 10_000_000:
        raise ValueError("竞品最高价 %s 大得离谱（上限 10,000,000）" % fmt(comp_high))
    if comp_low > comp_high:
        raise ValueError("竞品最低价 %s 高于最高价 %s：最低/最高是不是填反了？"
                         % (fmt(comp_low), fmt(comp_high)))
    if comp_median is not None:
        if comp_median <= 0:
            raise ValueError("竞品中位价必须 > 0")
        if comp_median < comp_low or comp_median > comp_high:
            raise ValueError("竞品中位价 %s 不在最低价 %s 与最高价 %s 之间："
                             "中位价是不是抄错行了？"
                             % (fmt(comp_median), fmt(comp_low), fmt(comp_high)))
    if cost <= 0:
        raise ValueError("自家 FOB 成本必须 > 0")
    if cost > 10_000_000:
        raise ValueError("自家 FOB 成本 %s 大得离谱（上限 10,000,000）：是不是把整柜总价当成了单价？"
                         % fmt(cost))
    if freight < 0:
        raise ValueError("海运费不能为负（负数会让 CIF 低于 FOB）")
    if freight > 10_000_000:
        raise ValueError("海运费 %s 大得离谱（上限 10,000,000）：是不是把整柜运费当成了每件运费？"
                         % fmt(freight))
    if duty_pct < 0:
        raise ValueError("关税税率不能为负")
    if duty_pct > MAX_DUTY_PCT:
        raise ValueError("关税税率 %.1f%% 大得离谱（上限 %.0f%%）：这里填百分比，10 表示 10%%，"
                         "不是 1000。" % (duty_pct, MAX_DUTY_PCT))
    if insurance_rate < 0:
        raise ValueError("保险费率不能为负")
    if insurance_rate > MAX_INSURANCE_RATE:
        raise ValueError("保险费率 %.3f%% 异常(>%.0f%%)？新手常把 0.3%% 输成 0.3。"
                         " --insurance 收的是百分比数值。" % (insurance_rate * 100,
                                                         MAX_INSURANCE_RATE * 100))
    if contingency < 0:
        raise ValueError("不可预见费比例不能为负")
    if contingency > 1:
        raise ValueError("不可预见费比例 %.2f 超过 100%%：这里填比率，0.03 表示 3%%。" % contingency)
    if local < 0:
        raise ValueError("本地费用不能为负")
    if local > 10_000_000:
        raise ValueError("本地费用 %s 大得离谱（上限 10,000,000）：是不是把整柜费用当成了每件费用？"
                         % fmt(local))
    if tax_rate_pct < 0:
        raise ValueError("增值税率不能为负")
    if tax_rate_pct > MAX_TAX_RATE_PCT:
        raise ValueError("增值税率 %.1f%% 大得离谱（上限 %.0f%%）：这里填百分比，13 表示 13%%，"
                         "不是 1300。" % (tax_rate_pct, MAX_TAX_RATE_PCT))
    verified = normalize_verified(verified)

    # ---- 中位价：没给就用（最低+最高）/2 估算，并注明是估算
    median_estimated = comp_median is None
    median = (comp_low + comp_high) / 2.0 if median_estimated else comp_median

    # ---- 成本基数与保本 CIF：与 quote_engine.build_quote() 同一条链路（含本地费）
    denom = 1 - INSURANCE_COVER_FACTOR * insurance_rate
    if denom <= 0:
        raise ValueError("保险费率过高(≥ %.1f%%)导致 CIF 分母非正，请检查 --insurance 单位"
                         % (100.0 / INSURANCE_COVER_FACTOR))
    cost_base = cost * (1 + contingency) + local
    cif_floor = (cost_base + freight) / denom
    ddp_floor = cif_floor * (1 + duty_pct / 100.0)
    # 自检：保本 CIF 必须等于成本基数+运费+保本保险费（防止公式写错却看不出来）
    insurance_floor = cif_floor * INSURANCE_COVER_FACTOR * insurance_rate
    if abs(cif_floor - (cost_base + freight + insurance_floor)) > 0.005:
        raise ValueError("CIF 恒等式校验失败，请检查投保加成参数")

    warnings = []
    if median_estimated:
        warnings.append("中位价未给，按（最低价 + 最高价）/ 2 估算为 %s：这是估算值，"
                        "先跟海关数据核对真实中位价再报。" % fmt(median))
    if (comp_high - comp_low) / median > 0.5:
        warnings.append("竞品价区间太宽（最高价比最低价高 %.0f%%）：中位价的代表性弱，"
                        "先确认区间里是不是混了不同规格/不同认证的货。"
                        % ((comp_high - comp_low) / comp_low * 100.0))

    # ---- 三档锚价：中位价 x 97% / 100% / 103%，每档毛利、毛利率、FOB 对等价、隐含加成
    tier_defs = (("aggressive", median * (1 - AGGRESSIVE_CUT_PCT / 100.0)),
                 ("median", median),
                 ("conservative", median * (1 + CONSERVATIVE_PREMIUM_PCT / 100.0)))
    tiers = []
    for key, price in tier_defs:
        profit = price - cif_floor
        fob_equiv = price * denom - freight
        tier = {
            "key": key,
            "name": TIER_NAMES[key],
            "price_cif": money(price),
            "price_ddp": money(price * (1 + duty_pct / 100.0)),
            "fob_equiv": money(fob_equiv),
            "profit_cif": money(profit),
            "margin_pct": money(profit / price * 100.0),
            "implied_markup_pct": money((fob_equiv / cost_base - 1) * 100.0),
            "below_cost": price < cif_floor,
            "scenario": TIER_SCENARIOS[key],
        }
        if tax_rate_pct > 0:
            # Tax-inclusive view / 含税价：CIF x (1+税率)，与 quote_engine 同口径。
            tier["price_cif_tax_incl"] = money(price * (1 + tax_rate_pct / 100.0))
            tier["price_ddp_tax_incl"] = money(price * (1 + duty_pct / 100.0)
                                               * (1 + tax_rate_pct / 100.0))
        tiers.append(tier)
    below_cost = any(t["below_cost"] for t in tiers)
    median_below_cost = tiers[1]["below_cost"]
    if below_cost:
        bad = "、".join(t["name"] for t in tiers if t["below_cost"])
        warnings.append("%s：%s（%s）低于到岸保本价 %s，报这个价每条都亏，"
                        "先谈量换价（量翻倍换低价）或换便宜规格，别硬接。"
                        % (BELOW_COST_WARNING, bad,
                           "、".join(fmt(t["price_cif"]) for t in tiers if t["below_cost"]),
                           fmt(cif_floor)))

    # ---- 5 项复核清单：--verified 里打勾的算已核，其余全是待核
    checklist = []
    for key, label in CHECKLIST_ITEMS:
        checklist.append({
            "key": key,
            "label": label,
            "status": "已核" if key in verified else "待核",
        })
    pending_count = sum(1 for item in checklist if item["status"] == "待核")
    if pending_count:
        warnings.append("复核清单还有 %d 项待核（%s），报出去之前逐项打勾，"
                        "用 --verified cost,freight,fx,payment,validity 一次勾完。"
                        % (pending_count,
                           "、".join(item["label"] for item in checklist
                                     if item["status"] == "待核")))

    return {
        "comp_low": money(comp_low),
        "comp_high": money(comp_high),
        "comp_median": money(median),
        "median_estimated": median_estimated,
        "cost": money(cost),
        "freight": money(freight),
        "local": money(local),
        "cost_base": money(cost_base),
        "cif_floor": money(cif_floor),
        "ddp_floor": money(ddp_floor),
        "duty_pct": duty_pct,
        "insurance_rate": insurance_rate,
        "insurance_cover_factor": INSURANCE_COVER_FACTOR,
        "contingency": contingency,
        "tax_rate_pct": money(tax_rate_pct),
        "tiers": tiers,
        "below_cost": below_cost,
        "median_below_cost": median_below_cost,
        "checklist": checklist,
        "pending_count": pending_count,
        "warnings": warnings,
    }


def client_view(a):
    """客户视图：只给三档报价与适用场景。

    只砍数字不够：成本基数 + 保本 CIF + 毛利三样凑在一起，客户能反推底价；
    FOB 对等价 + 运费也能反推成本基数；复核清单里藏着内部核对进度。
    所以成本、毛利、FOB 对等价、隐含加成、保本价、复核清单、内部提醒全砍，
    只留三档的价与场景。DDP 价是报价本身（给了关税才有意义），可以留。
    含税价也是报价本身（给了税率才有），可以留。
    """
    tiers_out = []
    for t in a["tiers"]:
        tier = {"key": t["key"], "name": t["name"], "price_cif": t["price_cif"],
                "price_ddp": t["price_ddp"], "scenario": t["scenario"]}
        if "price_cif_tax_incl" in t:
            tier["price_cif_tax_incl"] = t["price_cif_tax_incl"]
            tier["price_ddp_tax_incl"] = t["price_ddp_tax_incl"]
        tiers_out.append(tier)
    return {"tiers": tiers_out}


def render_table(a, currency=DEFAULT_CURRENCY, unit=DEFAULT_UNIT,
                 audience="internal", meta=None):
    meta = meta or {}
    per = "%s/%s" % (currency, unit)          # 每张表都带币种+单位，不让新人猜
    W = 66
    is_client = audience == "client"
    s = []
    s.append("=" * W)
    s.append("  竞品锚价（客户视图，只给三档报价与适用场景）" if is_client
             else "  竞品锚价（内部视图，含成本、毛利与复核清单，这版别发客户）")
    s.append("  币种: %s · 计价单位: %s · 生成时间: %s"
             % (currency, unit, meta.get("generated_at", "-")))
    s.append("=" * W)

    if not is_client:
        s.append("  竞品价区间: 最低 %s │ 最高 %s │ 中位 %s%s"
                 % (fmt(a["comp_low"]), fmt(a["comp_high"]), fmt(a["comp_median"]),
                    "（估算值，见下方提醒）" if a["median_estimated"] else ""))
        s.append("  自家成本: FOB 成本 %s │ 运费 %s │ 本地费 %s │ 成本基数（含不可预见费 %.0f%%） %s"
                 % (fmt(a["cost"]), fmt(a["freight"]), fmt(a["local"]),
                    a["contingency"] * 100, fmt(a["cost_base"])))
        s.append("  保本 CIF: %s │ 保本 DDP（关税 %.2f%%）: %s"
                 % (fmt(a["cif_floor"]), a["duty_pct"], fmt(a["ddp_floor"])))
        s.append("-" * W)
        s.append("  三档锚价（CIF 价，进取 = 中位 x 97%，保守 = 中位 x 103%）")
        for t in a["tiers"]:
            flag = "  ★ 低于成本" if t["below_cost"] else ""
            line = ("  %s: CIF %s │ DDP %s │ 毛利 %s │ 毛利率 %.2f%% │ FOB 对等价 %s │ 隐含加成 %.2f%%%s"
                    % (t["name"], fmt(t["price_cif"]), fmt(t["price_ddp"]),
                       fmt(t["profit_cif"]), t["margin_pct"], fmt(t["fob_equiv"]),
                       t["implied_markup_pct"], flag))
            if "price_cif_tax_incl" in t:
                line += " │ 含税 CIF %s" % fmt(t["price_cif_tax_incl"])
            s.append(line)
            s.append("      适用: %s" % t["scenario"])
    else:
        s.append("  三档建议报价（CIF 价，适用场景写在每档后面）")
        for t in a["tiers"]:
            line = ("  %s: CIF %s │ DDP %s"
                    % (t["name"], fmt(t["price_cif"]), fmt(t["price_ddp"])))
            if "price_cif_tax_incl" in t:
                line += " │ 含税 CIF %s" % fmt(t["price_cif_tax_incl"])
            s.append(line)
            s.append("      适用: %s" % t["scenario"])

    s.append("-" * W)
    s.append("  报价有效期: %s 天 · 付款条件: %s"
             % (meta.get("quote_validity_days", QUOTE_VALIDITY_DAYS),
                meta.get("payment_terms", DEFAULT_PAYMENT_TERMS)))

    if not is_client:
        s.append("-" * W)
        s.append("  报价复核清单（5 项，逐项打勾再报）")
        for item in a["checklist"]:
            mark = "[x] 已核" if item["status"] == "已核" else "[ ] 待核 ⚠"
            s.append("    %s  %s" % (mark, item["label"]))
        if a["pending_count"]:
            s.append("  ⚠ 还有 %d 项待核，报出去之前先逐项打勾："
                     "--verified cost,freight,fx,payment,validity" % a["pending_count"])
        s.append("-" * W)
        s.append("  顺手记几个词（完整版去翻 docs/anchor-price.md）")
        s.append("   · 保本 CIF = (成本基数 + 运费) ÷ (1 − 1.10×保险费率)，与 quote_engine.py /"
                 " landed_cost.py 同一条公式；FOB 对等价是把这条公式倒推回去。")
        s.append("   · 毛利率按售价算（毛利 ÷ 该档 CIF），与 landed_cost.py 的利润率同口径。")
        s.append("   · 中位价是默认档：跟市场齐平，不拼低价也不高挂；进取价抢单用，"
                 "保守价只在品牌/认证/交期有优势时用。")
        s.append("   · 低于成本的档别报：先谈量换价（量翻倍换低价）或换便宜规格，别硬接。")

    if not is_client and a.get("warnings"):
        s.append("-" * W)
        s.append("  内部提醒（这截别贴进发给客户的文件）:")
        for w in a["warnings"]:
            s.append("    - %s" % w)
    s.append("=" * W)
    return "\n".join(s)




def build_parser():
    p = _ZhArgumentParser(
        prog="anchor_price.py",
        description="竞品锚价：海关数据里的竞品价区间 + 自家成本，算出进取/中位/保守"
                    "三档建议报价（CIF 价），每档写清毛利空间和适用场景，报出去之前"
                    "再过一遍成本/运费/汇率/付款条件/有效期 5 项复核清单（只用标准库，不联网）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""可直接复制的例子（【示例】价格全部虚构，亲手跑过，输出见 docs/anchor-price.md）:
  python scripts/anchor_price.py --comp-low 38 --comp-high 46 --comp-median 42 --cost 28 --freight 6 --duty 10
    → 三档 CIF 40.74 / 42.00 / 43.26，保本 CIF 34.90，中位价毛利率 16.91%
  python scripts/anchor_price.py --comp-low 30 --comp-high 36 --comp-median 33 --cost 28 --freight 6
    → 中位价 33.00 低于保本 CIF 34.90：低于成本，别接单或先谈量换价
  python scripts/anchor_price.py --comp-low 38 --comp-high 46 --comp-median 42 --cost 28 --freight 6 --duty 10 --audience client
    → 同样三档报价，成本/毛利/复核清单全砍掉，这版才能发客户
  python scripts/anchor_price.py --comp-low 44 --comp-high 56 --cost 30 --freight 5
    → 中位价未给，按（44 + 56）/ 2 估算为 50.00，三档 CIF 48.50 / 50.00 / 51.50
  python scripts/anchor_price.py --comp-low 38 --comp-high 46 --comp-median 42 --cost 28 --freight 6 --duty 10 --format json
    → JSON 版，三档锚价 + 毛利 + 复核清单一次给全，方便贴进表格
  python scripts/anchor_price.py --comp-low 38 --comp-high 46 --comp-median 42 --cost 28 --freight 6 --duty 10 --local 5 --tax-rate 13
    → 本地费 5 进成本基数 33.84，保本 CIF 39.91；三档含税 CIF 46.04 / 47.46 / 48.88（【示例】税率虚构）
  发客户永远加 --audience client：内部视图的成本和毛利一旦寄出去就收不回来。""")
    p.add_argument("--comp-low", type=float, required=True,
                   help="竞品价最低价（海关数据，必填）")
    p.add_argument("--comp-high", type=float, required=True,
                   help="竞品价最高价（海关数据，必填）")
    p.add_argument("--comp-median", type=float, default=None,
                   help="竞品价中位价（海关数据）；不给就按（最低+最高）/2 估算并注明")
    p.add_argument("--cost", type=float, required=True,
                   help="自家 FOB 成本（工厂/EXW 价，必填）")
    p.add_argument("--freight", type=float, default=0.0,
                   help="到目的港海运费（每单位），默认 %(default)s")
    p.add_argument("--local", type=float, default=0.0,
                   help="本地费用（每单位），默认 %(default)s；进了成本基数，与 quote_engine 相同")
    p.add_argument("--tax-rate", type=float, default=0.0,
                   help="增值税率(%%)，默认 0=不算；给了三档价多一列含税价")
    p.add_argument("--duty", type=float, default=0.0,
                   help="关税税率(%%)，默认 %(default)s；给了才算 DDP 价")
    p.add_argument("--insurance", type=float, default=DEFAULT_INSURANCE_PCT,
                   help="保险费率(占 CIF 货值的百分比%%，默认 %(default)s)")
    p.add_argument("--insurance-rate", type=float, default=None,
                   help="高级入口：保险费率(比率，如 0.0015=0.15%%)，覆盖 --insurance")
    p.add_argument("--contingency", type=float, default=DEFAULT_CONTINGENCY,
                   help="不可预见费比例，默认 %(default)s（与 quote_engine.py 相同）")
    p.add_argument("--currency", default=DEFAULT_CURRENCY,
                   help="币种符号，默认 %(default)s")
    p.add_argument("--unit", default=DEFAULT_UNIT,
                   help="计价单位，默认 %(default)s")
    p.add_argument("--validity", type=int, default=QUOTE_VALIDITY_DAYS,
                   help="报价有效期天数，默认 %(default)s")
    p.add_argument("--payment", default=DEFAULT_PAYMENT_TERMS,
                   help="付款条件，默认与 quote_engine.py 相同")
    p.add_argument("--verified", default="",
                   help="已复核的项，逗号分隔：cost,freight,fx,payment,validity"
                        "（也可写中文：成本,运费,汇率,付款条件,有效期）；不写默认全是待核")
    p.add_argument("--audience", choices=["internal", "client"], default="internal",
                   help="internal=含成本、毛利与复核清单(默认) / client=客户视图，只给三档报价")
    p.add_argument("--out", default=None, help="把结果写入文件(UTF-8)")
    p.add_argument("--format", choices=["table", "json"], default="table",
                   help="输出格式：table=人看的版(默认) / json=给别的脚本用")
    return p


def main():
    parser = build_parser()
    if len(sys.argv) == 1:
        parser.print_usage(sys.stderr)
        print("\n没给参数：不知道怎么填就跑 python scripts/anchor_price.py --help，"
              "里面有能直接复制的例子。", file=sys.stderr)
        raise SystemExit(2)
    args = parser.parse_args()

    # 保险费率：默认收「百分比」，内部换算为比率；--insurance-rate 为高级比率入口
    rate = args.insurance_rate if args.insurance_rate is not None else args.insurance / 100.0

    if not 1 <= args.validity <= 365:
        raise SystemExit("✗ --validity 报价有效期必须是 1–365 天，收到的是 %s" % args.validity)

    try:
        verified = normalize_verified(args.verified)
    except ValueError as e:
        raise SystemExit("✗ %s" % e)
    try:
        a = build_anchor(args.comp_low, args.comp_high, args.comp_median,
                         args.cost, args.freight, args.duty, rate,
                         args.contingency, verified,
                         local=args.local, tax_rate_pct=args.tax_rate)
    except ValueError as e:
        raise SystemExit("✗ %s" % e)

    meta = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "currency": args.currency,
        "unit": args.unit,
        "audience": args.audience,
        "quote_validity_days": args.validity,
        "payment_terms": args.payment,
        "inputs": {"comp_low": args.comp_low, "comp_high": args.comp_high,
                   "comp_median": args.comp_median, "cost": args.cost,
                   "freight": args.freight, "local": args.local,
                   "duty_pct": args.duty,
                   "insurance_rate": rate, "contingency": args.contingency,
                   "tax_rate_pct": args.tax_rate},
    }

    if args.format == "json":
        payload_a = client_view(a) if args.audience == "client" else a
        # 客户视图的 meta 也得脱敏：inputs 里有成本/运费/费率，客户拿三档报价一除就能反推
        payload_meta = dict(meta)
        if args.audience == "client":
            payload_meta.pop("inputs", None)
        out = json.dumps({"meta": payload_meta, "anchor_price": payload_a},
                         ensure_ascii=False, indent=2)
    else:
        out = render_table(a, args.currency, args.unit, args.audience, meta)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
    print(out)


if __name__ == "__main__":
    main()
