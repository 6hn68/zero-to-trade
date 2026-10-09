# AI 提示词总库 · 27 条能直接抄走的英文稿

这里躺着 27 条提示词。它们的作用不是替你思考，是替你打字，以及在你脑子已经转不动的那个晚上，替你把事情一条条列出来。

**怎么用：整段复制，粘进对话框，`[...]` 里的东西换成你自己的，回车。** 方括号别留着——留着的话，AI 会给你一篇挑不出毛病、也一句用不上的通稿。

## 三句废话，但不说你一定会忘

1. **它出的东西一律当草稿。** 物流费、认证费、汇率，它编起来毫不脸红，而且编得特别具体，具体到你差点就转发给客户了。数字一律自己核。
2. **空着的方括号 = 通稿。** 你的产品、目标价带、客户国家、谈了多久，能填的全填。输出质量差多少，取决于你填了多少。
3. **判断是你的活。** 让它整理、生成、列选项、找茬。**它不知道你的工厂能不能做这个单，也不知道你赔得起多少。**

## 每条提示词的四件事

| | 在哪儿 | 干什么用 |
|---|---|---|
| **往里填** | 说明下面第一行 | 复制前先把这些占位符换了，少一个就多一轮废话 |
| **吐出来的** | 说明下面第二行 | 表格 / 条数 / 字数上限。写了字数上限的，**超了就让它重写，别读** |
| **别全信** | 说明下面第三行 | 这一条里最容易出假货的地方。**看到这行提到的东西，自己去核一遍** |
| **提示词正文** | 代码块里 | 英文。喂给 AI 的，逐字复制，语气不必改 |

## 编号与 P.S.

编号规则是 `P{环节号}-{序号}`，比如 P03-2 是环节 03 的第 2 条。

一句实话：**`docs/` 里的 7 篇环节文档各自在「AI 提示词」那一节复制了整段提示词**，标题写的是「提示词 1/2/3」，跟这里的编号对不上（历史遗留，我们也知道别扭）。两边不一致的时候，**以你手上这一份为准**，也欢迎顺手提 PR 把那边的重复内容删掉改引用。数量别动：**三个 README 里都写着 27 条**，加一条它们就错了。

---

## 01 选市场 · Pick a Market

### P01-1 · 三维打分与首站市场选定

**往里填：** `[PRODUCT CATEGORY]`、`[TARGET REGION]`、`[BUDGET USD]`、`[YEARS]`、`[LIST OF 5-8 COUNTRIES]`
**吐出来的：** 一张打分表 + 三句辩护 + 两个反驳承认。全文上限 700 词。
**别全信：** 关税率和认证时长。它给的数字，保质期大概和你冰箱里的生菜差不多。

候选国家扔给 AI，它十有八九会说"都挺好的"。这条的作用是把"都挺好"堵死：排得出第一名、写清凭什么排它、再自己交代哪条理由最站不住。

```text
Evaluate these candidate markets for my first export entry: [LIST OF 5-8 COUNTRIES].

Context: I sell [PRODUCT CATEGORY] to [TARGET REGION]. Budget for travel, samples, certifications and channel setup: [BUDGET USD]. I have [YEARS] years of export experience, none of it in this region.

Score each country 1-10 on three dimensions, and state the evidence behind every score:
1. LANGUAGE BARRIER — How much of my sales cycle is lost to language? Can I find local trade data in English, do buyers there negotiate in English, is Arabic/Spanish/etc. required?
2. DEMAND FIT — Is there real, current demand at MY price band? Not "they buy this product" but "they buy this product at this price with these specs".
3. ENTRY BARRIER — Tariff and duty burden, mandatory certifications (name them), local agent exclusivity, payment risk, and how long certification realistically takes.

Then:
- Rank all candidates.
- Pick ONE first market and defend it in exactly three sentences.
- Give the two strongest objections to that choice, and how I would test whether each objection is real before spending money.
- Name the ONE country you would pick if the budget were 10x smaller.

OUTPUT: Markdown tables, every cell on one line.
ANTI-HALLUCINATION: If you are not certain about a rate, a requirement, or a timeline, write "UNKNOWN — verify by: [how to verify]". Do not approximate a number you do not have. Do not pad with "promising market", "significant potential", or "good growth prospects" — I want evidence and numbers, not adjectives.
STOP: Under 700 words. If you cannot decide in 700 words, you have not scored tightly enough.
```

### P01-2 · 需求真实性反查

**往里填：** `[COUNTRY]`、`[PRODUCT]`、`[MY PRICE BAND]`
**吐出来的：** 5 条证伪理由 + 每条的低成本核验办法 + 我自己要算的那笔账。上限 600 词。
**别全信：** 宏观数字。进口额很大和你卖得出去是两回事，这条专门拆这个。

"这个市场很大"是外贸里最贵的一句话。这条让 AI 专门去找反证——它的任务不是附和你，是劝退你。劝得住就省你半年。

```text
Someone has just claimed [COUNTRY] is a great market for [PRODUCT]. Your job is NOT to confirm it. Your job is to find the strongest reasons that might be wrong, then give me an honest read.

Provide:
1. Five specific reasons this market might NOT work for me at my price band ([MY PRICE BAND]).
2. For each reason: what would have to be true for it to be false, and how I check that cheaply in under a week.
3. Translate any macro figure you cite into MY terms: at my price point and typical order size, how many orders per month would I need for this market to be worth my time? Show the arithmetic.
4. Name three existing suppliers already active in this market. If you cannot name them from verifiable sources, write "COULD NOT IDENTIFY" — that itself is a finding about how visible this market is.
5. One sentence: the single most likely reason I will fail here.

Be concrete. Cite source names and dates. If a figure comes from a paywalled report you cannot read, say so instead of guessing. Mark anything you are not confident about as "UNVERIFIED".
STOP: Under 600 words. Five reasons, not fifteen.
```

### P01-3 · 准入成本清单

**往里填：** `[COUNTRY]`、`[PRODUCT CATEGORY]`、`[CHANNEL]`
**吐出来的：** 六段 classified 清单，每段一张表，成本一律待核。上限 800 词。
**别全信：** 每一个金额和每一个周期。**它编一个认证费，比它承认不知道容易得多**——这条的价值在条目，不在数字。

能不能进一个市场从来不是判断题，是一张费用单。清单它来列，金额你自己打电话问。反过来会出事。

```text
Build me a market-access checklist for [COUNTRY] and [PRODUCT CATEGORY]. I am a direct exporter, not a trading company, selling through [CHANNEL: direct B2B / local distributor / marketplace / trade show leads].

Six sections, each as a Markdown table:

1. COMPANY REGISTRATION — what entity I need locally, cost, lead time, issuing authority.
2. PRODUCT CERTIFICATION & CONFORMITY — every certification, each marked MANDATORY / USUALLY REQUIRED / RARELY REQUIRED. For each mandatory one: full name, issuing body, cost range, lead time range in weeks, and whether it can be completed before I have a confirmed order.
3. IMPORT DUTIES & TAXES — HS code structure for my product, duty rate if known, VAT/GST rate, any special conformity regime (e.g. Gulf-style GSO/SABER schemes) that applies.
4. LABELING & PACKAGING — language requirements, mandatory declarations, unit-of-measure rules.
5. DOCUMENTS A BUYER WILL ASK FOR — commercial invoice, packing list, bill of lading, certificate of origin, insurance, plus anything specific to this country.
6. PAYMENT & RISK — normal payment terms in this market, preferred method, who bears credit risk, typical dispute mechanism.

CRITICAL RULES:
- Mark EVERY cost figure "ESTIMATE — verify with: [which authority or consultancy]".
- Every lead time must be a range, never a single number.
- Anything you are unsure about: write "UNKNOWN". An invented certification cost costs me more than a blank cell.
- End with the 3 items on this list that most often surprise first-time exporters, and why.
STOP: Under 800 words. Six tables, no prose.
```

---

## 02 找客户 · Find Leads

### P02-1 · 四路线索挖掘方案

