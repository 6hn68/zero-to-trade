# AI 提示词总库 · AI Prompt Library

**用法：** 每条提示词都是完整文本，直接复制粘贴进 ChatGPT / Claude / 任何模型即可用。方括号 `[...]` 里是你要替换的部分。

**三条使用纪律：**

1. **AI 出的东西一律当草稿。** 报价数字、客户结论、法规判断，必须自己核一遍再对外发。模型会编造物流费、认证要求和汇率。
2. **上下文喂进去，输出质量差一截。** 你的产品、目标价带、客户国家、规格，能填的 `[...]` 全填。
3. **不要让 AI 替你做判断。** 让它做整理、生成、列选项、找漏洞。决策是你的活——这正是本项目的核心理念。

**编号规则：** `P{环节号}-{序号}`，例如 P03-2 是环节 03 的第 2 条。环节文档（`docs/`）通过编号引用这里，不复制全文。

---

## 01 选市场 · Pick a Market

### P01-1 · 三维打分与首站市场选定

**中文说明：** 把手里的候选国家按语言-需求-壁垒三维打分，逼 AI 给出可辩护的结论而不是"都挺好"。强制它输出反面理由。

```text
You are a market entry analyst for a small Chinese exporter. I sell [PRODUCT CATEGORY] to [TARGET REGION], and I am choosing my FIRST market to enter. I have limited budget: roughly [BUDGET USD] for travel, samples, certifications, and channel setup. I have [YEARS] years of export experience but I have never entered this market.

Evaluate the following candidate markets: [LIST OF 5-8 COUNTRIES].

Score each country 1-10 on three dimensions, and state the evidence behind every score:
1. LANGUAGE BARRIER — How much of my sales cycle is lost to language? Consider: can I find local trade data in English, do buyers there conduct business in English, is Arabic/Spanish/etc. required for negotiation.
2. DEMAND FIT — Is there real, current demand for my product at MY price band? Not "they buy this product" but "they buy this product at this price with these specs".
3. ENTRY BARRIER — Tariff and duty burden, mandatory certifications (list them by name), local agent/distributor exclusivity, credit and payment risk, and how long certification realistically takes.

Then:
- Rank all candidates.
- Pick ONE first market and defend it in exactly three sentences.
- List the two strongest objections to that choice and how I would test whether the objection is real before committing money.
- Name the ONE country you would pick if the budget were 10x smaller.

Output as Markdown tables. Keep every cell to one line. Do not use phrases like "promising market", "significant potential", or "good growth prospects" — I want evidence and numbers, not adjectives. If you do not know something for certain, write "UNKNOWN — verify by: [how to verify]".
```

### P01-2 · 需求真实性反查

**中文说明：** 防止被"这个市场很大"的报告忽悠。强制 AI 找**反证**，并把宏观数字翻译成"我能卖几单"。

```text
Act as a skeptical market researcher. Someone has just claimed that [COUNTRY] is a great market for [PRODUCT]. Your job is NOT to confirm it. Your job is to find the strongest reasons it might be wrong, then give me an honest read.

Provide:
1. Five specific reasons this market might NOT work for me at my price band ([MY PRICE BAND]).
2. For each reason: what would have to be true for it to be false, and how I could check that cheaply in under a week.
3. Translate any macro figures you find into MY terms: given my price point and typical order size, how many orders per month would I need to make this market worth my time? Show the arithmetic.
4. Who are the three existing suppliers already in this market that I have never heard of? If I cannot name them, that itself is a finding.
5. One sentence: what is the single most likely reason I will fail in this market?

Be concrete. Cite source names and dates. If a figure is from a paywalled report you cannot read, say so instead of guessing. Mark anything you are not confident about as "UNVERIFIED".
```

### P01-3 · 准入成本清单

**中文说明：** 把"能不能进这个市场"变成一张带费用的清单。AI 只负责列和分类，**具体金额必须标为待核**。

```text
You are helping me prepare an entry checklist for [COUNTRY] for [PRODUCT CATEGORY]. I am a direct exporter, not a trading company, and I intend to sell through [CHANNEL: direct B2B / local distributor / Amazon / trade show leads].

Produce a complete market-access checklist in Markdown tables with these sections:

1. COMPANY REGISTRATION — what entity do I need locally, what does it cost, how long does it take, which authority issues it.
2. PRODUCT CERTIFICATION & CONFORMITY — list every certification and mark each as MANDATORY / USUALLY REQUIRED / RARELY REQUIRED. For each mandatory one: full name, issuing body, approximate cost range, typical lead time in weeks, and whether it can be done before you have a confirmed order.
3. IMPORT DUTIES & TAXES — HS code structure for my product, duty rate if known, VAT/GST rate, and any special regime (e.g. Gulf GSO/SABER-style conformity schemes) that applies.
4. LABELING & PACKAGING — language requirements for labels, mandatory declarations, unit-of-measure rules.
5. DOCUMENTS A BUYER WILL ASK FOR — commercial invoice, packing list, bill of lading, certificate of origin, insurance, and anything specific to this country.
6. PAYMENT & RISK — normal payment terms in this market, preferred method, who bears the credit risk, typical bad-debt dispute mechanism.

CRITICAL RULES:
- Mark EVERY cost figure as "ESTIMATE — verify with: [which authority or consultancy]".
- Mark every lead time as a range, never a single number.
- For anything you are unsure about, write "UNKNOWN" rather than guessing. An invented certification cost is worse than a blank.
- At the end, list the top 3 items on this list that most often surprise first-time exporters, and why.
```

---

## 02 找客户 · Find Leads

### P02-1 · 四路线索挖掘方案

**中文说明：** 让 AI 把四路来源拆成可执行的每日动作，并给出**产出量估算**，而不是列一堆网站名。

