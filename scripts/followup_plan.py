#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
排跟进节奏的。按 T0/T1/T2/T3 给你一张带具体日期的触达表：哪天、走哪个渠道、
这次说什么、必须带什么新信息、什么时候该停手。

第一条消息发出去之后，真正的钱在跟进。

节奏因 tier 而异（跨度不同，不是都叫「7 天」）:
    T0  D0 / D2 / D5     高频，首 6 天内三次差异化触达
    T1  D0 / D3 / D6     常规，首 7 天内三次
    T2  D0 / D7 / D14    低频培育，只在有行情时才发
    T3  不排触达          信息不足，先补信息；本级的止损线就是 0 次

止损线（第 3 次触达后还零回应就停）:
    第 3 次触达后仍无任何回应（含已读不回）→ 无条件停手，进长名单，季度扫一次。
    继续发只会拉低域名信誉，而且对方已经用行为告诉你答案了。

时间与地区（不联网，只给提示，具体节假日请自行核对当年日历）:
    · 海湾客户周五是主麻日（午间礼拜），当天基本不看邮件；沙特周末周五+周六，
      阿联酋已改为周六+周日。默认按 gcc 规则标注，可用 --market generic 切换。
    · 斋月/开斋节/宰牲节/当地国庆、8 月欧洲假期、12 月圣诞、中国春节与国庆：
      回复率骤降或停摆，节奏放宽或整体推后，不要在那时做「最后一次」催单。
    · 发信时间按对方当地时间上午 9-11 点，不是你的上午 9 点。
    · 加 --avoid-weekend 可把落在周末的触达自动顺延到下一个工作日。

防骚扰（别把自己域名玩进黑名单）:
    相邻两次至少间隔 MIN_GAP_DAYS 个自然日；同一批线索绝不用同一份文案群发
    （同文案群发会被判垃圾邮件，域名进黑名单后所有客户都受影响）。

只用标准库，Python 3.8+ 可直接跑。

用法:
    python scripts/followup_plan.py --tier T0 --start 2026-10-08
    python scripts/followup_plan.py --tier T1 --start 2026-10-08 --csv examples/leads_example.csv
    python scripts/followup_plan.py --tier T0 --start 2026-10-08 --format csv --out plan.csv
    python scripts/followup_plan.py --tier T0 --start 2026-10-08 --format json --out plan.json
    python scripts/followup_plan.py --tier T2 --start 2026-10-08 --market gcc --avoid-weekend

--start 必填，而且不吃你电脑的当天日期：
    计划日期得能复现——同样的 (tier, start) 换台机器跑，结果一模一样，别人能照着重排。

输出长这样（table / csv / json 三格式同一套字段）:
    tier, offset, gap_days, date, weekday, timing_note, company,
    channel, angle, new_info, stop_rule, draft_from
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta

TIER_LABEL = {
    "T0": "立即建联（多线并进）",
    "T1": "本周首触",
    "T2": "低频培育",
    "T3": "暂不投入",
}

# 每一级的实际跨度（标题里不再笼统写「7 天」，T2 跨度其实是 15 天）
TIER_SPAN = {
    "T0": "D0-D5，6 天 3 触达",
    "T1": "D0-D6，7 天 3 触达",
    "T2": "D0-D14，15 天低频培育",
    "T3": "不排触达（0 次）",
}

# 止损线：第 N 次之后无条件停手；以及相邻两次的最小间隔（防骚扰）
MAX_TOUCHES = 3
MIN_GAP_DAYS = 2
STOP_LINE = ("第 %d 次触达后仍无任何回应（含已读不回）→ 无条件停手，进长名单，季度扫一次。"
             % MAX_TOUCHES)

