#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
market_rules.py — Target-market and trade-barrier rules for lead scoring.
目标市场与贸易壁垒规则表，供 lead_score.py 分级时查。

This file is data plus a tiny lookup, nothing else: no I/O, no network,
stdlib only. To change a market rule, edit the tables below — do not
touch the scoring code in lead_score.py.
本文件只有数据表加一个小查询函数：不读写文件、不联网、只用标准库。
改市场规则只改下面这几张表，别动 lead_score.py 里的打分代码。

Where the numbers come from / 数字从哪来：
- Turkey 60% anti-dumping duty on Chinese TBR until 2029, and the
  Mexico / USA / EU permanent exclusion, are house rules handed down
  for this project (task baseline, given as-is). They were NOT re-checked
  against official sources in this round: re-check before quoting them
  to a buyer, and before shipping always confirm the current duty
  with the official source.
  土耳其对华 TBR 反倾销税 60% 至 2029、以及墨西哥 / 美国 / 欧盟永久排除，
  是本项目既有的内部口径（任务基线直接给定）。本轮没有重新核对官方原文：
  对外报价、发货前务必以官方最新要求复核。
- Brazil anti-dumping on Chinese truck/bus tyres exists (see tire_pack.py),
  but the rate was never written down anywhere in this repo, so it is
  recorded here as "rate not verified / 税率没核实", not as a number.
  巴西对华卡客车胎有反倾销税（见 tire_pack.py），但税率在本仓库任何地方
  都没写过，所以这里只记“税率没核实”，不编一个数字。
- The 8 target markets match tire_pack.py MARKETS exactly; keep the two
  tables in sync when either changes.
  8 个目标市场与 tire_pack.py 的 MARKETS 完全一致；改一边时另一边同步改。

How scoring uses this table / 分级怎么用这张表：
- Target market: no change, score as usual. / 目标市场：不加分不扣分，照常打。
- Barrier market (Turkey, Brazil): tier capped at T1 at most. The lead can
  still be good, but the first sentence must confirm re-export / bonded
  zone — until that is confirmed, it is not a "call today" T0.
  壁垒市场（土耳其、巴西）：最高只到 T1。线索本身可能很好，但第一句必须
  先确认做不做转口 / 保税区，没确认之前不配占今天的 T0。
- Barrier + note says re-export / bonded zone: cap lifted, score as usual.
  壁垒市场 + 备注写了转口 / 保税区：封顶解除，照常打。
- Excluded market (Mexico, USA, EU members): tier capped at T3 no matter
  how high the score is. The score itself is kept (it still says how
  reachable the contact is), but the tier and the next action say "don't call".
  排除市场（墨西哥、美国、欧盟成员国）：分再高也只到 T3。分数本身保留
  （它照样说明这个人好不好联系），但分级和下一步都写“别打”。
- Any other country: no change. A country we have no rule for is not
  punished — it just means "no rule yet", not "bad market".
  其他国家：不加分不扣分。没写进表的国家不等于差市场，只等于“还没规则”。