```text
You are a lead generation operator. I export [PRODUCT] to [COUNTRY/REGION]. My price band is [PRICE BAND], typical order [ORDER SIZE], and my target customer is [IDEAL CUSTOMER PROFILE — e.g. "importing distributor with 3-8 branches, currently buying from China"].

Design me a lead sourcing routine across FOUR channels: customs/import data, social media, web search, and trade shows. For each channel, specify:

1. THE SEARCH RECIPE — the exact source (named site, named database, named group, named show), the filter values to use, and the specific fields I should export. Generic advice like "search on Google" is useless; tell me which filters.
2. THE DAILY QUOTA — how many raw records I should pull per day, and what percentage I should expect to be genuinely usable. Be realistic. I would rather have 20 real leads than 200 junk ones.
3. THE VERIFICATION STEP — how to confirm this record is a real, active, reachable business before I invest time.
4. THE FAILURE MODE — the single most common way this channel wastes time for someone selling my product, and how to avoid it.

Then produce:
- A 7-day ramp-up plan: what I do on day 1 vs day 7, with the volume target for each day.
- A weekly output target expressed as: leads pulled, leads verified, leads worth contacting.
- A rule for when to stop using a channel and move on.

Assume I have [HOURS] hours per day to spend on this. Be honest if my target of 20 verified leads per day is unrealistic for the hours available — tell me what is actually achievable and what to trade off.
```

### P02-2 · 线索去重与合并

**中文说明：** 手工整理名单最烦的是同一家公司出现五次、不同拼写。交给 AI 做归并。

```text
You are a data cleaning assistant for a B2B lead list. Below is raw lead data I collected from customs data, a trade show directory, and LinkedIn. The same company appears multiple times with different spellings, different contact people, and inconsistent country formats.

RAW DATA:
[PASTE YOUR RAW LEAD LIST HERE — keep the original column headers]

Do the following:
1. NORMALIZE — standardize country names to a single format, standardize company name suffixes (Ltd/Limited/LLC/Co., LLC), strip tracking parameters from URLs, and normalize email domains to lowercase.
2. MERGE — group records that are clearly the same company. State your confidence level (HIGH / MEDIUM / LOW) for every merge and give the evidence you used.
3. FLAG CONFLICTS — where the same company has two different emails, two different websites, or two different countries, list the conflict and say which value you kept and why.
4. OUTPUT — a single deduplicated table with columns: company_name, country, website, primary_email, all_emails, contact_name, contact_title, linkedin, source(s), confidence, notes
5. DUMP LIST — give me a separate list of records you merged, so I can spot-check your merges.

RULES:
- Never delete a record silently. Every input record must appear in exactly one output row, or in the dump list with a reason.
- Never invent an email address or a website. If the input has none, leave it blank.
- Do not merge two companies just because they have similar names. Same name in different countries = two different companies.
- Explain your merge rules in 3 lines at the top, then output the tables.
```

### P02-3 · 搜索式速查表

**中文说明：** 让 AI 产出可直接粘贴的搜索算子。这是**找信息**用的，不是找客户名单用的。

```text
You are a search specialist. I need to find information about companies in [COUNTRY] that buy or distribute [PRODUCT CATEGORY].

Build me a cheat sheet of search queries in three blocks:

BLOCK A — DISCOVERY QUERIES (find candidate companies)
Provide at least 10 Boolean-style search strings I can paste directly. Examples of the shape: site:COMBINEDOMAIN "PRODUCT" distributor, "PRODUCT" "COUNTRY" importer filetype:pdf
For each query, note briefly what it tends to surface and its likely false-positive rate.

BLOCK B — QUALIFICATION QUERIES (check whether a specific company is worth contacting)
At least 8 queries for a named company, e.g. "[COMPANY]" annual report, "[COMPANY]" import records, "[COMPANY]" distributor "MY BRAND" — these are checks I run on a specific lead.

BLOCK C — NEGATIVE QUERIES (spot trouble)
At least 5 queries that surface warning signs: lawsuits, sanctions, non-payment, fraud complaints, shutdowns, unsatisfied importers.

For every query, mark which country-specific or language-specific terms I should swap in. If a query only works in English, say so — I am working in a market where English-language coverage may be thin.

Keep the cheat sheet as a Markdown table: query | what it finds | false positive rate | notes.
```

---

## 03 背调客户 · Vet the Buyer

### P03-1 · L1 快速筛查（淘汰骗子）

**中文说明：** L1 是筛杀，不是调查。三分钟内出结论，二元判定。

```text
You are screening a potential buyer for fraud and non-payment risk. Be fast, be blunt, and give me a kill-or-continue verdict. I need a decision in under three minutes, not a report.

BUYER: [COMPANY NAME]
COUNTRY: [COUNTRY]
WEBSITE: [URL OR "NONE FOUND"]
CONTACT: [NAME, TITLE, EMAIL]

Do an L1 screen. Check exactly these seven items:
1. Website — does it exist, does it load, is there a real company address and phone, or is it a template with placeholders left in.
2. Registration — is there a verifiable registration record for this company name? Tell me the registry or source you checked.
3. Age — how long has the business existed? Earliest evidence of activity (year, first social post, first mention).
4. Social accounts — do LinkedIn/Facebook/Instagram accounts exist, and are they active in the last 90 days or dormant/empty.
5. Email domain — is the email on the company's own domain or a free mailbox? If free, does the person have ANY other traceable footprint.
6. Contact plausibility — does the email local part match the person's name, and does the job title match what they claim to do.
7. Import footprint — any sign at all that this company imports goods at all, from anywhere, in any volume.

OUTPUT FORMAT:
- VERDICT: KILL / PROCEED TO L2 / UNCLEAR
- For each of the 7 items: FOUND / NOT FOUND / CONTRADICTORY, with one line of evidence and the source.
- RED FLAGS: list every contradiction you found. If none, say "none".
- CONFIDENCE: HIGH / MEDIUM / LOW, and what would raise it.

RULES:
- Do not infer that a company is legitimate because it looks professional. Assume fraud until the seven items above say otherwise.
- Never guess or fill in an email, address, or registration number.
- If you cannot access a source, write "COULD NOT CHECK: [source]". Do not substitute a guess.
- A missing item is not automatically a red flag, but three or more missing items must force a KILL verdict.
```

