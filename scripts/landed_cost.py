#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算到岸成本的。给你 FOB 价、海运费、保险费率、目的港杂费、关税税率，
它吐出 CIF / DDP 分项 breakdown + 单条成本 +（给了售价）每条利润空间。

只用了标准库，Python 3.10 往上都能直接跑，不联网。

CIF 口径与 scripts/quote_engine.py 完全一致，不许两套算法打架：
    CIF = (FOB + 海运费) ÷ (1 − 投保加成 × 保险费率)，投保加成 110%
    保险费 = CIF × 110% × 保险费率
    关税 = CIF × 关税税率
    DDP 单条 = CIF + 关税 + 目的港杂费
    总计 = 单条 × 条数

用法:
    python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2
    python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --qty 100 --sell-price 48
    python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --format json
    python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --audience client --out landed_client.txt

参数:
    --fob           FOB 单价（每条），必填，币种由 --currency 决定
    --freight       到目的港海运费（每条），默认 0
    --insurance     保险费率（占 CIF 货值的百分比 %），默认 0.15（海运险通常 0.1%–0.3%）
    --insurance-rate  高级入口：保险费率（比率），如 0.0015 = 0.15%，可覆盖 --insurance
    --port-charges  目的港杂费（每条：THC/卸货/清关代理等），默认 0
    --duty          关税税率（%），默认 0
    --vat-rate      进口增值税率（%，默认 0 = 不算；给了就按 (CIF+关税)×税率 计入 DDP，
                    DDP 就是含税价。13 只是示例（【示例】，未核实），不是默认税率；
                    它等于中国增值税标准税率（PwC，中国一般纳税人销售/进口大多数货物
                    自 2019-04-01 起 13%，2026-11-24 核实），不是任何目的港的进口增值税；
                    适用税率以税务规定/清关代理核实为准，报 DDP 前跟清关代理核对。
                    不给税率时 DDP 是未税价，表里和 JSON 里都会明说缺了进口增值税率）
    --qty           条数，默认 1
    --sell-price    拟售价（每条，可选），给了才算每条利润空间
    --currency      币种符号，默认 USD
    --unit          计价单位，默认 条
    --audience      internal(默认，含 FOB 底价与利润) / client(客户视图，FOB/费率/利润全砍)
    --out           同时写入文件（UTF-8），不指定则只打印
    --format        table(默认) / json

两条规矩：
    FOB 底价只在 internal 视图里露脸，发客户记得加 --audience client，别把底价寄出去。
    关税税率、目的港杂费都是估算口径——报 DDP 之前务必跟目的国清关代理核实最新税率，
    DDP 没有可靠的清关代理就别报（见 docs/06-quote.md 的 DDP 那一行）。
