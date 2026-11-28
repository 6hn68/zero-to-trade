# 04 · Outreach

> English version of [04-outreach.md](04-outreach.md). Translated from the Chinese original; figures, dates, commands and file names match the original exactly.

> What this step has to do: make one proper first contact, and hand over a 3-touch follow-up plan with dates and a stop-loss line — moving the list from "said hello" to "someone is answering".
> One sentence to get straight first: the goal of first contact is not a deal, it is getting a second sentence of conversation. One outreach email that gets a reply is worth twenty that vanished into the void unread.

## 1. Why this step goes wrong most easily

Between due diligence and closing, this stretch collapses most easily.

It always collapses the same way: you send emails into silence, occasionally get a "send more details", and then the person is gone again. You start doubting yourself — is the product wrong? The price wrong? Or is it me? Do not rush to blame yourself.

There are two layers to the truth, in this order:

1. **Layer one: the email never arrived.** The most common beginner failure is not bad copy — it is an unconfigured domain, a spam verdict, or a first email carrying an attachment straight into the spam folder. You are waiting for a reply that will never come, thinking your wording is the problem. Until this layer is fixed, any copy rewrite is wasted effort (see Step 2).
2. **Layer two: it arrived, but you never followed up.** Whether the first email gets a reply varies wildly — product category, country, list quality and send time can all swing the result, and **no percentage can be copied directly**. Do not believe talk of "reply rate X%" — **run 100 emails yourself and measure once** (the method is in Step 6). But one thing is certain: conversations mostly do not die on the first email; they die because there was no second or third email after it.

An overseas buyer receives a pile of cold emails every day. They probably will not read the first one carefully, and will not reply to the first one. But when your second and third emails are still coming, each carrying something new, they will reply.

So what you hand in at this step is not "how many emails I sent" — it is "**did the emails actually arrive** + did each one get followed up".

## 2. Step by step

**Step 1: Grade T0–T3 (deciding how much time to invest)**

| Tier | Definition | Investment | First-touch method |
|---|---|---|---|
| **T0** | Decision maker confirmed, need clear, purchasing timeline exists | Highest, fully customized one-to-one | Email + LinkedIn + WhatsApp, all three on the same day |
| **T1** | Probable purchaser / owner, need to be confirmed | Medium, template + personalized opening | Email + LinkedIn, two channels |
| **T2** | Contact person not certain enough, or need unclear | Low, lightweight template | Email only |
| **T3** | Nurture long-term, no selling for now | Minimal | Content / community only, no active selling |

**Rating bridge: A/B/C from 02/03 → T0–T3 in 04 (the only mapping definition for this stage)**

Due diligence graded every lead A/B/C; the outreach stage uses T0–T3 to decide investment. The mapping is as follows — do not invent your own:

| Due diligence rating | Outreach tier | Investment and approach |
|---|---|---|
| **A** | **T0** | Decision maker confirmed, need clear → three channels on the same day, highest investment, first touch within 48h |
| **B** | **T1–T2** | Product category matches but purchasing evidence is weak → two channels (email + LinkedIn) or one channel (email), move within the week |
| **C** | **T3** | Any L1 item failed or information incomplete → nurture only, low-frequency content, no active selling |

> Note: A is not automatically all T0, and B is not automatically all T1 — it also depends on "is the decision maker confirmed, is the need clear"; but C never enters the active outreach sequence.

T0 is your lifeline. T0s are usually only a small share of the list (the share depends on how strictly you filtered in [02-find-leads_en.md](02-find-leads_en.md) and [03-due-diligence.md](03-due-diligence_en.md); there is no universal number), but that tier is worth the most of your time.

**Email first-touch timing**: T0 defaults to email + LinkedIn + WhatsApp **all three on the same day** (email is the main battlefield). If the target market carries a high risk of emails landing in spam, **the email may be deferred to D1**, but it must sit inside the same follow-up plan (counted from the same `--start` day) — do not start a separate plan.

**Step 2: Confirm the email can arrive first (deliverability self-check) — skip this and everything after it is wasted**

The root of most "nobody replies to my outreach" cases is not the copy — it is that the email never reached the inbox. Run through these five items; fix whichever one fails before talking about copy.

**2.1 Use your own domain email — do not mass-send from a free mailbox**

Outreach must come from your own domain's email (`your name@your company domain.com`). Do not mass-send from free mailboxes like Gmail, 163 Mail or QQ Mail. Two reasons: free mailboxes have been used for mass sending so many times that receiving servers treat them with extra suspicion; and a free-mailbox address looks like an individual to a buyer, not a company.

**2.2 Set up all three DNS records: SPF / DKIM / DMARC**

These three are how the receiving side judges "was this email really sent from your domain". You can set them up in your domain provider or business email backend — usually no code needed:

| Record | What it does | What happens without it |
|---|---|---|
| **SPF** | Declares which servers are allowed to send mail as your domain | The receiver cannot confirm the sender — mail is judged spam or rejected outright |
| **DKIM** | Adds a digital signature to the email; if the email is altered in transit the signature breaks | The email's integrity cannot be verified, so its score drops |
| **DMARC** | Tells the receiver what to do with mail that fails verification, and sends you reports | Someone else can send mail impersonating your domain (impersonation is a real fraud risk in exporting) |

Do not assume it works once configured — verify it: check your domain records with a public SPF / DKIM testing tool, or send a test email to your own mailboxes on different providers (Gmail, Outlook, local business mail) and read the verification results in the email headers.

**2.3 A new domain needs warming up — do not send volume on day one**

A freshly registered, freshly configured domain is a blank sheet to receivers — no reputation record at all. The safe way:

- Use it for a few weeks of **normal back-and-forth mail** first (with colleagues, with existing customers), so the domain builds normal sending and receiving behavior;
- Start outreach small and **increase day by day** (e.g. single digits → a dozen or so → dozens). Do not jump to hundreds on day one;
- Watch bounces and inbox placement. The moment batches start landing in spam, cut the volume immediately and investigate the content;
- There is no universal standard for "how many per day is safe" (it depends on domain age, receiver, content). **Find it out with your own seed list** — do not copy someone else's number.

**2.4 The first email carries no attachment and no link**