### P03-2 · L2 标准背调（判断值不值得投入）

**中文说明：** L2 是算账：这家客户能带来多少量、多大概率付款、值多少时间。

```text
Act as a credit and sales potential analyst. I have already run an L1 screen on this buyer and it passed. Now I need a commercial judgment, not background reading.

COMPANY: [NAME] | COUNTRY: [COUNTRY] | MY PRODUCT: [PRODUCT] | MY PRICE BAND: [BAND]

Produce:

1. SIZE & CAPACITY ESTIMATE — annual revenue band, employee band, number of locations if any, and the reasoning chain from whatever public data exists to those bands. Show how you got there. Mark each band LOW / MEDIUM / HIGH confidence.

2. LIKELY ORDER REALITY — given their apparent size and channel position, what order quantity and frequency should I realistically expect? Give a conservative, likely, and optimistic case.

3. PAYMENT BEHAVIOR RISK — score 1-5 (5 = safest) on: how they typically pay, whether they ask for credit terms early, whether the market has a strong bad-debt / slow-payment problem, and whether enforcement is practical. Explain each score in one line.

4. CHANNEL POSITION — are they an end user, a distributor, a retailer chain, or a trading company? What does that mean for order size and for how hard I have to work to close?

5. WHAT WOULD MAKE THIS A PRIORITY — the 3 concrete signals that would justify spending my best effort here.

6. THE HONEST PROBABILITY — give me a percentage estimate that this account closes into a repeat buyer within 6 months, and name the single biggest reason it might not.

RULES:
- Every number needs a source or an explicit "[MY ESTIMATE]" tag.
- No motivational language. No "this is a great account". I want a commercial verdict.
- If the available public data is too thin to support any of this, say that plainly and tell me the two cheapest ways to get better information (e.g. one call to a trade office, one industry-association contact).
```

### P03-3 · L3 深度背调（谈单前 90 分钟）

**中文说明：** 已经要下决心投入时用。产出是**一份会议提纲 + 一串必须问到答案的问题**。

```text
You are preparing me for a first serious commercial conversation with a buyer I have already screened and sized up. My goal in this call is NOT to close, it is to walk away knowing whether this account is real, whether it has budget, and who actually decides.

COMPANY: [NAME] | COUNTRY: [COUNTRY] | THE PERSON I'M MEETING: [NAME, TITLE]
WHAT I KNOW SO FAR: [paste your L1 and L2 output here]
WHAT I'VE ALREADY ASKED THEM: [what you've said so far]

Deliver three things:

1. THINGS THAT ARE TRUE ABOUT THEM — facts I can state with confidence and use to build credibility in the first 60 seconds. Separate what is verified from what is inferred. Never blur the two.

2. THINGS I STILL DON'T KNOW, RANKED — the unknowns that matter most for whether I invest time. Order by "if the answer is bad, would I walk away?" Put those first.

3. THE CALL PLAN —
   a. Opening: 3 sentences I can actually say out loud, tailored to this specific company, not generic pleasantries.
   b. Seven questions I must get answered. For each: the question, why I am asking, and what a good answer sounds like versus a bad answer.
   c. Two questions that sound polite but are actually qualification questions, so I don't notice I'm being vetted.
   d. Three questions I should NOT answer directly in this call.
   e. The single question whose answer tells me whether to send a quote.

RULES:
- Every personalized item must reference something specific to THIS company. If you cannot make it specific, mark it as generic and tell me to fill it in.
- The bad answers must be concrete and quotable, e.g. "if they say 'we pay after the goods are inspected', ask who inspects and whether they pay the inspection fee".
- Do not pitch. I want to know, not to sell.
```

### P03-4 · 背调结论转行动清单

**中文说明：** 把一堆背调结论压成"下周具体做什么"，防止背调上瘾。

```text
You are converting research into action. Below is everything I learned about a prospect from background research. I have a habit of over-researching and under-contacting, so your job is to cut it down and force a decision.

RESEARCH NOTES:
[PASTE YOUR BACKGROUND RESEARCH HERE]

Give me back:
1. THE ONE-LINE VERDICT — A, B, or C grade, with the single reason that determined the grade.
2. WHAT I AM WRONGLY ASSUMING — list at most 3 things I seem to believe that the evidence does not support.
3. THE NEXT 3 ACTIONS — concrete, each with: the action, the day of the week to do it, and roughly how long it takes. No action may be "research more".
4. WHAT I SHOULD DELIBERATELY IGNORE — information I could chase that would not change the grade or the next action. This is the important one, so be honest and ruthless.
5. THE TRIGGER TO RE-CHECK — what would make me reopen this file, in specific terms (a news item, a price change, a silence period of N days).
6. THE TIME BUDGET — total minutes I should ever spend on this account this quarter, as a hard number. Be stingy.

Output as plain Markdown, under 400 words total. No preamble.
```

---

## 04 建联客户 · Make Contact

### P04-1 · 三线并进首触方案

**中文说明：** 首触的核心是**多渠道同时**，让对方觉得"这公司到处都在"。AI 负责排优先级和排期。

