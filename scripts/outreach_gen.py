#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
outreach_gen.py — 按线索分级生成中英对照建联消息

读lead_score.py 的分级逻辑，按T0/T1/T2/T3 分别生成不同语气的首触消息。
英文用于实际发送，中文供你审批核对（你看得懂，客户只收英文）。

用法:
    python scripts/outreach_gen.py examples/leads_example.csv --tier T0
    python scripts/outreach_gen.py examples/leads_example.csv --tier T1 --out drafts.md
    python scripts/outreach_gen.py examples/leads_example.csv --tier all --lang en

设计原则:
    · T0/T1 是「拿到第二个对话」，不是「成交」
    · 每封都必须有一句只对这家公司成立的话（why them），不能是模板套话
    · 报价永远不在第一封里出现
"""

import argparse
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import analyze, read_leads, _get  # noqa: E402

TIER_LABEL = {
    "T0": "立即建联（多线并进）",
    "T1": "本周首触",
    "T2": "低频培育",
    "T3": "暂不投入",
}

TIER_ENVELOPE = {
    # 主题行策略
    "T0": ("直接、具体、提到他提过的事",
           "Name it specifically — the first line must reference something they said or did"),
    "T1": ("轻、短、给对方一个容易回应的理由",
           "Low-friction — give them an easy reason to reply"),
    "T2": ("更轻，只求确认信息，不求回复",
           "Lightest touch — just confirm facts, do not ask for a reply"),
    "T3": ("先补信息，不发信",
           "Do not send. Fill the gaps first"),
}

BODY = {
    "T0": {
        "en": """Subject: {product} supply — {company}

Hi {contact},

I noticed {why_them}. We manufacture {product} and supply buyers in {country} on a regular basis.

Two things I can confirm straight away:
- Specification: {product}, mixed loading on 40HQ accepted
- Terms: FOB / CIF both workable; quote usually within 48 hours

If it helps, I can send our price list for {product} first — no obligation, and if the range does not fit you we will say so.

What are the specifications and annual volume you are working with?

Best regards,
{sender}""",

    "zh": """主题：{product} 供应 — {company}

{contact}，

{why_them_zh}。我们做{product}，长期给{country} 的买家供货。

两件事可以先给你确认：
- 规格：{product}，支持 40HQ 混装
- 条款：FOB / CIF 都可以，报价通常 48 小时内出

如果有用，我可以先把{product} 的价格单发给你看看 —— 不勉强，如果价格区间不合适我会直接说。

你现在做的规格和年用量大概是多少？

顺祝商祺，
{sender}""",
    },
    "T1": {
        "en": """Subject: {product} — quick question, {country}?

Hi {contact},

Quick question, not a pitch.

We supply {product} to {country} buyers. I am checking whether we should keep {product} on our quotation sheet for your market this quarter.

- If yes, I will send the current price list.
- If no, tell me and I will not bother you again.

Worth two minutes?

Best regards,
{sender}""",

    "zh": """主题：{product} —— 一个问题，{country}？

{contact}，

就一个问题，不是推销。

我们给{country} 买家供{product}。我在确认这个季度要不要把{product} 留在给贵司市场的报价单里。

- 要的话，我发当前价格单给你。
- 不要的话，回一句，我不再打扰。

值得花两分钟吗？

顺祝商祺，
{sender}""",
    },
    "T2": {
        "en": """Subject: {product} supplier list update — {company}

Hi,

I am updating my supplier records for {country}.

Is {company} still sourcing {product} from Asia this year? A one-word yes or no is enough.

If no, I will remove you. No follow-up, no mailing list.

Best regards,
{sender}""",

    "zh": """主题：{product} 供应商名录更新 — {company}

你好，

我在更新{country} 的供应商记录。

贵司今年还从亚洲采购{product} 吗？回一个是或不是就够了。

如果不是，我把你移出名单，不再跟进。