**往里填：** `[PRODUCT]`、`[COUNTRY/REGION]`、`[PRICE BAND]`、`[ORDER SIZE]`、`[IDEAL CUSTOMER PROFILE]`、`[HOURS]`
**吐出来的：** 四路各自的搜索配方 + 七天爬坡表 + 停手规则。上限 800 词。
**别全信：** 每日产出量的估算。**它是按平均情况猜的，你的名单质量决定了它错多少。**

新人找客户典型的一天：打开浏览器，搜了四个词，关掉，开始怀疑人生。这条把"找客户"拆成每天能数出来的动作，并且让 AI 说实话——按你每天这点时间，你要的那个数是够呛的。

```text
Design a daily lead sourcing routine for me. I export [PRODUCT] to [COUNTRY/REGION]. Price band [PRICE BAND], typical order [ORDER SIZE]. Target customer: [IDEAL CUSTOMER PROFILE — e.g. "importing distributor with 3-8 branches, currently buying from China"]. I have [HOURS] hours per day.

Cover FOUR channels: customs/import data, social media, web search, trade shows. For each, specify:
1. THE SEARCH RECIPE — the named source (site, database, group, show), the exact filter values, and the fields I export. "Search on Google" is not an answer; give me the filters.
2. THE DAILY QUOTA — raw records to pull per day, and the realistic percentage that will actually be usable. I would rather have 20 real leads than 200 junk ones.
3. THE VERIFICATION STEP — how I confirm a record is a real, active, reachable business before spending time on it.
4. THE FAILURE MODE — the single most common way this channel wastes time for someone selling my product, and how to avoid it.

Then produce:
- A 7-day ramp-up plan: what I do on day 1 vs day 7, with volume targets.
- A weekly output target stated as: leads pulled / leads verified / leads worth contacting.
- A rule for when to abandon a channel and move on.

Be honest about my [HOURS] hours/day: if my target is wrong for that time budget, say what is actually achievable and what I should trade off.
ANTI-HALLUCINATION: Do not invent filter names, database fields, or member counts for any source. If you are unsure a source has a feature, write "VERIFY ON SITE".
STOP: Under 800 words. Four channels, no fifth.
```

### P02-2 · 线索清洗、合并与批量定级

**往里填：** 你那一坨原始名单（海关数据、展会名录、LinkedIn 导出的，原样粘）
**吐出来的：** 一张去重后的表 + 一张被合并记录清单。**列名必须照抄下面那行**，否则喂不进 `scripts/lead_score.py`。
**别全信：** 它判定的"同一家公司"。同名不同国是两家，这条里写了，它偶尔还是会犯。

手工整理名单最烦的是同一家公司出现五次、五种拼法。这条让 AI 归并 + 批量排优先级，排完**直接落成一 CSV 喂给 `lead_score.py` 算分**——AI 打分会手抖，脚本不会。

```text
Clean, deduplicate and priority-rank this B2B lead list. The same company appears several times with different spellings, different contact people and inconsistent country formats.

RAW DATA:
[PASTE YOUR RAW LEAD LIST HERE — keep the original column headers]

WORK:
1. NORMALIZE — one country format, standardized company suffixes (Ltd/Limited/LLC/Co., LLC), tracking parameters stripped from URLs, email domains lowercased.
2. MERGE — group records that are clearly the same company. State confidence (HIGH / MEDIUM / LOW) for every merge and give the evidence.
3. FLAG CONFLICTS — where one company has two emails, two websites or two countries, list the conflict, say which value you kept and why.
4. RANK — for each surviving row give Priority A (contact within 3 days) / B (within 2 weeks) / C (backlog), plus Contactability 0-5 and Confidence 0-1. Use only information present in my data; if it is thin, drop Confidence rather than inventing detail.
5. DUMP LIST — every record you merged, so I can spot-check.

OUTPUT a single Markdown table with EXACTLY these column names, in this order:

company,country,product,source,email,phone,years,contact,note

- source must be one of: referral / trade_show / customs / linkedin / search / unknown
- years = number of years the business has existed (a bare number, e.g. 12)
- contact = the named person's role, e.g. "purchasing manager"
- note = one compressed line: positioning, import evidence, size signals, red flags
- Every remaining column left empty must be blank, never "N/A" or "-".

RULES:
- Never invent an email, phone, website or person. If the input has none, leave it blank.
- Never merge two companies on name similarity alone. Same name in two countries = two companies.
- Never delete a record silently: every input row appears either in the table or in the dump list with a reason.
- country, product, source, email, phone, years, contact, note are optional; company is not.
- After the table, give me the SAME rows again in CSV form (header line included) so I can save it as-is.
- Three lines at the top explaining your merge rules, before any table.
STOP: Table only after those three lines. No summaries of what you did.
```

**存成 CSV 之后直接接着跑**——两个脚本读同一份文件，同一个九列表头：

```bash
python scripts/lead_score.py my_leads.csv --format detail   # 算 T0-T3，顺便告诉你分是怎么来的
python scripts/outreach_gen.py my_leads.csv --tier T0       # 给今天该打的那几家出文案
python scripts/followup_plan.py --tier T1 --start 2026-03-02 --market gcc   # 排带日期的跟进
```

> 脚本只读这 9 列。**官网地址别塞进 `product` 或 `note` 以外的列**——塞进去也不会加分，`lead_score.py` 压根不读 `website`。

### P02-3 · 搜索式速查表

**往里填：** `[COUNTRY]`、`[PRODUCT CATEGORY]`
**吐出来的：** 三块共至少 23 条查询串，一张四列表。不用设字数上限，表越长越好。
**别全信：** 每条后面的"误命中率"。那玩意儿是它估的，跑一遍你自己就有数了。

搜索算子这种东西，自己想三分钟想不出，看别人写的又一行都想抄。这条直接给你一整张能粘贴的表。提醒一句：**这是找信息用的，不产客户名单。**

```text
Build me a cheat sheet of search queries to research companies in [COUNTRY] that buy or distribute [PRODUCT CATEGORY].

BLOCK A — DISCOVERY (find candidate companies). At least 10 Boolean strings I can paste as-is, shaped like:
site:[TARGET_COUNTRY_TLD] "PRODUCT" distributor
"PRODUCT" "COUNTRY" importer filetype:pdf
For each: what it tends to surface, and its likely false-positive rate.

BLOCK B — QUALIFICATION (check one named company). At least 8 queries using a placeholder company, e.g. "[COMPANY]" annual report, "[COMPANY]" import records, "[COMPANY]" distributor "MY BRAND".

BLOCK C — NEGATIVE (surface trouble). At least 5 queries that catch lawsuits, sanctions, non-payment complaints, fraud reports, shutdowns, or unsatisfied importers.

For every query mark which country-specific or language-specific terms I should swap in. If a query only works in English, say so — English coverage may be thin in my market.

FORMAT: one Markdown table — query | what it finds | false positive rate | notes.
ANTI-HALLUCINATION: Only give operators that actually work on the search engines you assume. State which engine each block assumes. If you are unsure an operator is supported, write "TEST FIRST". Do not invent site names, directories or registries — if you cannot name a real one, leave that slot to me.
STOP: Exactly three blocks — A, B and C, in that order. No fourth block, no "bonus" queries beyond the minimum counts stated above.
```

---

## 03 背调客户 · Vet the Buyer

### P03-1 · L1 快速筛查（淘汰骗子）

**往里填：** `[COMPANY NAME]`、`[COUNTRY]`、`[URL OR "NONE FOUND"]`、`[NAME, TITLE, EMAIL]`
**吐出来的：** 一个结论 + 七行判定 + 红旗清单。三分钟读完，不许超 300 词。
**别全信：** 反过来信——**这条假设对方是骗子**，七项里缺三项就 pass。心软的人在这一步能浪费掉整个职业生涯。

> `docs/03-due-diligence.md` 里那套「L1 四问」是两分钟速查版，这儿是它的完全体。四问用来当场扫一条，七项用来定案。