Attachments are a strong signal to spam filters, and a common interception target for the other company's IT gateway; several links in the first email drag the score down the same way. The first-touch copy generated by the project script `scripts/outreach_gen.py` is plain text with no attachments and no links at all — send it in that form.

Spec sheets, catalogs and quotation sheets get sent **after they reply** (which conveniently becomes the "new information" in your second email).

**2.5 Avoid spam triggers and sending rhythm**

- Content: all-caps words, several exclamation marks in a row, stacked words like `free` / `cheapest` / `100% guaranteed` / `best price` / `urgent`, whole paragraphs in big red type, flashy HTML templates, a body that is one image instead of text. **First touch is always plain text.**
- Rhythm: do not mass-send hundreds of emails in one minute. Spread them across time slots, randomize the gaps, and send during the other side's local working morning. Whole batches on the hour, hundreds in the same second, is machine behavior by definition.
- List: **hard bounces (address does not exist) must be deleted from the list immediately**. Once the bounce rate climbs, domain reputation drops faster than anything else. Using emails verified in [03-due-diligence.md](03-due-diligence_en.md) keeps bounces far lower.
- Self-test: prepare a **seed list** (your own test mailboxes across 3–5 different email providers). Every time you change the template, send it to yourself first to see inbox vs. spam, then send it out.

**Step 3: Three channels in parallel for first touch (same customer, same day)**

- **Email**: formal, forwardable to colleagues, leaves a written record. This is the main battlefield.
- **LinkedIn**: find the person, add them or send InMail. Its job is to **raise your credibility with them** — when they open your profile they can see who you are and what you do.
- **Instant messaging** (crucial in the Middle East, Southeast Asia and Africa): WhatsApp, WeChat, LinkedIn direct messages. **Before sending the first message, check whether they have a company WhatsApp Business account** — do not call a personal number at random.

The division of labor across the three channels must be explicit:
- Email = explain the value clearly and give a reason to reply
- LinkedIn = build a sense of identity, so they remember who you are
- WhatsApp = create the feeling that "someone is following up", especially in markets where WhatsApp is the main channel

One counter-intuitive point: in some markets, WhatsApp first and email second actually works better — they have already seen you once on the light channel, so by the time the email arrives you are no longer a stranger.

**Step 4: Write the first email (fixed structure — do not rethink it every time)**

**Fix the subject line first** (it decides whether they open it, and matters more than the body)

- Short, specific, reading like a work email rather than an ad. Target **under 40 characters** — the pre-send checklist in `scripts/outreach_gen.py` enforces exactly this; over the limit, shorten it.
- Include their company name or a specific product category, in the shape the script generates: `TBR 12.00R20 supply — [Example] Gulf Tire Trading`.
- Do not write empty words like `Cooperation` / `Best price` / `Hello`; no all-caps, no exclamation marks, no fake `Re:` pretending it is a reply (it gets spotted the first time, and it is deceptive).
- The subject line only promises what the body actually contains.

**Body: five parts, 130–170 words**

1. **The first sentence must be about them, not about you.** A buyer reads the first sentence to judge "is this email relevant to me". Opening with "I am XX from XX company" makes them read one line of advertising before deciding whether to continue. Put "why them" first: `I noticed... (one specific thing about their company)`, then bring in who you are in half a sentence.
2. **Half a sentence of identity**: who you are, what you make, which market you supply. One sentence, no founding year, factory area or certificate list.
3. **One concrete, small, verifiable value**: not "we are a professional manufacturer", but "we make 12.00R20 and 315/80R22.5 in full tread patterns, and the packaging is labeled in English + Arabic the way Middle East customers expect", or "we put together a list of the main TBR import specs for your country — I can send it for reference".
4. **One concrete question that is easy to answer**: something answerable in one sentence. "Which channel do you run TBR through — fleets or wholesale?" is ten times better than "are you interested in cooperating".
5. **One clear next step (one CTA per email)**: "either/or" means two forms of the same action — "shall I send you the spec sheet, or will you give me the sizes directly?" Both options point at "I send you material", so it is still one CTA. But "shall I send a quote / shall we book a call / shall I add you on WhatsApp" is three actions, and the result is zero replies.

**What the signature should carry**: name + company + one phrase of role. That is it. The script's `--sender` default is the one-line form `[Your Name] | [Company]` (override it with e.g. `--sender "Li | [Example] Far East Tire | Export"`). Do not stack a string of phones, three emails, a website link, WhatsApp, a company slogan and a banner image in the first email — links and images lower the spam score and turn a 150-word email into a 400-word ad. Full contact details come after they reply.

**Three things the first email never carries**: no attachment, no link, no price. The reasons for the first two are in Step 2; why the price cannot be given yet is in [05-negotiation.md](05-negotiation_en.md) and [06-quote.md](06-quote_en.md). No company brochure.

> **A known conflict with the script (handle it as follows)**: the T0 / T1 templates in `scripts/outreach_gen.py` contain `price list` and FOB/CIF terms, while the same script's self-check list says "does the body contain a price? No = correct" — the script contradicts itself. **This project follows "no price in the first email"**: after the script generates a draft, manually delete the price-list sentence and replace it with specs or container loading quantities. This conflict is already recorded; the script will be fixed later.

**Step 5: The first sentence on each channel (each channel has its own rules)**

Beyond email there are four more entry points. Their **first sentences are not abbreviated versions of the email** — each has its own rules.

**LinkedIn connection request (the note has a character limit — 2 sentences is enough)**

```
Hi {Name} — I supply {product} to buyers in {country}. Saw you handle {their product category / brand}.
Would like to connect and follow what you're doing there.

中文对照：{Name} 你好，我给 {country} 的买家供 {product}，看到贵司在做 {品类/品牌}。想加个好友，跟进一下你们那边的动向。
```
Key point: **do not sell in the connection request**. Your only goal is to get accepted; only after acceptance do you earn the right to send a message. If there is nothing quotable in their profile, better not to send it at all.

**LinkedIn first message (send it after they accept, ≤ 50 words)**

