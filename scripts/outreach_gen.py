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
    python scripts/outreach_gen.py examples/leads_example.csv --tier T0 --lang es
    python scripts/outreach_gen.py examples/leads_example.csv --tier T1 --lang pt --out drafts_pt.md

设计原则:
    · T0/T1 是「拿到第二个对话」，不是「成交」
    · 每封都必须有一句只对这家公司成立的话（why them），不能是模板套话
    · 报价永远不在第一封里出现（价格数字、价单附件都不发）
    · 一封信只有一个 CTA，对方一句话就能回
    · 正文 5-8 句；主题行 ≤40 字符、预览首句 ≤120 字符（手机端 Gmail 截断线）
    · 主题与正文不得出现 ALL CAPS 吼叫、连发感叹号、Free/Cheap/Best price 等 spam 触发词
    · note 为空导致 why them 退化成通用模板时，脚本会直接报警催你去补背调，而不是闷头出废信
"""

import argparse
import csv
import logging
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import LeadDataError, analyze, read_leads, _get, write_trace, _ZhArgumentParser, setup_log  # noqa: E402




TIER_LABEL = {
    "T0": "立即建联（多线并进）",
    "T1": "本周首触",
    "T2": "低频培育",
    "T3": "暂不投入",
}

TIER_LABEL_EN = {
    "T0": "Reach out now (multi-channel)",
    "T1": "First touch this week",
    "T2": "Low-frequency nurture",
    "T3": "No investment yet",
}

# 主题行候选：第一个超 40 字符就自动降级到下一个更短的写法
SUBJECT = {
    "T0": [("{product} supply — {company}", "{product} 供应 — {company}"),
           ("{product} supply", "{product} 供应")],
    "T1": [("{product} — one quick question", "{product} —— 一个问题")],
    "T2": [("{company} — {product} sourcing check", "{company} —— {product} 采购确认"),
           ("{product} sourcing check", "{product} 采购确认")],
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
        "en": """Subject: {subject}

{greeting}

{why_them}. That is why I am writing to you rather than to a general inbox.

We make {product} and ship to {country} on a regular basis. If you are sourcing this year, here are two things I can put in writing now:
- Specification: {product}, mixed loading on 40HQ accepted
- Terms: FOB / CIF both workable, quote turned around within 48 hours

What sizes and monthly volume are you running on {product} at the moment?

Best regards,
{sender}""",

    "zh": """主题：{subject}

{greeting}

{why_them}。所以我直接写给你，而不是发到总邮箱。

我们做{product}，长期发往{country}。如果贵司今年在采购，这两点我现在就能写清楚：
- 规格：{product}，支持 40HQ 混装
- 条款：FOB / CIF 都可以，报价 48 小时内出

贵司目前在跑的规格和月用量大概是多少？

顺祝商祺，
{sender}""",
    },
    "T1": {
        "en": """Subject: {subject}

{greeting}

{why_them}. One question, and then I will leave you alone.

We make {product} and supply other buyers in {country}. Before I put {company} on this quarter's call list — is {product} still something you source from Asia?

Reply with a size range and I will come back with numbers. Reply "not now" and I will not write again.

Best regards,
{sender}""",

    "zh": """主题：{subject}

{greeting}

{why_them}。就问一个问题，问完我就不再打扰。

我们做{product}，也给{country} 的其他买家供货。在把{company} 排进本季度的跟进名单之前 —— {product} 贵司还在从亚洲采购吗？

回我一个规格区间，我就给出数字；回一句「暂时不」，我就不再写信。

顺祝商祺，
{sender}""",
    },
    "T2": {
        "en": """Subject: {subject}

{greeting}

I am updating my notes on {country} importers of {product}.

Is {company} still sourcing {product} from Asia this year? One word is enough, and if it is no I will take you off the list and stop writing.

Best regards,
{sender}""",

    "zh": """主题：{subject}

{greeting}

我在更新{country} 的{product} 进口商记录。

{company} 今年还在从亚洲采购{product} 吗？回一个字就够了；如果不再采购，我就把贵司移出名单，不再写信。

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


# ---------------------------------------------------------------- 多语言建联 (V13)
# 模板与英文模板一一对应：同一条消息的 es/pt/ar 版。模板只此一处（脚本内嵌
# 字典），prompts/ 里不另建副本，免得两边 drift。每条非英语消息输出时后附
# 英文原文（见 render），供 John 按英文审批。对外文档中英对照、英文在前。
I18N_LANGS = ("es", "pt", "ar")

LANG_LABEL = {"es": "Español", "pt": "Português", "ar": "العربية"}