```text
Screen this potential buyer for fraud and non-payment risk. Fast and blunt, then stop.

BUYER: [COMPANY NAME]
COUNTRY: [COUNTRY]
WEBSITE: [URL OR "NONE FOUND"]
CONTACT: [NAME, TITLE, EMAIL]

Check exactly these seven items:
1. Website — does it load, is there a real company address and phone, or a template with placeholders left in.
2. Registration — any verifiable registration record for this name? State the registry or source you checked.
3. Age — how long has the business existed? Earliest evidence of activity (year, first social post, first mention).
4. Social accounts — do they exist, and were they active in the last 90 days or dormant/empty.
5. Email domain — own domain or free mailbox? If free, does the person have any other traceable footprint?
6. Contact plausibility — does the email local part match the person's name, and does the job title match the claim?
7. Import footprint — any sign at all that this company imports goods, from anywhere, in any volume.

OUTPUT:
- VERDICT: KILL / PROCEED TO L2 / UNCLEAR
- For each of the 7 items: FOUND / NOT FOUND / CONTRADICTORY, plus one line of evidence and its source.
- RED FLAGS: every contradiction found. Say "none" if none.
- CONFIDENCE: HIGH / MEDIUM / LOW, and what would raise it.

RULES:
- Assume fraud until these seven items say otherwise. A professional-looking site is not evidence.
- Never guess an email, address or registration number.
- If you cannot reach a source, write "COULD NOT CHECK: [source]". No substitutions.
- One missing item is not a red flag. Three or more missing items force a KILL verdict.
STOP: Under 300 words. I need a decision, not a report.
```

### P03-2 · L2 标准背调（判断值不值得投入）

**往里填：** `[NAME]`、`[COUNTRY]`、`[PRODUCT]`、`[BAND]`
**吐出来的：** 六段，含一组收入/人数区间和一个成交概率百分数。上限 600 词。
**别全信：** 那个百分数。**它是猜的，而且它自己不知道自己在猜。**看它的推理链，别看那个数字。

L2 就是算账：这家能给我多少量、多大可能付钱、配我多少时间。区间可以让它给，最后那个成交概率，你自己改。

```text
Give me a commercial judgment on this buyer, not background reading. I have already run an L1 screen and it passed.

COMPANY: [NAME] | COUNTRY: [COUNTRY] | MY PRODUCT: [PRODUCT] | MY PRICE BAND: [BAND]

Produce:
1. SIZE & CAPACITY — annual revenue band, employee band, number of locations, and the reasoning chain from whatever public data exists to those bands. Show your work. Mark each band LOW / MEDIUM / HIGH confidence.
2. LIKELY ORDER REALITY — given their size and channel position, what quantity and frequency should I realistically expect? Give conservative / likely / optimistic cases.
3. PAYMENT BEHAVIOR RISK — score 1-5 (5 = safest) on how they typically pay, whether they ask for credit terms early, whether this market has a slow-payment problem, and whether enforcement is practical. One line per score.
4. CHANNEL POSITION — end user, distributor, retail chain, or trading company? What does that mean for order size and how hard I must work to close?
5. WHAT WOULD MAKE THIS A PRIORITY — the 3 concrete signals that justify me spending my best effort here.
6. THE PROBABILITY — a percentage estimate that this becomes a repeat buyer within 6 months, plus the single biggest reason it might not.

RULES:
- Every number carries either a source or an explicit "[MY ESTIMATE]" tag. Untagged numbers will be treated as invented.
- No motivational language. No "this is a great account". I want a verdict.
- If public data is too thin to support any of this, say so plainly and give the two cheapest ways to get better information (e.g. one call to a trade office, one industry-association contact).
ANTI-HALLUCINATION: Do not infer size from how polished their website looks. Do not estimate revenue from employee counts without saying you did that.
STOP: Under 600 words. No preamble.
```

### P03-3 · L3 深度背调（谈单前 90 分钟）

**往里填：** `[NAME]`、`[COUNTRY]`、`[NAME, TITLE]`、你 L1/L2 的输出、你已经跟他说过的话
**吐出来的：** 三个部分，含一段开场白和七个必问的问题。上限 700 词。
**别全信：** 那些"关于他们的事实"。**已知和推断必须分两栏写**，混在一起你就分不清哪句能直接说出口了。

到这步说明你真打算投入了。产出不是报告，是一份能照着打电话的提纲，和一堆你必须问到答案的问题。

```text
Prepare me for a first serious commercial conversation. My goal in this call is NOT to close — it is to leave knowing whether this account is real, whether there is budget, and who actually decides.

COMPANY: [NAME] | COUNTRY: [COUNTRY] | THE PERSON I'M MEETING: [NAME, TITLE]
WHAT I KNOW SO FAR: [paste your L1 and L2 output]
WHAT I'VE ALREADY ASKED THEM: [what you've said so far]

Deliver three things:
1. THINGS THAT ARE TRUE ABOUT THEM — facts I can state confidently in the first 60 seconds. Two columns: VERIFIED vs INFERRED. Never blur them.
2. THINGS I STILL DON'T KNOW, RANKED — order by "if the answer is bad, would I walk away?" Those first.
3. THE CALL PLAN —
   a. Opening: 3 sentences I can say out loud, specific to this company, no generic pleasantries.
   b. Seven questions I must get answered. For each: the question, why I am asking, and what a good answer sounds like versus a bad answer.
   c. Two questions that sound polite but are qualification questions, so they don't notice they're being vetted.
   d. Three questions I should NOT answer directly in this call.
   e. The single question whose answer tells me whether to send a quote.

RULES:
- Every personalized item must reference something specific to THIS company. If you cannot make it specific, label it GENERIC and tell me to fill it in.
- Bad answers must be concrete and quotable, e.g. "if they say 'we pay after inspection', ask who inspects and who pays the inspection fee".
- Do not pitch. I want to know, not to sell.
ANTI-HALLUCINATION: Do not invent people, titles, certifications, contract values or news about this company. Every claim about them must be traceable to what I pasted, or written as "NEEDS VERIFICATION".
STOP: Under 700 words.
```

### P03-4 · 背调结论转行动清单

**往里填：** 你那一堆背调笔记（越乱越好，它就干这个的）
**吐出来的：** 六个部分，其中一个是"别再查了"。全文 400 词以内。
**别全信：** 它给的时间预算。**那个数字是拿来约束你的，不是建议。**

背调是会上瘾的。查到第三家的时候你已经忘了自己是要卖货的。这条把结论压成下周的三件事，还规定你这季度最多花多少分钟——包括你在这儿继续纠结的那部分。

```text
Convert this research into action. I have a habit of over-researching and under-contacting, so cut it down and force a decision.

RESEARCH NOTES:
[PASTE YOUR BACKGROUND RESEARCH HERE]

Give me back:
1. THE ONE-LINE VERDICT — A, B, or C grade, with the single reason that determined it.
2. WHAT I AM WRONGLY ASSUMING — at most 3 things I seem to believe that the evidence does not support.
3. THE NEXT 3 ACTIONS — each with: the action, the weekday to do it, roughly how long it takes. "Research more" is not an acceptable action.
4. WHAT I SHOULD DELIBERATELY IGNORE — information I could chase that would not change the grade or the next action. Be honest and ruthless here.
5. THE TRIGGER TO RE-CHECK — what would make me reopen this file, stated specifically (a news item, a price change, N days of silence).
6. THE TIME BUDGET — total minutes I should ever spend on this account this quarter, as a hard number. Be stingy.

Output plain Markdown, under 400 words, no preamble.
ANTI-HALLUCINATION: Work only from the notes I pasted. Do not invent a verdict, a re-check trigger, or a time budget I never implied. If a section needs a fact I did not give, write "NEEDS INPUT:" and say what. Do not dress your guess up as my conclusion.
STOP: Exactly six sections. If section 4 is empty, you were not ruthless enough.
```

---

## 04 建联客户 · Make Contact

### P04-1 · 三线并进首触方案

**往里填：** `[COMPANY]`、`[COUNTRY]`、`[CHANNEL]`、`[PRODUCT]`、`[SPECIFIC ANGLE]`
**吐出来的：** 三个渠道各自的 tailored 文案（中英各 120 词内）+ 排期表。
**别全信：** 时间段建议。**它不知道你客户的宗教节日和当地作息，你自己核日历。**