# 每个 tier 的节奏：[第几天, 渠道, 这次具体说什么（角度）, 必须带的新信息, 停止条件, 文案来源]
# 停止条件按「已经发出去的那一封」来写：D2 时只发过 D0，不能写「两次无回应」。
CADENCE = {
    "T0": [
        ("D0", "首触邮件",
         "直接 + 一句只对他成立的话（why them），结尾只问规格和年用量",
         "规格与报价区间（不含底价）",
         "—",
         "outreach_gen.py --tier T0 的产出，别自己另写一版"),
        ("D2", "换渠道：WhatsApp / 领英（同一诉求，不复制全文）",
         "承认他忙，一句话复述诉求，只问一个 20 秒能回答的问题",
         "配柜量参考（同规格 40HQ 能装多少）",
         "D0 明确拒绝 → 立刻停手；已读不回 → 按计划走",
         "自写，禁止复用 D0 全文"),
        ("D5", "最后一次（收尾信）",
         "给台阶：「这条路先放着，你随时找我」，并留下一条对他有用的信息",
         "一条真正有用的行业信息（价格带 / 认证提醒 / 行情）",
         STOP_LINE,
         "自写收尾信（写法见 docs/04-outreach.md）"),
    ],
    "T1": [
        ("D0", "首触邮件",
         "轻、短，只问一个 20 秒能答的问题（今年是否还在采购）",
         "一个具体数字（价格区间或规格）",
         "—",
         "outreach_gen.py --tier T1 的产出"),
        ("D3", "换渠道跟进（领英 / WhatsApp）",
         "把 D0 的问题换个说法再问一次，不要重发全文",
         "配柜量参考或一个同行案例",
         "D0 明确说不需要 → 停手；石沉大海 → 按计划走",
         "自写，禁止复用 D0 全文"),
        ("D6", "最后一次（二选一收尾）",
         "二选一：「现在不是时候」还是「规格不合适」？给他一个一键回复的选项",
         "一条行业信息或市场小新闻",
         STOP_LINE + "（本级停手后降进低频池）",
         "自写收尾信"),
    ],
    "T2": [
        ("D0", "确认信息（不求回复）",
         "只确认一件事：今年还从亚洲采购吗？回一个是/不是就够",
         "无需信息成本",
         "—",
         "outreach_gen.py --tier T2 的产出"),
        ("D7", "仅在有行情时发（没行情就跳过）",
         "带一条具体行情 / 涨价 / 认证变更通知，全程不催单",
         "行情或政策变化（没有就别发）",
         "无行情可发 → 跳过这一步，不要为了凑次数而发",
         "自写"),
        ("D14", "降级出池（不用写信）",
         "不发送。无回应视为不需要，直接归档",
         "—",
         "归档，移出主动触达名单",
         "不用写"),
    ],
    # T3 的止损线就是 0 次：信息不足，补齐前一次都不要发。空列表 = 不排任何触达。
    "T3": [],
}

CADENCE_HINT = {
    "T0": "多线并进：同一天可以同时推进多个 T0，但每个都要单独定制那一句 why them。",
    "T1": "每天固定时段批量处理（按对方当地时间上午），别随时零散发。",
    "T2": "每周最多一次，且只在有行业信息时才发。",
    "T3": "不发。信息不足，先补联系方式和需求判断，补完重跑 lead_score.py 重新分级。",
}

# 目标市场：决定「周末是哪两天」和发送时段。差别不小，海湾那边周五是主麻日。
MARKETS = {
    "gcc": {
        "label": "海湾 / 中东（沙特、阿曼、科威特等；阿联酋周末已改为周六+周日）",
        "weekend": (4, 5),          # datetime.weekday(): 周一=0 … 周五=4, 周六=5
        "weekend_note": "周五（主麻日）+ 周六",
        "tz_note": "UTC+3~+4，比北京时间晚 4-5 小时：对方上午 9 点 ≈ 北京 13-14 点",
    },
    "generic": {
        "label": "通用（欧洲 / 拉美 / 非洲等，周末按周六周日）",
        "weekend": (5, 6),
        "weekend_note": "周六 + 周日",
        "tz_note": "时区各异，统一按对方当地时间上午 9-11 点发，不要用你的上午",
    },
}

# 节假日提示只给提醒不替你查：脚本不联网，具体哪天自己对着当年日历核对
HOLIDAY_ADVISORY = [
    "周五是主麻日（午间礼拜），海湾客户当天基本不看邮件；触达排在周日至周四。",
    "斋月（伊斯兰历第九月，每年比公历提前约 10-11 天，日期逐年不同）：白天回复率极低，"
    "节奏放宽一倍，别催单。",
    "开斋节 / 宰牲节前后各一周、当地国庆日：业务基本停摆，不要把「最后一次」排在这时候。",
    "8 月欧洲休假、12 月中下旬圣诞、中国春节与国庆：同理，提前排完或整体推后。",
    "以上只作提示，本脚本不联网也不存节假日表，具体日期请自行核对当年日历。",
]

# 防骚扰：踩一次雷，赔掉的是你整个发信域名的信誉
ANTI_SPAM = [
    "相邻两次触达至少间隔 %d 个自然日，换渠道也一样（别因为换成 WhatsApp 就连着发）。"
    % MIN_GAP_DAYS,
    "同一批线索绝不用同一份文案群发：同文案群发会被判垃圾邮件，域名进黑名单后，"
    "你所有客户都受影响。",
    "同一家公司不要在同一封邮件线程里连续顶 3 次以上，第 2 封起换主题行重新起一封。",
    "每次都要带至少一条对对方有用的新信息；没有新信息就不要发这一封。",
]