```text
You are designing a first-touch sequence for a B2B export sale. My buyer is [COMPANY], in [COUNTRY], and I identified them via [CHANNEL]. My product is [PRODUCT], my angle is [SPECIFIC ANGLE — e.g. "we already supply a distributor in their neighbouring country with the same spec"].

I want a three-channel first touch: [EMAIL] + [WHATSAPP/LINKEDIN] + [FOLLOW-UP CHANNEL OF YOUR CHOICE, justified].

For each channel give me:
1. THE ANGLE — why this channel, for this buyer, at this moment. If a channel adds nothing, say so and drop it.
2. THE MESSAGE — the actual copy, English plus a Chinese version, under 120 words per language. Subject line included for email.
3. THE TIMING — which day and roughly what hour local time in the buyer's country. Justify it against that time zone's working pattern.
4. THE FAILURE MODE — the most likely way this message gets ignored, and the one change I would make if it does.

Then give me:
- The sequence order with the gap between touches in days.
- What the buyer's response should trigger at each step, and what silence should trigger.
- The single message in this sequence that is doing the most work, and why.

CONSTRAINTS:
- No "Dear Sir/Madam", no "I hope this email finds you well", no "we are a leading manufacturer with 20 years of experience" unless I actually told you that number.
- The first email must make it trivially easy to reply, even with "not interested". Ask something that takes one word to answer.
- Plain text formatting. No HTML, no images, no attachments in the first touch.
```

### P04-2 · 拒绝理由分类与应对

**中文说明：** 客户不回、明确拒绝、说要资料——每种对应的下一步动作完全不同。

```text
I run outbound B2B sales and I keep losing people in the first two contacts. Below are the actual responses I received this week. I need to know which of these are normal noise and which are real warnings.

RESPONSES:
[PASTE YOUR REAL REPLIES HERE — "no thanks", "send us your catalogue", "too expensive", "we are busy", "not interested", "call me next week", and anything else you got]

For each response, classify:
- WHAT IT ACTUALLY MEANS (three possibilities: real rejection, polite brush-off, or a genuine signal of interest disguised as a brush-off).
- THE PROBABILITY it means the buyer is still reachable — low, medium, or high, with your reasoning.
- THE ONE ACTION I should take next, written as a single specific sentence I could send.
- HOW LONG I wait before the next touch, in days.

Then:
1. Which of these responses am I most likely misreading? Point at the one you think I am getting wrong.
2. Which single response should I stop treating as a rejection? Argue for it.
3. Give me three subject lines that are more likely to get a reply than my current ones, using [MY PRODUCT] and [BUYER'S ACTUAL BUSINESS DESCRIPTION].
4. Tell me which of these replies signals a problem with my lead quality rather than my copy, and what to fix upstream.

Be direct and specific. If a response is genuinely ambiguous, say so and give me a tiebreaker question.
```

### P04-3 · 跟进话术变体生成器

**中文说明：** 同一封信不能发七次。这个提示词强制每次换角度。

```text
You are writing the follow-up sequence for a prospect who went quiet after my first email. My first email is below. My previous follow-ups are below. I do NOT want to send the same email six more times.

FIRST EMAIL:
[PASTE IT]

FOLLOW-UPS SO FAR:
[PASTE THEM]

Generate follow-up touches #3 through #7. Rules:
- Each touch must use a DIFFERENT reason to exist. Assign one of: new information, new question, new proof point, narrowing the ask, or a graceful close-out. State which one each touch uses and why it's not a repeat.
- Each touch must be under 80 words. Shorter than the first email, because each one costs less attention.
- Include an English version and a Chinese version for each.
- Touch #7 must be a genuine close-out: either a clear one-line "shall I close your file, or would you prefer I check back in [MONTH]?" or a graceful goodbye that leaves the door open. No fake urgency, no fake deadlines, no manufactured scarcity.
- Include a subject line for each touch. Reusing a subject line across three touches is allowed, and is sometimes correct.
- Never use: "just following up", "circling back", "did you see my last email", "I understand you're busy", "not to be a bother".
- Where a touch needs a fact I have not given you, insert [FACT I NEED: ...] rather than inventing one.

At the end, give me the cadence: which day each touch goes out, and what to do if they reply to any one of them.
```

### P04-4 · 沉默客户的收尾与重新激活

**中文说明：** 第 30 天没回怎么办。答案是明确收尾，不是继续骚扰。

```text
A prospect received my first email and two follow-ups over 35 days. No reply. I am not sure whether to keep pushing, close the file, or try a different channel.

DEAL CONTEXT:
[Who they are, what product, what you quoted or discussed, what channel you used]

Give me:
1. THE DIAGNOSIS — the most likely reason for the silence, ranked by probability. Be honest if "they simply don't want to buy" is the top answer.
2. KILL OR KEEP — one verdict, with the condition that would change it.
3. THE CLOSE-OUT MESSAGE — a 30-word email that closes the loop gracefully and gives them an easy way back in later. English plus Chinese. No resentment, no "did I do something wrong", no passive-aggressive "I'll assume you're not interested."
4. THE REACTIVATION TRIGGER — what would make it worth contacting this account again: a specific event, a specific date, or a specific change in your offering. Give me one concrete trigger, not "when the market improves".
5. THE LAST-RESORT CHANNEL — one channel I have NOT tried, and exactly when it is worth trying. Note honestly if the answer is "none, let it go".
6. WHAT TO CHANGE NEXT TIME — one change to how I sourced or approached this account that would have improved the odds. This is the most valuable part; do not skip it.

Under 300 words.
```

---

## 05 聊单 · Talk Specs

### P05-1 · 需求澄清问题清单

**中文说明：** 报价之前必须问清的规格项。**小要求先行**，先让对方动起来。