首触三线并行，不是同一段话群发三遍——一个采购同日在三个通道看到一模一样的话，只会得出一个结论。另外：英文首触文案 `scripts/outreach_gen.py` 已经能出一版了，**能用脚本就别让 AI 现编**，脚本不会临时编一句你厂里做不到的承诺。

```text
Design a first-touch sequence for a B2B export sale.

Buyer: [COMPANY], in [COUNTRY], found via [CHANNEL]. My product: [PRODUCT]. My angle: [SPECIFIC ANGLE — e.g. "we already supply a distributor in their neighbouring country with the same spec"].

Three channels: [EMAIL] + [WHATSAPP/LINKEDIN] + [one third channel of your choice, justified].

For each channel:
1. THE ANGLE — why this channel, for this buyer, right now. If a channel adds nothing, say so and drop it.
2. THE MESSAGE — the actual copy, English plus Chinese, under 120 words per language. Subject line included for email.
3. THE TIMING — which day and roughly what hour local time in the buyer's country, justified against that time zone's working pattern.
4. THE FAILURE MODE — the most likely way this gets ignored, and the one change I would make if it is.

Then give me:
- The sequence order with the gap between touches in days.
- What a response triggers at each step, and what silence triggers.
- The single message doing the most work in this sequence, and why.

CONSTRAINTS:
- No "Dear Sir/Madam", no "I hope this email finds you well", no "we are a leading manufacturer with 20 years of experience" unless I gave you that number.
- First email must be trivially easy to reply to, even with "not interested". Ask something answerable in one word.
- Plain text only. No HTML, no images, no attachments on first touch.
- The three messages must say the same thing to the same persona but be different text. Same copy across channels reads as bulk mail.
ANTI-HALLUCINATION: Do not attribute a fact to this buyer (a purchase, a post, an expansion, an award) that I did not supply. Anything you want to reference but cannot source goes in as "[FACT I NEED: ...]".
STOP: Under 800 words total.
```

### P04-2 · 拒绝理由分类与应对

**往里填：** 你这周收到的真实回复原文（"no thanks"、"too expensive"、"call me next week"，有多少粘多少）
**吐出来的：** 每条回复一行 + 三句更容易被回的主题行。上限 600 词。
**别全信：** 它判的"大概率还有戏"。**乐观是这个模型的默认设置。**

"send us your catalogue" 可能是真兴趣，也可能是最客气的再见。这条给它们分类，每种配一句你马上能发出去的话。

```text
I run outbound B2B sales and keep losing people in the first two contacts. Below are the actual replies I got this week. Which are normal noise, which are real warnings?

RESPONSES:
[PASTE YOUR REAL REPLIES — "no thanks", "send us your catalogue", "too expensive", "we are busy", "not interested", "call me next week", anything else]

For each response:
- WHAT IT ACTUALLY MEANS — three candidates: real rejection, polite brush-off, or genuine interest disguised as a brush-off. Pick one.
- THE PROBABILITY this buyer is still reachable — low / medium / high, with reasoning.
- THE ONE ACTION I take next, as a single specific sentence I could send.
- HOW LONG I wait before the next touch, in days.

Then:
1. Which of these am I most likely misreading? Point at the one.
2. Which single response should I stop treating as a rejection? Argue for it.
3. Three subject lines more likely to get a reply, built from [MY PRODUCT] and [BUYER'S ACTUAL BUSINESS DESCRIPTION].
4. Which replies signal a lead-quality problem rather than a copy problem, and what to fix upstream.

Be direct. If a response is genuinely ambiguous, say so and give me a tiebreaker question.
ANTI-HALLUCINATION: Work only from the replies I pasted. Do not invent quotes, do not assume context I did not give. Do not invent open rates or reply-rate benchmarks — there is no number either of us can cite.
STOP: Under 600 words. One row per response, no essays.
```

### P04-3 · 跟进话术变体生成器

**往里填：** 你的第一封信 + 已经发过的跟进信
**吐出来的：** 第 2、3 触达的中英文文案 + 排期。**只到第三次——脚本 `followup_plan.py` 的止损线是 MAX_TOUCHES=3，第三次之后无论发生什么都不再发。**
**别全信：** 它说"这封和第 1 封不重复"。**自己读一遍，十次里有三次它换了个连词就当新理由了。**

同一封信发七次不会提高回复率，只会提高你域名进黑名单的概率。所以这条只负责让你每次都存在得有点道理——**第三次必须是收尾**，不是"再试一次"。

```text
Write the follow-up touches for a prospect who went quiet after my first email. I do NOT want to resend the same email in different words.

FIRST EMAIL:
[PASTE IT]

FOLLOW-UPS ALREADY SENT:
[PASTE THEM]

Generate the remaining touches up to touch #3, inclusive. #3 is the last one I am willing to send. Rules:
- Each touch must exist for a DIFFERENT reason. Pick from: new information, new question, new proof point, narrowing the ask, graceful close-out. State which one each touch uses and why it is not a repeat.
- Each touch under 80 words. Shorter than the first email — each one costs less attention than the last.
- English version and Chinese version for each.
- Touch #3 must be a genuine close-out: either a clean one-line "shall I close your file, or would you prefer I check back in [MONTH]?" or a graceful goodbye that leaves the door open. No fake urgency, no fake deadlines, no manufactured scarcity.
- Subject line for each touch. Reusing one across touches is sometimes the right call.
- Never write: "just following up", "circling back", "did you see my last email", "I understand you're busy", "not to be a bother".
- Where a touch needs a fact I have not given you, insert [FACT I NEED: ...] rather than inventing one.

Then give me the cadence: which day each touch goes out, and what to do if they reply to any of them. Also state the stop condition in one line: what happens after #3 gets no response.
ANTI-HALLUCINATION: Do not credit this prospect with an action they did not take (opening an email, visiting the site, forwarding it internally). I have no such data and neither do you.
STOP: Touches #2 and #3 only. Do not propose a #4.
```

### P04-4 · 沉默客户的收尾与重新激活

**往里填：** `[Who they are, what product, what you quoted or discussed, what channel you used]`
**吐出来的：** 六个部分，含一封 30 词的收尾信。全文 300 词以内。
**别全信：** 它排的沉默原因概率榜。**第一位是不是"他根本不想买"，你自己心里有数。**

到第 3 封还没回，答案是收尾，不是再发一封。这条给你一句不卑不亢的收尾，外加一个具体到能写进日历的重新联系条件——不接受"等市场好转"这种回答。

> 排期别自己造：`python scripts/followup_plan.py --tier T1 --start 2026-03-02 --market gcc` 会按对方的工作日帮你算，周五主麻日它也会避开。

```text
A prospect got my three allowed touches and stayed silent for 35 days. I need to decide whether to close the file, and what would justify reopening it.

DEAL CONTEXT:
[Who they are, what product, what you quoted or discussed, what channel you used]

Give me:
1. THE DIAGNOSIS — the likely reasons for the silence, ranked. Be honest if "they simply don't want to buy" is number one.
2. KILL OR KEEP — one verdict, plus the single condition that would change it.
3. THE CLOSE-OUT MESSAGE — a 30-word email that closes the loop gracefully and leaves a way back in. English plus Chinese. No resentment, no "did I do something wrong", no passive-aggressive "I'll assume you're not interested".
4. THE REACTIVATION TRIGGER — one concrete trigger worth contacting them for again: a specific event, date, or change in my offering. Not "when the market improves".
5. THE LAST-RESORT CHANNEL — one channel I have NOT tried, and exactly when it is worth trying. Say "none, let it go" honestly if that is the answer.
6. WHAT TO CHANGE NEXT TIME — one change to how I sourced or approached this account that would have improved the odds. Do not skip this one; it is the only part that compounds.

Under 300 words.
ANTI-HALLUCINATION: Do not invent signals about this prospect (site visits, LinkedIn views, company news). Work from what I told you plus general reasoning, and label the general reasoning as such.
```

---

## 05 聊单 · Talk Specs

### P05-1 · 需求澄清问题清单