# 输出字段：table / csv / json 三种格式用同一套字段名与顺序
FIELDS = ["tier", "offset", "gap_days", "date", "weekday", "timing_note",
          "company", "channel", "angle", "new_info", "stop_rule", "draft_from"]


def _short(text, limit=40):
    """表格展示用：超长公司名截断，避免一行撑爆终端。CSV/JSON 仍写完整值。"""
    text = (text or "").strip()
    return text if len(text) <= limit else text[:limit] + "…"


def _day_offset(offset):
    """'D2' → 2。CADENCE 里的标签解析失败要立刻炸，不能悄悄排错日期。"""
    if not (len(offset) >= 2 and offset[0] == "D" and offset[1:].isdigit()):
        raise ValueError("节奏标签格式应为 D+天数（如 D2），收到的是 %r" % offset)
    return int(offset[1:])


def build_plan(tier, start, company=None, market="gcc", avoid_weekend=False):
    """按 tier 排出带具体日期的触达表。纯函数，跑完给你表就完事，不联网也不动你的文件。

    avoid_weekend=True 时，落在目标市场周末的触达自动顺延到下一个工作日，
    并在 timing_note 里写明原定日期（offset 仍是计划值，实际日期才是要执行的）。
    """
    if tier not in CADENCE:
        raise ValueError("未知 tier：%s（可选：%s）" % (tier, "/".join(CADENCE)))
    if market not in MARKETS:
        raise ValueError("未知 market：%s（可选：%s）" % (market, "/".join(MARKETS)))
    try:
        start_dt = datetime.strptime(start, "%Y-%m-%d")
    except ValueError:
        raise ValueError("起算日格式应为 YYYY-MM-DD，收到的是 %r" % start)

    mk = MARKETS[market]
    weekend = set(mk["weekend"])
    scope = (company or "").strip() or "(本级全部线索)"
    rows = []
    prev_dt = None
    for offset, channel, angle, newinfo, stop, draft in CADENCE[tier]:
        day = _day_offset(offset)
        planned = start_dt + timedelta(days=day)
        date = planned
        notes = []
        # 1) 保证与上一次至少间隔 MIN_GAP_DAYS：顺延周末后两步可能撞到同一天
        if prev_dt is not None and (date - prev_dt).days < MIN_GAP_DAYS:
            date = prev_dt + timedelta(days=MIN_GAP_DAYS)
            notes.append("与上一次间隔不足 %d 天，已推后" % MIN_GAP_DAYS)
        # 2) 周末处理：顺延（--avoid-weekend）或只标注提示
        if avoid_weekend:
            shifted = 0
            while date.weekday() in weekend and shifted < 7:
                date += timedelta(days=1)
                shifted += 1
            if shifted:
                notes.append("逢%s，已顺延 %d 天" % (mk["weekend_note"], shifted))
        elif date.weekday() in weekend:
            notes.append("逢%s，建议顺延（加 --avoid-weekend 自动排开）"
                         % mk["weekend_note"])

        rows.append({
            "tier": tier,
            "offset": offset,
            "gap_days": 0 if prev_dt is None else (date - prev_dt).days,
            "date": date.strftime("%Y-%m-%d"),
            "weekday": "一二三四五六日"[date.weekday()],
            "timing_note": "；".join(notes),
            "company": scope,
            "channel": channel,
            "angle": angle,
            "new_info": newinfo,
            "stop_rule": stop,
            "draft_from": draft,
        })
        prev_dt = date
    return rows


def plan_followups(tier, start, company=None, market="gcc", avoid_weekend=False):
    """README 对外承诺的可导入入口（同 build_plan）：纯函数，返回行字典列表。"""
    return build_plan(tier, start, company=company, market=market,
                      avoid_weekend=avoid_weekend)


