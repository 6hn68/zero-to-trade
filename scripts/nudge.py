#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nudge.py — 催单话术库：报价/发样/谈价之后，对方不回，你说什么

报价发出去了、样品寄出去了、价格谈到一半了——然后对方没了动静。
这时候最难的不是等，是下一封写什么：写轻了没用，写重了把人吓跑。
这个脚本只干一件事：按「过去了几天 × 卡在哪一步」给你一封现成的话术，
WhatsApp 短版 + 邮件长版，中英对照（英文发、中文你审）。

跟 followup_plan.py 怎么分工（两套节奏不打架）:
    followup_plan.py 管「报价之前」：首触发出去之后，按 T0 D0/D2/D5、
    T1 D0/D3/D6、T2 D0/D7/D14 排触达，问的是「今年还采不采购」这种
    首触问题；T2 的 D14 是归档日，那天不发信。
    nudge.py 管「报价/发样/谈价之后」：Day 0 是报价发出去、样品寄出去、
    或者价格谈起来的那一天，不是首触那天。同一客户同一线程只走一条线：
    报价前走 followup_plan，报价后走 nudge，别两边同时发——同一周里
    客户收到两封不同节奏的催信，等于告诉他你内部没谱。
    D3 对上 T1 的 D3、D7 对上 T2 的 D7 只是天数巧合：锚点不同（首触日
    vs 报价日），不要把两个 D3 当成同一天。

四档语气（一天比一天重，但 D30 也不撕破脸）:
    D3   轻提醒：只确认对方收到没有，不问决定、不施压。
    D7   问进度：问进展到哪一步，给对方一个「一句话就能回」的口子。
    D14  给台阶：降价 / 换规格 / 延账期三选一，对方不用自己想办法下台。
    D30  最后通牒但不撕破脸：明说这是最后一封，之后停手；同时留一句
         「以后有需要随时找我」，门一直开着。
    D30 之后停手，进长名单，季度扫一次（跟 followup_plan 的止损线同口径）。

每天早上的一张清单（--list）：不用一个个算日子——给它一个 JSON 文件，
里面是每个客户的 Day 0（报价/发样/谈价那天）和已经发过哪几档，它吐出
「今天该跟谁、为什么、说什么」：逾期的排最前面、标 ⚠ OVERDUE；今天到期的
其次；还没到的告诉你还有几天；D30 发完仍无回音的标停手、进长名单。
清单里每家都带一条现成的 WhatsApp 短版（英文在前、中文在后），复制就能发。
如果那家还填了规格 + 市场（size / market），清单里还会顺带贴上 tire_pack.py
出的规格包一句话摘要 + 缺什么没核实——两个工具一次跑通。

JSON 文件格式（公司名、联系人、产品全是虚构示例，【示例】前缀，真用之前换成自己的）:
    {"followups": [
      {"company": "【示例】海湾轮胎贸易", "contact": "Alex",
       "product": "TBR 12.00R20", "scenario": "quoted",
       "day0": "2026-11-10", "sent": ["D3"],
       "size": "12.00R20", "market": "saudi"},
      {"company": "【示例】尼罗河商贸", "contact": "Sara",
       "product": "TBR 11.00R20", "scenario": "sampled",
       "day0": "2026-11-19", "sent": []}
    ]}
字段说明：company / day0 / scenario 必填；contact / product 不填就用虚构示例值
（清单里会标出来，发送前换成真的）；sent 是已经发过的档（D3/D7/D14/D30），
不填当没发过；size / market / li / speed 选填，填了就链上 tire_pack.py。
--today 可以指定“今天是哪天”（默认就是今天，测试、补算旧账时用）。

只用标准库，Python 3.8+ 可直接跑，不联网，不写文件（除非你加 --out）。

