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

标准节奏（7 天 3 触达）是 Day1 / Day4 / Day7：
    Day1 = 起算日 D0（首触日），Day4 = D3，Day7 = D6 —— T1 的节奏就是标准节奏。
    T0 是高频变体（D0/D2/D5，6 天内三次，仍在 7 天包线内）；T2 是低频例外。
    check_cadence() / validate_cadence() 在每次排期时校验这条规则，
    节奏被改错会直接报错，不会悄悄排错日期。

明确拒绝立刻停（红线）：
    对方明确说不 / 不需要 / 别再联系 → 后续触达全部取消，一封都不再发，
    30 天内不再联系（最早再联系日 = 拒绝日 + 30 天）。
    执行入口是 remaining_touches() / plan_with_reply()，命令行用 --reply refused。

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

只用标准库，Python 3.10+ 可直接跑。

用法:
    python scripts/followup_plan.py --tier T0 --start 2026-10-08
    python scripts/followup_plan.py --tier T1 --start 2026-10-08 --csv examples/leads_example.csv
    python scripts/followup_plan.py --tier T0 --start 2026-10-08 --format csv --out plan.csv
    python scripts/followup_plan.py --tier T0 --start 2026-10-08 --format json --out plan.json
    python scripts/followup_plan.py --tier T2 --start 2026-10-08 --market gcc --avoid-weekend
    python scripts/followup_plan.py --tier T1 --start 2026-10-08 --csv examples/leads_example.csv --today
    python scripts/followup_plan.py --tier T1 --start 2026-10-08 --today 2026-10-11 --sent D0

--today（今日清单，报价前的跟进才用）:
    每天早上跑一遍，只看今天该发谁：过期（日期过了、没标记已发）的置顶，
    其次今天到期，再是下一次还有几天。不带值就是今天（--today），带值就
    算那一天（--today 2026-10-11，测试、补算旧账时用）。--sent D0,D2 把
    已经发过的触达标记掉，标记过的不再出现；本脚本不读你的邮箱，OVERDUE
    只代表“日期过了且你没标记已发”，发过了就加进 --sent，别当成没发。
    报价/发样/谈价之后（Day 0 是报价那天）的每日清单走 nudge.py --list，
    同一客户同一线程只走一条线，别两边同时发。

--start 必填，而且不吃你电脑的当天日期：
    计划日期得能复现——同样的 (tier, start) 换台机器跑，结果一模一样，别人能照着重排。

输出长这样（table / csv / json 三格式同一套字段）:
    tier, offset, gap_days, date, weekday, timing_note, company,
    channel, angle, new_info, stop_rule, draft_from