**往里填：** `[PRODUCT]`、`[COUNTRY, MARKET SEGMENT]`、`[BAND]`
**吐出来的：** 一张四列表，10 个必问 + 分好类的辅助问题。上限 700 词。
**别全信：** 它说"这题是致命项"。**你自己的产品你知道。**

报价前不问规格，等于先把价格交出去，再求人别砍。这条给你最少的必问题，还带一个小把戏：先问最容易答的，让对方先动起来——人一旦开始回答，就比较容易继续回答。

```text
Prepare me for a first technical conversation with a buyer who has asked for a quotation. My job is NOT to quote and NOT to close. It is to get specific enough that a later quote cannot be wrong, and to get the buyer investing a little effort so they feel ownership.

PRODUCT: [PRODUCT] | BUYER: [COUNTRY, MARKET SEGMENT] | MY PRICE BAND: [BAND]

Give me:
1. THE MINIMUM VIABLE SPEC SHEET — cap it at 10 questions. Every question must change the price or change whether I can serve them at all. Flag 3 deal-breakers versus 7 refinements.
2. THE THREE SMALL ASKS — three easy questions to ask FIRST, before anything heavy, ranked by how easy they are to answer.
3. THE QUESTIONS THAT LOOK LIKE SMALL ASKS BUT ARE SCREENING — 2 that sound like spec questions but tell me whether this buyer is serious. Explain the tell for each.
4. THE QUESTIONS TO SAVE FOR THE SECOND CALL — 3 I should deliberately NOT ask now, because asking too early shows I don't know my own product or gives away my cost structure.
5. THE QUESTIONS THAT EXPOSE A BUYER WHO CAN'T ANSWER — 3 a serious buyer answers instantly. Hesitation is information.

OUTPUT: numbered Markdown table — # | Question (English) | 问题（中文） | Deal-breaker or refinement | Why it matters.
Also flag any row that needs a quantity, a container split, or a pallet count — those feed the loadability math later.

RULES:
- Ask like a supplier genuinely trying to quote correctly, not like a form being filled in.
- No yes/no question unless you state what each specific answer reveals.
ANTI-HALLUCINATION: Do not invent industry standard specs, tolerances, or certifications for this product category. Anything product-specific you are unsure about goes in as "[CHECK WITH FACTORY]".
STOP: Ten rows maximum in section 1. Under 700 words overall.
```

### P05-2 · 询盘分类与优先级

**往里填：** 这周的询盘原文（带上公司名、国家、问的产品、他怎么说的、从哪找到你的）
**吐出来的：** 每封一串 rank + 一句能直接发的回复（中英）。上限 700 词。
**别全信：** 它排的第 1 名。**模型天生偏爱写得长的询盘，字数多不等于会下单。**

一堆询盘回来，先回哪个？AI 能排序，但"看着最诱人"和"最可能下单"经常不是同一封。这条专门把这两个分开指出来。

```text
Below are inbound inquiries I got this week. I cannot answer all of them today. Rank them.

INQUIRIES:
[PASTE YOUR INQUIRIES — company name, country, product asked about, what they specified, how they found you, and tone]

Rank on:
- FIT — does this fit my actual range, or is it a "can you also make this" request?
- SPECIFICITY — real specs and quantities, or a one-line "price please"?
- CREDIBILITY — verifiable company footprint, or a free-mailbox address asking for my lowest price?
- URGENCY SIGNAL — is there a real timeline in the message, or is "urgent" doing all the work?
- EFFORT COST — how much of my day does answering properly take?

For each inquiry:
1. RANK 1-5 (1 = answer today).
2. WHICH SIGNALS DROVE THE RANK — one line each.
3. THE EXACT REPLY — drafted, English plus Chinese, appropriate to that rank. Rank 1 asks 5 specific questions. Rank 5 gets a short polite reply that keeps the door open without giving anything away.
4. THE TELL TO WATCH — one specific thing in their reply that moves them up or down a rank.

Then answer directly: which single inquiry is most likely to become a real order, and which one looks most attractive but is most likely to waste my day?

Do not tell me to be polite. Tell me what to reply.
ANTI-HALLUCINATION: Judge only what is in the messages I pasted. Do not research or assume these companies. If a detail about them is missing, lower Credibility rather than filling it in. Do not cite reply-rate or conversion statistics.
STOP: Under 700 words. No commentary on my business strategy.
```

### P05-3 · 报价前的规格确认单

**往里填：** `[PRODUCT]`、`[BUYER, COUNTRY]`、你那份乱七八糟的通话笔记
**吐出来的：** 五部分确认单，外加一段可以连文件一起发的说明。**这份里不许出现任何价格。**
**别全信：** 它替你挑的那个"合理解读"。**模棱两可的话必须两种解读都列出来让他选，别让它悄悄替你做主。**

口头谈的规格，两个月后双方在集装箱前各执一词。这条把口头说法变成一份双方都要点头的清单，并且明确写清楚：**哪些东西我们根本没谈。**

```text
Turn this verbal conversation into a written specification confirmation that both sides sign off on before any price is discussed. It is my defense against a dispute later.

MY PRODUCT: [PRODUCT] | BUYER: [BUYER, COUNTRY]
WHAT WE AGREED IN THE CALL: [your notes — messy is fine, organize it]

Produce:
1. SPECIFICATION TABLE — item | buyer's stated requirement | my standard product | difference | acceptable to me and why | confirm/clarify needed. Mark any row I cannot meet "MISMATCH — DECISION NEEDED".
2. QUANTITY, PACKAGING & LOADABILITY — quantity, unit definition (this is where most disputes start), packaging type, pallet quantity, total gross weight, total volume, and the resulting container split (how many of which container type). Flag whether the container count constrains the quantity the buyer asked for. State explicitly which of these are MY assumptions.
3. SHIPPING AND TERMS — shipment mode, Incoterm with exact version and named location (never a bare "FOB"), destination port, latest shipment date, who arranges freight.
4. OPEN QUESTIONS — numbered, each question in English and Chinese, with why the answer changes the quote.
5. WHAT THIS DOCUMENT DOES NOT COVER — explicitly list what we did NOT agree on, so neither side assumes it later.

RULES:
- Every number is either [BUYER STATED] or [MY ASSUMPTION]. No unmarked numbers.
- Ambiguous buyer statement: write both readings and ask which one they meant. Never silently pick one.
- No prices anywhere in this document.
- End with a short cover note, English and Chinese, asking for written confirmation without sounding defensive.
ANTI-HALLUCINATION: Do not fill in standard load figures, pallet dimensions, or container capacities from memory. Every such figure gets [VERIFY WITH FORWARDER] unless I supplied it.
STOP: Under 800 words. Five sections.
```

---

## 06 报价谈判 · Quote & Negotiate

### P06-1 · 报价单结构审查

**往里填：** 你的报价草稿、`[PRODUCT]`、`[COUNTRY]`、`[TERM + LOCATION]`、`[CCY]`、`[COST LINES]`、你的让步清单
**吐出来的：** 六个部分，第 2 部分是重点：每个漏底价的位置 + 推理路径 + 替换文案。上限 700 词。
**别全信：** 它说"这个费率是标准做法"。**问银行，别问它。**

报价单最大的坑不是报错价，是把成本结构漏出去了——采购能从一行"包干理货费"反推出你的成本。这条逐行找漏。

> 发给客户前顺手跑一次 `python scripts/quote_engine.py ... --audience client`：客户视图里**脚本会把底价和成本行直接拿掉**，比你在 Word 里手动删可靠。

