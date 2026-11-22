#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily_video_list.py — Daily 5-video shooting list: 5 videos a day, no more
guessing what to shoot in the morning.

One run gives you today's 5 videos: each one has a tire size, a target
market, a one-line selling point, and a 3-item filming checklist. The first
3 go out in the morning, the last 2 in the afternoon — the same 3 + 2 rhythm
as the daily posting rule.

Only the standard library, Python 3.8+, no network. The size and market
tables are reused from tire_pack.py (imported, not copied), so a spec or a
market is never defined twice in this repo.

How the list is picked (deterministic, no randomness):
    The date decides the rotation. Same date -> same list, so you can
    re-run it and get the same plan. Tomorrow's list is different: sizes
    and markets rotate day by day, so the same size does not get shot
    five days in a row. --seed pins the rotation to a fixed number
    (handy for a demo or a test); --market pins all 5 videos to one
    market when you want a single-market day.

What each video is (5 fixed angles, one per slot):
    1. Spec close-up — show the size, the tread, the sidewall marking.
    2. Load & speed — load index and speed rating, what they mean in
       plain words.
    3. Certification — the market's conformity program (GCC / SONCAP /
       PVoC / INMETRO ...), what certificate travels with the goods.
    4. Market fit — which port it lands at, which truck it fits.
    5. Compare & answer — this size against the other size on the same
       rim, plus the one question buyers ask most.

Two honesty rules, same as tire_pack.py:
    Load index / speed rating here are common values, not a maker's
    datasheet — check the datasheet before you quote them on camera.
    Certification and documents are general guidance, not the law
    itself — verify the official requirement before shipping.

Usage:
    python scripts/daily_video_list.py
    python scripts/daily_video_list.py --date 2026-11-22
    python scripts/daily_video_list.py --date 2026-11-22 --market nigeria
    python scripts/daily_video_list.py --seed 7 --format json
    python scripts/daily_video_list.py --date 2026-11-22 --out today.txt

    Full spec pack for any single video (certification points, documents,
    market notes):
        python scripts/tire_pack.py --size 315/80R22.5 --market saudi