```text
You are preparing me for a first technical conversation with a buyer who has asked for a quotation. My job in this call is NOT to quote and NOT to close. My job is to get specific enough that a later quote cannot be wrong, and to get the buyer to invest a little effort so they feel ownership.

PRODUCT: [PRODUCT] | BUYER: [COUNTRY, MARKET SEGMENT] | MY PRICE BAND: [BAND]

Give me:
1. THE MINIMUM VIABLE SPEC SHEET — the smallest set of questions that lets me produce a defensible quote. Cap it at 10 questions. Every question must change the price or change whether I can serve them at all. Flag the 3 that are deal-breakers versus the 7 that are refinements.
2. THE THREE SMALL ASKS — three easy questions I can ask FIRST, before anything heavy, that make the buyer commit information without feeling interrogated. Rank them by how easy they are to answer.
3. THE QUESTIONS THAT LOOK LIKE SMALL ASKS BUT ARE SCREENING — 2 questions that sound like spec questions but tell me whether this buyer is serious. Explain the tell for each.
4. THE QUESTIONS TO SAVE FOR THE SECOND CALL — 3 questions I should deliberately NOT ask now, because asking too early reveals that I don't know the product, or gives away my cost structure.
5. THE QUESTIONS THAT EXPOSE A BUYER WHO CAN'T ANSWER — 3 questions a serious buyer answers instantly. If they hesitate on these, that is information.

OUTPUT FORMAT: a numbered Markdown table with columns: # | Question (English) | 问题（中文） | Deal-breaker or refinement | Why it matters.

RULES:
- Ask like a supplier who is genuinely trying to quote correctly, not like a form filling out.
- No question may be answerable with a single word if the answer would not actually be useful. If you include a yes/no question, state what the specific answer reveals.
```

### P05-2 · 询盘分类与优先级

**中文说明：** 一堆询盘里挑出先回谁。这个判断 AI 可以帮你排序，**最终决定你来做**。

```text
Below are inbound inquiries I received this week. I cannot answer all of them today and I need to rank them.

INQUIRIES:
[PASTE YOUR INQUIRIES — include company name, country, product asked about, what they specified, how they found you, and tone]

Rank them using:
- FIT: does this product fit my actual range, or is it a "can you also make this" request?
- SPECIFICITY: did they give real specs and quantities, or is the message a one-line "price please"?
- CREDIBILITY: are they a company with a verifiable footprint, or a gmail address asking for your lowest price?
- URGENCY SIGNAL: is there a real timeline in the message, or is "urgent" doing all the work?
- EFFORT COST: how much of my day would answering properly take?

For each inquiry give me:
1. RANK 1-5 (1 = answer today).
2. WHICH SIGNALS DROVE THE RANK — one line each.
3. THE EXACT REPLY — a drafted response, English plus Chinese, appropriate to that rank. Rank 1 gets a response that asks 5 specific questions. Rank 5 gets a polite short reply that keeps the door open without giving away anything.
4. THE TELL I SHOULD WATCH — one specific thing that, if it appears in their reply, moves them up or down a rank.

Then answer one question directly: which single inquiry is most likely to become a real order, and which single one looks most attractive but is most likely to waste your day?

Do not tell me to be polite. Tell me what to reply.
```

### P05-3 · 报价前的规格确认单

**中文说明：** 拿到对方口头说法，转成一份**双方都要确认的书面清单**，避免日后扯皮。

```text
Turn a verbal conversation into a written specification confirmation that both sides must sign off on before any price is discussed. This document is my defense against misunderstandings later.

MY PRODUCT: [PRODUCT] | BUYER: [BUYER, COUNTRY]
WHAT WE AGREED IN THE CALL: [your notes — messy is fine, I want you to organize it]

Produce a confirmation document with these parts:

1. SPECIFICATION TABLE — item | buyer's stated requirement | my standard product | difference | is this difference acceptable to me and why | confirm/clarify needed. Any row where the buyer's requirement is something I cannot meet must be marked "MISMATCH — DECISION NEEDED".

2. QUANTITY AND PACKAGING — quantity, unit definition (this is where most disputes start), packaging type, pallet quantity, total gross weight and volume. State explicitly whether any of these are MY assumptions, and flag every assumed figure.

3. SHIPPING AND TERMS — shipment mode, Incoterm with the exact version and location named (do not write just "FOB"), destination port, latest shipment date, and who arranges freight.

4. OPEN QUESTIONS — a numbered list of everything still unconfirmed, each with the question in both English and Chinese, and why the answer changes the quote.

5. WHAT THIS DOCUMENT DOES NOT COVER — explicitly list what we did NOT agree on, so neither of us assumes it later.

RULES:
- Every number must be marked as either [BUYER STATED] or [MY ASSUMPTION]. No unmarked numbers.
- If a buyer's statement is ambiguous, write both readings and ask which one they meant. Do not silently pick one.
- No prices anywhere in this document.
- End with a short cover note I can send with it, in English and Chinese, that asks for written confirmation without sounding defensive.
```

---

## 06 报价谈判 · Quote & Negotiate

### P06-1 · 报价单结构审查

**中文说明：** 检查报价单有没有把不该露的成本露出去。**这一步最容易漏，也最致命。**

```text
You are reviewing my quotation before I send it to a buyer. My goal is to send a professional, complete quote that survives comparison and does not leak information I need to keep.

MY QUOTE DRAFT:
[PASTE YOUR QUOTE]

PRODUCT: [PRODUCT] | BUYER: [COUNTRY] | INCOTERM: [TERM + LOCATION] | CURRENCY: [CCY]
MY COST STRUCTURE (confidential — tell me what must NOT appear): [COST LINES]
MY NEGOTIATION POSITION: [list the things I can concede and what I need in return for each]

Review and output:
1. MISSING ITEMS — everything a buyer in this market will expect to see on the quote but I omitted. Be specific about the market.
2. ITEMS THAT LEAK — every line where my price structure, margin, supplier identity, or cost breakdown is inferable. Quote the line and show me the inference path. This is the most important section.
3. AMBIGUITY — any line a buyer could read two ways, especially around Incoterms, unit definitions, validity period, and payment terms. Rewrite each one to be unambiguous.
4. STRUCTURE — should this be a line-item quote or a tiered quote by quantity? Recommend one and explain the commercial consequence of each.
5. WHAT I'M GIVING AWAY FOR FREE — anything I included that I should have priced as an extra (extended payment terms, free samples, free spare parts, free loading supervision, extended validity).
6. THE SENTENCE — one sentence telling me the single biggest thing to fix before sending.

Rules: be blunt. Do not compliment. For each problem, give the exact replacement wording. If a number I wrote is a guess rather than a costed figure, say "UNCONFIRMED — do not send".
```