"""

import re

# ---------------------------------------------------------------- Target markets
# The 8 markets this project actually sells to. Same list as tire_pack.py
# MARKETS — keep both in sync.
# 本项目真正做的 8 个市场，与 tire_pack.py 的 MARKETS 完全一致，两边同步改。
TARGET_MARKETS = {
    "nigeria": {"name": "尼日利亚", "name_en": "Nigeria"},
    "ghana": {"name": "加纳", "name_en": "Ghana"},
    "kenya": {"name": "肯尼亚", "name_en": "Kenya"},
    "tanzania": {"name": "坦桑尼亚", "name_en": "Tanzania"},
    "colombia": {"name": "哥伦比亚", "name_en": "Colombia"},
    "brazil": {"name": "巴西", "name_en": "Brazil"},
    "saudi": {"name": "沙特", "name_en": "Saudi Arabia"},
    "uae": {"name": "阿联酋", "name_en": "United Arab Emirates"},
}

# ---------------------------------------------------------------- Barriers (cap at T1)
# A barrier market is still sellable, just not "call today" until the
# re-export / bonded-zone question is answered.
# 壁垒市场不是不能卖，只是在“转口 / 保税区”问清楚之前不能算“今天就打”。
BARRIERS = {
    "turkey": {
        "name": "土耳其",
        "name_en": "Turkey",
        "kind": "anti-dumping",  # 反倾销税
        "product": "TBR",        # 只针对卡客车胎（TBR），不是所有轮胎
        "origin": "China",       # 只针对中国原产
        "rate_pct": 60,          # 60%：内部口径（任务基线给定），本轮未重核官方原文
        "until": "2029",         # 有效期至 2029：内部口径（任务基线给定），本轮未重核
        "rate_verified": False,  # True only after someone re-checks the official text
    },
    "brazil": {
        "name": "巴西",
        "name_en": "Brazil",
        "kind": "anti-dumping",  # 反倾销税
        "product": "TBR",        # 卡客车胎
        "origin": "China",
        "rate_pct": None,        # 税率没核实：仓库里没写过，别编
        "until": None,           # 有效期没核实
        "rate_verified": False,
    },
}

# ---------------------------------------------------------------- Excluded markets (cap at T3)
# Permanent exclusion: not a tariff problem to work around, just out of scope.
# 永久排除：不是“想办法绕过关税”的问题，是根本不在目标市场清单里。
EXCLUDED_MARKETS = {
    "mexico": {
        "name": "墨西哥",
        "name_en": "Mexico",
        # Anti-dumping on Chinese TBR until 2029 (see docs/tire-pack.md).
        # 反倾销税至 2029（见 docs/tire-pack.md）。
        "reason": "对华 TBR 反倾销税至 2029，永久排除",
        "reason_en": "anti-dumping duty on Chinese TBR until 2029, permanently excluded",
    },
    "usa": {
        "name": "美国",
        "name_en": "United States",
        # No duty rate is claimed here: exclusion is the house rule itself.
        # 这里不编任何税率数字：排除本身就是内部口径。
        "reason": "不在目标市场清单，永久排除",
        "reason_en": "outside the target-market list, permanently excluded",
    },
    "eu": {
        "name": "欧盟",
        "name_en": "European Union",
        # One entry for the whole bloc; members are listed below.
        # 欧盟整块只记一条，成员国见下面的 EU_MEMBERS。
        "reason": "不在目标市场清单，永久排除",
        "reason_en": "outside the target-market list, permanently excluded",
    },
}

# EU member states (27, as of 2026). The UK is NOT here: it left the EU.
# 欧盟成员国（27 个，2026 年口径）。英国不在里面：它已经脱欧了。
EU_MEMBERS = {
    "austria": "奥地利", "belgium": "比利时", "bulgaria": "保加利亚",
    "croatia": "克罗地亚", "cyprus": "塞浦路斯", "czechia": "捷克",
    "denmark": "丹麦", "estonia": "爱沙尼亚",
    "finland": "芬兰", "france": "法国", "germany": "德国",
    "greece": "希腊", "hungary": "匈牙利", "ireland": "爱尔兰",
    "italy": "意大利", "latvia": "拉脱维亚", "lithuania": "立陶宛",
    "luxembourg": "卢森堡", "malta": "马耳他", "netherlands": "荷兰",
    "poland": "波兰", "portugal": "葡萄牙", "romania": "罗马尼亚",
    "slovakia": "斯洛伐克", "slovenia": "斯洛文尼亚", "spain": "西班牙",
    "sweden": "瑞典",
}

# ---------------------------------------------------------------- Aliases
# Country input -> canonical code. Keys are matched after _normalize().
# 国家写法 -> 标准代码。匹配前先过 _normalize()（小写、去空格、去点）。
MARKET_ALIASES = {
    # Target markets (same aliases as tire_pack.py MARKET_ALIASES).
    # 目标市场（别名与 tire_pack.py 的 MARKET_ALIASES 一致）。
    "nigeria": "nigeria", "尼日利亚": "nigeria", "ng": "nigeria",
    "ghana": "ghana", "加纳": "ghana", "gh": "ghana",
    "kenya": "kenya", "肯尼亚": "kenya", "ke": "kenya",
    "tanzania": "tanzania", "坦桑尼亚": "tanzania", "tz": "tanzania",
    "colombia": "colombia", "哥伦比亚": "colombia", "co": "colombia",
    "brazil": "brazil", "巴西": "brazil", "br": "brazil",
    "saudi": "saudi", "沙特": "saudi", "沙特阿拉伯": "saudi",
    "saudi arabia": "saudi", "ksa": "saudi", "sa": "saudi",
    "uae": "uae", "阿联酋": "uae", "united arab emirates": "uae", "ae": "uae",
    # Barrier markets. / 壁垒市场。
    "turkey": "turkey", "turkiye": "turkey", "türkiye": "turkey",
    "土耳其": "turkey", "tr": "turkey",
    # Excluded markets. / 排除市场。
    "mexico": "mexico", "墨西哥": "mexico", "mx": "mexico",
    "usa": "usa", "us": "usa", "united states": "usa",
    "united states of america": "usa", "america": "usa", "美国": "usa",
    "eu": "eu", "european union": "eu", "欧盟": "eu",
}
# Every EU member name (English + Chinese) also means "eu".
# 每个欧盟成员国（英文名 + 中文名）都指向 "eu"。
for _member_en, _member_zh in EU_MEMBERS.items():
    MARKET_ALIASES.setdefault(_member_en, "eu")
    MARKET_ALIASES.setdefault(_member_zh, "eu")
# Short forms people actually type. / 常见简称。
MARKET_ALIASES.update({
    "czech": "eu", "czech republic": "eu", "holland": "eu",
    "uk": "other",  # UK is not EU; see note above.
    "英国": "other",  # The UK left the EU: no rule for it, so it stays "other".
})

# Note keywords that clear a barrier cap: the buyer does re-export or uses
# a bonded zone, so the duty does not land on them the same way.
# 能解除壁垒封顶的备注关键词：买家做转口或走保税区，税就不是照单全收。
REEXPORT_KEYWORDS = ("转口", "保税", "保税区", "re-export", "reexport",
                     "bonded", "free zone", "转口贸易")


# ---------------------------------------------------------------- Lookup
def _normalize(country):
    """Country input -> lookup key: lowercase, dots and extra spaces removed.

    国家写法 -> 查询键：转小写、去点、去多余空格。
    "U.S.A." and "usa" must hit the same entry, or the rule silently misses.
    "U.S.A." 和 "usa" 必须命中同一条，否则规则会被悄悄绕过。
    """
    if country is None:
        return ""
    text = str(country).strip().lower().replace(".", "")
    return re.sub(r"\s+", " ", text)


def lookup(country):
    """Country input -> canonical code ("nigeria", "turkey", "eu", ...).

    Returns "other" for a blank or unlisted country: no rule means no
    penalty, it never means "bad market".
    国家写法 -> 标准代码（"nigeria"、"turkey"、"eu"……）。
    空白或没写进表的国家返回 "other"：没规则不扣分，不等于差市场。
    """
    return MARKET_ALIASES.get(_normalize(country), "other")


def _barrier_label(code):
    """One-line barrier note for the score detail, e.g. "反倾销 60% 至 2029".

    壁垒一句话说明，进分级明细用，例如“反倾销 60% 至 2029”。
    """
    b = BARRIERS[code]
    if b["rate_pct"] is None:
        return "%s：对华%s有反倾销税，税率没核实，出货前查官方原文" % (
            b["name"], b["product"])
    return "%s：对华%s反倾销税 %d%% 至 %s" % (
        b["name"], b["product"], b["rate_pct"], b["until"])


def verdict(country, note=""):
    """Country (+ note) -> market verdict dict. Pure function, no I/O.

    国家（+ 备注）-> 市场结论 dict。纯函数，不读写文件。

    Keys / 字段：
      status: "target" | "barrier" | "barrier-cleared" | "excluded" | "other"
      code: canonical market code / 标准代码
      cap_tier: highest tier this lead may reach (None = no cap)
                这条线索最高能到哪一级（None = 不封顶）
      label: one line for the score detail / 进分级明细的一行字
      cap_next / cap_action: next step + action when capped, else ""
                             被封顶时的下一步 + 动作，没封顶为空
    """
    code = lookup(country)
    if code in TARGET_MARKETS and code not in BARRIERS:
        mkt = TARGET_MARKETS[code]
        return {"status": "target", "code": code, "cap_tier": None,
                "label": "目标市场：%s" % mkt["name"],
                "cap_next": "", "cap_action": ""}
    if code in BARRIERS:
        blob = (note or "").lower()
        if any(k in blob for k in REEXPORT_KEYWORDS):
            return {"status": "barrier-cleared", "code": code, "cap_tier": None,
                    "label": "%s（已确认转口/保税区，按正常分级打）" % _barrier_label(code),
                    "cap_next": "", "cap_action": ""}
        return {"status": "barrier", "code": code, "cap_tier": "T1",
                "label": "%s" % _barrier_label(code),
                "cap_next": "先确认转口/保税区",
                "cap_action": "壁垒（%s）；第一句先确认做不做转口/保税区，确认了再按 T0 打"
                              % _barrier_label(code)}
    if code in EXCLUDED_MARKETS or code == "eu":
        key = "eu" if code == "eu" else code
        mkt = EXCLUDED_MARKETS[key]
        return {"status": "excluded", "code": key, "cap_tier": "T3",
                "label": "市场排除：%s（%s）" % (mkt["name"], mkt["reason"]),
                "cap_next": "别打（市场排除）",
                "cap_action": "市场排除：%s，别浪费首触；有转口/保税区需求再单独评估"
                              % mkt["name"]}
    return {"status": "other", "code": "other", "cap_tier": None,
            "label": "市场：未在目标清单（没核实），按分数正常打",
            "cap_next": "", "cap_action": ""}


def _main(argv=None):
    """Tiny lookup CLI: print the verdict for one market.

    查一个市场的裁决（手工核对规则表时用，不改打分代码）。
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Look up the market rule for one country "
                    "(查一个市场的裁决：土耳其/巴西壁垒、墨西哥/美国/欧盟排除).")
    parser.add_argument("--country", required=True,
                        help="Country name, e.g. Turkey / Nigeria "
                             "(国家名，如 Turkey / Nigeria)")
    parser.add_argument("--note", default="",
                        help="Lead note, e.g. re-export confirmed "
                             "(线索备注，如已确认转口)")
    args = parser.parse_args(argv)
    result = verdict(args.country, args.note)
    print("Market / 市场：%s" % args.country)
    print("Verdict / 裁决：%s" % result["label"])
    if result.get("cap_next"):
        print("Next / 下一步：%s" % result["cap_next"])
    if result.get("cap_action"):
        print("Action / 打法：%s" % result["cap_action"])
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