def print_plan(tier, start, rows, companies, market="gcc", scope="(本级全部线索)",
               csv_path=None):
    mk = MARKETS[market]
    print("")
    print("=" * 74)
    print("  跟进计划（%s）  ·  %s (%s)" % (TIER_SPAN[tier], tier, TIER_LABEL[tier]))
    print("=" * 74)
    print("  起算日   : %s" % start)
    print("  适用对象 : %s" % _short(scope, 48))
    print("  目标市场 : %s" % mk["label"])
    print("  周末规则 : %s" % mk["weekend_note"])
    print("  发送时段 : %s" % mk["tz_note"])
    if csv_path:
        print("  本级线索 : %d 家" % len(companies))
    else:
        print("  本级线索 : 未指定 --csv，本次只排节奏、不带名单")
    print("  止损线   : %s" % STOP_LINE)
    print("=" * 74)
    print("")
    print("节奏提醒: %s" % CADENCE_HINT[tier])
    print("")
    print("文案衔接：D0 那封直接用 outreach_gen.py 吐出来的，别自己另憋一版：")
    print("    python scripts/outreach_gen.py %s --tier %s" % (csv_path or "你的.csv", tier))
    print("")
    print("-" * 74)
    for i, r in enumerate(rows, 1):
        print("【%s】%s 周%s   第 %d/%d 次触达（距上次 %s 天）" % (
            r["offset"], r["date"], r["weekday"], i, len(rows),
            r["gap_days"] if i > 1 else 0))
        print("  渠道     : %s" % r["channel"])
        print("  这次说什么: %s" % r["angle"])
        print("  必须带   : %s" % r["new_info"])
        print("  文案来源 : %s" % r["draft_from"])
        if r["stop_rule"] != "—":
            print("  停止条件 : %s" % r["stop_rule"])
        if r["timing_note"]:
            print("  时间提醒 : %s" % r["timing_note"])
        print("")
    print("-" * 74)
    if companies:
        print("本级公司清单（按 lead_score 得分从高到低，即跟进优先级）:")
        for i, c in enumerate(companies, 1):
            print("  %d. %s" % (i, _short(c)))
    elif csv_path:
        print("本级公司清单: %s 里没有 %s 级线索（用 --tier 换个级别看看）。"
              % (csv_path, tier))
    else:
        print("本级公司清单: 未指定 --csv；加 --csv examples/leads_example.csv 可带上名单。")
    print("")
    print("节假日 / 季节提醒:")
    for a in HOLIDAY_ADVISORY:
        print("  · %s" % a)
    print("")
    print("发之前先过这四关:")
    print("  □ 这封比上一封多了什么新东西？没有新东西就别发")
    print("  □ 「why them」那句话还是只对这家公司成立吗")
    print("  □ 发送时间是对方当地时间上午 9-11 点吗（不是你的上午 9 点）")
    print("  □ 已经是第 %d 次触达了？到 %d 次就停手，不要靠意志力硬撑"
          % (len(rows), MAX_TOUCHES))
    print("")
    print("防骚扰（踩一次雷，赔掉整个域名信誉）:")
    for a in ANTI_SPAM:
        print("  □ %s" % a)
    print("")
    print("=" * 74)
    print("")


def print_no_plan(tier, csv_path=None, count=0):
    """T3：不排任何触达，只说明理由和下一步。"""
    print("")
    print("=" * 74)
    print("  跟进计划（%s）  ·  %s (%s)" % (TIER_SPAN[tier], tier, TIER_LABEL[tier]))
    print("=" * 74)
    print("")
    print("节奏提醒: %s" % CADENCE_HINT[tier])
    print("")
    if csv_path:
        print("本级线索 %d 家：一家都不排触达。" % count)
    print("T3 的止损线就是 0 次。邮箱、采购记录、需求判断都没齐就发信，")
    print("烧的是你域名的信誉，而且你连发给谁都还没搞明白。")
    print("")
    print("下一步:")
    print("  1. 补齐邮箱 / WhatsApp / 采购记录（进口数据、官网、社媒）")
    print("  2. 重跑 python scripts/lead_score.py %s 重新分级" % (csv_path or "你的.csv"))
    print("  3. 升到 T1/T2 之后再回来排期：python scripts/followup_plan.py --tier T1 --start ...")
    print("")
    print("=" * 74)
    print("")