```
Thanks for connecting, {Name}. Quick context: we make {product} and currently ship to
{country}. Not pitching — I'd like to know whether you source {product} from Asia this year.
One word is enough.

中文对照：谢谢通过。简单说下背景：我们做 {product}，目前在供 {country}。不是推销——想确认贵司今年是否从亚洲采购 {product}，回一个词就行。
```

**WhatsApp first message (≤ 25 words — they read it on a phone, and they may be busy)**

```
Hi {Name}, {Your Name} from {Company} ({product}). Saw you import from Asia —
OK if I send the size list? One line is enough.

中文对照：{Name} 你好，我是 {Company} 的 {Your Name}，做 {product}。看到贵司从亚洲进货——发份规格表给你行吗？回一句就行。
```
Key point: before sending, confirm whether they use a **company business number** or a personal number (do not call a personal number at random); do not send a second message in a row; no voice messages; no links; do not send it in the middle of their night; if they reply "thanks", stop there and move the substantive sentence to the next round.

**Phone (the first 20 seconds of a cold call)**

```
Hello, may I speak to {Name}?
… Hi {Name}, {Your Name} calling from {Company}. We supply {product} to {country}.
I'm calling because {one sentence of why them}.
Is now a bad time for two minutes?

中文对照：你好，请找 {Name}。…… {Name} 你好，我是 {Company} 的 {Your Name}，我们给 {country} 供 {product}。打这个电话是因为 {为什么是他}。现在方便讲两分钟吗？
```
Key point: confirm you have the right person first, then introduce yourself, then give the reason, and finally **ask whether it is a good time first**. If they say it is not a good time, book a time — that is the only courtesy a cold call has, and the only way you get a second chance. If you are explicitly refused once, do not call again that day.

**Website contact form — lowest priority**

Forms usually land in `info@`, handled by marketing or by nobody, and the reply rate is far lower than reaching the right person. Use it only when **you cannot find any contact person at all**:

```
Subject: For the purchasing team — {product} supply enquiry

Please forward this to whoever handles {product} sourcing.
We manufacture {product} and supply {country}. {one sentence of why them}.
If you already have a supplier for this, a one-word reply is enough and I'll stop here.

中文对照：请转给负责 {product} 采购的同事。我们生产 {product} 并供应 {country}。{为什么是他}。如已有供应商，回一个词即可，我不再打扰。
```
Key point: the first sentence must say clearly **which department / person** you are looking for (otherwise the email dies inside info@); keep the word count inside the form's limit; do not paste a long company introduction.

**The one iron rule across all four channels**: the four channels talk about the same thing, the same persona and the same ask — but **the copy must not be the same paragraph**. A buyer who sees four identical messages in four channels on the same day will draw exactly one conclusion: mass sending. Consistency checking is in Prompt 3.

**Step 5 (appendix): Multilingual outreach (V13)**

English can be sent, but that does not mean the other side likes reading it. Latin American customers read Spanish, Brazilians read Portuguese, Gulf customers read Arabic — the same email in the local language gets replies at a higher rate. The script's `--lang es/pt/ar` produces the body in that language, **with the English original after every item** — you approve against the English, and the customer only receives the local-language version.

```bash
python scripts/outreach_gen.py my_leads.csv --tier T0 --lang es # Spanish + English对照
python scripts/outreach_gen.py my_leads.csv --tier T1 --lang pt --out drafts_pt.md # Portuguese, saved to a file
python scripts/outreach_gen.py my_leads.csv --tier T2 --lang ar # Arabic + English对照
```

The rules are exactly the same as the English version, only the language changes:

