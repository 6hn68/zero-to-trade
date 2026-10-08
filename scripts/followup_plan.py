#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
followup_plan.py — 生成 7 天 3 触达跟进计划表

第一条消息发出去之后，真正的钱在跟进。本脚本按T0/T1 生成一份带具体日期的
7 天三次触达表：哪天做什么、带什么新信息、什么时候该停手。

只用标准库，Python 3.8+ 可直接跑。

用法:
    python scripts/followup_plan.py --tier T0 --start 2026-10-08
    python scripts/followup_plan.py --tier T1 --start 2026-10-08 --csv examples/leads_example.csv
    python scripts/followup_plan.py --tier T0 --start 2026-10-08 --format csv --out plan.csv

为什么是 3 次而不是 7 次:
    跟进不是越多越好。第 3 次仍无回应，就该停手进长名单——
    继续发只会拉低你的域名信誉，而且对方已经用行为告诉你答案了。
"""

import argparse
import csv
import sys
from datetime import datetime, timedelta

TIER_LABEL = {
    "T0": "立即建联（多线并进）",
    "T1": "本周首触",
    "T2": "低频培育",
    "T3": "暂不投入",
}

# 每个tier 的 7 天节奏：[第几天, 触达方式, 主题, 必须带的新信息, 停止条件]
CADENCE = {
    "T0": [
        ("D0",  "首触邮件",
         "直接 + 一句只对他成立的话",
         "规格与报价区间（不含底价）",
         "—"),
        ("D2",  "第二条邮件（换渠道）",
         "同一封信转到WhatsApp / 领英，主题不变",
         "配柜量参考（同规格 40HQ 能装多少）",
         "两次都无回应 → 停手"),
        ("D5",  "最后一次",
         "给一个台阶：「这条路先放着，你随时找我」",
         "一条真正有用的行业信息（价格带/认证提醒/行情）",
         "仍无回应 → 进长名单，季度扫一次"),
    ],
    "T1": [
        ("D0",  "首触邮件",
         "轻、具体、给一个容易回应的理由",
         "一个具体数字（价格区间或规格）",
         "—"),
        ("D3",  "换渠道跟进",
         "领英/WhatsApp 同一诉求，不重复全文",
         "配柜量参考",
         "两次无回应 → 降到 T2 节奏"),
        ("D6",  "最后一次",
         "问「现在不是时候？」这种二选一",
         "一条行业信息或市场小新闻",
         "仍无回应 → 进低频池"),
    ],
    "T2": [
        ("D0",  "确认信息",
         "只问是否还在采购，不求回复",
         "无需信息成本",
         "—"),
        ("D7",  "仅在有行情时发",
         "带一条具体行情/涨价/认证通知",
         "行情或政策变化",
         "两次无回应 → 季度扫一次"),
        ("D14", "降级出池",
         "无回应视为不需要",
         "—",
         "归档，不再主动打扰"),
    ],
}

CADENCE_HINT = {
    "T0": "多线并进：同一天可以同时推进多个 T0，但每个都要单独定制那一句 why them。",
    "T1": "每天固定时段（如上午 9 点、下午 3 点）批量处理，别随时零散发。",
    "T2": "每周最多一次，且只在有行业信息时才发。",
    "T3": "不发。信息不足，先补联系方式和需求判断。",
}


def build_plan(tier, start, company=None):
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    steps = CADENCE[tier]
    rows = []
    for offset, channel, subject, newinfo, stop in steps:
        day = int(offset[1:])
        date = start_dt + timedelta(days=day)
        rows.append({
            "tier": tier,
            "offset": offset,
            "date": date.strftime("%Y-%m-%d"),
            "weekday": "一二三四五六日"[date.weekday()],
            "company": company or "(全部本级线索)",
            "channel": channel,
            "subject": subject,
            "new_info": newinfo,
            "stop_rule": stop,
        })
    return rows


def print_plan(tier, start, rows, companies):
    label = TIER_LABEL[tier]
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    print("")
    print("=" * 74)
    print("  7 天跟进计划  ·  %s (%s)" % (tier, label))
    print("  起算日: %s   线索数: %d" % (start_dt.strftime("%Y-%m-%d"), len(companies)))
    print("=" * 74)
    print("")
    print("节奏提醒: %s" % CADENCE_HINT[tier])
    print("")
    print("-" * 74)
    for r in rows:
        print("【%s】%s 周%s" % (r["offset"], r["date"], r["weekday"]))
        print("  触达方式 : %s" % r["channel"])
        print("  这封要什么: %s" % r["subject"])
        print("  必须带   : %s" % r["new_info"])
        if r["stop_rule"] != "—":
            print("  停止条件 : %s" % r["stop_rule"])
        print("")
    print("-" * 74)
    print("本级公司清单（按跟进优先级排）:")
    for i, c in enumerate(companies, 1):
        print("  %d. %s" % (i, c))
    print("")
    print("每次跟进前自查:")
    print("  □ 这封比上一封多了什么新东西？没有新东西就别发")
    print("  □ 「why them」那句话还是只对这家公司成立吗")
    print("  □ 第 %s 次了？该考虑停手，不要靠意志力硬撑" % rows[-1]["offset"])
    print("")
    print("=" * 74)
    print("")


def main():
    p = argparse.ArgumentParser(
        description="生成 7 天 3 触达跟进计划表（只用标准库）",
        epilog="示例:\n  python scripts/followup_plan.py --tier T0 --start 2026-10-08")
    p.add_argument("--tier", choices=["T0", "T1", "T2"], default="T0",
                   help="要规划的层级，默认 T0")
    p.add_argument("--start", required=True, help="起算日 YYYY-MM-DD（通常是首触发送日）")
    p.add_argument("--csv", help="线索 CSV，用于列出本级公司名（可选）")
    p.add_argument("--company", help="只给单个公司排期")
    p.add_argument("--format", choices=["table", "csv"], default="table")
    p.add_argument("--out", help="CSV 格式时的输出路径")
    args = p.parse_args()

    try:
        start_dt = datetime.strptime(args.start, "%Y-%m-%d")
    except ValueError:
        raise SystemExit("错误：--start 日期格式应为 YYYY-MM-DD，收到的是 %r" % args.start)

    companies = []
    if args.csv:
        try:
            sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
            from lead_score import analyze, read_leads
            leads = [l for l in analyze(read_leads(args.csv)) if l["tier"] == args.tier]
            companies = [l["company"] for l in leads]
        except FileNotFoundError:
            raise SystemExit("错误：找不到文件 %s" % args.csv)

    rows = build_plan(args.tier, args.start, args.company)

    if args.format == "csv":
        path = args.out or "followup_plan_%s.csv" % args.tier
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow(r)
            for c in companies:
                w.writerow(dict(r, company=c))
        print("已写入 %s" % path)
        return

    print_plan(args.tier, args.start, rows, companies)


if __name__ == "__main__":
    main()