```text
Review my quotation before I send it. Goal: survive comparison, and leak nothing I need to keep.

MY QUOTE DRAFT:
[PASTE YOUR QUOTE]

PRODUCT: [PRODUCT] | BUYER: [COUNTRY] | INCOTERM: [TERM + LOCATION] | CURRENCY: [CCY]
MY COST STRUCTURE (confidential — tell me what must NOT appear): [COST LINES]
MY NEGOTIATION POSITION: [what I can concede, and what I need in return for each]

Review and output:
1. MISSING ITEMS — what a buyer in this market expects to see and I omitted. Be specific to this market.
2. ITEMS THAT LEAK — every line from which my price structure, margin, supplier identity or cost breakdown is inferable. Quote the line, then show the inference path. This is the most important section.
3. AMBIGUITY — anything readable two ways, especially Incoterms, unit definitions, validity period, payment terms. Rewrite each unambiguously.
4. STRUCTURE — line-item or tiered-by-quantity? Recommend one and explain the commercial consequence of each.
5. WHAT I'M GIVING AWAY FOR FREE — anything I included that I should have priced as an extra (extended payment terms, free samples, free spare parts, loading supervision, extended validity).
6. THE SENTENCE — the single biggest thing to fix before sending.

Rules: be blunt, do not compliment. Every problem gets exact replacement wording. If a number I wrote looks guessed rather than costed, mark it "UNCONFIRMED — do not send".
ANTI-HALLUCINATION: Do not assert what competitors charge, what a "market rate" freight or insurance rate is, or what this buyer's budget is. Those go in as questions for me to verify.
STOP: Under 700 words. Point at lines, do not rewrite the whole quote.
```

### P06-2 · 三档让步阶梯设计

**往里填：** `[MY FLOOR PRICE]`、`[PRODUCT, SPEC, QTY, INCOTERM]`、`[BUYER OPENING]`、`[CURRENT ASKING PRICE]`、对方原话、你能换的和不能碰的
**吐出来的：** 三档，每档四件东西含中英文原话。上限 700 词。
**别全信：** 它写的英文话术。**读一遍，AI 写谈判语言有一种奇怪的、像在为整家公司道歉的味道。**

降价不是让步，是交易。这条逼它在每一档都写清楚你换回来什么。空手让步的那一档会被单独拎出来——因为那一档就是你以后再也拿不回来的那部分利润。

```text
Design a concession ladder for a negotiation in progress.

My floor: [MY FLOOR PRICE] for [PRODUCT, SPEC, QTY, INCOTERM]. The buyer has moved from [BUYER OPENING] to [CURRENT ASKING PRICE]. They said: [BUYER'S EXACT WORDS].
WHAT I CAN TRADE (each has a real cost to me): [price, payment terms, MOQ, lead time, packaging, warranty, spare parts, regional exclusivity, sample quantities, shipping mode]
WHAT I CANNOT TRADE: [hard limits]

Build three rungs:
RUNG 1 — SMALL CONCESSION, SMALL ASK. What I give, what I get back, and how to phrase the ask so it reads as a trade rather than a hostage situation.
RUNG 2 — MEDIUM CONCESSION, MEDIUM ASK. Same structure, but the ask must be worth more than the concession — the buyer who takes rung 1 and asks again is the buyer who breaks my floor.
RUNG 3 — THE FINAL MOVE. Usually not price. Usually the closest thing to walking away that still closes. Give me the exact wording.

For each rung:
- Exact words to say or write, English and Chinese.
- What I get back, stated as something I can verify.
- The signal to go to the next rung, and the signal to stop and hold.
- One sentence for why I will not go below my floor, phrased so I can say it out loud and believe it.

RULES:
- No concession without a return. If I want to give something free, name it as an optional goodwill move and state what it costs me in leverage.
- Never "our margin is very tight" or "we cannot go lower". Give a reason that is true and invites no counter-argument.
- The ladder must be usable in one conversation. If rung 3 needs a second call, say so.
- Close with the single most likely mistake I will make under pressure, and the sentence that prevents it.
ANTI-HALLUCINATION: Do not invent competitor prices, market benchmarks, or what this buyer pays today. Anything you do not have goes in as [UNKNOWN — ASK THEM].
STOP: Three rungs. Under 700 words.
```

### P06-3 · 客户压价应对话术

**往里填：** `[PRODUCT, MY PRICE, MY FLOOR, WHAT THEY'VE ALREADY TRIED, HOW LONG WE'VE BEEN TALKING]`、双方关系阶段
**吐出来的：** 八种说法，每种五行。上限 700 词。
**别全信：** 它说"这句话是虚张声势"。**它可能是对的，但你别当场把它当对的用。**

"你们比别家贵 30%"——这句话也许是真话，也许他今天就跟二十个供应商说过。这条按话术分门别类给回应，并且告诉你哪句大概率是试探。

```text
Coach me through a price negotiation. A buyer is applying pressure. For each tactic below I need a response that holds my position without losing the deal.

MY SITUATION: [PRODUCT, MY PRICE, MY FLOOR, WHAT THEY'VE ALREADY TRIED, HOW LONG WE'VE BEEN TALKING]
RELATIONSHIP: [new / second contact / existing customer / referral]

TACTICS:
1. "Your price is 30% higher than another supplier."
2. "If you can match [X], we order immediately."
3. "I need a 10% discount or I'll go with another supplier."
4. "The last supplier gave me a better deal and gave me 60 days payment."
5. "This is our only order, treat it as a trial."
6. "Sign this price and I can get you an immediate reply from our director."
7. Silence, then two weeks later: "we are still interested, are you?"
8. "I need to reduce my order but I need a better price."

For each tactic:
- WHAT THEY ARE ACTUALLY DOING — one honest line. Some are negotiation, some are bluffing. Tell me which.
- THE SIGNAL TO WATCH — how I separate a real constraint from a bluff.
- MY RESPONSE — exact words, English plus Chinese, under 80 words, calm, not defensive.
- WHAT I SHOULD NOT SAY — the tempting sentence that gives away my floor.
- THE TRADE I OFFER INSTEAD — a concession costing me less than the cut they asked for.

Finally: of these eight, which one do I never concede anything on, and which one do I concede something on immediately to buy goodwill? One line each.
ANTI-HALLUCINATION: Do not invent what this buyer's other supplier quoted, their budget, their order frequency, or any market price index. Anything you cannot know goes in as a question I should ask them, not as a fact.
STOP: One row per tactic. Under 700 words.
```

### P06-4 · 谈判复盘与底线校准

**往里填：** 你报的价、他开的价、成交价、你让了什么、换回什么、他的原话、你什么时候知道结果的
**吐出来的：** 六个部分，第 4 部分是一条能贴在下份报价单顶部的规则。400 词以内。
**别全信：** 它总结的"决定成败的那个瞬间"。**多半是它编的叙事，你看字数限制内它能不能举出你说过的原话。**

谈完不复盘，下次还是从零开始，而且会在同一个地方输。这条只要 400 字，也不给你鼓励——你需要的是下次少亏一点，不是心情好一点。

```text
I just finished a negotiation. I want the lesson so I stop re-learning it.

WHAT HAPPENED:
- My quoted price: [X]
- Their opening: [Y]
- Where we settled: [Z]
- What I conceded: [list]
- What I got in return: [list]
- Their stated reason for moving away or closing: [their words]
- The moment I knew the outcome: [or "I didn't know"]

Give me:
1. THE POST-MORTEM — where the price actually broke down, one paragraph. My anchor, my floor, my patience, or their leverage? Pick one.
2. WHAT I GAVE AWAY FOR FREE — every concession with nothing verifiable back, and the specific sentence I used to give it.
3. THE HINGE MOMENT — where it was decided, and what I said. If you are inferring rather than quoting, say "INFERRED".
4. THE ONE RULE TO ADD — an instruction to myself I could paste at the top of my next quote.
5. THE CALIBRATION QUESTION — I assumed [something about their budget/authority/timeline]. What should I test earlier next time?
6. WHAT TO REPEAT — one thing I did that felt like a mistake at the time and should keep doing.

Under 400 words. No encouragement. I do not need to feel better about it, I need to do it better.
ANTI-HALLUCINATION: Every claim about why the deal went the way it did must trace to a line I pasted above or be marked "INFERRED". Do not invent a turning point, a quote, or a buyer motive I never stated. The "hinge moment" is the easiest one to fake — only call it real if I gave you the actual words.
```

---

## 07 订单交付 · Delivery

### P07-1 · 交付检查表生成

**往里填：** 八个订单事实（产品、HS、Incoterm+地点、目的港、买方、付款阶段、运输方式、目标装船日）
**吐出来的：** 三段可勾选清单 + 最后五条最容易漏的。上限 900 词。
**别全信：** 单证要求。**报关行说的不算错，你客户的报关行说了算——这条里明确要求标出来。**