def main():
    p = argparse.ArgumentParser(
        description="按 T0/T1/T2/T3 排一张带日期的跟进节奏表（含止损线与防骚扰提醒）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python scripts/followup_plan.py --tier T0 --start 2026-10-08")
    p.add_argument("--tier", choices=["T0", "T1", "T2", "T3"], default="T0",
                   help="要规划的层级，默认 T0（T3 不排触达）")
    p.add_argument("--start", required=True,
                   help="起算日 YYYY-MM-DD（首触实际发送日；必填，不用本机日期，保证可复现）")
    p.add_argument("--csv", help="线索 CSV，用于列出本级公司名（可选）")
    p.add_argument("--company", help="只给单个公司排期（与 --csv 同时给时以此为准）")
    p.add_argument("--market", choices=sorted(MARKETS), default="gcc",
                   help="目标市场，决定周末与发送时段，默认 gcc")
    p.add_argument("--avoid-weekend", action="store_true",
                   help="把落在周末的触达自动顺延到下一个工作日")
    p.add_argument("--format", choices=["table", "csv", "json"], default="table")
    p.add_argument("--out", help="输出路径，仅对 --format csv / json 生效")
    args = p.parse_args()

    try:
        start_dt = datetime.strptime(args.start, "%Y-%m-%d")
    except ValueError:
        raise SystemExit("错误：--start 日期格式应为 YYYY-MM-DD（例 2026-10-08），"
                         "收到的是 %r" % args.start)
    # strptime 也接受 2026-10-8 这种非补零写法，统一回写成标准格式，避免后面算错
    args.start = start_dt.strftime("%Y-%m-%d")

    companies = []
    if args.csv:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from lead_score import analyze, read_leads
            scored = analyze(read_leads(args.csv))
            # lead_score.analyze() 返回 (线索列表, 被合并的重复条数)；
            # 也有版本只返回列表。两种都吃下，避免上游一改这边就崩。
            if isinstance(scored, tuple):
                scored = scored[0]
            leads = [l for l in scored if l.get("tier") == args.tier]
            companies = [l["company"] for l in leads]
        except FileNotFoundError:
            raise SystemExit("错误：找不到文件 %s" % args.csv)
        except ImportError:
            raise SystemExit("错误：导入 lead_score.py 失败，"
                             "请确保两个脚本同在 scripts/ 目录下。")

    rows = build_plan(args.tier, args.start, args.company,
                      args.market, args.avoid_weekend)
    scope = (args.company or "").strip() or "(本级全部线索)"

    if not rows:
        # T3：止损线就是 0 次，不生成任何触达行，也不写空文件
        print_no_plan(args.tier, args.csv, len(companies))
        return

    if args.format in ("csv", "json"):
        # companies 为空有多种含义，必须区分，不能靠 `or` 一把梭
        if (args.company or "").strip():
            targets = [args.company.strip()]
        elif companies:
            targets = companies
        elif args.csv:
            print("提示：%s 里没有 %s 级线索，不生成文件。"
                  "换 --tier 或先补线索。" % (args.csv, args.tier))
            return
        else:
            targets = ["(本级全部线索)"]

        all_rows = [dict(r, company=t) for t in targets for r in rows]

        if args.format == "csv":
            path = args.out or ("followup_plan_%s_%s.csv" % (args.tier, args.start))
            try:
                with open(path, "w", encoding="utf-8-sig", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=FIELDS)
                    w.writeheader()
                    w.writerows(all_rows)
            except OSError as e:
                raise SystemExit("错误：写不进 %s\n  %s" % (path, e))
            print("已写入 %s（%d 家 × %d 步 = %d 行）"
                  % (path, len(targets), len(rows), len(all_rows)))
            return

        payload = {
            "tier": args.tier,
            "tier_label": TIER_LABEL[args.tier],
            "span": TIER_SPAN[args.tier],
            "start": args.start,
            "market": args.market,
            "market_label": MARKETS[args.market]["label"],
            "avoid_weekend": args.avoid_weekend,
            "max_touches": MAX_TOUCHES,
            "min_gap_days": MIN_GAP_DAYS,
            "stop_line": STOP_LINE,
            "companies": targets,
            "steps": all_rows,
            "holiday_advisory": HOLIDAY_ADVISORY,
            "anti_spam": ANTI_SPAM,
            # 不含本机时间：同样的参数在任何机器上跑，输出完全一致
            "reproduce": ("python scripts/followup_plan.py --tier %s --start %s "
                          "--market %s%s" % (args.tier, args.start, args.market,
                                             " --avoid-weekend" if args.avoid_weekend
                                             else "")),
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2)
        if args.out:
            try:
                with open(args.out, "w", encoding="utf-8") as f:
                    f.write(text)
            except OSError as e:
                raise SystemExit("错误：写不进 %s\n  %s" % (args.out, e))
            print("已写入 %s（%d 家 × %d 步 = %d 行）"
                  % (args.out, len(targets), len(rows), len(all_rows)))
        else:
            print(text)
        return

    if args.out:
        print("提示：--out 仅对 --format csv / json 生效，本次为 table 已忽略。")

    print_plan(args.tier, args.start, rows, companies, args.market, scope, args.csv)


if __name__ == "__main__":
    main()