"""

import argparse
import json
import os
import sys
import unicodedata
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import _ZhArgumentParser, _pad, _width, fmt, money  # noqa: E402

# 可调常量：要改默认数值就动这边（与 quote_engine.py 同值，改一处必须改另一处）
DEFAULT_INSURANCE_PCT = 0.15     # 默认保险费率（占 CIF 货值的百分比）
INSURANCE_COVER_FACTOR = 1.10    # 投保加成：按 CIF 货值 110% 投保（行业惯例 110%）
MAX_INSURANCE_RATE = 0.05        # 费率 >5% 判定为「单位输错」，直接报错
MAX_DUTY_PCT = 1000.0            # 关税税率上限 1000%（反倾销税可能很高，但 1000% 以上基本是单位错）
MAX_VAT_RATE_PCT = 100.0         # 进口增值税率上限 100%（超过基本是单位错）
EXAMPLE_VAT_RATE_PCT = 13.0      # 示例增值税率 (example VAT rate ONLY)：只出现在 --help/示例里，
                                 # 从未核实、不是默认值（默认 0 = 不算税）。适用税率以税务规定/
                                 # 清关代理核实为准；拿它当真税率报 DDP 就是编数。
DEFAULT_CURRENCY = "USD"         # 输出币种符号（所有金额都带，不让新人猜）
DEFAULT_UNIT = "条"              # 计价单位（轮胎按条计）










def build_landed_cost(fob, freight, insurance_rate, duty_pct,
                      port_charges=0.0, qty=1, sell_price=None,
                      cover_factor=INSURANCE_COVER_FACTOR, vat_rate_pct=0.0):
    """算 CIF / DDP 分项 + 单条成本 +（给了售价）每条利润空间。

    计价链路（严格按顺序，每步只做一次）:
        FOB ──(+海运费)──> (FOB+运费) ──÷(1 − 投保加成×费率)──> CIF
             ──×投保加成×费率──> 保险费（自检：CIF = FOB+运费+保险费）
        关税 = CIF × 关税税率；DDP 单条 = CIF + 关税 + 目的港杂费；总计 = 单条 × 条数
    CIF 那一步与 quote_engine.build_quote() 逐字同一条公式，同一组 FOB+运费+费率
    两边算出的 CIF 必须一致（见 tests/test_landed_cost.py 的交叉核对）。

    Import VAT / 进口增值税 (vat_rate_pct > 0 时才算，不给税率就是老样子）:
        进口增值税 = (CIF + 关税) × 税率，计入 DDP：DDP = CIF + 关税 + 目的港杂费 + 进口增值税。
        给了税率，DDP 就是含税价；不给，DDP 是未税价——口径写在输出里，不让人猜。
    """
    # 输入校验：错了就直接报错，绝不悄悄塞个错成本出去
    if fob <= 0:
        raise ValueError("FOB 单价必须 > 0")
    if fob > 10_000_000:
        raise ValueError("FOB 单价 %s 大得离谱（上限 10,000,000/条）：是不是多输了几个 0，"
                         "或把整柜总价当成了单价？" % fmt(fob))
    if freight < 0:
        raise ValueError("海运费不能为负（负数会让 CIF 低于 FOB）")
    if freight > 10_000_000:
        raise ValueError("海运费 %s 大得离谱（上限 10,000,000/条）：是不是把整柜运费当成了每条运费？"
                         % fmt(freight))
    if port_charges < 0:
        raise ValueError("目的港杂费不能为负")
    if port_charges > 10_000_000:
        raise ValueError("目的港杂费 %s 大得离谱（上限 10,000,000/条）" % fmt(port_charges))
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
    if qty < 1:
        raise ValueError("条数必须 ≥ 1，收到的是 %s" % qty)
    if sell_price is not None and sell_price <= 0:
        raise ValueError("拟售价必须 > 0，收到的是 %s" % sell_price)
    if vat_rate_pct < 0:
        raise ValueError("进口增值税率不能为负")
    if vat_rate_pct > MAX_VAT_RATE_PCT:
        raise ValueError("进口增值税率 %.1f%% 大得离谱（上限 %.0f%%）：这里填百分比，例如 13 表示 13%%，"
                         "不是 1300。" % (vat_rate_pct, MAX_VAT_RATE_PCT))

    # ---- CIF：保险按 CIF 货值的 110% 投保 → CIF = (FOB+运费) / (1 - 投保加成×费率)
    denom = 1 - cover_factor * insurance_rate
    if denom <= 0:
        raise ValueError("保险费率过高(≥ %.1f%%)导致 CIF 分母非正，请检查 --insurance 单位"
                         % (100.0 / cover_factor))
    cif = (fob + freight) / denom
    insurance = cif * cover_factor * insurance_rate
    # 自检：CIF 必须等于 FOB+运费+保险费（防止公式写错却看不出来）
    if abs(cif - (fob + freight + insurance)) > 0.005:
        raise ValueError("CIF 恒等式校验失败，请检查投保加成参数")

    # ---- DDP 单条：CIF + 关税 + 目的港杂费（+ 进口增值税，如果给了税率）；总计 = 单条 × 条数
    duty = cif * duty_pct / 100.0
    vat = (cif + duty) * vat_rate_pct / 100.0 if vat_rate_pct > 0 else 0.0
    ddp_unit = cif + duty + port_charges + vat

    result = {
        "fob_unit": money(fob),
        "freight_unit": money(freight),
        "insurance_unit": money(insurance),
        "insurance_cover_factor": cover_factor,
        "insurance_rate": insurance_rate,
        "cif_unit": money(cif),
        "duty_pct": duty_pct,
        "duty_unit": money(duty),
        "port_charges_unit": money(port_charges),
        "ddp_unit": money(ddp_unit),
        "qty": qty,
        "cif_total": money(cif * qty),
        "duty_total": money(duty * qty),
        "port_charges_total": money(port_charges * qty),
        "ddp_total": money(ddp_unit * qty),
        "warnings": [],
        # Tax-rate provenance / 税率口径：税率是调用方显式输入的数，脚本没有核实过；
        # 没给税率时 DDP 是未税价，必须明说缺哪项，不能悄悄当成含税价发出去。
        "vat_status": "provided" if vat_rate_pct > 0 else "not_provided",
    }
    if vat_rate_pct <= 0:
        result["vat_missing"] = ["进口增值税率 (import VAT rate)"]
        result["warnings"].append(
            "未给进口增值税率：DDP 是未税价（不含进口增值税），不是含税价；"
            "报含税 DDP 先用 --vat-rate <税率> 补上，税率以税务规定/清关代理核实为准。")
    if vat_rate_pct > 0:
        result.update({
            "vat_rate_pct": money(vat_rate_pct),
            "vat_unit": money(vat),
            "vat_total": money(vat * qty),
        })

    # ---- 利润空间：给了售价才算（售价 − DDP 单条）；没给就不出利润字段
    if sell_price is not None:
        profit_unit = sell_price - ddp_unit
        result["sell_price"] = money(sell_price)
        result["profit_unit"] = money(profit_unit)
        result["profit_total"] = money(profit_unit * qty)
        result["profit_margin_pct"] = money(profit_unit / sell_price * 100.0)
        if profit_unit < 0:
            result["warnings"].append(
                "拟售价 %s 低于 DDP 单条成本 %s：这单按这个价做是亏的，"
                "先抬售价或压成本，别硬接。" % (fmt(sell_price), fmt(ddp_unit)))
    if duty_pct > 50:
        result["warnings"].append(
            "关税税率 %.1f%% 很高（反倾销税常见）：确认这是目的国最新税率再报 DDP，"
            "税率一变 DDP 全变。" % duty_pct)

    return result


def client_view(r):
    """客户视图：只给 CIF/DDP 总价和分项大类，FOB 底价、保险费率、利润空间全砍。

    只砍数字不够：FOB + 运费 + 保险费三样凑在一起能反推 CIF 的构成，
    所以运费、保险费、保险费率、拟售价、利润全部砍掉，只留 CIF、关税、目的港杂费、DDP。
    """
    return {k: v for k, v in r.items()
            if k not in ("fob_unit", "freight_unit", "insurance_unit",
                         "insurance_rate", "insurance_cover_factor",
                         "sell_price", "profit_unit", "profit_total",
                         "profit_margin_pct", "warnings")}


def render_table(r, currency=DEFAULT_CURRENCY, unit=DEFAULT_UNIT,
                 audience="internal", meta=None):
    meta = meta or {}
    per = "%s/%s" % (currency, unit)          # 每张表都带币种+单位，不让新人猜
    W = 66
    is_client = audience == "client"
    s = []
    s.append("=" * W)
    s.append("  到岸成本（客户视图，只给 CIF/DDP 总价和分项大类）" if is_client
             else "  到岸成本（内部视图，含 FOB 底价与利润，这版别发客户）")
    s.append("  币种: %s · 计价单位: %s · 条数: %s · 生成时间: %s"
             % (currency, unit, r["qty"], meta.get("generated_at", "-")))
    s.append("=" * W)

    rows = []
    if not is_client:
        rows.append(("FOB 单价: 离岸价，不含运费保险", fmt(r["fob_unit"])))
        rows.append(("海运费: 装运港 → 目的港（每条）", fmt(r["freight_unit"])))
        rows.append(("其中保险费 = CIF×%.0f%%×费率" % (r["insurance_cover_factor"] * 100),
                     fmt(r["insurance_unit"])))
    rows.append(("CIF 单条: 到岸价，含运费+保险", fmt(r["cif_unit"])))
    rows.append(("关税（单条）: CIF × %.2f%%" % r["duty_pct"], fmt(r["duty_unit"])))
    rows.append(("目的港杂费（单条）: THC/卸货/清关代理", fmt(r["port_charges_unit"])))
    if "vat_unit" in r:
        rows.append(("进口增值税（单条，估算）: (CIF+关税) × %.2f%%" % r["vat_rate_pct"],
                     fmt(r["vat_unit"])))
    rows.append(("DDP 单条: 完税后交货价%s" % ("（含进口增值税）" if "vat_unit" in r else "（未含进口增值税）"),
                 fmt(r["ddp_unit"])))
    label_w = max(_width(l) for l, _ in rows)
    for label, val in rows:
        s.append("  %s │ %10s %s" % (_pad(label, label_w), val, per))

    s.append("-" * W)
    s.append("  合计（%s %s）" % (r["qty"], unit))
    total_rows = [
        ("CIF 总计", fmt(r["cif_total"])),
        ("关税总计", fmt(r["duty_total"])),
        ("目的港杂费总计", fmt(r["port_charges_total"])),
        ("DDP 总计", fmt(r["ddp_total"])),
    ]
    if "vat_total" in r:
        total_rows.insert(3, ("进口增值税总计", fmt(r["vat_total"])))
    label_w = max(_width(l) for l, _ in total_rows)
    for label, val in total_rows:
        s.append("  %s │ %10s %s" % (_pad(label, label_w), val, currency))

    if not is_client and "sell_price" in r:
        s.append("-" * W)
        s.append("  利润空间（拟售价 %s %s）" % (fmt(r["sell_price"]), per))
        s.append("  每条利润 %s %s · 合计利润 %s %s · 利润率 %.2f%%（按售价）"
                 % (fmt(r["profit_unit"]), per, fmt(r["profit_total"]), currency,
                    r["profit_margin_pct"]))

    s.append("-" * W)
    s.append("  顺手记几个词（完整版去翻 docs/06-quote.md 的条款表）")
    s.append("   · CIF 到岸价：FOB + 海运费 + 保险费，卖方付到目的港。")
    s.append("   · DDP 完税后交货：CIF + 关税 + 目的港杂费，包到买方门口。")
    if "vat_unit" in r:
        s.append("   · 进口增值税（估算）：(CIF + 关税) × %.2f%%，已计入上面 DDP；"
                 "给了税率 DDP 就是含税价；税率是调用方输入的数，脚本没有核实过，"
                 "适用税率以税务规定/清关代理核实的最新税率为准。"
                 % r["vat_rate_pct"])
    else:
        s.append("   · 进口增值税：未给税率，未计入上面 DDP —— 缺：进口增值税率；"
                 "补上用 --vat-rate <税率>（示例 13，【示例】，未核实），"
                 "适用税率以税务规定/清关代理核实为准。")
    s.append("   · 投保加成 %.0f%%：保险按 CIF 货值的 %.0f%% 投保，所以 "
             "CIF = (FOB+运费) ÷ (1 − %.2f×费率)，与 quote_engine.py 同一条公式。"
             % (r["insurance_cover_factor"] * 100, r["insurance_cover_factor"] * 100,
                r["insurance_cover_factor"]))
    s.append("   · 关税按 CIF 计：税率、目的港杂费都是估算口径，报 DDP 前务必跟目的国"
             "清关代理核实最新税率；没有可靠清关代理就别报 DDP。")

    if not is_client and r.get("warnings"):
        s.append("-" * W)
        s.append("  内部提醒（这截别贴进发给客户的文件）:")
        for w in r["warnings"]:
            s.append("    - %s" % w)
    s.append("=" * W)
    return "\n".join(s)




def main():
    p = _ZhArgumentParser(
        prog="landed_cost.py",
        description="算到岸成本：FOB + 运费 + 保险 → CIF，再加关税 + 目的港杂费 → DDP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例（【示例】价格全部虚构，亲手跑过，输出见 docs/landed-cost.md）:\n"
               "  python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2\n"
               "    → CIF 单条 35.06，DDP 单条 40.56（USD/条，内部视图）\n"
               "  python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --qty 100 --sell-price 48\n"
               "    → DDP 总计 4056.36，每条利润 7.44，利润率 15.49%\n"
               f"  python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --qty 100 --sell-price 48 --vat-rate {EXAMPLE_VAT_RATE_PCT:g}\n"
               "    → 进口增值税每条 5.01，DDP 单条 45.58（含税价），每条利润 2.42，利润率 5.05%（【示例】13% 只是算例：它等于中国增值税标准税率，不是目的港进口增值税；报 DDP 前按清关代理核实的税率算）\n"
               "  python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --audience client\n"
               "    → 同样两个总价，FOB/运费/保险费率/利润全砍掉，这版才能发客户\n"
               "  python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --format json\n"
               "    → JSON 版，分项 breakdown 一次给全，方便贴进表格\n"
               "  发客户永远加 --audience client：内部视图的 FOB 底价和利润一旦寄出去就收不回来。")
    p.add_argument("--fob", type=float, required=True, help="FOB 单价(每条)")
    p.add_argument("--freight", type=float, default=0.0, help="到港海运费（每条）")
    p.add_argument("--insurance", type=float, default=DEFAULT_INSURANCE_PCT,
                   help="保险费率(占 CIF 货值的百分比%%，默认 %(default)s)")
    p.add_argument("--insurance-rate", type=float, default=None,
                   help="高级入口：保险费率(比率，如 0.0015=0.15%%)，覆盖 --insurance")
    p.add_argument("--port-charges", type=float, default=0.0,
                   help="目的港杂费（每条：THC/卸货/清关代理等）")
    p.add_argument("--duty", type=float, default=0.0, help="关税税率(%%)，默认 %(default)s")
    p.add_argument("--vat-rate", type=float, default=0.0,
                   help="进口增值税率(%%)，默认 0=不算；给了就按 (CIF+关税)×税率 计入 DDP；"
                        "示例 13（【示例】，未核实）")
    p.add_argument("--qty", type=int, default=1, help="条数，默认 %(default)s")
    p.add_argument("--sell-price", type=float, default=None,
                   help="拟售价（每条，可选），给了才算每条利润空间")
    p.add_argument("--currency", default=DEFAULT_CURRENCY, help="币种符号, 默认 USD")
    p.add_argument("--unit", default=DEFAULT_UNIT, help="计价单位, 默认 条")
    p.add_argument("--audience", choices=["internal", "client"], default="internal",
                   help="internal=含 FOB 与利润(默认) / client=客户视图，绝不泄露底价与利润")
    p.add_argument("--out", default=None, help="把结果写入文件(UTF-8)")
    p.add_argument("--format", choices=["table", "json"], default="table")
    if len(sys.argv) == 1:
        p.print_usage(sys.stderr)
        print("\n没给参数：不知道怎么填就跑 python scripts/landed_cost.py --help，"
              "里面有能直接复制的例子。", file=sys.stderr)
        raise SystemExit(2)
    args = p.parse_args()

    # 保险费率：默认收「百分比」，内部换算为比率；--insurance-rate 为高级比率入口
    rate = args.insurance_rate if args.insurance_rate is not None else args.insurance / 100.0

    if args.qty < 1:
        raise SystemExit("✗ --qty 条数必须 ≥ 1，收到的是 %s" % args.qty)
    if args.sell_price is not None and args.sell_price <= 0:
        raise SystemExit("✗ --sell-price 拟售价必须 > 0，收到的是 %s" % args.sell_price)

    try:
        r = build_landed_cost(args.fob, args.freight, rate, args.duty,
                              args.port_charges, args.qty, args.sell_price,
                              vat_rate_pct=args.vat_rate)
    except ValueError as e:
        raise SystemExit("✗ %s" % e)

    meta = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "currency": args.currency,
        "unit": args.unit,
        "audience": args.audience,
        "inputs": {"fob": args.fob, "freight": args.freight, "duty_pct": args.duty,
                   "port_charges": args.port_charges, "qty": args.qty,
                   "insurance_rate": rate, "sell_price": args.sell_price,
                   "vat_rate_pct": args.vat_rate},
    }

    if args.format == "json":
        payload_r = client_view(r) if args.audience == "client" else r
        # 客户视图的 meta 也得脱敏：inputs 里有 FOB/运费/费率/售价，客户拿 CIF 一除就能反推
        payload_meta = dict(meta)
        if args.audience == "client":
            payload_meta.pop("inputs", None)
        out = json.dumps({"meta": payload_meta, "landed_cost": payload_r},
                         ensure_ascii=False, indent=2)
    else:
        out = render_table(r, args.currency, args.unit, args.audience, meta)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
    print(out)


if __name__ == "__main__":
    main()