### P06-2 · 三档让步阶梯设计

**中文说明：** 让步必须**换条件**。这个提示词逼 AI 生成有对价的让步路径。

```text
Design a concession ladder for a negotiation that is already in progress. My current position is a floor of [MY FLOOR PRICE] for [PRODUCT, SPEC, QTY, INCOTERM]. The buyer has pushed from their initial [BUYER OPENING] to [CURRENT ASKING PRICE]. They said: [BUYER'S EXACT WORDS].

THE THINGS I CAN TRADE (each has a real cost to me): [list — price, payment terms, MOQ, lead time, packaging, warranty, free spare parts, exclusivity for a region, sample quantities, shipping mode]
THE THINGS I CANNOT TRADE: [hard limits]

Build me three rungs:
RUNG 1 — SMALL CONCESSION, SMALL ASK. How much do I give, what exactly do I get in return, and how do I phrase the ask so the trade feels natural rather than like a hostage situation?
RUNG 2 — MEDIUM CONCESSION, MEDIUM ASK. Same structure, but the ask must be worth more than the concession, because a buyer who gets rung 1 and asks again is the buyer who breaks your floor.
RUNG 3 — THE FINAL MOVE. Usually not a price concession. Usually the closest thing to a walk-away that still closes. Give me the exact wording.

For each rung give me:
- The exact words to say or write, in English and Chinese.
- What I get in return, stated as something concrete I can verify.
- What signal tells me to go to the next rung, and what signal tells me to stop and hold.
- The reason I will not go below the floor even if they push again — a sentence I can say out loud and believe.

RULES:
- Never let me make a concession without a return. If I want to give something for free, name it as an optional goodwill move and tell me exactly what it costs me in leverage.
- Do not use "our margin is very tight" or "we cannot go lower". Give me a reason that is true and does not invite a counter-argument.
- The ladder must be usable in a single conversation. If rung 3 needs a second call, say so.
- At the end: state the single most likely mistake I will make under pressure, and the sentence that prevents it.
```

### P06-3 · 客户压价应对话术

**中文说明：** 按压价的具体说法分类应对，每类给可照抄的回应。

```text
You are coaching me for a price negotiation. A buyer has used one of the pressure tactics below. For each one, give me a response that holds my position without losing the deal.

MY SITUATION: [PRODUCT, MY PRICE, MY FLOOR, WHAT THEY'VE ALREADY TRIED, HOW LONG WE'VE BEEN TALKING]
THE BUYER'S RELATIONSHIP SO FAR: [new / second contact / existing customer / referral]

TACTICS:
1. "Your price is 30% higher than another supplier."
2. "If you can match [X], we order immediately."
3. "I need a 10% discount or I'll go with another supplier."
4. "The last supplier gave me a better deal and gave me 60 days payment."
5. "This is our only order, treat it as a trial."
6. "Sign this price and I can get you an immediate reply from our director."
7. Silence, followed two weeks later by "we are still interested, are you?"
8. "I need to reduce my order but I need a better price."

For each tactic give me:
- WHAT THEY ARE ACTUALLY DOING — one honest line. Some tactics are negotiation, some are bluffing, and I need to know which.
- THE SIGNAL TO WATCH — how I tell a real constraint from a bluff.
- MY RESPONSE — exact words, English plus Chinese, under 80 words, calm and non-defensive.
- WHAT I SHOULD NOT SAY — the tempting sentence that gives away my floor.
- THE TRADE I'M WILLING TO OFFER INSTEAD — a concession that costs me less than the price cut they asked for.

Finally: tell me which of these eight I should never concede anything on, and which one I should concede something on immediately to buy goodwill. Justify both answers in one line each.
```

### P06-4 · 谈判复盘与底线校准

**中文说明：** 一单谈完，把结果变成下次用的规则。防止每次都从零开始。

```text
I just finished a negotiation. I want to extract the lesson so I stop re-learning it.

WHAT HAPPENED:
- My quoted price: [X]
- Their opening: [Y]
- Where we settled: [Z]
- What I conceded: [list]
- What I got in return: [list]
- Their stated reason for moving away or closing: [their words]
- The moment I knew the outcome: [or "I didn't know"]

Give me:
1. THE POST-MORTEM — where the price actually broke down, in one paragraph. Was it my anchor, my floor, my patience, or their leverage? Be specific about which.
2. WHAT I GAVE AWAY FOR FREE — every concession where I received nothing verifiable in return, and the specific sentence I used to give it.
3. THE HINGE MOMENT — the exact point where the negotiation was decided, and what I said.
4. THE ONE RULE TO ADD — a rule for my own pricing or negotiation policy that would have improved this outcome. Phrase it as an instruction to myself that I could paste at the top of my next quote.
5. THE CALIBRATION QUESTION — I assumed [something about their budget/authority/timeline]. What should I test earlier next time to know it faster?
6. WHAT TO REPEAT — one thing I did that I should keep doing, even though it felt like a mistake at the time.

Under 400 words. No encouragement. I do not need to feel better about it, I need to do it better.
```

---

## 07 订单交付 · Delivery

### P07-1 · 交付检查表生成

**中文说明：** 交单环节的遗漏是**真金白银**的损失：单证不符直接清关被卡。这个提示词生成可勾选清单。