用法见 --help（里面的例子都能直接复制）。
"""

import argparse
import json
import os
import sys
from datetime import date
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import _ZhArgumentParser  # noqa: E402

DAYS = ("D3", "D7", "D14", "D30")

TONE = {
    "D3": "轻提醒",
    "D7": "问进度",
    "D14": "给台阶（降价 / 换规格 / 延账期三选一）",
    "D30": "最后通牒但不撕破脸（留后路）",
}

# 场景：卡在哪一步。别名照单收，拼错了当场报错，不悄悄归到别的场景。
SCENARIOS = {
    "quoted": "已报价未回",
    "sampled": "已发样未回",
    "negotiating": "已谈价未定",
}
SCENARIO_ALIAS = {
    "quoted": "quoted", "quote": "quoted", "报价": "quoted",
    "sampled": "sampled", "sample": "sampled", "发样": "sampled",
    "negotiating": "negotiating", "negotiation": "negotiating",
    "price": "negotiating", "谈价": "negotiating",
}

# 止损线：D30 发完仍无任何回应 → 停手，进长名单，季度扫一次。
STOP_RULE = "D30 发完仍无任何回应（含已读不回）→ 停手，进长名单，季度扫一次。"

# 每条话术的占位符：{contact} 联系人、{company} 公司、{product} 产品。
# 示例默认值全是虚构的（【示例】前缀），别拿去真发——填自己的客户再跑。
DEFAULT_COMPANY = "【示例】海湾轮胎贸易"
DEFAULT_CONTACT = "Alex"
DEFAULT_PRODUCT = "TBR 12.00R20"


def normalize_day(raw):
    """'D3' / '3' / 'd3' 都收；别的直接报错，别悄悄排错日子。"""
    text = str(raw or "").strip().upper()
    if text.startswith("D"):
        text = text[1:]
    day = "D" + text
    if day not in DAYS:
        raise ValueError("天数只能是 D3 / D7 / D14 / D30，收到的是 %r" % raw)
    return day


def normalize_scenario(raw):
    """场景别名归一；认不出的词直接报错，别猜。"""
    text = str(raw or "").strip().lower()
    if text in SCENARIO_ALIAS:
        return SCENARIO_ALIAS[text]
    raise ValueError("场景只能是 quoted（已报价未回）/ sampled（已发样未回）/ "
                     "negotiating（已谈价未定），收到的是 %r" % raw)


# 12 条话术：4 个天数 × 3 个场景，每条 WhatsApp 短版 + 邮件长版，
# 每版英文在前、中文在后。D14 每版都含降价 / 换规格 / 延账期三个选项；
# D30 每版都含留后路句（英文 "reach out any time"，中文 "以后有需要随时找我"）。
_DRAFTS = {
    ("D3", "quoted"): {
        "whatsapp": {
            "en": ("Hi {contact}, just checking in — did the quote for {product} "
                   "reach you all right? Happy to resend it or adjust the sizes "
                   "if anything looks off."),
            "zh": ("{contact} 你好，冒昧打扰一下——{product} 的报价收到没有？"
                   "要是没收到或者规格想调整，我再发你一版。"),
        },
        "email": {
            "subject_en": "Quick check — your {product} quote from {company}",
            "subject_zh": "确认一下——{company} 发的 {product} 报价收到了吗",
            "en": ("Hi {contact},\n\nHope you are doing well. I sent over the quote "
                   "for {product} a few days ago and wanted to make sure it landed "
                   "in the right inbox — sometimes attachments get caught in spam.\n\n"
                   "If the prices or sizes need tweaking, just tell me which line "
                   "and I will rework it. No rush at all.\n\nBest regards"),
            "zh": ("{contact} 你好，\n\n前几天发了 {product} 的报价，想确认一下有没有收到"
                   "——附件有时会被当成垃圾邮件。\n\n价格或规格想改的话，告诉我是哪一行，"
                   "我重新给你算一版。不着急，等你方便的时候回就行。\n\n祝好"),
        },
    },
    ("D3", "sampled"): {
        "whatsapp": {
            "en": ("Hi {contact}, just checking in — has the {product} sample arrived? "
                   "Keen to hear how it looks and feels on your side."),
            "zh": ("{contact} 你好，{product} 的样品到了吗？"
                   "想听听你那边看上去、手感怎么样。"),
        },
        "email": {
            "subject_en": "Did the {product} sample arrive?",
            "subject_zh": "{product} 的样品到了吗？",
            "en": ("Hi {contact},\n\nJust a quick note to check whether the {product} "
                   "sample arrived safely. If it is still in transit, I can chase "
                   "the courier for you.\n\nWhenever you have had a chance to look at it, "
                   "I would love to hear what you think — even a one-line reply helps.\n\n"
                   "Best regards"),
            "zh": ("{contact} 你好，\n\n写信是想确认 {product} 的样品有没有平安到你手里。"
                   "要是还在路上，我帮你去问快递。\n\n你看过之后随便回一句感受就行，"
                   "一行字也帮大忙。\n\n祝好"),
        },
    },
    ("D3", "negotiating"): {
        "whatsapp": {
            "en": ("Hi {contact}, just checking in on the {product} price we were "
                   "discussing. Is there a number that would work on your side? "
                   "Happy to meet in the middle if I can."),
            "zh": ("{contact} 你好，{product} 的价格咱们上次聊到一半，"
                   "想问问你那边能接受的价位大概是多少？"
                   "我看看能不能往中间靠一靠。"),
        },
        "email": {
            "subject_en": "Picking up our {product} price talk",
            "subject_zh": "接着聊 {product} 的价格",
            "en": ("Hi {contact},\n\nPicking up where we left off on {product} — I am "
                   "still keen to find a price that works for both of us.\n\n"
                   "If you can share the number you have in mind, or what your other "
                   "suppliers are offering, I will see what I can do. "
                   "No pressure either way.\n\nBest regards"),
            "zh": ("{contact} 你好，\n\n接着聊 {product} 的价格——我还是想找一个两边都合适的价位。"
                   "\n\n你方便的话，告诉我你心里那个数，或者别的供应商报了多少，"
                   "我看看能怎么靠。不成也没关系。\n\n祝好"),
        },
    },
    ("D7", "quoted"): {
        "whatsapp": {
            "en": ("Hi {contact}, following up on the {product} quote — has anything "
                   "changed on your side, or is there a question I can answer? "
                   "If the timing is not right, just say so and I will check back later."),
            "zh": ("{contact} 你好，跟进一下 {product} 的报价——你那边有什么新情况，"
                   "或者有什么问题我可以解答？要是现在时机不对，直说就行，"
                   "我过段时间再来问。"),
        },
        "email": {
            "subject_en": "Any update on the {product} quote?",
            "subject_zh": "{product} 的报价有新进展吗？",
            "en": ("Hi {contact},\n\nIt has been a week since I sent the {product} quote, "
                   "so I wanted to check where things stand. A few things that might help:\n\n"
                   "- If the price is the blocker, tell me your target and I will see "
                   "what I can move.\n"
                   "- If the sizes are wrong, send me the right ones and I will re-quote "
                   "the same day.\n"
                   "- If the order is simply on hold, a quick 'not yet' is enough — "
                   "I will not chase you every week.\n\n"
                   "One line back would be a big help.\n\nBest regards"),
            "zh": ("{contact} 你好，\n\n{product} 的报价发过去一周了，"
                   "想问问现在进展到哪一步了。几件事或许能帮上忙：\n\n"
                   "- 要是价格卡住了，告诉我你的目标价，我看看能动多少。\n"
                   "- 要是规格不对，把对的规格发我，当天重新报价。\n"
                   "- 要是订单只是先放一放，回一句“还没定”就行，我不会每周都来问。\n\n"
                   "回一行字就帮大忙了。\n\n祝好"),
        },
    },
    ("D7", "sampled"): {
        "whatsapp": {
            "en": ("Hi {contact}, it has been a week since the {product} sample went out "
                   "— how did it test on your side? Even a short 'good' or "
                   "'not for us' helps me plan."),
            "zh": ("{contact} 你好，{product} 的样品寄出一周了，"
                   "你那边测试得怎么样？回一句“还行”或者“不合适”都行，"
                   "帮我心里有个数。"),
        },
        "email": {
            "subject_en": "How did the {product} sample test?",
            "subject_zh": "{product} 的样品测试得怎么样？",
            "en": ("Hi {contact},\n\nA week on from the {product} sample — how did it hold up "
                   "in your testing? I am especially keen to hear about the tread wear "
                   "and the sidewall finish, since those are the two things buyers "
                   "usually judge first.\n\n"
                   "If it is not the right fit, tell me what missed and I will suggest "
                   "a different size or compound. A short reply is plenty.\n\nBest regards"),
            "zh": ("{contact} 你好，\n\n{product} 的样品寄出一周了，测试结果怎么样？"
                   "我最想听的是花纹磨损和胎侧做工这两点，买家一般先看这两样。\n\n"
                   "要是不合适，告诉我差在哪，我给你换个规格或配方推荐。"
                   "简单回一句就行。\n\n祝好"),
        },
    },
    ("D7", "negotiating"): {
        "whatsapp": {
            "en": ("Hi {contact}, checking in on our {product} price talk — where are we? "
                   "If there is a gap I have not understood, tell me and I will work on it."),
            "zh": ("{contact} 你好，问问 {product} 的价格谈到哪一步了？"
                   "要是我还有哪点没理解到位，你直接告诉我，我来想办法。"),
        },
        "email": {
            "subject_en": "Where are we on the {product} price?",
            "subject_zh": "{product} 的价格谈到哪一步了？",
            "en": ("Hi {contact},\n\nChecking in on the {product} price we have been "
                   "discussing. I would rather hear a straight 'too high' than silence "
                   "— at least then I know what to work on.\n\n"
                   "If you can share your target price, or the one term that matters most "
                   "to you (price, payment terms, or delivery time), I will come back "
                   "with something concrete.\n\nBest regards"),
            "zh": ("{contact} 你好，\n\n问问 {product} 的价格谈到哪一步了。"
                   "与其没回音，我更想听一句实在的“太贵了”，至少知道该往哪使劲。\n\n"
                   "你方便的话，告诉我目标价，或者你最看重的那一项"
                   "（价格、账期还是交货期），我回来给你一个具体的方案。\n\n祝好"),
        },
    },
    ("D14", "quoted"): {
        "whatsapp": {
            "en": ("Hi {contact}, I do not want to keep chasing the {product} quote, "
                   "so here are three ways we can move forward — pick whichever fits: "
                   "(1) a lower price on a smaller first order, "
                   "(2) a different size/spec that costs less, or "
                   "(3) longer payment terms instead of a price cut. "
                   "Or just tell me 'not now' and I will leave it there."),
            "zh": ("{contact} 你好，我不想一直追着问 {product} 的报价，"
                   "给你三个台阶、任选一个：(1) 首单量小一点、价格降一点；"
                   "(2) 换规格、换个便宜点的型号；"
                   "(3) 价格不动、账期放长一点。"
                   "或者直接回一句“现在不合适”，我就不打扰了。"),
        },
        "email": {
            "subject_en": "Three ways forward on the {product} quote",
            "subject_zh": "{product} 的报价，三个往下走的办法",
            "en": ("Hi {contact},\n\nTwo weeks since the {product} quote, and I would "
                   "rather give you options than keep asking the same question. "
                   "Pick any one of these:\n\n"
                   "1. Lower price — a smaller first order at a lower unit price, "
                   "so you can test us without committing big.\n"
                   "2. Different size/spec — swap to a size or spec that costs less; "
                   "I will re-quote the same day.\n"
                   "3. Longer payment terms — keep the price as quoted, but with "
                   "payment terms stretched out.\n\n"
                   "Or reply 'not now' and I will close the file with no hard feelings. "
                   "The choice is yours.\n\nBest regards"),
            "zh": ("{contact} 你好，\n\n{product} 的报价发过去两周了，"
                   "与其反复问同一个问题，不如给你三个选择：\n\n"
                   "1. 降价——首单量小一点、单价降一点，先小批量试试，不用一次押大。\n"
                   "2. 换规格——换个便宜点的规格或型号，我当天重新报价。\n"
                   "3. 延账期——价格按报价来，账期给你放长一点。\n\n"
                   "或者回一句“现在不合适”，我就把这单先合上，不会有任何芥蒂。"
                   "怎么选都由你。\n\n祝好"),
        },
    },
    ("D14", "sampled"): {
        "whatsapp": {
            "en": ("Hi {contact}, the {product} sample has been with you two weeks — "
                   "if it is not the right fit, here are three ways forward: "
                   "(1) a lower price on a different compound, "
                   "(2) a different size/spec to test instead, or "
                   "(3) longer payment terms on the first order. "
                   "Or a plain 'not for us' closes it cleanly."),
            "zh": ("{contact} 你好，{product} 的样品到你手里两周了，"
                   "要是不合适，给你三个台阶：(1) 换个配方、价格降一点；"
                   "(2) 换规格、再寄个别的型号试试；"
                   "(3) 首单账期放长一点。"
                   "或者直接回一句“不合适”，这事就干净利落地合上。"),
        },
        "email": {
            "subject_en": "Three ways forward after the {product} sample",
            "subject_zh": "{product} 样品之后，三个往下走的办法",
            "en": ("Hi {contact},\n\nTwo weeks since the {product} sample arrived, and I "
                   "would rather give you options than keep asking how the test went. "
                   "Pick any one of these:\n\n"
                   "1. Lower price — a different compound at a lower price, if the "
                   "sample's cost was the problem.\n"
                   "2. Different size/spec — I will send another size or spec to test "
                   "instead, same courier, no charge for the second sample.\n"
                   "3. Longer payment terms — keep the price as quoted, but with "
                   "payment terms stretched out on the first order.\n\n"
                   "Or reply 'not for us' and I will close the file with no hard "
                   "feelings. The choice is yours.\n\nBest regards"),
            "zh": ("{contact} 你好，\n\n{product} 的样品到你手里两周了，"
                   "与其反复问测试结果，不如给你三个选择：\n\n"
                   "1. 降价——换个便宜点的配方，要是样品的成本卡住了就走这条。\n"
                   "2. 换规格——再寄个别的规格或型号给你试，同一家快递，第二份样品不收费。\n"
                   "3. 延账期——价格按报价来，首单账期给你放长一点。\n\n"
                   "或者回一句“不合适”，我就把这单先合上，不会有任何芥蒂。"
                   "怎么选都由你。\n\n祝好"),
        },
    },
    ("D14", "negotiating"): {
        "whatsapp": {
            "en": ("Hi {contact}, we have been going back and forth on {product} for two "
                   "weeks, so let me put three options on the table: "
                   "(1) a lower price if the first order is smaller, "
                   "(2) a different size/spec at a lower cost, or "
                   "(3) longer payment terms while the price stays. "
                   "Pick one, or tell me what would actually close it."),
            "zh": ("{contact} 你好，{product} 的价格来回谈了两周，"
                   "我把三个选择摆出来：(1) 首单小一点、价格降一点；"
                   "(2) 换规格、换个成本低的型号；"
                   "(3) 价格不动、账期放长。"
                   "你选一个，或者直接告诉我怎样才算谈成。"),
        },
        "email": {
            "subject_en": "Three options to close the {product} price",
            "subject_zh": "谈成 {product} 的价格，三个选择",
            "en": ("Hi {contact},\n\nWe have been going back and forth on the {product} price "
                   "for two weeks, so let me put three options on the table:\n\n"
                   "1. Lower price — a smaller first order at a lower unit price; "
                   "you test us small, we earn the bigger orders later.\n"
                   "2. Different size/spec — swap to a size or spec that costs less; "
                   "I will re-quote the same day.\n"
                   "3. Longer payment terms — the price stays where it is, but the "
                   "payment terms stretch out.\n\n"
                   "Pick one, or tell me plainly what would actually close it — "
                   "a straight answer helps us both more than another round.\n\n"
                   "Best regards"),
            "zh": ("{contact} 你好，\n\n{product} 的价格来回谈了两周，"
                   "我把三个选择摆出来：\n\n"
                   "1. 降价——首单小一点、单价降一点，先小批量试试，大单以后再说。\n"
                   "2. 换规格——换个成本低的规格或型号，我当天重新报价。\n"
                   "3. 延账期——价格不动，账期给你放长一点。\n\n"
                   "你选一个，或者直接告诉我怎样才算谈成——一句实在话，"
                   "比再绕一圈对两边都有用。\n\n祝好"),
        },
    },
    ("D30", "quoted"): {
        "whatsapp": {
            "en": ("Hi {contact}, this is my last note on the {product} quote — "
                   "I will not chase it again after this. If the timing or the price "
                   "was the problem, the door stays open: feel free to reach out "
                   "any time, and I will pick it up where we left off."),
            "zh": ("{contact} 你好，这是关于 {product} 报价的最后一封消息，"
                   "之后我不会再追了。要是时机或价格不对，门一直开着："
                   "以后有需要随时找我，咱们从停下的地方接着聊。"),
        },
        "email": {
            "subject_en": "Closing the file on the {product} quote (for now)",
            "subject_zh": "{product} 的报价先合上（随时可以再打开）",
            "en": ("Hi {contact},\n\nThis is my last note on the {product} quote — a month "
                   "has passed, and I do not want to be the supplier who keeps pushing "
                   "after the answer is clear.\n\n"
                   "If the price, the sizes, or the timing was the problem, none of that "
                   "is final. The door stays open: feel free to reach out any time, "
                   "and I will pick it up where we left off, no awkwardness.\n\n"
                   "Thank you for your time, and I wish you well with the season ahead.\n\n"
                   "Best regards"),
            "zh": ("{contact} 你好，\n\n这是关于 {product} 报价的最后一封消息——"
                   "一个月过去了，我不想做那个答案已经很清楚了还一直推的供应商。\n\n"
                   "不管是价格、规格还是时机卡住了，这些都不是定局。门一直开着："
                   "以后有需要随时找我，咱们从停下的地方接着聊，不会尴尬。\n\n"
                   "谢谢你抽时间看这些，祝你接下来的旺季顺利。\n\n祝好"),
        },
    },
    ("D30", "sampled"): {
        "whatsapp": {
            "en": ("Hi {contact}, last note on the {product} sample — I will leave it "
                   "here. If the sample did not fit, or the timing was wrong, "
                   "feel free to reach out any time and we can try a different "
                   "size or compound."),
            "zh": ("{contact} 你好，这是关于 {product} 样品的最后一封消息，"
                   "之后我就不打扰了。要是样品不合适，或者时机不对，"
                   "以后有需要随时找我，咱们可以换个规格或配方再试。"),
        },
        "email": {
            "subject_en": "Closing the file on the {product} sample (for now)",
            "subject_zh": "{product} 的样品先合上（随时可以再打开）",
            "en": ("Hi {contact},\n\nThis is my last note on the {product} sample — a month "
                   "has passed since it arrived, and I will leave it here rather than "
                   "keep asking.\n\n"
                   "If the sample did not fit, or the timing was wrong, none of that is "
                   "final. Feel free to reach out any time and we can try a different "
                   "size or compound — no awkwardness about the gap.\n\n"
                   "Thank you for your time.\n\nBest regards"),
            "zh": ("{contact} 你好，\n\n这是关于 {product} 样品的最后一封消息——"
                   "样品到你手里一个月了，我不打算再追着问了。\n\n"
                   "要是样品不合适，或者时机不对，这些都不是定局。"
                   "以后有需要随时找我，咱们可以换个规格或配方再试，中间隔了多久都没关系。\n\n"
                   "谢谢你抽时间看这些。\n\n祝好"),
        },
    },
    ("D30", "negotiating"): {
        "whatsapp": {
            "en": ("Hi {contact}, this is my last note on the {product} price — "
                   "I will not push it further. We could not close the gap this time, "
                   "and that is fine. Feel free to reach out any time if things "
                   "change on your side."),
            "zh": ("{contact} 你好，这是关于 {product} 价格的最后一封消息，"
                   "之后我不会再推了。这次没谈拢没关系。"
                   "以后有需要随时找我，你那边情况变了咱们再聊。"),
        },
        "email": {
            "subject_en": "Closing the file on the {product} price (for now)",
            "subject_zh": "{product} 的价格先合上（随时可以再打开）",
            "en": ("Hi {contact},\n\nThis is my last note on the {product} price — a month of "
                   "back and forth, and the gap is still there. I will not push it "
                   "further.\n\n"
                   "We could not close it this time, and that is fine. If things change "
                   "on your side — a new budget, a new season, a different size — "
                   "feel free to reach out any time and we will start from where we "
                   "left off.\n\nThank you for the honest conversation.\n\nBest regards"),
            "zh": ("{contact} 你好，\n\n这是关于 {product} 价格的最后一封消息——"
                   "来回谈了一个月，差距还在，我不会再推了。\n\n"
                   "这次没谈拢没关系。要是你那边情况变了——新预算、新一季、换个规格——"
                   "以后有需要随时找我，咱们从停下的地方接着聊。\n\n"
                   "谢谢你这段时间的坦诚沟通。\n\n祝好"),
        },
    },
}


def _fill(text, company, contact, product):
    """把占位符填成真值。缺了也不炸——空串顶上去，话术照样能读。"""
    return text.format(company=company, contact=contact, product=product)


def get_nudge(day, scenario, company=None, contact=None, product=None):
    """拿一条催单话术。纯函数：只查表填空，不读文件、不联网。

    day: D3 / D7 / D14 / D30（'3'、'd7' 也收）；scenario: quoted / sampled /
    negotiating（别名 quote / sample / price 也收）。company / contact /
    product 不填就用虚构示例值——示例值只用来演示，往外发之前必须换成真的。
    """
    day = normalize_day(day)
    scenario = normalize_scenario(scenario)
    company = (company or "").strip() or DEFAULT_COMPANY
    contact = (contact or "").strip() or DEFAULT_CONTACT
    product = (product or "").strip() or DEFAULT_PRODUCT
    draft = _DRAFTS[(day, scenario)]
    wa = {"en": _fill(draft["whatsapp"]["en"], company, contact, product),
          "zh": _fill(draft["whatsapp"]["zh"], company, contact, product)}
    em = draft["email"]
    email = {
        "subject_en": _fill(em["subject_en"], company, contact, product),
        "subject_zh": _fill(em["subject_zh"], company, contact, product),
        "en": _fill(em["en"], company, contact, product),
        "zh": _fill(em["zh"], company, contact, product),
    }
    return {
        "day": day,
        "scenario": scenario,
        "scenario_zh": SCENARIOS[scenario],
        "tone": TONE[day],
        "company": company,
        "contact": contact,
        "product": product,
        "whatsapp": wa,
        "email": email,
        "stop_rule": STOP_RULE,
        "followup_plan_note": (
            "Day 0 是报价/发样/谈价那天，不是首触那天。报价前走 followup_plan.py "
            "（T0 D0/D2/D5、T1 D0/D3/D6、T2 D0/D7/D14），报价后走本脚本，"
            "同一客户同一线程只走一条线，别两边同时发。"),
        "reproduce": ("python scripts/nudge.py --day %s --scenario %s "
                      "--company %r --contact %s --product %s"
                      % (day, scenario, company, contact, product)),
    }


def render_table(nudge, channels=("whatsapp", "email")):
    """人看的版：先讲这封是什么语气、卡在哪一步，再贴话术（英文在前、中文在后）。"""
    lines = ["=" * 76,
             "  催单话术  %s · %s（%s）  ·  语气：%s"
             % (nudge["day"], nudge["scenario"], nudge["scenario_zh"], nudge["tone"]),
             "  客户：%s（联系人 %s）· 产品：%s"
             % (nudge["company"], nudge["contact"], nudge["product"]),
             "=" * 76, ""]
    if "whatsapp" in channels:
        wa = nudge["whatsapp"]
        lines += ["[WhatsApp 短版 — 直接复制发]", "",
                  "  EN:", "  " + wa["en"].replace("\n", "\n  "), "",
                  "  中文对照:", "  " + wa["zh"].replace("\n", "\n  "), ""]
    if "email" in channels:
        em = nudge["email"]
        lines += ["[邮件长版 — 主题行 + 正文]", "",
                  "  Subject: %s" % em["subject_en"],
                  "  主题（中文对照）: %s" % em["subject_zh"], "",
                  "  EN:"]
        lines += ["  " + ln for ln in em["en"].split("\n")]
        lines += ["", "  中文对照:"]
        lines += ["  " + ln for ln in em["zh"].split("\n")]
        lines += [""]
    lines += ["-" * 76,
              "  止损线：%s" % nudge["stop_rule"],
              "  衔接：%s" % nudge["followup_plan_note"],
              "  复现：%s" % nudge["reproduce"],
              "=" * 76, ""]
    return "\n".join(lines)


def render_json(nudge, channels=("whatsapp", "email")):
    """机器读的版：只含选中的渠道，不含本机时间，同样参数换台机器结果一致。"""
    payload = {"day": nudge["day"], "scenario": nudge["scenario"],
               "scenario_zh": nudge["scenario_zh"], "tone": nudge["tone"],
               "company": nudge["company"], "contact": nudge["contact"],
               "product": nudge["product"],
               "stop_rule": nudge["stop_rule"],
               "followup_plan_note": nudge["followup_plan_note"],
               "reproduce": nudge["reproduce"]}
    for ch in channels:
        payload[ch] = nudge[ch]
    return json.dumps(payload, ensure_ascii=False, indent=2)



# ---------------------------------------------------------------------------
# Daily list / 每日清单：今天该跟谁、为什么、说什么
# ---------------------------------------------------------------------------
# One ladder, four rungs: D3 → D7 → D14 → D30. Days are counted from Day 0
# (the day the quote went out / the sample shipped / the price talk started).
# 四档一根梯子：D3 → D7 → D14 → D30，天数从 Day 0（报价/发样/谈价那天）算起。
DAY_BUCKETS = (3, 7, 14, 30)

# Status labels: English first, Chinese after.
# 状态：英文在前、中文在后。
STATUS_LABELS = {
    "due_today": ("DUE TODAY", "今天就发"),
    "overdue": ("OVERDUE", "过期了"),
    "upcoming": ("NOT YET DUE", "还没到"),
    "stopped": ("STOPPED — long list", "已停手，进长名单"),
}

# Why-line per scenario: English first, Chinese after. {days} = days elapsed.
# 原因句：英文在前、中文在后。{days} 是过去的天数。
WHY_LINES = {
    "quoted": ("Quote sent {days} days ago, no reply since",
               "报价发出 {days} 天，一直没回"),
    "sampled": ("Sample sent {days} days ago, no feedback since",
                "样品寄出 {days} 天，一直没反馈"),
    "negotiating": ("Price talk started {days} days ago, still open",
                    "价格谈了 {days} 天，还没定"),
}


def parse_date(text):
    """Parse YYYY-MM-DD strictly; anything else is a human error, not a crash.

    Returns a datetime.date. Raises ValueError with a plain-language message.
    """
    raw = str(text or "").strip()
    try:
        year, month, day = (int(part) for part in raw.split("-"))
        return date(year, month, day)
    except (ValueError, TypeError):
        raise ValueError("日期 %r 格式不对：写 YYYY-MM-DD，如 2026-11-10。"
                         % (text,))


def _coerce_today(today):
    """Accept a date, or a YYYY-MM-DD string, or None (= today)."""
    if today is None:
        return date.today()
    if isinstance(today, date):
        return today
    return parse_date(today)


def next_nudge(elapsed_days, sent):
    """Which rung is next, and is it due, overdue, or not yet?

    elapsed_days: days since Day 0. sent: day labels already sent
    (e.g. ["D3"]). Returns (next_day, status, overdue_days, due_in_days):
      next_day  — "D3"/"D7"/"D14"/"D30", or None when the ladder is done.
      status    — due_today / overdue / upcoming / stopped.
      overdue_days — how many days past the rung's day (0 unless overdue).
      due_in_days  — how many days until the rung's day (0 unless upcoming).
    D30 sent + still no reply = stopped: move to the quarterly long list.
    """
    sent_days = set(sent or [])
    remaining = [d for d in DAY_BUCKETS if ("D%d" % d) not in sent_days]
    if not remaining:
        return None, "stopped", 0, 0
    rung = remaining[0]
    if elapsed_days == rung:
        return "D%d" % rung, "due_today", 0, 0
    if elapsed_days > rung:
        return "D%d" % rung, "overdue", elapsed_days - rung, 0
    return "D%d" % rung, "upcoming", 0, rung - elapsed_days


def _pack_for_item(entry):
    """Chain to tire_pack.py: one-line pack summary + what is still unverified.

    entry may carry size / market / li / speed. Returns
    (summary, gaps, error) — summary is None when the entry has no size
    or market at all (no pack to build); error is a plain-language line
    when the pack cannot be built (bad size/market, tire_pack.py missing).
    Nothing here raises: a bad pack never kills the whole daily list.
    """
    size = str(entry.get("size") or "").strip()
    market = str(entry.get("market") or "").strip()
    if not size and not market:
        return None, [], None
    if not size or not market:
        return None, [], ("spec pack needs both size and market — one is missing / "
                          "规格包要规格和市场两个都给，缺了一个")
    try:
        import tire_pack
    except ImportError:
        return None, [], ("tire_pack.py not found next to nudge.py — pack skipped / "
                          "没找到 tire_pack.py，规格包跳过")
    try:
        pack = tire_pack.build_tire_pack(size, market,
                                         entry.get("li"), entry.get("speed"))
    except ValueError as e:
        return None, [], "spec pack error / 规格包报错：%s" % e
    summary = ("%s → %s (%s); GCC %s; %d docs (%s); %s"
               % (pack["size"], pack["market"], pack["market_en"],
                  "applies / 适用" if pack["gcc_applies"] else "n/a / 不适用",
                  len(pack["docs"]), pack["program"], pack["disclaimer"]))
    return summary, list(pack.get("gaps") or []), None


def _check_entry(entry, today):
    """Validate one follow-up entry; return (item, error).

    item is the daily-list row (or None); error is a plain-language line
    (or None). Bad rows go to the errors list — they never kill the list.
    """
    if not isinstance(entry, dict):
        return None, "entry is not an object / 这一条不是一个对象：%r" % (entry,)
    company = str(entry.get("company") or "").strip()
    if not company:
        return None, "missing company — every row needs a company name / 缺公司名"
    raw_day0 = entry.get("day0")
    if raw_day0 is None or not str(raw_day0).strip():
        return None, ("%s: missing day0 — the day the quote went out / sample "
                      "shipped / price talk started (YYYY-MM-DD) / %s：缺 day0——"
                      "报价/发样/谈价那天（YYYY-MM-DD）" % (company, company))
    try:
        day0 = parse_date(raw_day0)
    except ValueError as e:
        return None, "%s: %s" % (company, e)
    if day0 > today:
        return None, ("%s: day0 %s is in the future — the quote/sample/price talk "
                      "has not happened yet / %s：day0 %s 还没到，报价/发样/谈价"
                      "还没发生" % (company, day0.isoformat(), company,
                                    day0.isoformat()))
    try:
        scenario = normalize_scenario(entry.get("scenario"))
    except ValueError as e:
        return None, "%s: %s" % (company, e)
    sent_raw = entry.get("sent") or []
    if isinstance(sent_raw, str):
        sent_raw = [sent_raw]
    sent = []
    for raw in sent_raw:
        try:
            sent.append(normalize_day(raw))
        except ValueError as e:
            return None, "%s: bad sent value / sent 里有错值：%s" % (company, e)

    contact = str(entry.get("contact") or "").strip()
    product = str(entry.get("product") or "").strip()
    uses_example_defaults = False
    if not contact:
        contact, uses_example_defaults = DEFAULT_CONTACT, True
    if not product:
        product, uses_example_defaults = DEFAULT_PRODUCT, True

    elapsed = (today - day0).days
    next_day, status, overdue_days, due_in_days = next_nudge(elapsed, sent)
    en, zh = WHY_LINES[scenario]
    why = "%s / %s" % (en.format(days=elapsed), zh.format(days=elapsed))
    status_en, status_zh = STATUS_LABELS[status]
    if status == "overdue":
        status_label = "%s %d days / %s %d 天" % (status_en, overdue_days,
                                                  status_zh, overdue_days)
    elif status == "upcoming":
        status_label = "%s — in %d days (%s) / %s——还有 %d 天（%s）" % (
            status_en, due_in_days, next_day, status_zh, due_in_days, next_day)
    elif status == "stopped":
        status_label = "%s / %s" % (status_en, status_zh)
    else:
        status_label = "%s (%s) / %s（%s）" % (status_en, next_day,
                                               status_zh, next_day)

    item = {
        "company": company,
        "contact": contact,
        "product": product,
        "uses_example_defaults": uses_example_defaults,
        "scenario": scenario,
        "scenario_zh": SCENARIOS[scenario],
        "day0": day0.isoformat(),
        "days_elapsed": elapsed,
        "sent": sent,
        "next_day": next_day,
        "tone": TONE[next_day] if next_day else "",
        "status": status,
        "status_label": status_label,
        "overdue_days": overdue_days,
        "due_in_days": due_in_days,
        "why": why,
        "nudge": get_nudge(next_day, scenario, company, contact, product)
                 if next_day else None,
        "pack_summary": None,
        "pack_gaps": [],
        "pack_error": None,
    }
    summary, gaps, pack_error = _pack_for_item(entry)
    item["pack_summary"] = summary
    item["pack_gaps"] = gaps
    item["pack_error"] = pack_error
    return item, None


def build_daily_list(followups, today=None):
    """Turn a follow-up list into today's list: who, why, what to say.

    followups: list of dicts (see the module docstring for the JSON shape).
    today: a date, a YYYY-MM-DD string, or None (= today). Pure function:
    no files, no network. Returns:
      {"today": "YYYY-MM-DD",
       "items": [rows sorted overdue first, then due today, then upcoming,
                 then stopped — most overdue first inside each group],
       "errors": [plain-language lines for rows that could not be used],
       "counts": {"due_today": n, "overdue": n, "upcoming": n, "stopped": n}}
    Each item carries the ready-to-send WhatsApp short version (EN first,
    ZH after) inside item["nudge"], plus the tire-pack summary and gaps
    when the row has a size + market.
    """
    today = _coerce_today(today)
    if followups is None:
        followups = []
    if isinstance(followups, dict):
        followups = followups.get("followups", [])
    items, errors = [], []
    for entry in followups:
        item, error = _check_entry(entry, today)
        if error is not None:
            errors.append(error)
        else:
            items.append(item)

    def sort_key(item):
        order = {"overdue": 0, "due_today": 1, "upcoming": 2, "stopped": 3}
        return (order[item["status"]],
                -item["overdue_days"] if item["status"] == "overdue" else 0,
                item["due_in_days"] if item["status"] == "upcoming" else 0,
                item["company"])

    items.sort(key=sort_key)
    counts = {status: sum(1 for it in items if it["status"] == status)
              for status in ("due_today", "overdue", "upcoming", "stopped")}
    return {"today": today.isoformat(), "items": items,
            "errors": errors, "counts": counts}


def render_daily_list(daily, channels=("whatsapp",)):
    """Human-readable daily list: overdue first, flagged loud, then the rest.

    Each row says who (company/contact/product), why (days since Day 0 +
    scenario), and what to say (the WhatsApp short version, EN first,
    ZH after — copy and send). Stopped rows carry no draft, only the
    stop rule. channels=("whatsapp",) by default; ("email",) swaps the
    draft for the full email version instead.
    """
    counts = daily["counts"]
    lines = ["=" * 76,
             "  Today's follow-ups / 今天该跟谁  (%s)" % daily["today"],
             "  OVERDUE %d — act first / 先处理过期的 %d 家  ·  "
             "DUE TODAY %d / 今天到期 %d 家  ·  "
             "NOT YET %d / 还没到 %d 家  ·  STOPPED %d / 已停手 %d 家"
             % (counts["overdue"], counts["overdue"],
                counts["due_today"], counts["due_today"],
                counts["upcoming"], counts["upcoming"],
                counts["stopped"], counts["stopped"]),
             "=" * 76, ""]
    if not daily["items"] and not daily["errors"]:
        lines += ["  Nothing to follow up today / 今天没人要跟。",
                  "  (Add a row to your JSON file when a new quote / sample / "
                  "price talk starts.)",
                  ""]
    for item in daily["items"]:
        flag = "⚠ " if item["status"] == "overdue" else ""
        lines += ["%s%s — %s (contact %s) · %s"
                  % (flag, item["status_label"], item["company"],
                     item["contact"], item["product"]),
                  "  Next / 下一步：%s · %s"
                  % (item["next_day"] or "—", item["tone"] or "—"),
                  "  Why / 为什么：%s" % item["why"]]
        if item["uses_example_defaults"]:
            lines += ["  Note / 注意：contact or product is the fictional example "
                      "default — replace it before you send / 联系人或产品还是虚构"
                      "示例值，发送前换成真的"]
        if item["pack_summary"]:
            lines += ["  Spec pack / 规格包：%s" % item["pack_summary"]]
        if item["pack_gaps"]:
            lines += ["  Pack gaps / 规格包缺项：%s" % "; ".join(item["pack_gaps"])]
        if item["pack_error"]:
            lines += ["  Pack note / 规格包提示：%s" % item["pack_error"]]
        if item["nudge"] is None:
            lines += ["  Stop / 停手：%s" % STOP_RULE, ""]
            continue
        nudge = item["nudge"]
        if "email" in channels and "whatsapp" not in channels:
            em = nudge["email"]
            lines += ["  Say this by email / 邮件这样发：",
                      "  Subject: %s" % em["subject_en"],
                      "  主题（中文对照）: %s" % em["subject_zh"], "",
                      "  EN:"]
            lines += ["  " + ln for ln in em["en"].split("\n")]
            lines += ["", "  中文对照:"]
            lines += ["  " + ln for ln in em["zh"].split("\n")]
        else:
            wa = nudge["whatsapp"]
            lines += ["  Say this on WhatsApp / WhatsApp 这样发：",
                      "  EN: %s" % wa["en"],
                      "  中文对照：%s" % wa["zh"]]
            lines += ["  Email subject / 邮件主题：%s" % nudge["email"]["subject_en"]]
        lines += [""]
    if daily["errors"]:
        lines += ["-" * 76,
                  "  Rows skipped / 跳过的行（%d 条，先修好再跑）："
                  % len(daily["errors"])]
        for error in daily["errors"]:
            lines += ["   - %s" % error]
        lines += [""]
    lines += ["-" * 76,
              "  Stop rule / 止损线：%s" % STOP_RULE,
              "  Day 0 is the day the quote went out / sample shipped / price talk "
              "started — not the first-touch day. / Day 0 是报价/发样/谈价那天，"
              "不是首触那天。",
              "=" * 76, ""]
    return "\n".join(lines)


def render_daily_list_json(daily):
    """Machine-readable daily list: same rows, same order, no local time
    beyond the "today" the caller passed in."""
    return json.dumps(daily, ensure_ascii=False, indent=2)


def build_parser():
    p = _ZhArgumentParser(
        prog="nudge.py",
        description="催单话术库：报价/发样/谈价之后对方不回，按天数（D3/D7/D14/D30）×"
                    "场景（已报价未回/已发样未回/已谈价未定）给你 WhatsApp 短版 + "
                    "邮件长版，中英对照（只用标准库，不联网）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""可直接复制的例子:
  python scripts/nudge.py --day D3 --scenario quoted
  python scripts/nudge.py --day D7 --scenario sampled --channel whatsapp
  python scripts/nudge.py --day D14 --scenario negotiating --company "【示例】海湾轮胎贸易" --contact Alex --product "TBR 12.00R20"
  python scripts/nudge.py --day D30 --scenario quoted --format json --out nudge.json

每天一张清单（--list）：给它一个 JSON 文件，里面是每个客户的 Day 0 和已发过哪几档，
它吐出「今天该跟谁、为什么、说什么」，逾期的排最前面、标 ⚠ OVERDUE：
  python scripts/nudge.py --list followups.json
  python scripts/nudge.py --list followups.json --today 2026-11-22 --format json
JSON 文件格式（公司名、联系人、产品全是虚构示例，真用之前换成自己的）:
  {"followups": [
    {"company": "【示例】海湾轮胎贸易", "contact": "Alex",
     "product": "TBR 12.00R20", "scenario": "quoted",
     "day0": "2026-11-10", "sent": ["D3"],
     "size": "12.00R20", "market": "saudi"},
    {"company": "【示例】尼罗河商贸", "contact": "Sara",
     "product": "TBR 11.00R20", "scenario": "sampled",
     "day0": "2026-11-19", "sent": []}]}
company / day0 / scenario 必填；contact / product 不填就用虚构示例值（清单里会标出来）；
sent 是已发过的档，不填当没发过；size / market / li / speed 选填，填了就链上 tire_pack.py，
清单里贴规格包一句话摘要 + 缺什么没核实。

--day 和 --scenario：单条话术模式必填；--list 模式不用填。
--channel 默认两者都出（whatsapp/email/both）；--list 模式默认只出 WhatsApp 短版，
--channel email 改出邮件长版。
Day 0 是报价/发样/谈价那天，不是首触那天——报价前走 followup_plan.py，
报价后走这个脚本，同一客户同一线程只走一条线。""")
    p.add_argument("--day", required=False, default=None,
                   help="过去了几天：D3 / D7 / D14 / D30（单条模式必填）")
    p.add_argument("--scenario", required=False, default=None,
                   help="卡在哪一步：quoted（已报价未回）/ sampled（已发样未回）/ "
                        "negotiating（已谈价未定）（单条模式必填）")
    p.add_argument("--list", default=None, metavar="FILE",
                   help="每日清单模式：JSON 文件路径，里面是跟进中的客户列表"
                        "（格式见 --help 末尾的例子）")
    p.add_argument("--today", default=None, metavar="YYYY-MM-DD",
                   help="清单模式里“今天是哪天”，默认就是今天（测试、补算旧账时用）")
    p.add_argument("--company", default=DEFAULT_COMPANY,
                   help="客户公司名（默认虚构示例：%s；往外发之前必须换成真的）"
                        % DEFAULT_COMPANY)
    p.add_argument("--contact", default=DEFAULT_CONTACT,
                   help="联系人名字（默认 %s）" % DEFAULT_CONTACT)
    p.add_argument("--product", default=DEFAULT_PRODUCT,
                   help="产品/规格（默认 %s）" % DEFAULT_PRODUCT)
    p.add_argument("--channel", choices=["whatsapp", "email", "both"],
                   default="both", help="出哪个渠道的话术，默认 both（两者都出）")
    p.add_argument("--format", choices=["table", "json"], default="table",
                   help="输出格式：table=人看的版(默认) / json=给别的脚本用")
    p.add_argument("--out", help="把结果写到文件（两种格式都支持）")
    return p