# 主题行候选：与 SUBJECT 同一规则，第一个超 40 字符就降级到更短的写法
SUBJECT_I18N = {
    "es": {
        "T0": [("{product} — suministro — {company}"),
               ("{product} — suministro")],
        "T1": [("{product} — una pregunta rápida")],
        "T2": [("{company} — revisión de compras de {product}"),
               ("{product} — revisión de compras")],
    },
    "pt": {
        "T0": [("{product} — fornecimento — {company}"),
               ("{product} — fornecimento")],
        "T1": [("{product} — uma pergunta rápida")],
        "T2": [("{company} — verificação de compras de {product}"),
               ("{product} — verificação de compras")],
    },
    "ar": {
        "T0": [("{product} — توريد — {company}"),
               ("{product} — توريد")],
        "T1": [("{product} — سؤال سريع")],
        "T2": [("{company} — التحقق من مشتريات {product}"),
               ("{product} — التحقق من المشتريات")],
    },
}

# why them：与 WHY_THEM 一一对应（同一来源同一句，三种语言版）
WHY_THEM_I18N = {
    "es": {
        "referral":   "un cliente que conoce el mercado de {country} nos recomendó su empresa",
        "trade_show": "nos conocimos en la feria y preguntaron por el precio de {product}",
        "customs":    "su empresa muestra un historial de importación constante en esta categoría",
        "linkedin":   "encontré su perfil mientras mapeaba los importadores de {product} en {country}",
        "search":     "encontré su empresa mientras investigaba los importadores de {product} en {country}",
    },
    "pt": {
        "referral":   "um cliente que conhece o mercado de {country} recomendou a sua empresa",
        "trade_show": "nos conhecemos na feira e perguntaram pelo preço de {product}",
        "customs":    "a sua empresa apresenta um histórico de importação constante nesta categoria",
        "linkedin":   "encontrei o seu perfil enquanto mapeava os importadores de {product} em {country}",
        "search":     "encontrei a sua empresa enquanto pesquisava os importadores de {product} em {country}",
    },
    "ar": {
        "referral":   "أوصى بنا إليكم عميل يعرف سوق {country}",
        "trade_show": "التقينا في المعرض وسألتم عن سعر {product}",
        "customs":    "تُظهر شركتكم سجل استيراد ثابتاً في هذه الفئة",
        "linkedin":   "عثرت على ملفكم أثناء رسم خريطة مستوردي {product} في {country}",
        "search":     "وجدت شركتكم أثناء البحث عن مستوردي {product} في {country}",
    },
}

# 正文模板：与 BODY 的 T0/T1/T2 一一对应 —— 同一段落结构、同样的两个要点、
# 同一个 CTA、不报价、不带附件。占位符与英文版完全相同。
BODY_I18N = {
    "es": {
        "T0": """Subject: {subject}

{greeting}

{why_them}. Por eso le escribo directamente a usted y no a un buzón general.

Fabricamos {product} y enviamos a {country} con regularidad. Si este año están comprando, puedo confirmar por escrito desde ahora:
- Especificación: {product}, carga mixta en 40HQ aceptada
- Condiciones: FOB / CIF, cotización en 48 horas

¿Qué medidas y qué volumen mensual están manejando actualmente en {product}?

Saludos cordiales,
{sender}""",
        "T1": """Subject: {subject}

{greeting}

{why_them}. Solo una pregunta, y luego no le molestaré más.

Fabricamos {product} y abastecemos a otros compradores en {country}. Antes de incluir a {company} en la lista de llamadas de este trimestre: ¿siguen comprando {product} desde Asia?

Respóndame con un rango de medidas y le enviaré los números. Si me responde «ahora no», no volveré a escribirle.

Saludos cordiales,
{sender}""",
        "T2": """Subject: {subject}

{greeting}

Estoy actualizando mis notas sobre los importadores de {product} en {country}.

¿Sigue {company} comprando {product} desde Asia este año? Basta una palabra, y si la respuesta es no, les quitaré de la lista y dejaré de escribir.

Saludos cordiales,
{sender}""",
    },
    "pt": {
        "T0": """Subject: {subject}

{greeting}

{why_them}. Por isso escrevo diretamente para você, e não para um e-mail geral.

Fabricamos {product} e enviamos para {country} regularmente. Se estiverem comprando este ano, posso confirmar por escrito desde já:
- Especificação: {product}, carga mista em 40HQ aceita
- Condições: FOB / CIF, cotação em 48 horas

Quais medidas e qual volume mensal estão movimentando atualmente em {product}?

Atenciosamente,
{sender}""",
        "T1": """Subject: {subject}

{greeting}

{why_them}. Só uma pergunta, e depois não vou mais incomodar.

Fabricamos {product} e fornecemos a outros compradores em {country}. Antes de incluir a {company} na lista de contatos deste trimestre: {product} continua sendo algo que compram da Ásia?

Responda com uma faixa de medidas e voltarei com os números. Se responder «agora não», não escreverei novamente.

Atenciosamente,
{sender}""",
        "T2": """Subject: {subject}

{greeting}

Estou atualizando minhas anotações sobre os importadores de {product} em {country}.

A {company} continua comprando {product} da Ásia este ano? Basta uma palavra, e se for não, tiro vocês da lista e paro de escrever.

Atenciosamente,
{sender}""",
    },
    "ar": {
        "T0": """Subject: {subject}

{greeting}

{why_them}. لهذا السبب أكتب إليك مباشرة وليس إلى بريد عام.

نصنّع {product} ونشحن إلى {country} بانتظام. إذا كنتم تشترون هذا العام، يمكنني أن أؤكد كتابياً من الآن:
- المواصفات: {product}، مع قبول التحميل المختلط في حاوية 40HQ
- الشروط: FOB / CIF، وعرض السعر خلال 48 ساعة

ما المقاسات وحجم الطلب الشهري الذي تتعاملون به حالياً في {product}؟

مع أطيب التحيات،
{sender}""",
        "T1": """Subject: {subject}

{greeting}

{why_them}. سؤال واحد فقط، ثم لن أزعجك بعدها.

نصنّع {product} ونورّد لمشترين آخرين في {country}. قبل أن أضع {company} في قائمة الاتصال لهذا الربع: هل ما زلتم تشترون {product} من آسيا؟

أجب بنطاق مقاسات وسأعود إليك بالأرقام. وإذا أجبت «ليس الآن»، فلن أكتب مرة أخرى.

مع أطيب التحيات،
{sender}""",
        "T2": """Subject: {subject}

{greeting}

أحدّث ملاحظاتي حول مستوردي {product} في {country}.

هل ما زالت {company} تشتري {product} من آسيا هذا العام؟ تكفي كلمة واحدة، وإذا كانت الإجابة لا، فسأحذفكم من القائمة وأتوقف عن الكتابة.

مع أطيب التحيات،
{sender}""",
    },
}


