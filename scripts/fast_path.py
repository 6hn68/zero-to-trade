#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7 天快路径互动版：把 docs/fast-path.md 的 7 天任务清单变成能打卡的脚本。

内容与 docs/fast-path.md 逐条对齐，不另编一套任务清单：
    Day 1 定 1 个市场 + 找 10-15 条线索（docs/01-market-selection.md、docs/02-find-leads.md）
    Day 2 背调 + 补联系方式 + 自动分级（docs/03-due-diligence.md、scripts/lead_score.py）
    Day 3 首触，硬底线，必须发出去（scripts/outreach_gen.py、docs/04-outreach.md）
    Day 4 探渠道 + 继续补线索，今天不发正式消息（scripts/followup_plan.py）
    Day 5 第 2 次触达 D2 + 给新冒出来的 T0/T1 发一轮（scripts/lead_score.py 再跑一遍）
    Day 6 写好第 3 封信 + 收尾复盘（草稿 + 发出/回复/回复率三个数 + 3 行复盘）
    Day 7 收官：发第 3 次触达 D5 + 把结果存成档案（3 次触达全部发出就停手）

首发在 Day 3，之后按「首发当天 / 首发后第 2 天 / 首发后第 5 天」触达 3 次，
落到 Day 3 / Day 5 / Day 7。间隔是脚本定死的，别自己压缩成每天发一次。

只用了标准库，不联网。打卡状态存在 --state 指定的 JSON 文件里，
默认 fast_path_state.json（当前目录），格式 {"start": "YYYY-MM-DD" 或 null,
"done": {"1": "打卡时间戳", ...}}。

用法:
    python scripts/fast_path.py --day 1
    python scripts/fast_path.py --list
    python scripts/fast_path.py --start 2026-11-09 --done 1
    python scripts/fast_path.py --done 3 --state /tmp/fast_path_state.json
    python scripts/fast_path.py --progress
    python scripts/fast_path.py --progress --start 2026-11-02
    python scripts/fast_path.py --day 3 --state /tmp/fast_path_state.json

参数:
    --day N       打印第 N 天的任务清单（任务名 + 要产出什么 + 用哪个脚本/哪篇文档）
    --done N      给第 N 天打卡（带打卡时间戳，写入 --state 文件；已打卡过的不重复记）
    --progress    汇总 7 天进度（已完成几天 / 待完成几天 / 逾期几天）
    --list        列出 7 天总览（每天标题 + 状态）
    --start DATE  设第 1 天日期，格式 YYYY-MM-DD（与 --progress / --done 配合用；
                  只给 --start 时只保存日期不打卡）
    --state PATH  打卡状态文件，默认 fast_path_state.json（当前目录）

逾期定义：第 N 天的计划日期 = 第 1 天日期 + (N-1) 天；计划日期早于今天
且未打卡即逾期。没给 --start 时不算逾期，会明确提示「未设开始日期」。

本脚本里的日期均为【示例】，请换成你自己的开始日期；不含真实公司名。
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import _ZhArgumentParser  # noqa: E402

DEFAULT_STATE = "fast_path_state.json"
TOTAL_DAYS = 7