def main():
    parser = build_parser()
    if len(sys.argv) == 1:
        parser.print_usage(sys.stderr)
        print("\n没给参数：不知道怎么填就跑 python scripts/nudge.py --help，"
              "里面有能直接复制的例子。", file=sys.stderr)
        raise SystemExit(2)
    args = parser.parse_args()

    # Daily-list mode: --list FILE [--today YYYY-MM-DD].
    # 清单模式：--list 文件 [--today 日期]。
    if args.list:
        try:
            with open(args.list, encoding="utf-8") as f:
                data = json.load(f)
        except OSError as e:
            raise SystemExit("错误：打不开「%s」：%s（先确认文件在不在）"
                             % (args.list, e.strerror or e))
        except json.JSONDecodeError as e:
            raise SystemExit("错误：「%s」不是合法 JSON：第 %d 行 %s"
                             % (args.list, e.lineno, e.msg))
        if isinstance(data, dict):
            if "followups" not in data:
                raise SystemExit("错误：「%s」里没找到 followups 列表——文件该是 "
                                 "{\"followups\": [...]} 这种格式，例子见 "
                                 "python scripts/nudge.py --help" % args.list)
            followups = data["followups"]
        elif isinstance(data, list):
            followups = data
        else:
            raise SystemExit("错误：「%s」该是 JSON 列表或 {\"followups\": [...]}，"
                             "现在是 %s" % (args.list, type(data).__name__))
        if not isinstance(followups, list):
            raise SystemExit("错误：followups 该是个列表，现在是 %s"
                             % type(followups).__name__)
        try:
            daily = build_daily_list(followups, today=args.today)
        except ValueError as e:
            raise SystemExit("错误：%s\n  不知道怎么填就跑：python scripts/nudge.py --help"
                             % e)
        channels = ("whatsapp",) if args.channel in ("both", "whatsapp") \
            else ("email",)
        text = render_daily_list_json(daily) if args.format == "json" \
            else render_daily_list(daily, channels)
        if not text.endswith("\n"):
            text += "\n"
        sys.stdout.write(text)
        if args.out:
            try:
                with open(args.out, "w", encoding="utf-8", newline="") as f:
                    f.write(text)
            except OSError as e:
                raise SystemExit("错误：写不进「%s」：%s（换个目录，或先关掉打开它的程序）"
                                 % (args.out, e.strerror or e))
            print("已写入 %s" % args.out)
        return

    # Single-nudge mode: --day and --scenario are required here.
    # 单条模式：--day 和 --scenario 必填。
    if not args.day or not args.scenario:
        parser.print_usage(sys.stderr)
        print("\n单条话术要 --day 和 --scenario 两个都给（如 --day D3 --scenario quoted）；"
              "\n要每天一张清单就跑 --list followups.json。不知道怎么填就跑 "
              "python scripts/nudge.py --help，里面有能直接复制的例子。",
              file=sys.stderr)
        raise SystemExit(2)
    try:
        nudge = get_nudge(args.day, args.scenario, args.company,
                          args.contact, args.product)
    except ValueError as e:
        raise SystemExit("错误：%s\n  不知道怎么填就跑：python scripts/nudge.py --help"
                         % e)
    channels = ("whatsapp", "email") if args.channel == "both" else (args.channel,)
    text = render_json(nudge, channels) if args.format == "json" \
        else render_table(nudge, channels)
    if not text.endswith("\n"):
        text += "\n"
    sys.stdout.write(text)
    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8", newline="") as f:
                f.write(text)
        except OSError as e:
            raise SystemExit("错误：写不进「%s」：%s（换个目录，或先关掉打开它的程序）"
                             % (args.out, e.strerror or e))
        print("已写入 %s" % args.out)


if __name__ == "__main__":
    main()