顺祝商祺，
{sender}""",
    },
}

WHY_THEM = {
    "referral":   ("a client who knows the {country} market recommended your company to us",
                   "一位熟悉{country} 市场的客户把贵司介绍给了我们"),
    "trade_show": ("we met at the trade show and you asked about {product} pricing",
                   "展会上见过面，贵司问过{product} 的价格"),
    "customs":    ("your company shows a steady import record in this category",
                   "贵司在这一类目有稳定的进口记录"),
    "linkedin":   ("I came across your profile while mapping {country} importers of {product}",
                   "我在梳理{country} 的{product} 进口商时看到贵司主页"),
    "search":     ("I found your company while researching {country} importers of {product}",
                   "我在查{country} 的{product} 进口商时找到贵司"),
}


def short_product(product):
    """产品串可能很长（'TBR 12.00R20, PCR tubes'），取第一个品类词给主题行用。"""
    if not product:
        return "our products"
    first = re.split(r"[,;/|、]| and ", product)[0].strip()
    return first if len(first) <= 24 else product[:24].strip()


def build_why_them(row, product):
    prod = product or _get(row, "product", "") or "the products you handle"
    short = short_product(prod)
    country = _get(row, "country", "your market")
    note = _get(row, "note", "").strip()
    # 优先用这一家真实的备注情报，拼一句只对它成立的话（杜绝模板套话）
    if note:
        return ("your note mentioned: %s" % note,
                "贵司备注提到：%s" % note)
    src = _get(row, "source", "search").strip().lower()
    en, zh = WHY_THEM.get(src, WHY_THEM["search"])
    return en.format(product=short, country=country), \
           zh.format(product=short, country=_get(row, "country", "贵司所在市场"))


def render(lead, sender):
    tier = lead["tier"]
    short_prod = short_product(lead.get("product"))
    # 联系人：CSV 里没写contact 就退回Hi there / 你好，不要在正文里塞占位符
    raw_contact = (lead.get("contact") or "").strip()
    if raw_contact and raw_contact.lower() not in ("there", "-", "n/a"):
        contact_en = raw_contact
        contact_zh = raw_contact
    else:
        contact_en = "there"
        contact_zh = "你好"
    en_why, zh_why = lead["why_them"]

    body = BODY.get(tier)
    if body is None:
        return None

    env_en = TIER_ENVELOPE[tier]
    out = []
    out.append("=" * 70)
    out.append("%s  |  %s  |  %d 分" % (tier, TIER_LABEL[tier], lead["score"]))
    out.append("公司: %s (%s)" % (lead["company"], lead["country"]))
    out.append("写信策略: %s" % env_en[0])
    out.append("-" * 70)
    out.append("[EN — send this]")
    out.append(body["en"].format(company=lead["company"], contact=contact_en,
                                 product=short_prod, sender=sender,
                                 country=lead["country"], why_them=en_why))
    out.append("")
    out.append("[ZH — 中文对照，仅供你审批，客户不收]")
    out.append(body["zh"].format(company=lead["company"], contact=contact_zh,
                                 product=short_prod, sender=sender,
                                 country=lead["country"], why_them_zh=zh_why))
    out.append("")
    out.append("发送前自查:")
    out.append("  □ why them 那句是不是只对这家公司成立？换成同行还成立就重写")
    out.append("  □ 有没有一个具体数字（数量/规格/港口）？没有就补")
    out.append("  □ 全文有没有出现价格？没有 = 正确")
    out.append("  □ 主题行 40 字符以内？超了就改短")
    out.append("")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(
        description="按线索分级生成中英对照建联消息（只用标准库）")
    p.add_argument("csv_path", help="线索 CSV 路径")
    p.add_argument("--tier", choices=["T0", "T1", "T2", "T3", "all"], default="T0")
    p.add_argument("--sender", default="[Your Name] | [Company]",
                   help="落款，默认留占位符")
    p.add_argument("--lang", choices=["both", "en", "zh"], default="both")
    p.add_argument("--out", help="输出到 .md 文件，不填则打印到屏幕")
    args = p.parse_args()

    try:
        rows = read_leads(args.csv_path)
    except FileNotFoundError:
        raise SystemExit("错误：找不到文件 %s" % args.csv_path)

    leads = analyze(rows)
    # 把 why_them 与 contact 都透传给 lead，供 render 用
    for lead in leads:
        raw = next((r for r in rows
                    if _get(r, "company", "").lower() == lead["company"].lower()),
                   None)
        if raw is None:
            lead["contact"] = ""
            lead["why_them"] = build_why_them({}, lead.get("product", ""))
        else:
            lead["contact"] = _get(raw, "contact", "")
            lead["why_them"] = build_why_them(raw, lead.get("product", ""))

    if args.tier == "all":
        targets = [t for t in ("T0", "T1", "T2", "T3")
                   if any(l["tier"] == t for l in leads)]
    else:
        targets = [args.tier]

    blocks, skipped = [], 0
    for t in targets:
        picked = 0
        for lead in leads:
            if lead["tier"] != t:
                continue
            text = render(lead, args.sender)
            if text is None:
                skipped += 1
                continue
            if args.lang == "en":
                keep, out = False, []
                for line in text.split("\n"):
                    if line.startswith("[EN"):
                        keep = True
                    if line.startswith("[ZH"):
                        keep = False
                    if keep:
                        out.append(line)
                text = "\n".join(out)
            elif args.lang == "zh":
                keep, out = False, []
                for line in text.split("\n"):
                    if line.startswith("[EN"):
                        keep = False
                    if line.startswith("[ZH"):
                        keep = True
                    if keep:
                        out.append(line)
                text = "\n".join(out)
            blocks.append(text)
            picked += 1
        if picked == 0:
            count = sum(1 for l in leads if l["tier"] == t)
            if count > 0:
                blocks.append("[%s] 存在 %d 条 %s 线索，但无需写首触文案，先补齐信息。"
                              % (t, count, t))
            else:
                blocks.append("[%s] 本级无线索。" % t)

    if args.lang == "en":
        header = (
            "# Outreach drafts\n\n"
            "- Generated from: `%s`\n"
            "- Tiers: %s\n"
            "- Signature: %s\n"
            "- ⚠️ Review the checklist before sending; send the EN part, ZH is for your review only.\n\n"
            % (args.csv_path, ", ".join(targets), args.sender)
        )
        footer = ("\n" + "-" * 70 + "\n"
                  "Generated %d drafts. T3 needs no copy — fill the gaps first.\n" % len(blocks))
    else:
        header = (
            "# 建联文案草稿\n\n"
            "- 生成自: `%s`\n"
            "- 分级: %s\n"
            "- 落款: %s\n"
            "- ⚠️ 每封发前必看自查清单；EN 段发送，ZH 段仅供审批。\n\n"
            % (args.csv_path, ", ".join(targets), args.sender)
        )
        footer = ("\n" + "-" * 70 + "\n"
                  "共生成 %d 份草稿。T3 无需写文案——先把信息补齐。\n" % len(blocks))

    body = header + "\n".join(blocks) + footer

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(body)
        print("已写入 %s（%d 份草稿）" % (args.out, len(blocks)))
    else:
        print(body)


if __name__ == "__main__":
    main()