- The templates correspond one-to-one with the English T0/T1/T2 (same paragraph structure, same two key points, same CTA, no price, no attachment); the templates live only in one embedded dictionary inside `scripts/outreach_gen.py` — `prompts/` holds no separate copy.
- An illegal `--lang` value (e.g. `fr`) raises an argparse error directly and does not run wild; a missing CSV file raises a human-readable error (see the real examples in the script's `--help`).
- The self-check list runs in English, and length checks use the version that will actually be sent (Spanish / Portuguese / Arabic); the subject line is still capped at 40 characters, and if it is over the limit it automatically falls back to a shorter wording.
- Before sending, run the Step 2 deliverability self-check as usual — the language changed, the spam-folder rules did not.

Three real outputs (measured 2026-11-07, `examples/leads_example.csv`, pasted verbatim):

**Spanish T0 ([Example] Gulf Tire Trading):**

```text
======================================================================
T0 | Reach out now (multi-channel) | 95 pts
Company: 海湾轮胎贸易 (Saudi Arabia)
Angle: Name it specifically — the first line must reference something they said or did
----------------------------------------------------------------------
[Español — send this]
Subject: TBR 12.00R20 — suministro — 海湾轮胎贸易

Hola,

Su nota menciona: Annual RFQ for truck tyres, looking for supplier, 40HQ container regular. Por eso le escribo directamente a usted y no a un buzón general.

Fabricamos TBR 12.00R20 y enviamos a Saudi Arabia con regularidad. Si este año están comprando, puedo confirmar por escrito desde ahora:
- Especificación: TBR 12.00R20, carga mixta en 40HQ aceptada
- Condiciones: FOB / CIF, cotización en 48 horas

¿Qué medidas y qué volumen mensual están manejando actualmente en TBR 12.00R20?

Saludos cordiales,
[Your Name] | [Company]

[EN — English original, for approval]
Subject: TBR 12.00R20 supply — 海湾轮胎贸易

Hello,

Your note mentioned: Annual RFQ for truck tyres, looking for supplier, 40HQ container regular. That is why I am writing to you rather than to a general inbox.

We make TBR 12.00R20 and ship to Saudi Arabia on a regular basis. If you are sourcing this year, here are two things I can put in writing now:
- Specification: TBR 12.00R20, mixed loading on 40HQ accepted
- Terms: FOB / CIF both workable, quote turned around within 48 hours

What sizes and monthly volume are you running on TBR 12.00R20 at the moment?

Best regards,
[Your Name] | [Company]

Pre-send checklist:
✓ To: demo01@sample.example
☐ Attachments: spec sheet / one-pager (<=2 files, <3MB)
✗ FIX Signature: still the placeholder '[Your Name] | [Company]' — put your real name, company, phone and WhatsApp in
✓ why them is company-specific
✓ Subject 38 chars (<=40 or mobile truncates)
✓ Preview line 91 chars (<=120 or Gmail cuts it): "Su nota menciona: Annual RFQ for truck tyres, looking for…"
✓ No price number / price list in the body
✓ No leftover placeholder
✗ FIX No spam trigger 疑似吼叫大写: 00R20
```

**Portuguese T1 ([Example] Oman Blue Sea):**

```text
======================================================================
T1 | First touch this week | 77 pts
Company: 阿曼蓝海 (Oman)
Angle: Low-friction — give them an easy reason to reply
----------------------------------------------------------------------
[Português — send this]
Subject: TBR 12.00R20 — uma pergunta rápida

Olá,

Sua nota menciona: Tender invitation issued by Oman municipality. Só uma pergunta, e depois não vou mais incomodar.

Fabricamos TBR 12.00R20 e fornecemos a outros compradores em Oman. Antes de incluir a 阿曼蓝海 na lista de contatos deste trimestre: TBR 12.00R20 continua sendo algo que compram da Ásia?

Responda com uma faixa de medidas e voltarei com os números. Se responder «agora não», não escreverei novamente.

Atenciosamente,
[Your Name] | [Company]

[EN — English original, for approval]
Subject: TBR 12.00R20 — one quick question

Hello,

Your note mentioned: Tender invitation issued by Oman municipality. One question, and then I will leave you alone.

We make TBR 12.00R20 and supply other buyers in Oman. Before I put 阿曼蓝海 on this quarter's call list — is TBR 12.00R20 still something you source from Asia?

Reply with a size range and I will come back with numbers. Reply "not now" and I will not write again.

Best regards,
[Your Name] | [Company]

Pre-send checklist:
✓ To: sales@sample.example
☐ Attachments: spec sheet / one-pager (<=2 files, <3MB)
✗ FIX Signature: still the placeholder '[Your Name] | [Company]' — put your real name, company, phone and WhatsApp in
✓ why them is company-specific
✓ Subject 34 chars (<=40 or mobile truncates)
✓ Preview line 65 chars (<=120 or Gmail cuts it): "Sua nota menciona: Tender invitation issued by Oman…"
✓ No price number / price list in the body
✓ No leftover placeholder
✗ FIX No spam trigger 疑似吼叫大写: 00R20
```

**Arabic T2 ([Example] Nigeria Pioneer):**

```text
======================================================================
T2 | Low-frequency nurture | 50 pts
Company: 尼日利亚先锋 (Nigeria)
Angle: Lightest touch — just confirm facts, do not ask for a reply
----------------------------------------------------------------------
[العربية — send this]
Subject: 尼日利亚先锋 — التحقق من مشتريات PCR tubes

مرحباً،

أحدّث ملاحظاتي حول مستوردي PCR tubes في Nigeria.

هل ما زالت 尼日利亚先锋 تشتري PCR tubes من آسيا هذا العام؟ تكفي كلمة واحدة، وإذا كانت الإجابة لا، فسأحذفكم من القائمة وأتوقف عن الكتابة.

مع أطيب التحيات،
[Your Name] | [Company]

[EN — English original, for approval]
Subject: 尼日利亚先锋 — PCR tubes sourcing check

Hello,

I am updating my notes on Nigeria importers of PCR tubes.

Is 尼日利亚先锋 still sourcing PCR tubes from Asia this year? One word is enough, and if it is no I will take you off the list and stop writing.

Best regards,
[Your Name] | [Company]

Pre-send checklist:
✗ FIX To: NO EMAIL ON FILE — go fill it in before you send
☐ Attachments: spec sheet / one-pager (<=2 files, <3MB)
✗ FIX Signature: still the placeholder '[Your Name] | [Company]' — put your real name, company, phone and WhatsApp in
✓ why them is company-specific
✓ Subject 40 chars (<=40 or mobile truncates)
✓ Preview line 48 chars (<=120 or Gmail cuts it): "أحدّث ملاحظاتي حول مستوردي PCR tubes في Nigeria."
✓ No price number / price list in the body
✓ No leftover placeholder
✓ No spam trigger
```

**Step 6: Run an A/B test (split the list — do not send three versions to the same person)**

Write one version per angle for the same batch of leads:
- Version A: specs / product angle (emphasize which sizes you can make)
- Version B: cost angle (emphasize container efficiency and mixed loading; no floor price mentioned)
- Version C: market angle (emphasize a change you see in their market)

**How to test it properly:**

- **Split by list, not by person.** Randomly split the leads in the same tier into two groups — group A gets version A, group B gets version B — with everything else (send time, signature, follow-up rhythm) exactly the same. **Do not send three different-angle versions to the same customer in a row** — once they receive all three, they can see at a glance it is mass sending, the three emails contradict each other, and credibility drops to zero. Variants are a **list-level** dimension (this group gets A, that group gets B), not a **same-person** dimension.
- **Change only one variable at a time.** Change only the "why them" sentence, or only the value point offered — nothing else. Change two things at once and you will never know which one worked.
- **The sample must be big enough.** A dozen or so emails per version is basically noise. **Target 50–100 emails per version** before drawing a conclusion; before reaching that volume, do not declare A the winner because "A got two replies today".
- **Measure only one metric: did you get a reply.** At this stage do not measure clicks, quotations or deals.
- **Self-test method (a substitute for any ready-made percentage)**: send 100 emails → record how many replied, which version they replied to, and on which touch they replied → change one variable and run another 100 → compare the two rounds. That is your own baseline, and it is the only number that is valid for you.

**Step 7: Schedule the 3-touch follow-up plan (into the calendar, not into your head)**

The project script `scripts/followup_plan.py` runs at this real rhythm: **3 touches per tier, then stop**. There is no endless D7/D14/D30 sequence — `T2`'s D14 is "archive", the 3rd touch, not a fourth follow-up. The documentation follows the script:

| Tier | D0 first touch | Second touch | Third touch | Stop rule (script's definition) |
|---|---|---|---|---|
| **T0** <br>D0/D2/D5 | First-touch email: direct + one sentence that only holds for them | **D2** switch channel (same ask moved to WhatsApp / LinkedIn, same subject), with a container-loading reference | **D5** give them an out — "I'll leave this here, reach out any time" — with one piece of industry information | Explicit refusal on D0 → stop immediately; still no response after the 3rd touch (including read-but-unanswered) → **stop unconditionally**, move to the long list, sweep once a quarter |
| **T1** <br>D0/D3/D6 | First-touch email: light, specific, one easy reason to respond, with one concrete number | **D3** switch channel (LinkedIn / WhatsApp, do not repeat the full text), with a container-loading reference | **D6** ask an either/or like "is now not the right time?" | Same as above; after the 3rd touch with no response → stop unconditionally, move to the long list, sweep once a quarter (after stopping, this tier drops into the low-frequency pool) |
| **T2** <br>D0/D7/D14 | Confirm the information: only ask whether they are still buying, do not ask for a reply | **D7** only send if there is market news (price movement / price rise / certification notice); **if there is no news to send, skip this step** — do not send just to fill the count | **D14** archive | Archive, remove from the active outreach list |
| **T3** | No touches scheduled | — | — | The stop-loss line for this tier is 0 touches: information is insufficient, so fill in the information first |

**T3 gets no touches** (the script supports `--tier T3`, but the output is "no touches scheduled"). The three tier timelines were never the same length in the first place — the script's comment says it plainly: **not all of them are called "7 days"** — T0/T1 finish inside the first week, T2 stretches to D14.

Generate the plan with these commands (`--start` is required — fill in the **actual first-send day** as `YYYY-MM-DD`; the script does not accept the machine's date, so that results are reproducible):

```bash
# Table version (default GCC market rules; warns about weekends / holidays)
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv my_leads.csv

# Automatically move touches that land on a weekend to the next working day
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --avoid-weekend

# Export into a table / CRM
python scripts/followup_plan.py --tier T1 --start 2026-10-08 --csv my_leads.csv --format csv --out plan.csv
python scripts/followup_plan.py --tier T2 --start 2026-10-08 --market gcc --avoid-weekend --format json --out plan.json
```

Three more built-in constraints in the script — better to follow them directly than to write them in the docs:
- **Minimum gap**: at least `MIN_GAP_DAYS` natural days between two adjacent touches. Do not bombard them with one email a day.
- **No mass-sending the same copy**: `ANTI_SPAM` states explicitly that "the same batch of leads must never receive the same copy in a mass send" — mass-sending identical copy gets judged as spam, and **once a domain is blacklisted it is not just this one customer who is affected, it is all your customers**.
- **Time zones and holidays**: send at the other side's local 9–11 AM, not your 9 AM; for Gulf customers Friday is the main congregational prayer day and they basically do not read email, Saudi weekends are Friday + Saturday, the UAE has switched to Saturday + Sunday; Ramadan / Eid al-Fitr / Eid al-Adha, August European holidays, Christmas in December, Chinese New Year and National Day — replies drop sharply or stop entirely during those periods, so **do not schedule a "last" chase during them**. Check the actual calendar for the specific holidays of the year (the script does not go online; it only gives the reminder).

Remember one thing: every follow-up must carry new information — never just "following up" or "Any update?". The value of a follow-up is in that one new thing. The script lists what each step "must carry" — fill it in as written.

> Note: the script's T0 D0 is labeled "specs and quotation range (excluding the floor price)". This project holds that **the first email contains no price figure at all**, so replace that item with "specs + container loading quantities"; keep the "quotation range" for after the conversation in 05.

**Step 8: The action sequence for 0 replies (do them in order — do not power through on willpower)**

"No reply" is not a feeling; it is a process state that needs handling. After all three touches get no response, execute in this order:

1. **Rule out technical problems first (this is step one, not the last step)**: use your own seed list to check whether the mail went to spam; check for hard bounces (address does not exist — if there is one, **delete it from the list immediately**; a high bounce rate kills domain reputation). Email not delivered = not a copy problem, and rewriting copy fixes nothing.
2. **Change the person**: switch to another entry point in the same company — besides purchasing there is operations, logistics, the sales lead, or the website's `info@` / main switchboard. Find the person, then run another 3-touch round — but the "why them" must be rewritten.
3. **Change the channel**: after three unanswered emails, switch to a phone call or WhatsApp and ask one question: "who handles purchasing for this now?" The point of that question is not to sell — it is to get the right person's name.
4. **Change the angle**: if the first three emails all talked specs, switch to the market angle next round (market movement / certification / delivery risk). Change the angle of approach, not the wording.
5. **Downgrade, do not delete**: T0 → T1/T2 rhythm, into the long list, swept once a quarter. A change of season, a price rise, a new certification, or the period around a trade fair are all legitimate reasons to touch them again. Entering the long list does not mean never contacting them again — it means no more weekly investment.
6. **Stop line**: three non-responses from the same person on the same angle (including read-but-unanswered) means stop. Continuing to send will not raise the reply probability — it only burns domain reputation and the few chances you have to show your face in this market. The script writes this as a hard stop-loss (`MAX_TOUCHES`), with the original reasoning: "continuing to send only lowers domain reputation, and they have already told you the answer with their behavior." An explicit refusal on D0 means stop on the spot — no need to wait for the third touch.
7. **Fix the upstream**: if a whole market's batch of leads gets 0 replies, the problem is most likely not in 04 — it is in 02 (inaccurate list) or 03 (due diligence not done properly). Go back to [02-find-leads_en.md](02-find-leads_en.md) and [03-due-diligence.md](03-due-diligence_en.md) and redo them. Do not grind on copy inside 04.

**Step 9: Record responses and review**

Record every day: what you sent, which channel, which variant, whether they replied, what the reply said, and which step they stopped at. **Draw conclusions only once a week**, and only after the sample has accumulated to 50–100 emails per version — lock in the winning angle, note the losing angle, and do not switch back next week on a feeling.

## 3. Pass criteria

The hard standards for "this stage is done well":

- **Deliverability has been self-checked**: you use your own domain email, SPF / DKIM / DMARC are configured and verified, the first email has no attachment, no link and no price, and the seed list self-test lands in the inbox.
- All A leads have been converted to **T0** per the mapping table and first-touched on three channels the same day (or, for market risk, the email deferred to D1 but still inside the same plan).
- Every first-touch email: **the first sentence is about the other side** (not self-introduction), contains a "why them" line quoting information verified during due diligence, has **exactly one CTA**, a subject line under 40 characters carrying the company name / product category, and **no price, no quotation sheet, no attachment**.
- Each channel's first touch used that channel's first-sentence template (LinkedIn ≤ 50 words, WhatsApp ≤ 25 words); the three channels say the same thing but the copy is not identical.
- A/B tests were run **split by list**, changing one variable at a time, targeting 50–100 emails per version; conclusions rest on your own 100-email field test, not on percentages passed around online.
- The follow-up plan is in the calendar and matches the script's 3-touch rhythm (T0 = D0/D2/D5, T1 = D0/D3/D6, T2 = D0/D7/D14), with each follow-up carrying a pre-planned "new information point" — not an empty chase.
- Leads with three non-responses have been handled through the Step 8 sequence (check deliverability → change person → change channel → change angle → downgrade) — not hammered with the same angle.
- Response status has been recorded (channel + variant number + which touch), so a weekly review is possible.

## 4. AI prompts

**Prompt 1: First cold email generator**

```
You are an export sales writer for a Chinese tire manufacturer. Write a cold outreach email.

MY INPUT:
- Target country: {country}
- Buyer: {name}, {role}, {company}
- What I know about them: {paste verified intel from due diligence, e.g. "carries
  Goodyear/Bridgestone, distributes to garages in Riyadh, importing TBR regularly"}
- Our products: {e.g. TBR 12.00R20, 315/80R22.5, 7.00R16; Tread pattern options;
  OEM and export packaging; MOQ}
- Verified selling points: {only things I can prove}

RULES — non-negotiable:
1. Language: English, 130-170 words, plain text, no Chinglish, no translated-from-Chinese phrasing.
2. SUBJECT LINE: under 40 characters, concrete, must contain their company name or a specific
   product/category. No "Cooperation", no "Best price", no ALL CAPS, no exclamation marks,
   no fake "Re:".
3. STRUCTURE (5 parts, label nothing):
   (a) FIRST SENTENCE MUST BE ABOUT THEM — one specific fact about their business, from MY INPUT.
       Never open with who I am. Open with what I noticed about them.
   (b) half a sentence of who I am and what we make (no founding year, no factory size,
       no certificate list)
   (c) ONE concrete small value offer tied to our products (NOT "high quality", NOT "best price")
   (d) ONE easy-to-answer question they can reply to in a few words
   (e) ONE CTA only. A "this or that" choice is allowed only if both options lead to the SAME
       action. Never ask for a call, a quote and a WhatsApp add in the same email.
4. DO NOT include prices, quote sheets, MOQ numbers, any attachment, or any link.
5. DO NOT write: "we are a leading manufacturer", "factory direct", "best quality",
   "looking forward to your reply", "our company was established in...",
   no spam-trigger stacking (free / urgent / 100% guaranteed / cheapest).
6. End with a ONE-LINE signature: name | company | one role phrase. No phone list, no website
   link, no banner, no slogan.
7. No emojis, no more than one exclamation mark.

OUTPUT:
- The subject line
- The email body
- Then a 3-line note: the ONE variable I should test next, the risk of this angle, and which
  spam-trigger words (if any) I should re-read for.

Then write ONE follow-up version (Day 4) that adds a NEW piece of information and does NOT
say "just following up" or "any update".
```

Note in Chinese (translated): the most valuable parts of this prompt are the ban list and rule 3(a). It drags the AI back from "generating a very polite piece of nothing" to concrete information, and it forces the first sentence to be about the other side rather than about you — that one sentence is the watershed between reply and no reply. Rule 2 writes the 40-character subject limit and "must carry the company name / product category" as hard rules, in the same terms as the self-check list in `scripts/outreach_gen.py`.

**Prompt 2: Follow-up message generator (guards against "just chasing")**

```
You are writing follow-up messages for a B2B tire export sale. My previous email to
{buyer} sent on {date} got {reply status: no reply / polite brush-off / asked for more info}.

RULES:
1. Each follow-up MUST contain at least one piece of genuinely NEW information the earlier
   messages did not contain. Possible new-value types: a specific size list, a container load
   plan, a packing-mark note, a market observation, an answer to an objection, a specific question
   they have not been asked before.
2. Never write: "just following up", "any update", "bumping this up", "did you see my email",
   "waiting for your reply", "please let me know".
3. Never apologize for following up.
4. Never repeat the same pitch. Each message should feel like a different person with something
   to say, or the same person who had something new to add.
5. Keep it under 90 words. English.
6. Match the politeness level of their market: GCC = warm and conversational with light
   honorifics; Europe = concise and formal; Latin America = warmer and more relational.
7. If the previous message asked for something and they went silent, the follow-up should
   lower the ask (from "quote for 3 sizes" to "shall I just send the spec sheet first?").

OUTPUT: the message body, plus one line stating which new-value type I used and why it's
relevant to a tire buyer.

Then write a Day-7 "clear ask" message that makes responding trivially easy (yes/no question).
```

Note in Chinese (translated): the biggest failure mode of a follow-up email is "repeating the first email in different words". This prompt writes "must contain new information" as a hard rule, and gives five types of new information as a menu — just pick one and plug it in.

**Prompt 3: Three-channel content consistency check**

```
You are an outreach strategist. Below are three messages I plan to send to the SAME buyer on the
SAME day: an email, a LinkedIn InMail, and a WhatsApp first message.

Check and fix. Output each channel revised, with a one-line reason for each change.

REQUIREMENTS:
- All three must say the same thing about WHO I AM and WHAT I WANT. A buyer who gets three
  different pitches in one day will distrust at least two of them.
- But they must NOT be identical texts: WhatsApp max 25 words, LinkedIn max 50 words,
  email can be longer. Same message, different shape — never copy-paste the same paragraph.
- Each message carries exactly ONE CTA, and it is the same CTA across all three channels.
- Channel behaviour: WhatsApp = assume they will read it on a phone while busy; be warm,
  extremely short, one clear ask. LinkedIn = short, professional, mention why I'm contacting
  them through this channel specifically (their profile/company). Email = the full substance.
- No channel may promise something the others don't, and none may mention a price the others hide.
- No attachments and no links in any first-touch message (deliverability).
- Do not use "Dear Sir/Madam" in WhatsApp. Do not use all-caps. Do not exceed word limits.

Then flag any place where the three channels could contradict each other.
```

Note in Chinese (translated): the most common accident when sending three channels on the same day is, first, the three versions saying inconsistent things, and second, the three versions being **word-for-word identical** (the customer sees at once it is a mass-send template). This prompt does a consistency check and word-count compression, writes "each channel has exactly one CTA, and the three channels share the same CTA" as a hard rule, and parameterizes "politeness level by market" (GCC warm, Europe concise, Latin America relationship-led).

## 5. Checklist

- [ ] **Deliverability**: own-domain email; SPF / DKIM / DMARC configured and verified; seed list self-test lands in the inbox; first email is plain text, no attachment, no link
- [ ] All A customers have been marked T0, with the decision maker and the need identified
- [ ] Every first-touch email opens with the other side, and the "why them" quotes real information verified during due diligence (if it would still hold for a competitor, rewrite it)
- [ ] Exactly one CTA in the whole email (an either/or is fine, three actions is not); subject line under 40 characters, carrying the company name or product category, no empty words
- [ ] No price, quotation sheet or MOQ figure sent at any point in this stage; signature is one line only, with no stack of phones / links / banner
- [ ] A/B tests split by list, one variable changed at a time, targeting 50–100 emails per version
- [ ] T0 customers reached on three channels the same day (or, for market risk, email deferred to D1 but still inside the same follow-up plan), with the three channels saying the same thing in non-identical copy
- [ ] The follow-up plan is in the calendar, matching the script's 3-touch rhythm, with each follow-up pre-loaded with a "new information point" — not an empty chase
- [ ] Before sending, confirmed: no typos in the email, no spam-trigger words, plain text, no attachment
- [ ] Sending rhythm throttled (spread across time slots, increasing day by day) — not hundreds in one minute; hard bounces deleted from the list
- [ ] Send times follow **the other side's local 9–11 AM**, not your 9 AM; for Gulf customers avoid Friday (main congregational prayer day); Saudi weekends are Friday + Saturday, UAE Saturday + Sunday (or use `--avoid-weekend` / `--market` and let the script defer them)
- [ ] This round does not fall in Ramadan, Eid al-Fitr, Eid al-Adha, August European holidays, Christmas in December, Chinese New Year or National Day — reply-dead periods; **do not make the "last" chase in such a period**
- [ ] Every lead's response status is recorded, with channel + variant number + which touch, for the weekly review
- [ ] Leads with three non-responses have gone through the Step 8 sequence (check deliverability → change person → change channel → change angle → downgrade) — not hammered further

## 6. The traps beginners step into most

**Trap 1: Quoting a price in the first email**
- What it looks like: afraid the customer will not come, you stuff the price list into the first email.
- Why: a beginner treats "giving something" as politeness.
- What to do instead: the first email's value is not price — it is "a reason worth replying to". Quoting comes after the conversation; the reasons are in 05 and 06. Quoting early zeroes your negotiation room on the spot.

**Trap 2: Writing the outreach email as a company brochure**
- What it looks like: founding year, factory area, number of production lines, certificates won — all written in.
- Why: treating your own introduction as the other side's concern.
- What to do instead: replace "how big I am" with "what you can get". A buyer does not care how many production lines you have — only whether the sizes they need can be made, whether they arrive on time, and whether the price is right.

**Trap 3: Follow-ups that only say "Any update?"**
- What it looks like: a "Gentle reminder" on D2, D4 and D7, then getting blocked.
- Why: treating follow-up as a reminder, not as delivering new value.
- What to do instead: every follow-up carries a "new thing" — a spec sheet, a container-loading plan, a market change you noticed. If there is nothing new that time, do not send it.

**Trap 4: Only sending email, never touching instant messaging**
- What it looks like: email sent, three days of silence treated as "not interested".
- Why: not understanding market habits. In the Middle East, South Asia and Africa, a large share of decisions are made on WhatsApp; email is only the record.
- What to do instead: in a market where decisions run on instant messaging, send one very short WA message on the day of first touch. If there is no reply, do not send another in a row — touch them again on D7.

**Trap 5: Sending 200 emails in one day**
- What it looks like: blasting them out with a tool and staring at the send count.
- Why: treating send volume as the KPI, and putting a new domain on high volume on day one.
- What to do instead: verify with a small batch first (say 20–30 emails), confirm they land in the inbox and get replies, then **increase day by day**. Mass-sending hundreds from a new domain on day one is the fastest way to destroy it. Whether replies are good or bad, run 100 emails yourself and count once (send 100, record how many replied and which version replied) and use that as the baseline; do not take percentages passed around online as true, and do not draw conclusions from too small a sample. Piling on volume does not solve the problem — it only burns domain reputation first.

**Trap 6: Mass-sending the same email with only the company name changed**
- What it looks like: swapping {company name} in the template and sending 300 copies.
- Why: thinking personalization means changing a company name.
- What to do instead: real personalization is the "why them" sentence in the second paragraph — which brands they sell, which sizes they push, which city they are in, what is distinctive on their website. If you cannot do that, send only to A/B leads.

**Trap 7: Sending it and then going still**
- What it looks like: first touch sent, ten days of silence treated as "this route does not work".
- Why: the follow-up plan lives in your head, and the next day's busyness makes you forget it.
- What to do instead: put follow-up tasks in the calendar, each with a time. But **follow-up has a cap**: after 3 touches with no response, follow Step 8 — change person, change channel, change angle, and finally downgrade into the long list. The same person is not the only entry point, and not an entry point you can send to forever.

**Trap 8: Attaching files or links in the first email**

- What it looks like: to look professional, stuffing a PDF catalog, a website link and a product photo into the first email.
- Why: treating "giving something" as "looking capable".
- What to do instead: attachments and multiple links are strong signals to spam filters, and a common interception target for the other side's IT gateway — they can get you judged dead before you even appear in their inbox. **The first email is plain text, with zero attachments.** The catalog and spec sheet are the best "new information" for your second email — save them for then.

**Trap 9: Mass-sending from a free mailbox / never configuring SPF-DKIM-DMARC**

- What it looks like: bulk-sending outreach from a free mailbox (Gmail, 163 Mail, QQ Mail), or using a company domain whose DNS was never configured, then complaining that "not one email got a reply".
- Why: not knowing the email may never have arrived at all, and assuming "sent" means "delivered".
- What to do instead: see Step 2. First confirm all three SPF / DKIM / DMARC records are in place and verified, use the seed list to self-test inbox placement, and only then talk about copy. **Rewriting copy before fixing deliverability is optimizing something nobody can see.**

**Trap 10: Stuffing three requests into one email**

- What it looks like: ending with "shall I send a quote? Or book a call? Or add me on WhatsApp?"
- Why: afraid of missing out, so you list every possibility and hand the choice to the other side.
- What to do instead: listing three requests makes the other side make three decisions, and usually they make none. **One email, one CTA.** An "either/or" is allowed, but both options must point at the same action (send the spec sheet / give me the sizes so I can quote) — not two different actions.

**Trap 11: Introducing yourself first**

- What it looks like: opening with "I am XX from XX company, we are a professional manufacturer of...".
- Why: thinking politeness means introducing yourself first.
- What to do instead: a buyer reads the first sentence to judge "is this relevant to me". Write one concrete fact about them first (something you saw them do), and bring in who you are in half a sentence. **Opening with yourself wastes the most valuable sentence on yourself.**

## 7. Copy-paste templates (fill in, no AI needed)

**Template A: First outreach email (Chinese–English对照, fill in as written)**

Rules recap: first sentence about them · one CTA · plain text · no attachment / link / price · one-line signature.

```
Subject: {product category / spec} supply — {their company name}          ← under 40 characters
主题：{品类/规格} 供应 — {他的公司名}

Hi {contact name},

I noticed {why them: one concrete fact about their company, one sentence}. I'm {your name} at {company name} —
we make {product category} and ship to {their country} regularly.

One thing that may be useful to you: {one concrete verifiable point, e.g. size list / bilingual packaging / container loading quantities}.

{one question answerable in a sentence, e.g. "Are you supplying fleets or wholesale on this?"}

Want me to send the size list, or would you rather give me the sizes you need?

Best regards,
{your name} | {company name} | {one role phrase, e.g. Export}

—— 中文对照（仅供你核对，客户不收）——

{联系人名} 你好，

我注意到 {为什么是他}。我是 {公司名} 的 {你的名字}，我们做 {品类}，长期发 {他的国家}。

有一件事可能对你有用：{具体可验证的点}。

{一句话能回的问题，如「你们这块是供车队还是走批发？」}

我把规格表发你，还是你直接给需要的型号？

顺祝商祺，
{你的名字} | {公司名} | 外贸
```

**Three hard checks when filling it in** (the script `outreach_gen.py` also carries these three at the end of every draft):
1. Would the "why them" still hold if you swapped in a competitor? If yes = rewrite.
2. Does the body contain any price figure? If yes = delete it (the script's T0/T1 drafts carry a price-list sentence by default — delete it by hand).
3. Is the subject line over 40 characters? If yes = shorten it.

Generate drafts:

```bash
python scripts/outreach_gen.py my_leads.csv --tier T0                 # Chinese–English对照
python scripts/outreach_gen.py my_leads.csv --tier T1 --lang en --out drafts.md   # English only
```

**Template B: LinkedIn connection request / first message**

```
Connection request (note, 2 sentences):
Hi {Name} — I supply {product category} to buyers in {country}. Saw you handle {their product category / brand}.
Would like to connect and follow what you're doing there.
中文：{Name} 你好，我给 {country} 供 {品类}，看到贵司在做 {品类/品牌}，想加个好友跟进一下。

First message after acceptance (≤ 50 words):
Thanks for connecting, {Name}. Quick context: we make {product category} and ship to {country}.
Not pitching — are you sourcing {product category} from Asia this year? One word is enough.
中文：谢谢通过。我们做 {品类}，发 {country}。不是推销——贵司今年还从亚洲采购 {品类} 吗？回一个词就行。
```

**Template C: WhatsApp first message (≤ 25 words)**

```
Hi {Name}, {your name} from {company name} ({product category}). Saw you import from Asia —
OK if I send the size list? One line is enough.
中文：{Name} 你好，我是 {公司名} 的 {你的名字}，做 {品类}。看到贵司从亚洲进货——发份规格表行吗？回一句就行。
```

**Template D: Phone opening (20 seconds)**

```
Hello, may I speak to {Name}? … Hi {Name}, {your name} from {company name}. We supply {product category} to {country}.
I'm calling because {why them}. Is now a bad time for two minutes?
中文：你好，请找 {Name}。…… {Name} 你好，我是 {公司名} 的 {你的名字}，我们给 {country} 供 {品类}。
打电话是因为 {为什么是他}。现在方便讲两分钟吗？
```

**Template E: Website contact form (only when no contact person can be found)**

```
Subject: For the purchasing team — {product category} supply enquiry
Please forward this to whoever handles {product category} sourcing. We manufacture {product category} and supply {country}.
{why them}. If you already have a supplier, a one-word reply is enough and I'll stop here.
中文：请转给负责 {品类} 采购的同事。我们生产 {品类} 并供应 {country}。{为什么是他}。
如已有供应商，回一个词即可，我不再打扰。
```

> All company names in the templates carry the **[Example]** prefix, email domains always use **sample.example**, and phone numbers always use placeholders (e.g. `+000-0000-0000`). Real customer data goes only into your local CSV, never into the repo.

## 8. Next stage

Someone has replied — asking for a price, asking for samples, anything counts — the conversation is open. The next step is **Qualifying** [05-negotiation.md](05-negotiation_en.md): before quoting, get the requirements clear.

If there are still 0 replies after three touches, go through the Step 8 action sequence first; if the whole batch of leads has no replies, the problem is in [02-find-leads_en.md](02-find-leads_en.md) or [03-due-diligence.md](03-due-diligence_en.md), not in this document.