单证上少一个字，货在港口躺两周，仓储费按天算。这条生成的是站在集装箱前能逐条勾的清单，不是给办公室文员看的清单。

```text
Generate a delivery checklist I can print and tick off. Because the payment milestone must tie to each step, keep it in order.

ORDER FACTS:
- Product: [PRODUCT], described as on the proforma invoice
- HS code (if known): [HS CODE]
- Incoterm + named place: [e.g. FOB Ningbo / CIF Jebel Ali]
- Destination country and port: [COUNTRY, PORT]
- Buyer: [BUYER NAME]
- Payment method and stage: [e.g. 30% T/T deposit received, balance before shipment / confirmed L/C at sight]
- Shipping mode: [sea FCL / LCL / air / rail / courier]
- Target shipment date: [DATE]

Three sections:
1. PRODUCTION & PRE-SHIPMENT INSPECTION — every checkpoint from PO confirmation to loading, who owns it (me / factory / third-party inspector / forwarder / buyer), and what evidence proves it is done. For each: what "passed" means, which photo or document counts as proof, what happens if it fails. Flag the 3 checkpoints where skipping causes a dispute.
2. DOCUMENT SET — one row per document: exact name as it must appear, who issues it, when it must exist, how many originals, most common reason it is rejected at customs. For certificate of origin and commercial invoice, give the exact required field list. Mark any country-variable requirement [VERIFY WITH BUYER'S BROKER].
3. SHIPPING & CASH FLOW — milestone by milestone from ex-factory to the buyer receiving goods, with the payment milestone attached to each step and what I must hold before releasing each payment. State who bears risk at each point under the Incoterm I gave.

RULES:
- Every line must be checkable by a person standing at the container, not by a document reviewer in an office.
- Never invent a document requirement. Write "UNKNOWN — confirm with [who]".
- Where the buyer's broker has told me something different from standard practice, mark it — buyer instructions usually win.
- End with the 5 items most likely to be missed on a first export, ordered by cost if forgotten.
STOP: Under 900 words. Checklist rows only.
```

### P07-2 · 生产跟单与异常处理

**往里填：** 订单事实、到底出了什么事、你手上有什么证据（照片/报告/聊天记录，别夸大）
**吐出来的：** 六个部分，含接下来 48 小时按小时排的动作。上限 700 词。
**别全信：** 它对供应商动机的判断。**你只给它证据，它只能基于证据猜——把证据写诚实一点。**

工厂说出事了，第一句话通常是"没问题"。这条判断到底有没有问题，以及接下来 48 小时你每小时干什么。

```text
Something has gone wrong in production. I need to know what to do in the next 48 hours, and what leverage I still have.

PRODUCT / ORDER: [description, PO number, quantity, agreed spec, agreed price, Incoterm, shipment date, payment already made]
WHAT HAPPENED: [be specific — late by X days / material failed inspection / supplier proposed a cheaper substitute / quantity short-shipped / quality downgraded without telling me / factory went quiet / production subcontracted]
WHAT I HAVE PROVEN: [photos, inspection report, messages — be honest about how solid this is]

Give me:
1. THE REAL ASSESSMENT — what is actually happening, separate from what the supplier claims. If their explanation does not fit the facts, say so plainly.
2. WHAT'S STILL SALVAGEABLE — yes / yes-with-conditions / no. Straight answer.
3. MY NEXT 48 HOURS — hour-by-hour actions with the wording I use with the supplier. Include the specific question that gets a straight answer instead of a reassuring one.
4. MY LEVERAGE — what I can actually do: stop payment, change forwarder, withhold the balance, complain to their association, replace goods elsewhere. Rank by speed and by damage to the future relationship.
5. THE FALLBACK PLAN — if this cannot ship on time, the two best recovery options with cost bands marked [ESTIMATE], the words I use with the buyer, and how I tell them before they ask.
6. WHAT TO PUT IN WRITING NOW — one short email I send today that protects me later without being hostile.

CONSTRAINTS:
- Do not assume the supplier is dishonest. Do not assume they are honest either. Give me evidence-based tests.
- Any cost estimate must be marked [ESTIMATE].
- Never "communicate more" or "build a stronger relationship". Sentences and deadlines only.
- If the honest answer is "ship late and apologise", say that.
ANTI-HALLUCINATION: Do not invent legal remedies, arbitration rules, or contract clauses — if it depends on the contract, tell me which clause to check.
STOP: Under 700 words. Six sections.
```

### P07-3 · 收款与风险控制

**往里填：** 买方 + 国家、Incoterm+地点、金额+币种、约定的付款方式、已收多少、运输方式与天数、保险、你的钱压在哪儿
**吐出来的：** 六个部分，含一张暴露表和一套催收阶梯。**特别要盯信用证软条款**——那种写着银行付款、实际上是客户想付才付的东西。
**别全信：** 汇率管制、银行费用、催收成本。**它编这些的速度比查这些快一百倍，一条都别直接用。**

货运走了钱没到，这单就是慈善。这条把风险点从头到尾排一遍。**整张单据里最贵的那一行通常不是海运费，是那句你以为不用管的付款条件。**

```text
Structure the payment and risk picture for an export order so I can see where I am exposed, and what I can still change.

ORDER FACTS:
- Buyer: [BUYER], in [COUNTRY]
- Incoterm and place: [TERM, PLACE]
- Invoice value and currency: [AMOUNT, CCY]
- Payment terms agreed: [100% L/C at sight / 30% T/T deposit + 70% before shipment / O/A 60 days / D/P at sight]
- Amount already received: [AMOUNT], and how
- Shipping mode and transit time: [MODE, DAYS]
- Insurance: [none / cargo insurance under CIF / warehouse-to-warehouse]
- Where my money actually sits: [how I fund production, and for how long]

Deliver:
1. THE EXPOSURE TABLE — at each point (ex-factory, loading, in transit, at destination, customs hold, final delivery): who bears risk, who bears cost, when I actually get paid. Show the gap between "goods move" and "money arrives".
2. THE DANGEROUS CLAUSES — the agreed terms that hurt me, in plain language, with the version I should have asked for. If payment is by L/C, go clause by clause for SOFT CLAUSES: any condition that lets the buyer or their agent block payment unilaterally (inspection certificates the buyer controls, unobtainable consular documents, discrepancies only their nominated inspector can clear, drafts requiring documents I cannot produce). Explain, for each, how the bank's payment obligation gets neutralised.
3. WHAT I CAN STILL DO NOW — actions available before this ships, ordered by impact. Who to ask, what document to request, what to amend while it is still legal.
4. THE FIRST SIGNAL OF TROUBLE — the earliest observable sign this buyer will not pay on time, and the specific data I check weekly.
5. THE RECOVERY LADDER — escalation sequence with timing: who to contact first, at what day past due, what to demand at each step. Include where a formal demand letter goes, and the last step involving a collections agency or legal counsel, with rough cost bands marked [ESTIMATE].
6. THE INSURANCE QUESTION — whether cargo insurance fits this transaction, and what it would and would not cover.

RULES:
- Do not invent exchange control rules, bank fees, or collection costs. Mark them UNKNOWN and name the authority to ask. Do not cite UCP article numbers you are not certain of.
- Assume the buyer is good until a signal appears, but make every signal checkable.
- If the agreed terms are already bad, say it in the first two lines.
STOP: Under 800 words. Six sections.
```

### P07-4 · 交付复盘与复购计划

**往里填：** 订单摘要（买方、国家、产品、数量、金额、各环节耗时、出了什么岔子、花了多少钱、客户对交付和单证的反应、是不是首单）
**吐出来的：** 六个部分，含一句要转介绍的话术和一个带期限的动作。500 词以内。
**别全信：** 它对客户满意度的判断。**客户说"fine"到底是什么意思，只有你知道。**

交货不是结束，是复购的开始——虽然这时候你只想躺两天。这条把这一单变成下一单，外加一句能换来两个名字的话术：**大部分客户会给，前提是你把那句话说对他就会给。**