# ---------------------------------------------------------------- 字段净化

_TAG_RE = re.compile(r"<[^<>]{0,200}>")
_WS_RE = re.compile(r"\s+")
_LEFT_PH_RE = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}")
_PRICE_RE = re.compile(
    r"(usd|eur|cny)\s?\d|[$¥€]\s?\d|\bprice\s?list\b|\b价格单\b|\b报价单\b|\b底价\b", re.I)

# 行业缩写本来就是大写，不算「吼叫」
ALLCAPS_ALLOW = {"TBR", "PCR", "OTR", "FOB", "CIF", "EXW", "DDP", "SASO", "SABER",
                 "RFQ", "MOQ", "ISO", "DOT", "ECE", "GCC", "HQ", "40HQ", "20GP",
                 "FCL", "LCL", "UAE", "TT", "LC", "OEM", "ODM"}

SPAM_WORDS = ["free", "cheap", "cheapest", "best price", "lowest price", "best offer",
              "discount", "save up", "guaranteed", "risk-free", "act now",
              "limited time", "limited offer", "urgent", "click here", "buy now",
              "order now", "dear friend", "make money", "100%"]

SUBJECT_LIMIT = 40      # 手机端主题行不截断
PREVIEW_LIMIT = 120     # 手机端 Gmail 预览截断线