"""

import argparse
import json
import os
import sys
from datetime import date
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import _ZhArgumentParser  # noqa: E402
from tire_pack import (  # noqa: E402
    MARKETS,
    TIRE_SIZES,
    build_tire_pack,
    normalize_market,
)

# ------------------------------------------------------------------ constants
# 常量：改口径只改这一块，改完务必跑一次：
#   python3 -m pytest tests/test_daily_video_list.py -q

VIDEOS_PER_DAY = 5  # 每天 5 条：上午 3 条 + 下午 2 条
MORNING_SLOTS = 3   # 前 3 条上午拍，后 2 条下午拍

SIZES = list(TIRE_SIZES.keys())          # 4 个常见 TBR 规格
MARKET_KEYS = list(MARKETS.keys())       # 8 个目标市场

# 5 个固定角度：slot -> (angle_en, angle_zh, checklist_en, checklist_zh)
# 检查项只写拍什么、核什么，不编数字、不编厂家说法。
ANGLES = [
    (
        "Spec close-up",
        "规格特写",
        ["Film the sidewall marking so the size reads clearly on camera",
         "Show the tread pattern in one steady close shot",
         "Say the size out loud once, slowly, at the start"],
        ["胎侧规格字拍清楚，镜头里能直接读出规格",
         "花纹拍一个稳的特写，别晃",
         "开头慢速念一遍规格"],
    ),
    (
        "Load & speed",
        "载重与速度",
        ["Show the load index on the sidewall and say what it means",
         "Say the speed rating and its speed in km/h, in plain words",
         "Remind viewers the numbers are common values — check the "
         "maker's datasheet before quoting"],
        ["胎侧载重指数拍出来，并用人话说它是什么意思",
         "速度级别和对应时速用人话说一遍",
         "提醒一句：这是常见值，报价前以厂家数据表为准"],
    ),
    (
        "Certification",
        "认证合规",
        ["Name the market's conformity program and the certificate "
         "that travels with the goods",
         "Say which document the buyer must see before the goods sail",
         "Remind viewers the rules change — verify the official "
         "requirement before shipping"],
        ["说出这个市场的符合性程序名，和随货走的证书名",
         "说清买家装船前必须看到哪份文件",
         "提醒一句：规则会变，发货前按官方最新要求复核"],
    ),
    (
        "Market fit",
        "市场适配",
        ["Name the destination port the goods land at",
         "Say which truck this size fits and where it runs",
         "End with one line on why this size suits this market"],
        ["说出货到哪个目的港",
         "说清这个规格配什么车、跑什么路",
         "结尾一句话：这个规格为什么适合这个市场"],
    ),
    (
        "Compare & answer",
        "对比问答",
        ["Put this size next to the other size on the same rim",
         "Say in one line when to pick this size over the other",
         "Answer the one question buyers ask most about this size"],
        ["把这个规格和同轮辋的另一个规格放一起比",
         "一句话说清什么时候选这个、不选那个",
         "回答买家问得最多的一个问题"],
    ),
]


# ------------------------------------------------------------------ core logic
# 核心逻辑：纯函数，不读文件、不联网，方便测试。


def parse_date(text: Optional[str]) -> date:
    """Parse a YYYY-MM-DD date; empty input means today.

    解析 YYYY-MM-DD 日期；不给就用今天。
    Raises ValueError on a bad date, with a plain message.
    """
    if text is None or str(text).strip() == "":
        return date.today()
    try:
        year, month, day = (int(part) for part in str(text).strip().split("-"))
        return date(year, month, day)
    except (ValueError, TypeError):
        raise ValueError(
            "Bad date: %r — use YYYY-MM-DD, e.g. 2026-11-22" % text
        )


def _rotation(day: date, seed: Optional[int] = None) -> int:
    """Rotation base for the day: the date ordinal, or --seed if given.

    当天的轮换基数：默认用日期序号，--seed 给了就用种子。
    Same input -> same list, every time.
    """
    if seed is not None:
        return int(seed)
    return day.toordinal()


def _selling_point(pack: Dict, angle_index: int) -> str:
    """One-line selling point, built only from tire_pack data.

    一句话卖点，只用 tire_pack.py 里已有的数据拼，不编新数。
    """
    if angle_index == 0:
        return "%s：%s" % (pack["size"], pack["typical_use"])
    if angle_index == 1:
        return "%s，载重指数 %s、速度级别 %s，以厂家数据表为准" % (
            pack["size"], pack["load_index"], pack["speed_rating"])
    if angle_index == 2:
        # build_tire_pack puts the market's conformity certificate last
        # in docs; use it directly, don't redefine it here.
        return "%s：%s走%s，%s随货走" % (
            pack["size"], pack["market"], pack["program"], pack["docs"][-1])
    if angle_index == 3:
        return "%s：%s，目的港%s" % (
            pack["size"], pack["typical_use"], pack["port"])
    # angle 4: compare with the other size on the same rim.
    same_rim = [s for s in SIZES
                if TIRE_SIZES[s]["rim_in"] == pack["rim_in"]
                and s != pack["size"]]
    other = same_rim[0] if same_rim else pack["size"]
    return "%s 对比 %s：同轮辋，选哪个看载重与路况" % (pack["size"], other)


def build_daily_list(day: Optional[date] = None,
                     seed: Optional[int] = None,
                     market: Optional[str] = None) -> List[Dict]:
    """Build today's 5-video list. Pure function, no I/O.

    生成当天的 5 条视频清单。纯函数，不读写文件。
    day defaults to today; market pins all 5 videos to one market.
    """
    day = day or date.today()
    base = _rotation(day, seed)
    market_key = normalize_market(market) if market else None

    items = []
    for slot in range(VIDEOS_PER_DAY):
        size_key = SIZES[(base + slot) % len(SIZES)]
        if market_key is not None:
            mkey = market_key
        else:
            # Step 3 through 8 markets: 5 slots, all different markets.
            # 步长 3 与 8 互质，5 条的市场全不重样。
            mkey = MARKET_KEYS[(base + slot * 3) % len(MARKET_KEYS)]
        pack = build_tire_pack(size_key, mkey)
        angle_en, angle_zh, checks_en, checks_zh = ANGLES[slot]
        items.append({
            "slot": slot + 1,
            "time_block": "morning" if slot < MORNING_SLOTS else "afternoon",
            "time_block_zh": "上午" if slot < MORNING_SLOTS else "下午",
            "angle": angle_en,
            "angle_zh": angle_zh,
            "size": pack["size"],
            "market": pack["market"],
            "market_en": pack["market_en"],
            "selling_point": _selling_point(pack, slot),
            "checklist": checks_en,
            "checklist_zh": checks_zh,
            "pack_hint": "python scripts/tire_pack.py --size %s --market %s"
                         % (pack["size"], mkey),
        })
    return items


# ------------------------------------------------------------------ rendering
# 输出渲染：table 给人看，json 给机器/别的脚本接。


def render_table(items: List[Dict], day: date) -> str:
    """Plain-text table for the terminal. 人看的纯文本表。"""
    lines = [
        "Daily 5-video list — %s (morning 3 + afternoon 2)" % day.isoformat(),
        "每日 5 条视频清单 — %s（上午 3 条 + 下午 2 条）" % day.isoformat(),
        "",
    ]
    for it in items:
        lines.append(
            "%d. [%s %s] %s — %s / %s"
            % (it["slot"], it["time_block_zh"], it["angle_zh"],
               it["size"], it["market"], it["angle"]))
        lines.append("   Selling point / 卖点：%s" % it["selling_point"])
        for check in it["checklist_zh"]:
            lines.append("   [ ] %s" % check)
        lines.append("   Full pack / 完整资料包：%s" % it["pack_hint"])
        lines.append("")
    lines.append("Numbers are common values — check the maker's datasheet "
                 "before quoting;")
    lines.append("certification is general guidance — verify the official "
                 "requirement before shipping.")
    lines.append("数字是常见值，报价前以厂家数据表为准；认证是一般性提示，"
                 "发货前按官方最新要求复核。")
    return "\n".join(lines)


def render_json(items: List[Dict], day: date) -> str:
    """JSON output. 给机器读的 JSON。"""
    return json.dumps(
        {"date": day.isoformat(), "videos": items},
        ensure_ascii=False, indent=2)


# ------------------------------------------------------------------ CLI


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point. Returns a process exit code."""
    parser = _ZhArgumentParser(
        description="Daily 5-video shooting list (morning 3 + afternoon 2). "
                    "每日 5 条视频拍摄清单（上午 3 条 + 下午 2 条）。")
    parser.add_argument("--date", default=None,
                        help="Date as YYYY-MM-DD; default today. "
                             "日期，YYYY-MM-DD；不填就是今天。")
    parser.add_argument("--seed", type=int, default=None,
                        help="Pin the rotation to a fixed number "
                             "(demo / test). 固定轮换种子（演示/测试用）。")
    parser.add_argument("--market", default=None,
                        help="Pin all 5 videos to one market, e.g. nigeria. "
                             "5 条全钉在一个市场，如 nigeria。")
    parser.add_argument("--format", choices=["table", "json"],
                        default="table",
                        help="table (default) or json. 表格（默认）或 JSON。")
    parser.add_argument("--out", default=None,
                        help="Also write the output to this file (UTF-8). "
                             "同时写入这个文件（UTF-8）。")
    args = parser.parse_args(argv)

    try:
        day = parse_date(args.date)
        items = build_daily_list(day=day, seed=args.seed, market=args.market)
    except ValueError as exc:
        print("Error / 出错：%s" % exc, file=sys.stderr)
        return 2

    text = render_json(items, day) if args.format == "json" \
        else render_table(items, day)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