```text
An order has shipped or been delivered. Turn it into the next order, and into a process I can reuse.

ORDER SUMMARY:
- Buyer, country, product, quantity, value
- First contact to first payment: how long
- Payment to shipment: how long
- Total lead time, and who caused the delays
- What went wrong, and what it cost in money, in time, or in goodwill
- Buyer's response to delivery and to my documentation
- First order or repeat?

Give me:
1. THE HONEST POST-MORTEM — three things that went well and three that did not, each with the concrete consequence rather than a feeling.
2. THE REPEAT ORDER PLAY — how I ask for the reorder, when I ask (timed to their selling cycle), what I offer to make round two easier. Give me the actual message, English and Chinese.
3. THE GROWTH PLAY — the realistic next step up: larger quantity, second product from my range, referral to their contact, longer payment terms they have now earned. Recommend one and say what it costs to ask for it.
4. THE REUSABLE PROCESS — the 3-step routine I repeat on every future order, and the 1 thing I do differently each time.
5. THE DOCUMENT CACHE — documents to keep from this order as templates, and which need anonymising before I store them.
6. THE REFERRAL ASK — exact wording to ask this buyer for two other people in their market with the same problem I just solved. Most customers will give names if you hand them the sentence. Give me that sentence.

Under 500 words. No sentimentality. End with the single most valuable follow-up action and a deadline.
ANTI-HALLUCINATION: Base this only on what I wrote above. Do not assume the buyer was satisfied, do not invent their market conditions, and do not quote a satisfaction score neither of us has.
```

---

## 通用 · General

### P-GEN-1 · 环节自检（改文档时用）

**往里填：** 你写的那篇环节文档草稿
**吐出来的：** 按七个维度编号的问题清单，最严重的在前。**明确禁止它替你重写全文。**
**别全信：** 它夸的部分。**它没有分数可以给，我们也不设。**

写完了？让 AI 反过来挑你自己的毛病。**它挑刺比它写东西靠谱得多**，这是它难得不犯糊涂的时候。

```text
Review a stage document from an open-source repository that teaches foreign-trade beginners. Quality rule: every judgment must be decidable, every instruction must be an action.

STAGE DOCUMENT:
[PASTE YOUR DRAFT]

Numbered list of problems, worst first:
1. VAGUENESS — every sentence that could not be used to make a binary decision about a real case. Quote it, suggest the specific rewrite.
2. UNACTIONS — every step that describes a topic rather than an action. Acceptable only if a beginner could do it without being told where to go.
3. UNSOURCED NUMBERS — every figure with no source, marked with whether it is likely wrong.
4. MISSING FAILURE CASES — mistakes this document lets a beginner make, and where it fails to warn them.
5. COUNTRY/INDUSTRY OVERREACH — statements presented as universal that are only true for some markets or categories.
6. EMPTY PHRASES — every instance of motivational filler carrying no information.
7. STRUCTURE — confirm the six sections present and in order: what this stage is for / how to do it step by step / pass-fail criteria / common mistakes / copy-paste templates / AI prompts for this stage.

Then give me the three highest-priority fixes. Do not rewrite the whole document. I want to learn what was wrong, not receive a replacement I have to re-read.
STOP: Problems only. Under 700 words. No praise section.
```

### P-GEN-2 · 行业环节包适配

**往里填：** `[PRODUCT CATEGORY]`、`[COUNTRIES/REGIONS]`、你要改的那篇通用文档
**吐出来的：** 七个部分，最后一部分是"新手会按什么顺序搞错哪三件事"。
**别全信：** 它建议的认证和展会。**一个字母之差，一张证书就是废纸——全部自己核。**

通用文档对你的品类基本没用：它最得意的那句"对所有品类都成立"，落到你这一个品类上往往哪一招都使不上。这条让它指出通用版在你这行会翻车的地方。

```text
Adapt a generic foreign-trade workflow to a specific industry, so the advice is usable rather than generic.

MY PRODUCT: [PRODUCT CATEGORY] | MY TARGET MARKETS: [COUNTRIES/REGIONS]
THE GENERIC STAGE DOCUMENT I AM ADAPTING:
[PASTE]

Tell me:
1. WHAT THE GENERIC VERSION GETS WRONG FOR MY PRODUCT — where the advice fails, is illegal, or wastes time because it assumes a different product's characteristics. Cover the specs that matter, who the buyer actually is, what they buy on, how they qualify suppliers, and what they negotiate besides price.
2. MY PRODUCT'S REAL SPECIFICATION SET — the fields a quote must contain, split into what buyers care about and what is noise.
3. WHO MY REAL BUYER IS — job titles, not company types. The person who signs, the person who specifies, the person who blocks me.
4. THE INDUSTRY-SPECIFIC QUALIFICATION CHECKS — what a buyer or inspector checks here that has no equivalent elsewhere.
5. THE CHANNEL REALITY — how this product reaches the end user in my target market, including who sits in between and takes a margin.
6. THE TRADE SHOWS AND ASSOCIATIONS THAT MATTER for this product in this market, with what is verifiable about each rather than what is commonly claimed.
7. THE THREE THINGS A BEGINNER WILL GET WRONG in this industry, in the order they will go wrong.

RULES:
- Do not invent certifications, standards or test requirements. Write "UNKNOWN — verify with [authority]".
- Prefer specifics over categories. "Distributors with [X] profile" beats "the B2B segment".
- If my product has genuine regional variation, say where it lies and which of my target markets needs which version.
STOP: Under 800 words. Seven sections.
```

---

## 提 PR 之前，自己勾一遍

追加到本文件末尾，并遵守 [CONTRIBUTING.md](../CONTRIBUTING.md) 的自查清单：

- [ ] 是一条**完整可粘贴的英文提示词**，不是要点提纲
- [ ] 说明下面三行齐全：**往里填 / 吐出来的（含字数上限）/ 别全信**
- [ ] 编号连续：`P{环节号}-{序号}`，中间不跳号
- [ ] 输出格式写死了：表格列名 / 条数 / 字数上限，三者至少有一个
- [ ] **有停止条件**（字数上限或"只到第三次"这种硬边界）
- [ ] **有防幻觉条款**：不许编，不确定就写 `UNKNOWN` / `[VERIFY WITH ...]`
- [ ] 没有任何指令是"让 AI 替你做判断"
- [ ] 数字要么用户自己给了，要么被打成 `[ESTIMATE]` / `UNKNOWN`
- [ ] 没有编造法规条文号、认证名称、费率、 UCP 条款、市场数据、行业内数字
- [ ] 用到的公司名一律 `【示例】` 前缀，邮箱域名只用 `sample.example`
- [ ] 代码块围栏成对（和已有的一样，`text` 或 `bash`）
- [ ] 如果产出要喂脚本，**列名和 `scripts/` 里的完全一致**（`lead_score.py` 认的是：company / country / product / source / email / phone / years / contact / note）
- [ ] **别改数量**。三个 README 都写着 27 条，动一条它们就错了

### 已知还没补的缺口

对照 `docs/` 七篇，这份里目前**没有单独成条**的东西（欢迎照着补，或者先拿上面的通用条款凑合用）：

| 缺口 | 出处 | 现在怎么办 |
|---|---|---|
| 从公司官网提取固定字段（8 字段结构化） | `docs/02` 提示词 1 | 用 P02-2 顶着，但字段没那么严 |
| 装柜量 / 数量可行性核算 | `docs/05` 提示词 2 | P05-3 第 2 部分顺带算，但没单独成条；能算的脚本优先用脚本 |
| 报价单生成（这条只有**审查**，不生成） | `docs/06` 提示词 1 | 用 `scripts/quote_engine.py` 出，再用 P06-1 审 |
| 合同条款自查（交货期 / 违约金 / 不可抗力） | `docs/07` 提示词 1 | 无。目前只能靠 P07-2 兜 correspondence |
| 信用证软条款逐条排查 | `docs/07` 提示词 4 | 已部分并进 P07-3 第 2 部分，复杂单据还是找银行 |

另外一处全项目级别的不一致：'`docs/` 里那 7 篇各自复制了提示词全文，编号对不上这里'——上面开头说过了，再提醒一次是因为**它还没被修掉**。