"""

import argparse
import csv
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import LeadDataError, analyze, read_leads, write_trace, _ZhArgumentParser, setup_log  # noqa: E402




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

# Standard rhythm: Day1 / Day4 / Day7, counted from 1; Day1 is the start day (D0).
# 标准节奏：Day1 / Day4 / Day7（从 1 数起；Day1 就是起算日 D0）。
# Offsets are 0-based day counts from the start date; T1 runs exactly this rhythm.
STANDARD_RHYTHM_OFFSETS = (0, 3, 6)
STANDARD_RHYTHM = ("D0", "D3", "D6")

# Explicit refusal: stop at once, do not contact them again for 30 days.
# 明确拒绝：立刻停手，30 天内不再联系。
REFUSAL_COOLDOWN_DAYS = 30

# Reply status of a lead: what the other side said back (or did not say).
# 线索的回复状态：对方回了什么（或者没回）。
REPLY_NO_REPLY = "no_reply"    # Silence so far — keep the plan going. / 还没回——按计划继续。
REPLY_REPLIED = "replied"      # They answered — cadence done, talk instead. / 回了——节奏结束，转正常对话。
REPLY_REFUSED = "refused"      # Explicit no — stop at once. / 明确拒绝——立刻停。
REPLY_NOT_NOW = "not_now"      # "Not now" — park in the long list. / 现在不是时候——进长名单。
REPLY_STATUSES = (REPLY_NO_REPLY, REPLY_REPLIED, REPLY_REFUSED, REPLY_NOT_NOW)

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
    # Self-check the rhythm before scheduling anything: a tampered CADENCE
    # fails loudly here instead of silently producing wrong dates.
    # 排期前先自检节奏：CADENCE 被改错会在这里直接报错，不会悄悄排错日期。
    validate_cadence(tier)
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


def validate_standard_rhythm(offsets):
    """Raise ValueError unless offsets are exactly Day1/Day4/Day7 (0, 3, 6).

    Offsets are 0-based day counts from the start date: Day1 = 0, Day4 = 3,
    Day7 = 6. Anything else is not the standard 7-day 3-touch rhythm.
    校验标准节奏：offsets 必须是 Day1/Day4/Day7（0, 3, 6），否则报错。
    """
    try:
        got = tuple(int(o) for o in offsets)
    except (TypeError, ValueError):
        raise ValueError("标准节奏应为天数偏移 (0, 3, 6)，收到的是 %r" % (offsets,))
    if got != STANDARD_RHYTHM_OFFSETS:
        raise ValueError(
            "标准节奏必须是 Day1/Day4/Day7（偏移 0, 3, 6），收到的是 %s"
            % (got,))


def check_cadence(tier):
    """Check one tier's rhythm. Returns a list of problems (empty = OK).

    Rules — the 7-day 3-touch envelope / 规则——7 天 3 触达包线：
    - T1 must be exactly the standard rhythm Day1/Day4/Day7 (D0/D3/D6).
      T1 必须是标准节奏 Day1/Day4/Day7（D0/D3/D6）。
    - Every tier: at most MAX_TOUCHES touches, offsets strictly increasing,
      each gap >= MIN_GAP_DAYS. / 每级：最多 3 次，偏移递增，间隔 ≥ 2 天。
    - T0/T1 must finish within 7 days (last offset <= 6). / T0/T1 须在 7 天内排完。
    - T2 is the documented low-frequency exception (D0/D7/D14, only sends when
      there is market news; D14 archives, it does not send), so it is exempt
      from the 7-day span. / T2 是低频例外，不受 7 天跨度限制。
    - T3 must schedule nothing (0 touches is its stop line). / T3 必须 0 次。
    """
    if tier not in CADENCE:
        return ["未知 tier：%s（可选：%s）" % (tier, "/".join(CADENCE))]
    steps = CADENCE[tier]
    problems = []
    if tier == "T3":
        if steps:
            problems.append("T3 不应排任何触达，但排了 %d 次" % len(steps))
        return problems
    if len(steps) != MAX_TOUCHES:
        problems.append("%s 应排 %d 次触达，实际排了 %d 次"
                        % (tier, MAX_TOUCHES, len(steps)))
        return problems
    offsets = [_day_offset(s[0]) for s in steps]
    if tier == "T1":
        try:
            validate_standard_rhythm(offsets)
        except ValueError as e:
            problems.append(str(e))
    for prev, cur in zip(offsets, offsets[1:]):
        if cur <= prev:
            problems.append("%s 的偏移必须递增，收到 %s" % (tier, offsets))
            break
        if cur - prev < MIN_GAP_DAYS:
            problems.append("%s 相邻两次间隔 %d 天，小于最少 %d 天"
                            % (tier, cur - prev, MIN_GAP_DAYS))
    if tier in ("T0", "T1") and offsets[-1] > 6:
        problems.append("%s 最后一次在 D%d，超出 7 天包线（应在 D6 之前）"
                        % (tier, offsets[-1]))
    return problems


def validate_cadence(tier):
    """Raise ValueError if check_cadence(tier) finds any problem."""
    problems = check_cadence(tier)
    if problems:
        raise ValueError("节奏校验失败（%s）：%s" % (tier, "；".join(problems)))


def stop_after_reply(reply):
    """True if this reply ends the cadence (no more touches).

    - no_reply: keep going. / 没回——继续。
    - replied / refused / not_now: stop. / 回了 / 拒绝 / 不是时候——都停。
    Raises ValueError on an unknown status.
    """
    if reply not in REPLY_STATUSES:
        raise ValueError("未知回复状态：%r（可选：%s）"
                         % (reply, "/".join(REPLY_STATUSES)))
    return reply != REPLY_NO_REPLY


def remaining_touches(rows, reply):
    """Filter a planned touch list by the lead's reply. Returns a new list.

    - no_reply: everything stays. / 没回——全留。
    - refused: nothing stays — stop at once, even mid-cadence. A refusal that
      arrives after D0 still cancels D3 and D6. / 明确拒绝——全取消，哪怕 D0 已发出。
    - replied / not_now: nothing stays either (talk instead, or park them).
      / 已回复 / 不是时候——同样停，不再按计划发。
    The input list is untouched. Raises ValueError on an unknown status.
    """
    if reply not in REPLY_STATUSES:
        raise ValueError("未知回复状态：%r（可选：%s）"
                         % (reply, "/".join(REPLY_STATUSES)))
    if reply == REPLY_NO_REPLY:
        return list(rows)
    return []


def refusal_cooldown_until(reply_date):
    """Earliest date you may contact them again after an explicit refusal.

    reply_date: YYYY-MM-DD (the day they said no). Returns YYYY-MM-DD,
    REFUSAL_COOLDOWN_DAYS (30) days later. Raises ValueError on a bad date.
    明确拒绝后的最早再联系日 = 拒绝日 + 30 天。
    """
    try:
        day = datetime.strptime(reply_date, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError("拒绝日期格式应为 YYYY-MM-DD，收到的是 %r" % reply_date)
    return (day + timedelta(days=REFUSAL_COOLDOWN_DAYS)).strftime("%Y-%m-%d")


def plan_with_reply(tier, start, reply=REPLY_NO_REPLY, reply_date=None,
                    company=None, market="gcc", avoid_weekend=False):
    """build_plan + the refusal state machine. Returns (rows, note).

    note is "" when the plan runs as-is; otherwise a plain-language reason
    why the remaining touches are gone (and, for a refusal with a date,
    the earliest day you may reach out again).
    排期 + 回复状态机：返回（剩余触达行，说明）。没回复时说明为空。
    """
    rows = build_plan(tier, start, company=company, market=market,
                      avoid_weekend=avoid_weekend)
    if reply == REPLY_NO_REPLY:
        return rows, ""
    if reply == REPLY_REFUSED:
        if reply_date:
            note = ("明确拒绝：立刻停手，后续 %d 次触达全部取消；"
                    "最早 %s 之后再联系。"
                    % (len(rows), refusal_cooldown_until(reply_date)))
        else:
            note = ("明确拒绝：立刻停手，后续 %d 次触达全部取消；30 天内不再联系。"
                    % len(rows))
        return [], note
    if reply == REPLY_REPLIED:
        return [], "对方已回复：跟进节奏结束，转去正常对话，不再按计划发。"
    return [], "对方说现在不是时候：停手，进长名单，季度扫一次。"


# ---------------------------------------------------------------------------
# Today's list / 今日清单：每天早上只看今天该发谁
# ---------------------------------------------------------------------------
# The batch model: one tier + one start date = one batch of leads that were
# first touched on the same day (the usual way a batch goes out). --today
# filters that batch's plan down to what matters this morning: overdue
# (date passed, not marked sent) first, most overdue on top; due today
# next; then the next upcoming touch and how many days away.
# 批量模型：同一级 + 同一起算日 = 同一天首触的一批线索。--today 只挑出今早
# 该看的：过期（日期过了、没标记已发）的置顶，其次今天到期，再是下一次
# 还有几天。
#
# How this differs from nudge.py --list / 和 nudge --list 怎么分工：
# nudge --list tracks the post-quote ladder (Day 0 = the day the quote went
# out / the sample shipped / the price talk started), one row per lead in a
# JSON file with its own sent list. This --today tracks the pre-quote cadence
# for a whole batch, and "sent" is passed on the command line (--sent D0,D2)
# because the batch was sent together. One lead, one thread, one line —
# never run both lists for the same lead on the same day.
# nudge --list 管报价之后（Day 0 是报价/发样/谈价那天），每家一行 JSON、
# 各记各的 sent；这里的 --today 管报价之前的一批线索，sent 走命令行
# （--sent D0,D2），因为一批是一起发出去的。同一客户同一线程只走一条线。

# Sentinel for a bare "--today" (no date given): it means today.
# 裸写 --today（不带日期）时的标记值：意思就是今天。
TODAY_SENTINEL = "__TODAY__"


def parse_today(value):
    """Resolve --today: None / "__TODAY__" means today; a YYYY-MM-DD string
    means that day (reproducible runs and tests). Returns a datetime.date.
    解析 --today：不给 / "__TODAY__" 就是今天；给 YYYY-MM-DD 就算那一天
    （可复现，测试、补算旧账时用）。返回 datetime.date。
    """
    if value is None or value == TODAY_SENTINEL:
        return datetime.now().date()
    raw = str(value).strip()
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("今天的日期格式应为 YYYY-MM-DD，收到的是 %r" % value)


def parse_sent(value):
    """Parse --sent "D0,D2" into a tuple of offset labels ("D0", "D2").
    Empty / None means nothing sent yet. A bad label raises ValueError
    instead of silently dropping a touch.
    解析 --sent "D0,D2"：返回触达标签元组。空着 = 一封都没发过；写错的
    标签直接报错，不会悄悄漏掉一封。
    """
    if value is None:
        return ()
    parts = [p.strip().upper() for p in str(value).split(",") if p.strip()]
    for part in parts:
        _day_offset(part)  # raises ValueError on a bad label, in words
    return tuple(parts)


def todays_followups(rows, today, sent=()):
    """Split a planned touch list into overdue / due today / upcoming.

    rows: build_plan() output. today: a date or YYYY-MM-DD string.
    sent: offset labels already sent (e.g. ("D0",)). Sent touches never
    show up again — neither as overdue nor as due. Returns a dict:
      {"today": "YYYY-MM-DD", "overdue": [...], "due": [...],
       "upcoming": row-or-None, "upcoming_in_days": int-or-None,
       "sent": [...], "all_done": bool}
    Overdue is most overdue first (earliest date on top). Raises ValueError
    if a sent label is not one of the plan's offsets.
    把计划表切成过期 / 今天到期 / 下一次三档。sent 里标记过的触达不再出现。
    过期按最过期（日期最早）的排最前面。sent 里写了本批没有的触达就报错。
    """
    if isinstance(today, str):
        today = parse_today(today)
    sent = tuple(s.strip().upper() for s in (sent or ()))
    for label in sent:
        _day_offset(label)
    known = [r["offset"] for r in rows]
    unknown = [s for s in sent if s not in known]
    if unknown:
        raise ValueError("已发标记里有这批计划没有的触达：%s（本批只有 %s）"
                         % (", ".join(unknown),
                            "、".join(known) if known else "无"))
    overdue, due, future = [], [], []
    for r in rows:
        if r["offset"] in sent:
            continue
        day = datetime.strptime(r["date"], "%Y-%m-%d").date()
        if day < today:
            overdue.append(r)
        elif day == today:
            due.append(r)
        else:
            future.append(((day - today).days, r))
    upcoming = future[0][1] if future else None
    return {
        "today": today.strftime("%Y-%m-%d"),
        "overdue": overdue,
        "due": due,
        "upcoming": upcoming,
        "upcoming_in_days": future[0][0] if future else None,
        "sent": list(sent),
        "all_done": not overdue and not due and upcoming is None,
    }


def _print_today_touch(row, flag=""):
    """One touch row in the morning list: what to say and what to bring.

    一条触达：这次说什么、必须带什么新信息、文案从哪来。
    """
    print("%s【%s】%s 周%s" % (flag, row["offset"], row["date"], row["weekday"]))
    print("  渠道     : %s" % row["channel"])
    print("  这次说什么: %s" % row["angle"])
    print("  必须带   : %s" % row["new_info"])
    print("  文案来源 : %s" % row["draft_from"])
    if row["stop_rule"] != "—":
        print("  停止条件 : %s" % row["stop_rule"])
    if row["timing_note"]:
        print("  时间提醒 : %s" % row["timing_note"])
    print("")


def print_today(tier, start, result, companies, scope, market="gcc",
                csv_path=None):
    """Human-readable morning list: overdue first, then due today, then next.

    人看的今日清单：过期置顶，其次今天到期，再是下一次还有几天。
    """
    counts = (len(result["overdue"]), len(result["due"]),
              1 if result["upcoming"] else 0)
    print("")
    print("=" * 74)
    print("  今日跟进 / Today's follow-ups (%s)  ·  %s (%s)"
          % (result["today"], tier, TIER_LABEL[tier]))
    print("  OVERDUE %d / 过期 %d 封  ·  DUE TODAY %d / 今天到期 %d 封  ·  "
          "NOT YET %d / 还没到 %d 封"
          % (counts[0], counts[0], counts[1], counts[1], counts[2], counts[2]))
    print("=" * 74)
    print("  起算日（首触日）: %s" % start)
    print("  适用对象 : %s" % _short(scope, 48))
    print("  已发过   : %s"
          % ("、".join(result["sent"]) if result["sent"]
             else "一封都没发（传 --sent D0,D2 标记已发的）"))
    if csv_path:
        print("  本级线索 : %d 家" % len(companies))
    print("  止损线   : %s" % STOP_LINE)
    print("=" * 74)
    print("")
    if result["all_done"]:
        print("  本批三封都发完了：没有过期、没有今天到期、没有下一次。")
        print("  接下来：三封发完仍无回应就停手，进长名单，季度扫一次；")
        print("  有人回了就用 --reply replied / refused / not_now 停掉这批。")
        print("")
    if result["overdue"]:
        print("⚠ OVERDUE / 过期了，先处理这 %d 封（日期过了、没标记已发）："
              % len(result["overdue"]))
        print("-" * 74)
        for row in result["overdue"]:
            _print_today_touch(row, flag="⚠ ")
    if result["due"]:
        print("DUE TODAY / 今天就发这 %d 封：" % len(result["due"]))
        print("-" * 74)
        for row in result["due"]:
            _print_today_touch(row)
    if result["upcoming"] is not None:
        print("NOT YET / 下一次还有 %d 天（%s）："
              % (result["upcoming_in_days"], result["upcoming"]["date"]))
        print("-" * 74)
        _print_today_touch(result["upcoming"])
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
    print("注意：本脚本不知道你到底发没发——OVERDUE 只代表“日期过了且你没用")
    print("  --sent 标记已发”。发过了就加进 --sent（例：--sent D0），别当成没发")
    print("  又发一遍；7 天内同客户最多 3 次，换渠道也算。")
    print("  报价/发样/谈价之后的跟进走 nudge.py --list，别跟这张表双线并行。")
    print("  复现：python scripts/followup_plan.py --tier %s --start %s --today %s%s"
          % (tier, start, result["today"],
             " --sent %s" % ",".join(result["sent"]) if result["sent"] else ""))
    print("")
    print("=" * 74)
    print("")


def print_stopped(reply, note):
    """Refusal / reply stop notice: no plan, just the reason. Plain words.

    停手提示：不打印计划表，只讲清为什么停、什么时候能再联系。
    """
    print("")
    print("=" * 74)
    print("  跟进已停止（回复状态：%s）" % reply)
    print("=" * 74)
    print("")
    print("  %s" % note)
    print("")
    print("  提醒：停了就是停了，别换个渠道再发一遍——换渠道也算触达。")
    print("")
    print("=" * 74)
    print("")


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
    p = _ZhArgumentParser(
        prog="followup_plan.py",
        description="按 T0/T1/T2/T3 排一张带日期的跟进节奏表（含止损线与防骚扰提醒）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="可直接复制的例子:\n"
               "  python scripts/followup_plan.py --tier T0 --start 2026-10-08\n"
               "每天早上只看今天该发谁（过期置顶、其次今天到期）:\n"
               "  python scripts/followup_plan.py --tier T1 --start 2026-10-08 "
               "--csv examples/leads_example.csv --today\n"
               "  python scripts/followup_plan.py --tier T1 --start 2026-10-08 "
               "--today 2026-10-11 --sent D0")
    p.add_argument("--tier", choices=["T0", "T1", "T2", "T3"], default="T0",
                   help="要规划的层级，默认 T0（T3 不排触达）")
    p.add_argument("--start", "--start-date", required=True,
                   help="起算日 YYYY-MM-DD（首触实际发送日；必填，不用本机日期，保证可复现。"
                        "--start-date 是旧版写法，同样可用）")
    p.add_argument("--csv", help="线索 CSV，用于列出本级公司名（可选）")
    p.add_argument("--company", help="只给单个公司排期（与 --csv 同时给时以此为准）")
    p.add_argument("--market", choices=sorted(MARKETS), default="gcc",
                   help="目标市场，决定周末与发送时段，默认 gcc")
    p.add_argument("--reply", choices=list(REPLY_STATUSES), default=REPLY_NO_REPLY,
                   help="对方的回复状态：no_reply（默认，没回，按计划继续）/ "
                        "replied（已回复，停）/ refused（明确拒绝，立刻停）/ "
                        "not_now（现在不是时候，停）")
    p.add_argument("--reply-date",
                   help="对方回复的日期 YYYY-MM-DD（仅 --reply refused 时用于算 "
                        "30 天冷却期，可选）")
    p.add_argument("--avoid-weekend", action="store_true",
                   help="把落在周末的触达自动顺延到下一个工作日")
    p.add_argument("--today", nargs="?", const=TODAY_SENTINEL, default=None,
                   metavar="YYYY-MM-DD",
                   help="今日清单模式：只打印今天该发谁（过期置顶、其次今天到期、"
                        "再是下一次）。不带值就是今天（--today），带值就算那一天"
                        "（--today 2026-10-11）。只出表格版，--format/--out 忽略")
    p.add_argument("--sent", default="",
                   help="已经发过的触达，逗号隔开（例：--sent D0,D2），只和 "
                        "--today 一起用；标记过的不再出现在今日清单里")
    p.add_argument("--format", choices=["table", "csv", "json"], default="table")
    p.add_argument("--out", help="输出路径，仅对 --format csv / json 生效")
    if len(sys.argv) == 1:
        p.print_usage(sys.stderr)
        print("\n没给参数：不知道怎么填就跑 python scripts/followup_plan.py --help，"
              "里面有能直接复制的例子。", file=sys.stderr)
        raise SystemExit(2)
    args = p.parse_args()
    log = setup_log("followup_plan")
    started = time.monotonic()
    # trace 里只记参数摘要：公司名不记（--company 给了也只记“单家”）。
    trace_input = ("tier=%s start=%s market=%s%s%s"
                   % (args.tier, args.start, args.market,
                      " csv=%s" % os.path.basename(args.csv) if args.csv
                      else " 单家" if (args.company or "").strip() else " 本级全部",
                      " today=%s sent=%s" % (args.today or "-",
                                              args.sent or "-")
                      if args.today is not None else ""))

    try:
        start_dt = datetime.strptime(args.start, "%Y-%m-%d")
    except ValueError:
        log.info("RESULT error=bad_start value=%r", args.start)
        write_trace("followup_plan.py", trace_input, "",
                    time.monotonic() - started,
                    "--start 日期格式应为 YYYY-MM-DD，收到的是 %r" % args.start)
        raise SystemExit("错误：--start 日期格式应为 YYYY-MM-DD（例 2026-10-08），"
                         "收到的是 %r" % args.start)
    # strptime 也接受 2026-10-8 这种非补零写法，统一回写成标准格式，避免后面算错
    args.start = start_dt.strftime("%Y-%m-%d")

    companies = []
    if args.csv:
        try:
            scored = analyze(read_leads(args.csv))
            # lead_score.analyze() 返回 (线索列表, 被合并的重复条数)；
            # 也有版本只返回列表。两种都吃下，避免上游一改这边就崩。
            if isinstance(scored, tuple):
                scored = scored[0]
            leads = [l for l in scored if l.get("tier") == args.tier]
            companies = [l["company"] for l in leads]
        except FileNotFoundError:
            write_trace("followup_plan.py", trace_input, "",
                        time.monotonic() - started,
                        "找不到文件 %s" % args.csv)
            raise SystemExit("错误：找不到文件 %s" % args.csv)
        except LeadDataError as e:
            log.info("RESULT error=%s", e)
            write_trace("followup_plan.py", trace_input, "",
                        time.monotonic() - started, str(e))
            raise SystemExit("错误：%s" % e)

    try:
        rows, reply_note = plan_with_reply(args.tier, args.start, args.reply,
                                           args.reply_date, args.company,
                                           args.market, args.avoid_weekend)
    except ValueError as e:
        write_trace("followup_plan.py", trace_input, "",
                    time.monotonic() - started, str(e))
        raise SystemExit("错误：%s" % e)
    log.info("RESULT tier=%s start=%s company=%s rows=%d reply=%s",
             args.tier, args.start, (args.company or "").strip() or "(本级全部)",
             len(rows), args.reply)
    scope = (args.company or "").strip() or "(本级全部线索)"

    if reply_note:
        # Replied / refused / not now: no plan at all, just the stop notice.
        # 回了 / 拒绝了 / 不是时候：不打印计划表，只讲停手原因。
        write_trace("followup_plan.py", trace_input, reply_note,
                    time.monotonic() - started)
        print_stopped(args.reply, reply_note)
        return

    if not rows:
        # T3：止损线就是 0 次，不生成任何触达行，也不写空文件
        write_trace("followup_plan.py", trace_input, "0 行（无触达计划）",
                    time.monotonic() - started)
        print_no_plan(args.tier, args.csv, len(companies))
        return

    if args.today is not None:
        # Morning list: only what is due today / overdue / next. Table only.
        # 今日清单：只看过期、今天到期、下一次三档，只出表格版。
        if args.format != "table" or args.out:
            print("提示：--today 只出表格版，--format/--out 本次已忽略。")
        try:
            today = parse_today(args.today)
            sent = parse_sent(args.sent)
            result = todays_followups(rows, today, sent)
        except ValueError as e:
            write_trace("followup_plan.py", trace_input, "",
                        time.monotonic() - started, str(e))
            raise SystemExit("错误：%s" % e)
        log.info("RESULT tier=%s start=%s today=%s sent=%s overdue=%d due=%d",
                 args.tier, args.start, result["today"],
                 ",".join(result["sent"]) or "-",
                 len(result["overdue"]), len(result["due"]))
        print_today(args.tier, args.start, result, companies, scope,
                    args.market, args.csv)
        write_trace("followup_plan.py", trace_input,
                    "今日清单 %s：过期 %d 封，今天到期 %d 封%s"
                    % (result["today"], len(result["overdue"]),
                       len(result["due"]),
                       "，下一次 %d 天后" % result["upcoming_in_days"]
                       if result["upcoming"] is not None else "，已发完"),
                    time.monotonic() - started)
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
            write_trace("followup_plan.py", trace_input,
                        "0 行（该级无线索，不生成文件）",
                        time.monotonic() - started)
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
                write_trace("followup_plan.py", trace_input, "",
                            time.monotonic() - started,
                            "写不进 %s：%s" % (path, e))
                raise SystemExit("错误：写不进 %s\n  %s" % (path, e))
            print("已写入 %s（%d 家 × %d 步 = %d 行）"
                  % (path, len(targets), len(rows), len(all_rows)))
            write_trace("followup_plan.py", trace_input,
                        "%d 家 × %d 步 = %d 行"
                        % (len(targets), len(rows), len(all_rows)),
                        time.monotonic() - started)
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
                write_trace("followup_plan.py", trace_input, "",
                            time.monotonic() - started,
                            "写不进 %s：%s" % (args.out, e))
                raise SystemExit("错误：写不进 %s\n  %s" % (args.out, e))
            print("已写入 %s（%d 家 × %d 步 = %d 行）"
                  % (args.out, len(targets), len(rows), len(all_rows)))
        else:
            print(text)
        write_trace("followup_plan.py", trace_input,
                    "%d 家 × %d 步 = %d 行"
                    % (len(targets), len(rows), len(all_rows)),
                    time.monotonic() - started)
        return

    if args.out:
        print("提示：--out 仅对 --format csv / json 生效，本次为 table 已忽略。")

    print_plan(args.tier, args.start, rows, companies, args.market, scope, args.csv)
    write_trace("followup_plan.py", trace_input,
                "%d 步计划" % len(rows), time.monotonic() - started)


if __name__ == "__main__":
    main()