```text
You are a trade documentation specialist. Generate a delivery checklist I can print and tick off, for an export order with these specifics.

ORDER FACTS:
- Product: [PRODUCT] and technical description as on the proforma invoice
- HS code (if known): [HS CODE]
- Incoterm + named place: [e.g. FOB Ningbo, / CIF Jebel Ali]
- Destination country and port: [COUNTRY, PORT]
- Buyer: [BUYER NAME]
- Payment method and stage: [e.g. 30% T/T deposit received, balance before shipment / L/C at sight confirmed]
- Shipping mode: [sea FCL LCL / air / rail / courier]
- Target shipment date: [DATE]

Produce three sections:

1. PRODUCTION & PRE-SHIPMENT INSPECTION — every checkpoint from PO confirmation to loading, with who is responsible for each (me / factory / third-party inspector / forwarder / buyer) and what evidence proves it is done. Include: what "passed" means, what photo or document is acceptable proof, and what happens if it fails. Flag the 3 checkpoints where skipping causes a dispute.

2. DOCUMENT SET — one row per document: exact name as it should appear, who issues it, when it must exist, how many originals, and the most common reason it is rejected at customs. For the certificate of origin and commercial invoice, give the exact required field list. Mark any document whose requirements vary by country with [VERIFY WITH BUYER'S BROKER].

3. SHIPPING & CASH FLOW — the milestone-by-milestone sequence from ex-factory to buyer receiving the goods, with the payment milestone attached to each step, and what I must have in hand before I release each payment. Include who bears risk at each point under the Incoterm I specified.

RULES:
- Every line must be checkable by a person standing at the container, not by a document reviewer.
- Never invent a document requirement. Write "UNKNOWN — confirm with [who]" instead.
- Mark clearly the items where the buyer's own broker has told me something different from standard practice, since buyer instructions usually win.
- End with the 5 items most likely to be missed in a first export, in order of cost if forgotten.
```

### P07-2 · 生产跟单与异常处理

**中文说明：** 生产过程中的延期、质量、降标——每种情况的应对。

```text
I am monitoring an order in production and something has gone wrong. Act as a production and supplier-management advisor. I need to know what to do in the next 48 hours, and what my leverage is.

PRODUCT / ORDER: [description, PO number, quantity, agreed spec, agreed price, Incoterm, shipment date, payment already made]
WHAT HAPPENED: [be specific — late by X days / material failed inspection / supplier proposed a cheaper substitute / quantity short-shipped / quality downgraded without telling me / factory went quiet / subcontracted the production]
WHAT I HAVE PROVEN: [photos, inspection report, messages — be honest about how solid this is]

Give me:
1. THE REAL ASSESSMENT — what is actually happening, separate from what the supplier is telling me. If their explanation does not fit the facts, say so plainly.
2. WHAT'S STILL SALVAGEABLE — can this shipment still ship on time and be accepted? Give a straight yes / yes-with-conditions / no.
3. MY NEXT 48 HOURS — hour-by-hour actions, with the wording I use with the supplier. Include the specific message that gets a straight answer instead of a reassuring one.
4. MY LEVERAGE — what can I actually do: stop payment, change the forwarder, withhold the balance, complain to the supplier's association, replace the goods elsewhere. Rank these by speed and by damage to my future business with this supplier.
5. THE FALLBACK PLAN — if the order cannot ship on time, the two best recovery options with real cost estimates, and which words I use with the buyer. Include how to tell the buyer before they ask.
6. WHAT TO PUT IN WRITING NOW — one short record I should send by email today that protects me later, without being hostile.

CONSTRAINTS:
- Do not assume the supplier is dishonest, but do not assume they are honest either. Give me evidence-based tests.
- Any cost estimate must be marked [ESTIMATE].
- Do not tell me to "communicate more" or "build a stronger relationship". Give me sentences and deadlines.
- If the honest answer is that I should ship late and apologise, say that.
```

### P07-3 · 收款与风险控制

**中文说明：** 单证和物流做得再好，收不回来钱等于没做。这个提示词梳理资金链风险点。

```text
You are a trade finance advisor. Structure the payment and risk picture for an export order so I can see where I am exposed and what I can still change.

ORDER FACTS:
- Buyer: [BUYER], in [COUNTRY]
- Incoterm and place: [TERM, PLACE]
- Invoice value and currency: [AMOUNT, CCY]
- Payment terms agreed: [e.g. 100% L/C at sight / 30% T/T deposit + 70% before shipment / O/A 60 days / D/P at sight]
- Amount already received: [AMOUNT] and how it was received
- Shipping mode and transit time: [MODE, DAYS]
- Insurance: [none / cargo insurance under CIF / warehouse-to-warehouse]
- Where my money actually sits: [how I fund production and for how long]

Deliver:
1. THE EXPOSURE TABLE — for each point in the transaction (ex-factory, loading, in transit, at destination, customs hold, final delivery), who bears risk, who bears cost, and when I actually get paid. Show clearly where there is a gap between "the goods move" and "the money arrives".
2. THE DANGEROUS CLAUSES — clauses in the agreed terms that hurt me, explained in plain terms, with the version I should have asked for.
3. WHAT I CAN STILL DO NOW — actions available before this order ships, in order of impact. Be concrete: who to ask, what document to request, what to change on the shipping documents while it's still legal.
4. THE FIRST SIGNAL OF TROUBLE — the earliest observable sign that this buyer will not pay on time, and the specific data I should check weekly to catch it.
5. THE RECOVERY LADDER — if payment is late, the escalation sequence with timing: who to contact first, at what day past due, what to demand at each step. Include the step where a formal demand letter and the last step where I involve a collections agency or legal counsel, with rough cost bands marked [ESTIMATE].
6. THE INSURANCE QUESTION — state whether cargo insurance is appropriate for this transaction and what it would and would not cover.

RULES:
- Do not invent exchange control rules, bank fees, or collection costs. Mark them UNKNOWN and name the authority to ask.
- Assume the buyer is good until a signal appears, but make the signals checkable.
- If the agreed terms are already bad, say so in the first two lines rather than burying it.
```