def clip(s, limit):
    """掐长度，尽量断在词边界并补省略号（原来的 [:24] 会把词切一半）。"""
    if not limit or len(s) <= limit:
        return s
    cut = s[:limit]
    sp = cut.rfind(" ")
    if sp >= max(1, limit // 2):
        cut = cut[:sp]
    return cut.rstrip(" ,;-/、") + "…"


def one_line(value, limit=0):
    """字段入信前一律压成单行。

    公司名里带换行会直接把 Subject: 头折断；note 里带 <script>/<b> 会污染
    Markdown 输出。所以去标签、折叠所有空白、再掐长度。
    """
    s = "" if value is None else str(value)
    s = _TAG_RE.sub(" ", s)
    s = s.replace("<", "‹").replace(">", "›")
    s = _WS_RE.sub(" ", s).strip()
    return clip(s, limit)


def spam_scan(text):
    """扫描垃圾邮件特征：spam 触发词、ALL CAPS 吼叫、连发感叹号、货币符号堆砌。"""
    hits = []
    low = text.lower()
    for w in SPAM_WORDS:
        if w in low:
            hits.append("spam 触发词 '%s'" % w)
    caps = sorted({w for w in re.findall(r"\b[A-Z0-9]{4,}\b", text)
                   if any(c.isalpha() for c in w) and w not in ALLCAPS_ALLOW})
    if caps:
        hits.append("疑似吼叫大写: %s" % "/".join(caps[:3]))
    if text.count("!") > 1:
        hits.append("感叹号 %d 个" % text.count("!"))
    if text.count("$") >= 2:
        hits.append("货币符号 %d 个" % text.count("$"))
    return hits


def short_product(product, lang="en"):
    """产品串可能很长（'TBR 12.00R20, PCR tubes'），取第一个品类词给主题行用。
    lang 决定兜底词的语言，避免英文兜底串进中文主题。"""
    if not product:
        return "our products" if lang == "en" else "相关品类"
    # 不按 "/" 切：轮胎规格（PCR 195/65R15、TBR 315/80R22.5）里自带斜杠，切了就成了残规格
    first = re.split(r"[,;|、]| and ", product)[0].strip() or product.strip()
    return clip(first, 24)


def fit_subject(tier, prod_en, prod_zh, company, limit=SUBJECT_LIMIT):
    """挑第一条不超 limit 的主题行候选；全超就用最短那条，并回传 fits=False。"""
    cands = SUBJECT.get(tier) or [("{product}", "{product}")]
    chosen = None
    for en_t, zh_t in cands:
        if len(en_t.format(product=prod_en, company=company)) <= limit:
            chosen = (en_t, zh_t)
            break
    if chosen is None:
        chosen = cands[-1]
    return (chosen[0].format(product=prod_en, company=company),
            chosen[1].format(product=prod_zh, company=company),
            len(chosen[0].format(product=prod_en, company=company)) <= limit)


_ROLE_HINTS = ("manager", "director", "buyer", "procurement", "purchasing", "sourcing",
               "sales", "officer", "owner", "ceo", "founder", "team", "dept",
               "department", "admin", "info", "support", "export", "import",
               "总经理", "采购", "负责人", "经理", "销售", "主管", "团队", "客服", "外贸")


def greeting(contact):
    """返回 (英文招呼, 中文招呼)。

    「Hi purchasing manager,」是把职位当人名，「Hi there,」是群发味，两者都像
    垃圾邮件。命中职位词或没联系人时降级成不带名字的 Hello, / 您好，
    """
    c = one_line(contact, 48)
    low = c.lower()
    if (not c
            or low in ("there", "-", "--", "n/a", "na", "unknown", "none", "?", "??", "tbd")
            or any(h in low for h in _ROLE_HINTS)):
        return "Hello,", "您好，"
    return "Hi %s," % c, "%s，" % c


def cap_first(s):
    """句首大写。中文本来就没有大小写，命中也无副作用。"""
    return s[:1].upper() + s[1:] if s else s


def build_why_them(row, product):
    """返回 (英文 why them, 中文 why them, 是否退化为通用模板)。"""
    prod = product or _get(row, "product", "") or ""
    short_en = short_product(prod, "en")
    short_zh = short_product(prod, "zh")
    country_en = _get(row, "country", "") or "your market"
    country_zh = _get(row, "country", "") or "贵司所在市场"
    # 95 是留给预览首句的预算：note 会原样进第一句，太长会被 Gmail 截断
    note = one_line(_get(row, "note", ""), 95)
    # 优先用这一家真实的备注情报，拼一句只对它成立的话（杜绝模板套话）
    if note:
        return ("your note mentioned: %s" % note,
                "贵司备注提到：%s" % note, False)
    src = _get(row, "source", "search").strip().lower()
    en, zh = WHY_THEM.get(src, WHY_THEM["search"])
    # 第三位 True = note 为空，这句换成同行也成立，得报警催人去补背调
    return (en.format(product=short_en, country=country_en),
            zh.format(product=short_zh, country=country_zh), True)


def greeting_i18n(contact, lang):
    """返回该语言的招呼；命中职位词或没联系人时降级成不带名字的招呼。"""
    c = one_line(contact, 48)
    low = c.lower()
    bare = {"es": "Hola,", "pt": "Olá,", "ar": "مرحباً،"}
    if (not c
            or low in ("there", "-", "--", "n/a", "na", "unknown", "none", "?", "??", "tbd")
            or any(h in low for h in _ROLE_HINTS)):
        return bare[lang]
    if lang == "ar":
        return "مرحباً %s،" % c
    if lang == "es":
        return "Hola %s," % c
    return "Olá %s," % c


def build_why_them_i18n(row, product, lang):
    """返回该语言的 why them 单句（与 build_why_them 一一对应）。"""
    prod = product or _get(row, "product", "") or ""
    short = short_product(prod, "en")
    country = _get(row, "country", "") or "your market"
    note = one_line(_get(row, "note", ""), 95)
    if note:
        prefix = {"es": "su nota menciona: %s",
                  "pt": "sua nota menciona: %s",
                  "ar": "ذكرت ملاحظتك: %s"}[lang]
        return prefix % note
    src = _get(row, "source", "search").strip().lower()
    template = WHY_THEM_I18N[lang].get(src, WHY_THEM_I18N[lang]["search"])
    return template.format(product=short, country=country)


def fit_subject_i18n(tier, prod_en, company, lang, limit=SUBJECT_LIMIT):
    """挑第一条不超 limit 的该语言主题行候选；全超就用最短那条。"""
    cands = SUBJECT_I18N[lang].get(tier) or [("{product}")]
    chosen = None
    for cand in cands:
        if len(cand.format(product=prod_en, company=company)) <= limit:
            chosen = cand
            break
    if chosen is None:
        chosen = cands[-1]
    text = chosen.format(product=prod_en, company=company)
    return text, len(text) <= limit


def preview_line(body_text):
    """手机端 Gmail 预览截的是正文第一句（跳过主题行和招呼），不是整段。"""
    for ln in body_text.split("\n"):
        s = ln.strip()
        if not s or s.startswith(("Subject:", "主题：")):
            continue
        if s.startswith(("Hi ", "Hello", "您好", "Hola", "Olá", "مرحباً")):
            continue
        m = re.match(r".*?[.。!?！؟؟](?=\s|$)", s)
        return (m.group(0).strip() if m else s)
    return ""


def checklist(lang, en_text, zh_text, subject, sub_fits, email, sender, why_generic,
              measured, why_texts=()):
    """发送前自查：收件人/附件/签名档 + 长度/spam/价格/占位符的机器自检。

    measured 是当前语言下真正会显示/发出的那版正文，长度类检查以它为准。
    why_texts 是 why them 的原文：备注里写着 "{product}" 字样时，它是被引用
    的用户原文，不是模板漏填的占位符，要从残留里扣掉。
    """
    blob = en_text + "\n" + zh_text
    leftover = set(_LEFT_PH_RE.findall(blob))
    for wt in why_texts:
        leftover -= set(_LEFT_PH_RE.findall(wt or ""))
    leftover = sorted(leftover)
    hits = spam_scan(blob)
    price_hit = bool(_PRICE_RE.search(blob))
    preview = preview_line(measured)
    sig_missing = (not sender.strip()) or ("[Your Name]" in sender) or ("[Company]" in sender)
    sub_len = len(subject)

    def auto(ok):
        return ("✓" if ok else "✗ FIX") if lang == "en" else ("✓" if ok else "✗ 需改")

    if lang == "en":
        lines = ["Pre-send checklist:"]
        lines.append("  %s To: %s" % (
            auto(bool(email)),
            email or "NO EMAIL ON FILE — go fill it in before you send"))
        lines.append("  ☐ Attachments: spec sheet / one-pager (<=2 files, <3MB)")
        if sig_missing:
            lines.append("  %s Signature: still the placeholder '%s' — put your real "
                         "name, company, phone and WhatsApp in" % (auto(False), sender))
        else:
            lines.append("  %s Signature: %s" % (auto(True), sender))
        if why_generic:
            lines.append("  %s why them is generic (note column empty) — do NOT send yet, "
                         "run 03 back-check and write one fact only this company has"
                         % auto(False))
        else:
            lines.append("  %s why them is company-specific" % auto(True))
        lines.append("  %s Subject %d chars (<=%d or mobile truncates)"
                     % (auto(sub_fits), sub_len, SUBJECT_LIMIT))
        lines.append("  %s Preview line %d chars (<=%d or Gmail cuts it): \"%s\""
                     % (auto(len(preview) <= PREVIEW_LIMIT), len(preview), PREVIEW_LIMIT,
                        clip(preview, 60)))
        lines.append("  %s No price number / price list in the body" % auto(not price_hit))
        lines.append("  %s No leftover placeholder %s"
                     % (auto(not leftover), (" ".join(leftover) if leftover else "")))
        lines.append("  %s No spam trigger %s"
                     % (auto(not hits), ("; ".join(hits) if hits else "")))
        return lines

    lines = ["发送前自查:"]
    lines.append("  %s 收件人：%s" % (
        auto(bool(email)),
        email or "本条没邮箱 —— 先补邮箱，别用群发"))
    lines.append("  ☐ 附件：规格表/单页（≤2 个、<3MB），文件名别用中文，容易乱码")
    if sig_missing:
        lines.append("  %s 签名档：落款还是占位符「%s」—— 换成真实姓名/公司/电话/WhatsApp"
                     % (auto(False), sender))
    else:
        lines.append("  %s 签名档：%s" % (auto(True), sender))
    if why_generic:
        lines.append("  %s why them 已退化成通用模板（note 列为空）—— 先别发，"
                     "回去跑第 03 步背调，补一条只对这家成立的事实" % auto(False))
    else:
        lines.append("  %s why them 只对这家成立" % auto(True))
    lines.append("  %s 主题行 %d 字符（≤%d，超了手机端会截断）"
                 % (auto(sub_fits), sub_len, SUBJECT_LIMIT))
    lines.append("  %s 预览首句 %d 字符（≤%d，超了 Gmail 会截断）：「%s」"
                 % (auto(len(preview) <= PREVIEW_LIMIT), len(preview), PREVIEW_LIMIT,
                    clip(preview, 60)))
    lines.append("  %s 正文没有具体价格数字/价单" % auto(not price_hit))
    lines.append("  %s 无占位符残留 %s"
                 % (auto(not leftover), (" ".join(leftover) if leftover else "")))
    lines.append("  %s 无垃圾邮件特征 %s"
                 % (auto(not hits), ("；".join(hits) if hits else "")))
    return lines


def as_leads(result):
    """lead_score.analyze 的返回形态有两种：直接给 list，或 (list, 重复条数)。
    这里两种都兼容，免得上游一改签名本脚本就崩。"""
    if isinstance(result, tuple):
        return result[0]
    return result


def render(lead, sender, lang="both"):
    """按 lang 一次性拼好整块（both/en/zh），不再靠事后扫行切段。"""
    tier = lead["tier"]
    body = BODY.get(tier)
    if body is None:
        return None

    company = one_line(lead.get("company"), 60)
    country = one_line(lead.get("country"), 32)
    prod_en = short_product(lead.get("product"), "en")
    prod_zh = short_product(lead.get("product"), "zh")
    g_en, g_zh = greeting(lead.get("contact", ""))
    why_en, why_zh, why_generic = lead["why_them"]
    sub_en, sub_zh, sub_fits = fit_subject(tier, prod_en, prod_zh, company)
    email = one_line(lead.get("email", ""), 64)

    # why_them 是插在段首的，首字母必须大写，否则正文一开头就是小写
    en_text = body["en"].format(subject=sub_en, greeting=g_en, company=company,
                                product=prod_en, sender=sender,
                                country=country or "your market",
                                why_them=cap_first(why_en))
    zh_text = body["zh"].format(subject=sub_zh, greeting=g_zh, company=company,
                                product=prod_zh, sender=sender,
                                country=country or "贵司所在市场", why_them=why_zh)

    if lang in I18N_LANGS:
        why_loc = (lead.get("why_them_i18n") or {}).get(lang)
        if why_loc is None:
            why_loc = WHY_THEM_I18N[lang]["search"].format(
                product=prod_en, country=country or "your market")
        sub_loc, sub_loc_fits = fit_subject_i18n(tier, prod_en, company, lang)
        g_loc = greeting_i18n(lead.get("contact", ""), lang)
        loc_text = BODY_I18N[lang][tier].format(
            subject=sub_loc, greeting=g_loc, company=company,
            product=prod_en, sender=sender,
            country=country or "your market", why_them=cap_first(why_loc))

    out = ["=" * 70]
    if lang in ("en", "es", "pt", "ar"):
        out.append("%s | %s | %d pts" % (tier, TIER_LABEL_EN[tier], lead["score"]))
        out.append("Company: %s (%s)" % (company, country or "—"))
        out.append("Angle: %s" % TIER_ENVELOPE[tier][1])
    else:
        out.append("%s  |  %s  |  %d 分" % (tier, TIER_LABEL[tier], lead["score"]))
        out.append("公司: %s (%s)" % (company, country or "—"))
        out.append("写信策略: %s" % TIER_ENVELOPE[tier][0])
    out.append("-" * 70)

    if lang in I18N_LANGS:
        out.append("[%s — send this]" % LANG_LABEL[lang])
        out.append(loc_text)
        out.append("")
        out.append("[EN — English original, for approval]")
        out.append(en_text)
        out.append("")
        # 自查清单走英文（John 按英文审批）；长度类检查以真正会发的那版为准
        out.extend(checklist("en", loc_text, en_text, sub_loc, sub_loc_fits,
                             email, sender, why_generic, loc_text,
                             why_texts=(why_loc, why_en)))
    else:
        if lang in ("both", "en"):
            out.append("[EN — send this]")
            out.append(en_text)
            out.append("")
        if lang in ("both", "zh"):
            out.append("[ZH — 中文对照，仅供你审批，客户不收]")
            out.append(zh_text)
            out.append("")

        # 单语模式以当前显示的那一版为准（both 时以真正会发出去的 EN 为准）
        measured = zh_text if lang == "zh" else en_text
        out.extend(checklist(lang, en_text, zh_text, sub_en, sub_fits,
                             email, sender, why_generic, measured,
                             why_texts=(why_en, why_zh)))
    out.append("")
    return "\n".join(out)




def main():
    p = _ZhArgumentParser(
        prog="outreach_gen.py",
        description="按线索分级生成中英对照建联消息（只用标准库）",
        epilog="可直接复制的例子:\n"
               "  python scripts/outreach_gen.py examples/leads_example.csv --tier T0 --lang es\n"
               "  python scripts/outreach_gen.py examples/leads_example.csv --tier T1 --lang pt --out drafts_pt.md\n"
               "  python scripts/outreach_gen.py examples/leads_example.csv --tier T2 --lang ar\n"
               "  python scripts/outreach_gen.py --company 'Acme Ltd' --country Nigeria "
               "--contact Adaeze --product 'LED flood lights' --tier T1\n"
               "    (no CSV: one-off draft for a single lead; --tier is the tier to write for)")
    p.add_argument("csv_path", nargs="?", default=None,
                   help="线索 CSV 路径；不填时用 --company 单条生成")
    p.add_argument("--company", default="",
                   help="单条模式：只给这一家公司写文案（不用 CSV）")
    p.add_argument("--country", default="", help="单条模式：国家")
    p.add_argument("--contact", default="", help="单条模式：联系人姓名")
    p.add_argument("--product", default="", help="单条模式：产品")
    p.add_argument("--tier", choices=["T0", "T1", "T2", "T3", "all"], default="T0")
    p.add_argument("--sender", default="[Your Name] | [Company]",
                   help="落款，默认留占位符")
    p.add_argument("--lang", choices=["both", "en", "zh", "es", "pt", "ar"],
                   default="both",
                   help="输出语言：both（中英对照，默认）/ en / zh / es（西语）/ pt（葡语）/"
                        "ar（阿语）；es/pt/ar 每条后附英文原文供审批")
    p.add_argument("--out", help="输出到 .md 文件，不填则打印到屏幕")
    args = p.parse_args()
    log = setup_log("outreach_gen")
    started = time.monotonic()

    if args.csv_path:
        trace_input = os.path.basename(args.csv_path)
        try:
            rows = read_leads(args.csv_path)
        except LeadDataError as e:
            log.info("RESULT error=%s", e)
            write_trace("outreach_gen.py", trace_input, "",
                        time.monotonic() - started, str(e))
            raise SystemExit("错误：%s" % e)
        except FileNotFoundError:
            log.info("RESULT error=file_not_found file=%s", args.csv_path)
            write_trace("outreach_gen.py", trace_input, "",
                        time.monotonic() - started,
                        "找不到文件 %s" % args.csv_path)
            raise SystemExit("错误：找不到文件 %s" % args.csv_path)
        source_label = args.csv_path
        single = False
    else:
        # 单条模式（本地版旧用法）：不用 CSV，只给一家公司写文案，
        # --tier 就是要写的分级（不按打分结果定）。
        trace_input = "单条模式（--company）"
        if not (args.company or "").strip():
            write_trace("outreach_gen.py", "（未给 CSV 也未给 --company）", "",
                        time.monotonic() - started,
                        "请给一个线索 CSV 路径，或用 --company 单条生成")
            raise SystemExit("错误：请给一个线索 CSV 路径，或用 --company/--country/"
                             "--contact/--product 单条生成一条文案。")
        rows = [{"company": args.company.strip(),
                 "country": (args.country or "").strip(),
                 "product": (args.product or "").strip(),
                 "contact": (args.contact or "").strip(),
                 "email": "", "phone": "", "years": "",
                 "source": "", "note": ""}]
        source_label = "单条：%s（--company，不读 CSV）" % args.company.strip()
        single = True

    leads = as_leads(analyze(rows))
    if single and args.tier != "all":
        for lead in leads:
            lead["tier"] = args.tier
    # 回配原始行：按 (公司/国家/产品/邮箱) 分桶逐个取用，
    # 同名公司不会互相串数据（旧实现按公司名匹配，第二条同名线索会拿到第一条的备注）
    exact, by_company = {}, {}
    for row in rows:
        key = (_get(row, "company", "").strip().lower(),
               _get(row, "country", "").strip().lower(),
               _get(row, "product", "").strip().lower(),
               _get(row, "email", "").strip().lower())
        exact.setdefault(key, []).append(row)
        by_company.setdefault(key[0], []).append(row)

    used, unmatched = set(), 0
    for lead in leads:
        key = (str(lead.get("company", "")).strip().lower(),
               str(lead.get("country", "")).strip().lower(),
               str(lead.get("product", "")).strip().lower(),
               str(lead.get("email", "")).strip().lower())
        raw = None
        for cand in (exact.get(key) or by_company.get(key[0]) or []):
            if id(cand) not in used:
                raw = cand
                break
        if raw is None:
            unmatched += 1
            lead["contact"] = ""
            lead["why_them"] = build_why_them({}, lead.get("product", ""))
        else:
            used.add(id(raw))
            lead["contact"] = _get(raw, "contact", "")
            lead["why_them"] = build_why_them(raw, lead.get("product", ""))
        lead["why_them_i18n"] = {
            lg: build_why_them_i18n(raw if raw is not None else {},
                                    lead.get("product", ""), lg)
            for lg in I18N_LANGS}

    if args.tier == "all":
        targets = [t for t in ("T0", "T1", "T2", "T3")
                   if any(l["tier"] == t for l in leads)]
    else:
        targets = [args.tier]

    blocks, drafts = [], 0
    for t in targets:
        picked = 0
        for lead in leads:
            if lead["tier"] != t:
                continue
            text = render(lead, args.sender, args.lang)
            if text is None:
                continue
            blocks.append(text)
            picked += 1
        drafts += picked
        if picked == 0:
            count = sum(1 for l in leads if l["tier"] == t)
            if count > 0:
                if args.lang in ("en", "es", "pt", "ar"):
                    blocks.append("[%s] %d leads found — no first-touch copy needed. "
                                  "Fill the contact / need gaps first." % (t, count))
                else:
                    blocks.append("[%s] 存在 %d 条 %s 线索，但无需写首触文案，先补齐信息。"
                                  % (t, count, t))
            else:
                blocks.append(("[%s] no leads at this tier." % t)
                              if args.lang in ("en", "es", "pt", "ar")
                              else ("[%s] 本级无线索。" % t))

    log.info("RESULT drafts=%d tier=%s lang=%s", drafts, args.tier, args.lang)
    write_trace("outreach_gen.py", trace_input,
                "%d 份草稿 · tier=%s lang=%s" % (drafts, args.tier, args.lang),
                time.monotonic() - started)

    if args.lang in I18N_LANGS:
        header = (
            "# Outreach drafts (%s + English reference)\n\n"
            "- Generated from: `%s`\n"
            "- Tiers: %s\n"
            "- Signature: %s\n"
            "- ⚠️ Every draft ends with a checklist; clear the ✗ items before you send.\n"
            "- Every %s draft is followed by its English original — approve against the English.\n\n"
            % (LANG_LABEL[args.lang], source_label, ", ".join(targets), args.sender,
               LANG_LABEL[args.lang])
        )
        footer = ("\n" + "-" * 70 + "\n"
                  "Generated %d draft(s). T3 needs no copy — fill the gaps first.\n" % drafts)
        if unmatched:
            footer += ("⚠️ %d lead(s) could not be matched back to a CSV row; their "
                       "why-them line fell back to a generic template.\n" % unmatched)
    elif args.lang == "en":
        header = (
            "# Outreach drafts\n\n"
            "- Generated from: `%s`\n"
            "- Tiers: %s\n"
            "- Signature: %s\n"
            "- ⚠️ Every draft ends with a checklist; clear the ✗ items before you send.\n\n"
            % (source_label, ", ".join(targets), args.sender)
        )
        footer = ("\n" + "-" * 70 + "\n"
                  "Generated %d draft(s). T3 needs no copy — fill the gaps first.\n" % drafts)
        if unmatched:
            footer += ("⚠️ %d lead(s) could not be matched back to a CSV row; their "
                       "why-them line fell back to a generic template.\n" % unmatched)
    else:
        header = (
            "# 建联文案草稿\n\n"
            "- 生成自: `%s`\n"
            "- 分级: %s\n"
            "- 落款: %s\n"
            "- ⚠️ 每封末尾都有自查清单，先把 ✗ 项清掉再发。\n\n"
            % (source_label, ", ".join(targets), args.sender)
        )
        footer = ("\n" + "-" * 70 + "\n"
                  "共生成 %d 份草稿。T3 不用写文案——先把信息补齐，别对着空白客户写小作文。\n" % drafts)
        if unmatched:
            footer += ("⚠️ 有 %d 条线索回配不到 CSV 原始行，why them 已退化为通用模板，"
                       "发前务必人工重写。\n" % unmatched)

    body = header + "\n".join(blocks) + footer

    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(body)
        except OSError as e:
            write_trace("outreach_gen.py", trace_input, "",
                        time.monotonic() - started,
                        "写不进「%s」：%s" % (args.out, e.strerror or e))
            raise SystemExit("错误：写不进「%s」：%s（换个目录，或先关掉打开它的 Excel）"
                             % (args.out, e.strerror or e))
        print("已写入 %s（%d 份草稿）" % (args.out, drafts))
    else:
        print(body)


if __name__ == "__main__":
    main()