# 每一天：标题 / 用时 / 任务（任务名，要产出什么，用哪个脚本或哪篇文档）/ 过关标准。
# 任务名与产出逐字对齐 docs/fast-path.md 对应章节，不另编。
DAYS = {
    1: {
        "title": "定 1 个市场 + 找 10-15 条线索",
        "time": "≤2 小时",
        "tasks": [
            ("定 1 个首站：照三维法（语言 / 需求 / 壁垒）挑 1 个国家，写 3 条理由",
             "1 个国家 + 3 条理由",
             "docs/01-market-selection.md"),
            ("按四路（海关数据 / 社媒 / 搜索 / 展会）找线索，今天只要 10-15 条；"
             "先攒公司名 + 国家 + 来源就成，邮箱电话 Day 2 再补",
             "10-15 条线索",
             "docs/02-find-leads.md"),
            ("整理成 CSV 存仓库根目录：表头 company,country,product,source,email,"
             "phone,years,contact,note；source 只能填 referral / trade_show / "
             "customs / linkedin / search 其中一个",
             "my_leads.csv（≥10 行，每行 company 都有值）",
             "docs/02-find-leads.md"),
        ],
        "done_when": "一个 ≥10 行的 CSV，company 列每行都有值，source 列每行都是上面五个合法值之一。",
    },
    2: {
        "title": "背调 + 补联系方式 + 自动分级",
        "time": "≤2 小时",
        "tasks": [
            ("L1 筛查：官网存在？成立年份？社媒活跃？逐条过，任一不过直接淘汰，"
             "并把查到的 years 补进 CSV",
             "淘汰掉皮包公司，years 已补进 CSV",
             "docs/03-due-diligence.md"),
            ("补联系方式：给留下的公司补邮箱 / 电话 / WhatsApp；补不到就如实留空，"
             "别瞎填错邮箱（邮箱格式不对会被倒扣 18 分）",
             "每家至少一种真实联系方式，补不到的留空",
             "docs/03-due-diligence.md"),
            ("跑分级：python scripts/lead_score.py my_leads.csv（想看每条为什么得这个分，"
             "加 --format detail）",
             "分级表 + 底部「汇总: T0:x / T1:x / T2:x / T3:x」",
             "scripts/lead_score.py"),
        ],
        "done_when": "屏幕出现分级表 + 汇总行，并且你能说出「先回谁」（T0）和「先打谁」（T1）。"
                     "新手第一份 CSV 跑出 T0 是 0 条很正常，Day 3 照样发 T1 里分数最高的那几家。",
    },
    3: {
        "title": "首触（今天是硬底线，必须发出去）",
        "time": "≤2 小时",
        "tasks": [
            ("生成文案：python scripts/outreach_gen.py my_leads.csv --tier T0 "
             "--sender \"你的名字 | 你的公司\" --lang en --out drafts_day3.md；"
             "不加 --sender 时落款是占位符，必须替换；T0 是 0 条就换 --tier T1",
             "drafts_day3.md（至少 3 封草稿）",
             "scripts/outreach_gen.py"),
            ("改那句「为什么是你」：脚本用 CSV 的 note 列拼一句只对这家公司成立的话；"
             "note 是空的会退化成模板句，这时必须自己补（刚参展？在招采购？发了 RFQ？）",
             "每封的「为什么是你」换成同行就不成立",
             "docs/04-outreach.md"),
            ("发出去：LinkedIn / WhatsApp 先发，邮箱作为跟进；今天的目标是 3-5 家，不是全部",
             "至少 3 封已实际发出",
             "docs/04-outreach.md"),
        ],
        "done_when": "drafts_day3.md 里至少 3 封已实际发出；每封那句「为什么是你」换成同行就不成立；"
                     "全文没有出现价格。把今天这个日期记下来，Day 4 要用——今天就是首发日。",
    },
    4: {
        "title": "探渠道 + 继续补线索（今天不发正式消息）",
        "time": "≤2 小时",
        "tasks": [
            ("生成跟进计划：python scripts/followup_plan.py --tier T0 --start <首发日> "
             "--csv my_leads.csv；--start 填你 Day 3 实际首发那天的日期，格式 YYYY-MM-DD；"
             "T0 的节奏是 D0 / D2 / D5，共 3 次，不是每天发一次",
             "跟进计划表（3 次触达的日期）",
             "scripts/followup_plan.py"),
            ("探渠道：把 Day 3 那几家在另一个渠道上先加一下好友 / 打个招呼，"
             "但今天不发正式消息；WhatsApp 上加好友通过率比直接发消息高",
             "明天 D2 要用的那个渠道已经加上了人",
             "docs/04-outreach.md"),
            ("继续补线索：顺手再补 5-10 条进 my_leads.csv；名单是复利资产，"
             "不要只在 Day 1 找一次",
             "my_leads.csv 比昨天多 ≥5 行",
             "docs/02-find-leads.md"),
        ],
        "done_when": "明天要用的那个渠道已经加上了人；my_leads.csv 比昨天多 ≥5 行；"
                     "收到的回复（哪怕是 \"not interested\"）已记进 note 列。",
    },
    5: {
        "title": "第 2 次触达（D2）+ 给新冒出来的 T0/T1 发一轮",
        "time": "≤2 小时",
        "tasks": [
            ("发 D2 那一次：昨天加好的那个渠道今天用上；诉求不变，但必须带一条新信息"
             "（配柜量参考 / 一个规格细节 / 一条行情）；不要原封不动把 Day 3 那封再发一遍",
             "D2 触达已发（换渠道 + 换说法 + 一条新信息）",
             "scripts/followup_plan.py"),
            ("重跑分级：python scripts/lead_score.py my_leads.csv；新补进来的 5-10 条里，"
             "大概率有几家跳进了 T0/T1",
             "新的分级表（新冒出来的 T0/T1 已认出）",
             "scripts/lead_score.py"),
            ("给新冒出来的 T0/T1 也发一轮：照 Day 3 那套走一遍（生成文案 → 改「为什么是你」→ 发），"
             "注意换渠道，别和刚才那批人用同一种方式撞上",
             "新 T0/T1 至少 1 家已被触达",
             "scripts/outreach_gen.py"),
            ("整理回复：把收到的每一条回复记进 note 列，写清楚是哪一类客户、回了什么；"
             "回 \"not interested\" 也记——它告诉你该换钩子还是该换名单",
             "回复全部记进 note 列",
             "docs/02-find-leads.md"),
        ],
        "done_when": "D2 触达已发；新补的线索里至少 1 家已被触达；回复全部记进 note。",
    },
    6: {
        "title": "写好第 3 封信 + 收尾复盘",
        "time": "≤2 小时",
        "tasks": [
            ("把第 3 封信写完：给对方一个台阶——「这条路先放着，你随时找我」，"
             "再带一条对他有用的行业信息；今天写好存草稿，明天早上只管发；写完就别再改了",
             "第 3 封信已在草稿箱",
             "docs/04-outreach.md"),
            ("算三个数：发出去多少条、收到几封回复、回复率多少；回 1 封是正样本，"
             "回 0 封也是有效数据——它说明钩子或名单有问题，换一个再试",
             "发出 / 回复 / 回复率三个数字",
             "docs/fast-path.md"),
            ("写 3 行复盘：哪一类客户在回 / 哪一句钩子有用 / 下周只主攻哪一类",
             "3 行复盘",
             "docs/fast-path.md"),
            ("定下周动作：名单补到多少条、哪一类客户主攻、下周哪天发第二轮；写进日历，别靠脑子记",
             "下周动作已写进日历",
             "docs/fast-path.md"),
        ],
        "done_when": "第 3 封信已在草稿箱；有「发出 / 回复 / 回复率」三个数字；写下下周主攻的客户类型。",
    },
    7: {
        "title": "收官：发第 3 次触达 + 把结果存成档案",
        "time": "≤2 小时",
        "tasks": [
            ("发 D5 那一次：把 Day 6 存好的信发出去；发完就停手，不要发第 4 次——"
             "继续发只会消耗你的信誉",
             "第 3 次触达（D5）已发；3 次触达全部发出",
             "scripts/followup_plan.py"),
            ("把这一周存成档案：分级结果、跟进表、草稿、三个数字，存到一个文件夹里",
             "一周档案文件夹（带日期、带数字、带操作记录）",
             "docs/fast-path.md"),
            ("补上这一周欠的账：名单不到 20 条就补到 20 条；source 全是 search 的，"
             "下周把几家挪成 linkedin / trade_show 再跑一遍分级，看看 T0 会不会冒出来",
             "my_leads.csv ≥20 行",
             "scripts/lead_score.py"),
            ("挑一条反馈回去：哪一句钩子有用、哪一步你卡住了，写成一条 Issue 提上去；"
             "或者明确记下「这周什么都不想提」——那也正常",
             "至少提了 1 条反馈，或记下「这周什么都不想提」",
             "docs/fast-path.md"),
        ],
        "done_when": "3 次触达全部发出；这一周的档案存好了；下周的动作写进日历；"
                     "至少提了 1 条反馈（或者明确记下「这周什么都不想提」）。",
    },
}