### P07-4 · 交付复盘与复购计划

**中文说明：** 交完货才是复购的开始。这个提示词把交付经验变成下一单的动作。

```text
An order has shipped or been delivered. Turn it into the foundation of the next order, and into a reusable process.

ORDER SUMMARY:
- Buyer, country, product, quantity, value
- From first contact to first payment: how long
- From payment to shipment: how long
- Total lead time and who caused the delays
- What went wrong, and what it cost me in money, in time, or in goodwill
- Buyer's response to delivery and to my documentation
- Whether this was a first order or a repeat

Give me:
1. THE HONEST POST-MORTEM — three things that went well and three that did not, each with the concrete consequence rather than a feeling.
2. THE REPEAT ORDER PLAY — how I ask for the reorder, when I ask (timing relative to their selling cycle), and what I offer to make the second order easier. Give me the actual message, English and Chinese.
3. THE GROWTH PLAY — the realistic next step up: a larger quantity, a second product from my range, a referral to their contact, a longer payment term they have now earned. Recommend one and say what it costs to ask for.
4. THE REUSABLE PROCESS — the 3-step routine I should repeat on every future order, and the 1 thing I should do differently each time.
5. THE DOCUMENT CACHE — the list of documents I should keep from this order as templates, and which ones need anonymising before I store them.
6. THE REFERRAL ASK — the exact wording to ask this buyer for two other people in their market who have the same problem I just solved for them. Most customers will give you names if you give them the sentence. Give me that sentence.

Under 500 words. No sentimentality. End with the single most valuable follow-up action and a deadline.
```

---

## 通用 · General

### P-GEN-1 · 环节自检（改文档时用）

**中文说明：** 自己写完环节文档后，让 AI 按贡献规范挑毛病。

```text
You are reviewing a stage document from an open-source repository that teaches foreign-trade beginners. The repo's quality rule is simple: every judgment must be decidable, and every instruction must be an action.

STAGE DOCUMENT:
[PASTE YOUR DRAFT]

Review it against these criteria and give me a numbered list of problems, worst first:

1. VAGUENESS — find every sentence that could not be used to make a binary decision about a real case. Quote each one. Suggest the specific rewrite.
2. UNACTIONS — find every step that describes a topic rather than an action. A step is only acceptable if a beginner could do it without being told where to go.
3. UNSOURCED NUMBERS — list every figure with no source, and mark which ones are likely wrong.
4. MISSING FAILURE CASES — list the mistakes this document would let a beginner make, and where the document fails to warn them.
5. COUNTRY/INDUSTRY OVERREACH — flag any statement presented as universal that is actually only true for some markets or some product categories.
6. EMPTY PHRASES — list every instance of motivational filler that carries no information.
7. STRUCTURE — confirm the six sections are present and in order: what this stage is for / how to do it step by step / pass-fail criteria / common mistakes / copy-paste templates / AI prompts for this stage.

Then give me the three highest-priority fixes, and do not rewrite the whole document for me. I want to learn what was wrong, not receive a replacement I have to re-read.
```

### P-GEN-2 · 行业环节包适配

**中文说明：** 把通用文档改成某个具体行业的版本。**写进 prompts 前先用它。**

```text
You are adapting a generic foreign-trade workflow to a specific industry, so that the advice is actually usable rather than generic.

MY PRODUCT: [PRODUCT CATEGORY] | MY TARGET MARKETS: [COUNTRIES/REGIONS]
THE GENERIC STAGE DOCUMENT I AM ADAPTING:
[PASTE]

Tell me:
1. WHAT THE GENERIC VERSION GETS WRONG FOR MY PRODUCT — where the advice would fail, be illegal, or waste time, because it assumes a different product's characteristics. Cover: specifications that matter, who the buyer actually is, what they actually buy on, how they qualify suppliers, and what they negotiate on besides price.
2. WHAT MY PRODUCT'S REAL SPECIFICATION SET IS — the fields a quote must contain, which are the ones buyers care about and which are noise.
3. WHO MY REAL BUYER IS — job titles, not company types. The specific person who signs, the person who specifies, and the person who blocks me.
4. THE INDUSTRY-SPECIFIC QUALIFICATION CHECKS — what a buyer or an inspection would check that has no equivalent in other industries.
5. THE CHANNEL REALITY — how this product actually reaches the end user in my target market, including who sits in between and takes a margin.
6. THE TRADE SHOWS AND ASSOCIATIONS THAT ACTUALLY MATTER for this product in this market, and what is verifiable about each rather than what is commonly claimed.
7. THE THREE THINGS A BEGINNER WILL GET WRONG in my industry, in the order they will go wrong.

RULES:
- Do not invent certifications, standards, or test requirements. Write "UNKNOWN — verify with [authority]" for anything you cannot confirm.
- Prefer specifics over categories. "Distributors with [X] profile" beats "the B2B segment".
- If my product has genuine regional variation, say where the variation lies and which of my target markets needs which version.
```

---

## 贡献新提示词

提交 PR 时请在文件末尾追加，并遵守 [CONTRIBUTING.md](../CONTRIBUTING.md) 的自查清单：

- [ ] 每条提示词是**完整可粘贴文本**，不是要点罗列
- [ ] 方括号占位符 `[...]` 全部填了中文说明
- [ ] 编号符合 `P{环节号}-{序号}`
- [ ] 输出格式是明确指定的（表格 / 编号 / 字段清单）
- [ ] 没有让 AI 代替人做判断的指令
- [ ] 任何数字要么是用户自己提供，要么被标为 `[ESTIMATE]` / `UNKNOWN`
- [ ] 提示词里没有编造的法规、认证、费率、市场数据