def parse_day(value):
    """天数只认 1-7 的整数；别的给人话报错，不裸奔。"""
    try:
        n = int(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError("天数不对：「%s」不是数字。7 天快路径只有 Day 1 到 Day 7，"
                         "比如 --day 1 看第一天，--done 3 给第三天打卡。" % value)
    if n < 1 or n > TOTAL_DAYS:
        raise ValueError("天数不对：第 %d 天不存在。7 天快路径只有 Day 1 到 Day 7，"
                         "比如 --day 1 看第一天，--done 7 给第七天打卡。" % n)
    return n


def parse_start(value):
    """开始日期只认 YYYY-MM-DD；别的给人话报错，不裸奔。"""
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("日期不对：「%s」不是 YYYY-MM-DD 格式（比如 2026-11-09）。"
                         "请换成真实的第 1 天日期再跑，比如 --start 2026-11-09。" % value)


def load_state(path):
    """读打卡状态文件；文件不存在当作一张白纸，不报错。"""
    if not os.path.exists(path):
        return {"start": None, "done": {}}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise SystemExit("错误：打卡状态文件 %s 读不出来\n  %s\n  删掉它重打一次卡就行，"
                         "任务清单不受影响。" % (path, e))
    if not isinstance(data, dict):
        raise SystemExit("错误：打卡状态文件 %s 里不是一张表，删掉它重打一次卡就行。" % path)
    done = data.get("done") or {}
    if not isinstance(done, dict):
        done = {}
    return {"start": data.get("start"), "done": {str(k): v for k, v in done.items()}}


def save_state(path, state):
    """写打卡状态文件；写不进去给人话报错。"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except OSError as e:
        raise SystemExit("错误：打卡写不进 %s\n  %s" % (path, e))


def planned_date(start, day):
    """第 N 天的计划日期 = 第 1 天日期 + (N-1) 天。"""
    return start + timedelta(days=day - 1)


def compute_progress(state, today=None):
    """汇总三数：已完成 / 待完成 / 逾期。没给 --start 时不算逾期。"""
    today = today or date.today()
    done = state.get("done") or {}
    done_days = sorted(int(k) for k in done if str(k).isdigit() and 1 <= int(k) <= TOTAL_DAYS)
    start = None
    if state.get("start"):
        try:
            start = parse_start(state["start"])
        except ValueError:
            start = None
    overdue = []
    if start is not None:
        for n in range(1, TOTAL_DAYS + 1):
            if n not in done_days and planned_date(start, n) < today:
                overdue.append((n, planned_date(start, n)))
    return {
        "start": start,
        "done_days": done_days,
        "done_count": len(done_days),
        "remaining_count": TOTAL_DAYS - len(done_days),
        "overdue": overdue,
        "overdue_count": len(overdue),
        "has_start": start is not None,
        "today": today,
    }


def format_day(n, state=None):
    """打印某一天的任务清单：任务名 + 要产出什么 + 用哪个脚本/哪篇文档。"""
    day = DAYS[n]
    state = state or {"start": None, "done": {}}
    lines = []
    lines.append("Day %d · %s（%s）" % (n, day["title"], day["time"]))
    lines.append("内容来源：docs/fast-path.md Day %d，任务清单与它逐条对齐。" % n)
    done = (state.get("done") or {}).get(str(n))
    if done:
        lines.append("状态：已打卡（%s）" % done)
    else:
        lines.append("状态：未打卡")
    if state.get("start"):
        try:
            lines.append("计划日期：%s（第 1 天 %s + %d 天）"
                         % (planned_date(parse_start(state["start"]), n), state["start"], n - 1))
        except ValueError:
            pass
    for i, (task, output, tool) in enumerate(day["tasks"], 1):
        lines.append("%d. %s" % (i, task))
        lines.append("   产出：%s" % output)
        lines.append("   用哪处：%s" % tool)
    lines.append("过关标准：%s" % day["done_when"])
    if n == 3:
        lines.append("提醒：Day 3 是整条路径的硬底线。这一天发不出去，前面两天找的名单就只是名单。")
    if n == 4:
        lines.append("提醒：今天不是第 2 次触达日——D2 是首发后第 2 天，也就是 Day 5。别提前发。")
    if n == 7:
        lines.append("提醒：发完第 3 次就停手，不要发第 4 次。")
    return "\n".join(lines)


def format_list(state=None):
    """列出 7 天总览：每天标题 + 状态（已打卡 / 逾期 / 待完成）。"""
    state = state or {"start": None, "done": {}}
    progress = compute_progress(state)
    lines = ["7 天快路径总览（内容来源：docs/fast-path.md）"]
    if progress["start"]:
        lines.append("第 1 天：%s · 今天：%s" % (progress["start"], progress["today"]))
    else:
        lines.append("第 1 天：未设开始日期（先跑 --start YYYY-MM-DD 设第 1 天，逾期才算得出来）")
    for n in range(1, TOTAL_DAYS + 1):
        day = DAYS[n]
        done = (state.get("done") or {}).get(str(n))
        if done:
            status = "已打卡（%s）" % done
        elif any(d == n for d, _ in progress["overdue"]):
            status = "逾期（计划 %s，未打卡）" % dict(progress["overdue"])[n]
        else:
            status = "待完成"
        plan = ""
        if progress["start"]:
            plan = " · 计划 %s" % planned_date(progress["start"], n)
        lines.append("Day %d · %s（%s）%s · %s" % (n, day["title"], day["time"], plan, status))
    lines.append("已完成 %d 天 / 待完成 %d 天 / 逾期 %d 天"
                 % (progress["done_count"], progress["remaining_count"], progress["overdue_count"]))
    return "\n".join(lines)


def format_progress(state, today=None):
    """汇总 7 天进度：已完成几天 / 待完成几天 / 逾期几天。"""
    progress = compute_progress(state, today=today)
    lines = ["7 天快路径进度（今天：%s）" % progress["today"]]
    if progress["has_start"]:
        lines.append("第 1 天：%s" % progress["start"])
    else:
        lines.append("第 1 天：未设开始日期（逾期不算——先跑 --start YYYY-MM-DD 设第 1 天，"
                     "比如 python scripts/fast_path.py --start 2026-11-09）")
    lines.append("已完成 %d 天 / 待完成 %d 天 / 逾期 %d 天"
                 % (progress["done_count"], progress["remaining_count"], progress["overdue_count"]))
    if progress["done_days"]:
        lines.append("已打卡：%s" % "、".join("Day %d" % n for n in progress["done_days"]))
    if progress["overdue"]:
        lines.append("逾期：%s" % "、".join(
            "Day %d（计划 %s）" % (n, d) for n, d in progress["overdue"]))
        lines.append("逾期不是失败，是提醒：先把逾期那天的任务补上，再往下走，别跳过。")
    elif progress["has_start"] and progress["remaining_count"]:
        lines.append("暂无逾期：按计划日期走，今天该做的那天还没过期。")
    if progress["remaining_count"] == 0:
        lines.append("7 天全部打卡完成：3 次触达发完了吗？档案存好了吗？对照 docs/fast-path.md "
                     "最后那份可验收清单再过一遍。")
    return "\n".join(lines)




def build_parser():
    parser = _ZhArgumentParser(
        prog="fast_path.py",
        description="7 天快路径互动版：看当天任务、打卡、看进度。内容与 docs/fast-path.md 逐条对齐。",
        epilog="真实例子（日期是【示例】，换成你自己的第 1 天）：\n"
               "  python scripts/fast_path.py --day 1\n"
               "  python scripts/fast_path.py --list\n"
               "  python scripts/fast_path.py --start 2026-11-09 --done 1\n"
               "  python scripts/fast_path.py --done 3 --state /tmp/fast_path_state.json\n"
               "  python scripts/fast_path.py --progress\n"
               "  python scripts/fast_path.py --progress --start 2026-11-02\n"
               "  python scripts/fast_path.py --day 3 --state /tmp/fast_path_state.json\n"
               "打卡存在 --state 指定的 JSON 文件里，默认 fast_path_state.json（当前目录）。",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--day", metavar="N", default=None,
                        help="打印第 N 天的任务清单（1-7），比如 --day 1")
    parser.add_argument("--done", metavar="N", default=None,
                        help="给第 N 天打卡（1-7），比如 --done 3；已打卡过的不重复记")
    parser.add_argument("--progress", action="store_true",
                        help="汇总 7 天进度：已完成几天 / 待完成几天 / 逾期几天")
    parser.add_argument("--list", action="store_true",
                        help="列出 7 天总览（每天标题 + 状态）")
    parser.add_argument("--start", metavar="YYYY-MM-DD", default=None,
                        help="设第 1 天日期，比如 --start 2026-11-09；与 --progress / --done 配合用")
    parser.add_argument("--state", metavar="PATH", default=DEFAULT_STATE,
                        help="打卡状态文件，默认 fast_path_state.json（当前目录）")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.day is None and args.done is None and not args.progress \
            and not args.list and args.start is None:
        print("没给动作：加 --day N 看当天任务，或 --list 看总览，或 --progress 看进度。\n"
              "先看一眼用法：python scripts/fast_path.py --help", file=sys.stderr)
        return 2

    try:
        day = parse_day(args.day) if args.day is not None else None
        done_day = parse_day(args.done) if args.done is not None else None
        start = parse_start(args.start) if args.start is not None else None
    except ValueError as e:
        print("错误：%s" % e, file=sys.stderr)
        return 2

    # --start：先写进状态文件（只给 --start 时只保存日期不打卡）。
    state = load_state(args.state)
    if start is not None:
        state["start"] = str(start)
        save_state(args.state, state)
        if args.done is None and not args.progress and not args.list and args.day is None:
            print("第 1 天日期已设为 %s（已写入 %s）。" % (start, args.state))
            print("接下来：python scripts/fast_path.py --day 1 --state %s" % args.state)
            return 0

    if done_day is not None:
        done = state.setdefault("done", {})
        if str(done_day) in done:
            print("第 %d 天已打卡过（打卡时间 %s），不重复记。"
                  % (done_day, done[str(done_day)]))
            return 0
        stamp = datetime.now().isoformat(timespec="seconds")
        done[str(done_day)] = stamp
        save_state(args.state, state)
        print("已打卡：第 %d 天 · %s（%s）" % (done_day, DAYS[done_day]["title"], stamp))
        print("打卡已写入 %s。" % args.state)

    if day is not None:
        print(format_day(day, state))
        return 0

    if args.list:
        print(format_list(state))
        return 0

    if args.progress:
        print(format_progress(state))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
