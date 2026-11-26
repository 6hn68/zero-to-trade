# 02 · Find Leads

> English version of [02-find-leads.md](02-find-leads.md). Translated from the Chinese original; figures, dates, commands and file names match the original exactly.

> **Goal of this stage**: build a channel mix that reliably produces 20 real leads a day, and accumulate 200 raw names.
> **The principle in one sentence**: customers are not "found", they are "filtered". Walking one road to the end will eventually leave you with nothing; opening several roads keeps you fed.

## 1. Why this step comes first

The biggest illusion a beginner has is thinking they lack "customer resources".

The truth is: whenever a product category has import volume, most of the real buyers inside it — traders, distributors, chains, fleets — are not sitting on LinkedIn waiting for your message; and almost no company writes "looking for a Chinese supplier" on its homepage.

> **Where the numbers come from (do not guess)**: how much the target country imports in a year, and mainly from whom — pull the annual import records from UN Comtrade (comtradeplus.un.org) by "reporter + HS code + year", or check the target country's customs / statistics bureau's public import statistics pages. If you find it, copy down the source and the statistics date; if you cannot find it, put an [Example] placeholder — never invent a number that looks good.

So finding customers is not searching, it is filtering. Filter through a pile of company names; no matter how impressive a name sounds, only recognize three things: is it buying now, can it afford to buy, and can you reach it.

Three hard standards — a lead missing any one of them is a fake lead:
1. **Real signs of purchasing** — the website has a product catalog, wholesale price lists, a business contact page. Not a company with only a homepage image.
2. **Traces of import/export activity** — it has imported before, exhibited at a trade fair, or written about working with suppliers.
3. **A reachable contact person** — you must get a **specific person's name** + their personal email or WhatsApp / phone. A company name alone does not count as a lead; getting only a public mailbox like `info@` / `sales@` / `support@` is the same as getting no one — downgrade it to "person still to dig out", not a qualified lead.

20 a day does not mean sending 20 outreach emails a day. 20 **filtered** leads and 20 randomly searched company names are not in the same league for hit rate.

## 2. Step by step

**Step 0: Draw the legal boundary first (if this step is not done, everything after it is wasted)**

Finding customers may only use **public information**. The allowed sources in this stage are exactly the same as the compliance red lines in [03 · Due Diligence](03-due-diligence.md):

Allowed:

- Company official websites (company information, product catalogs, contact details, founding statements)
- Public customs / import-export data (UN Comtrade, official statistics bodies of each country, the public search functions of licensed commercial data platforms)
- LinkedIn public company pages (roles, company information, public posts)
- Public trade fair exhibitor directories, industry association / chamber membership directories, public yellow pages
- Press releases published through a company's official channels, and official social media accounts

Forbidden:

- Social engineering databases (社工库), leaked contact lists, stolen databases
- Buying personal private data (personal phone numbers, private emails, home addresses) for prospecting
- Impersonating someone to extract information, bribing or buying off the other side's staff to get customer lists
- Scraping or mirroring website content in violation of a platform's terms of service

**Why this is non-negotiable**: selling or providing citizens' personal information to others, and illegally obtaining such information, can constitute the crime of **infringing citizens' personal information** (Article 253-1 of the Criminal Law of the People's Republic of China) where the circumstances are serious. That is criminal liability, not "industry practice". The easiest trap for an export beginner to step into is "buy a list of purchasing contacts in the target country" — cheap, fast, and it sends both the company and you in together.

One sentence of principle: **only a web page you can openly open counts as a source.** Data that needs "special means" to obtain does not go into the lead table, and does not go into the customer file.

---

**Step 1: Lay out the channels (a seven-route list, with click paths and whether they cost money)**

Run through all seven routes first, then decide which ones to bet on. **Get at least 4 routes actually working** — bet on only one, and the day it breaks you have nothing to eat.

| # | Channel | Click path (follow the clicks) | What you can get | Free / paid |
|---|---|---|---|---|
| 1 | **Customs / import data** | Free version: UN Comtrade (comtradeplus.un.org) → pick Goods → fill in reporter + HS code + year → Preview. Paid version: a licensed commercial customs data platform → search by HS code or product keyword → export importer names + suppliers + container volumes | Company names that really import, product categories, volumes, source countries | **The free version has no importer names; commercial databases with company names cost money** (check each provider's country coverage and price yourself) |
| 2 | **Google search syntax** | Type the syntax strings attached to Step 1 below straight into the search box, one by one | Official sites, distributor pages, directory PDFs, contact details | **All free** |
| 3 | **Target-country importer directories / yellow pages** | Search `{country} yellow pages`, `{country} chamber of commerce member directory`, `{country} importers association`, then filter by industry category inside the site | Company names, addresses, phone numbers, industry categories | **Mostly free**; a few association directories need registration or a membership fee |
| 4 | **LinkedIn** | Type the company name in the search box → switch to Companies → open the company page → click People → filter one by one with `purchasing / procurement / import / sourcing / owner` | Purchasing lead's name, role, employment status | **A free account is enough** (you can send connection requests with a short message); Sales Navigator is a paid upgrade |
| 5 | **Trade fair directories** | Fair's official site → find Exhibitor / Exhibitor List / exhibitor directory → usually a PDF or a page filterable by country → filter by product category + country | Lists of active buyers who exhibit year after year, and their product lines | **Mostly free**; a few fairs require registration to download |
| 6 | **B2B platforms** | Alibaba / Made-in-China / GlobalSources etc. → RFQ or buyer channels → filter by country + product category | Buyer inquiries, buyer business cards | **Limited information free; deep information needs a membership fee** |
| 7 | **Competitors' official sites, distributor pages** | Find a brand in the same category that is already in the target country → look for `Where to buy / Distributors / Dealer locator / 经销商` → filter by country | Ready-made channels **already selling the same kind of goods** locally | **All free** (the most easily overlooked route) |

> One more word on route 7: a competitor's distributor page is someone else having filtered "who sells locally" for you, for free. Product category, price band and channel role are all ready-made — it is basically the least-effort route of the seven.

**Appendix: Google search syntax you can actually use (copy directly, replace the bracketed parts)**

```
site:{country domain} "tyre importer"                       # limit to a country domain + exact phrase
intitle:"tyre" "importer" {country} -alibaba             # intitle hits the title; -alibaba removes platform noise
"TBR" "wholesale" "distributor" site:.ae             # stack several exact phrases
"importer" "{category word}" "contact" -alibaba -amazon      # find importer pages that carry contact details
filetype:pdf "exhibitor list" {category} {country}           # pull directory PDFs directly
"{importer word in the local language}" {city}                          # local-language words often hit better than English
```

Syntax points:

- `site:` limits to a site or country domain (`.sa` `.ae` `.eg`), but it misses local companies using `.com` — **use it only as a helper, never as the main route**.
- `intitle:` only searches page titles. It is far more accurate than body-text hits, and the fastest way to filter "what does this company mainly do".
- `"quotes"` mean an exact phrase. Without quotes the words get split apart and the results are all noise.
- `-word` excludes. When searching for importers, **always include `-alibaba -amazon -aliexpress`**, or half the results will be platform pages.
- `filetype:pdf` pulls list-type PDFs directly. Trade fair directories and association directories are often published as PDFs.

**Daily quota split (by count, not by percentage)**: split 20 leads a day into

- Customs data **8** (the main source of names)
- Search + official sites **6** (filling in contact details, including the 6 syntax strings above)
- Distributor pages / yellow pages **3** (filling in product category and channel role)
- LinkedIn **2** (digging out specific people)
- Trade fair directories **1** (gap-filling and verification)

If any one route breaks, the other four can still carry the load. **Do not** put all 20 on customs data — that is exactly Trap 1.

**Step 2: Fix the HS code first, then pull customs data (the most time-consuming step, but the most valuable)**

A wrong HS code wastes everything after it. Check the code in this order — do not write it from memory:

1. **The WCO HS database** (the HS Nomenclature on wcoomd.org) + your own country's General Administration of Customs tariff lookup page, to confirm the chapter and subheading for the product category (tires mostly sit under HS Chapter 40 — **the exact subheading must be verified yourself; do not copy it from this document**).
2. **The target country's customs authority tariff lookup page**, to confirm the other country's classification practice — the same product can sit under different subheadings in different countries.
3. Still unsure: **ask a freight forwarder, or apply for a pre-classification** and get a written classification opinion before pulling data in bulk.

Once the code is fixed, pull the target country's import records and focus on three columns:

- **Who is importing**: company names → these are the main body of the list
- **Import volume**: sort high to low — these are most likely your target customers
- **Source-country structure**: if large volumes come from China, they are used to Chinese goods and the bar is low

After pulling a batch, do a first filter. If any one of these hits, **downgrade it and write the reason in `note`** (do not delete it outright — keep it for re-checking):

- One import so small it was only a sample
- Frequently switching suppliers
- A company name that only says "trading" but has no verifiable physical address or warehouse
- The company name on the official site does not match the name in the customs records

**Step 3: Find the official site + fill in the information (3–5 minutes per lead)**

Once you have the company name, find the official site first. The two fastest paths:

1. Google `"full company name"`, or use `site:{country domain} "full company name"` to rule out same-name companies.
2. If no official site turns up → go back to routes 3 and 7 in Step 1 (yellow pages / competitor distributor pages) and reverse-check. Many small traders have no standalone website at all.

Once found, look at three places:

- The `/contact`, `/about`, `/products` pages — find a **named** email, phone, WhatsApp and address
- Whether the product catalog includes the category you sell (e.g. TBR commercial tires, OTR off-road tires)
- Whether there is any wording about "wholesale / distribution / agency / distributor / dealer / wholesale" — that decides whether it is a channel player or an end user

While you are there, note one piece of "intelligence": which brands they mainly carry, roughly which price band, whether they mention their own warehouses or store counts. This is ammunition for later outreach emails and quotations — **write it in the `note` field** (the script scores it by keyword, see Step 6).

**The 5-minute stop-loss rule**: if a lead still yields no contact details after 5 minutes, stop — write the company name, `country`, `product`, `source` and "contact details to be filled in" into `note` and save it to the table. **Do not keep digging.** The script will automatically grade it T3 (not enough information — nurture for now), and you can fill in a batch of T3s together later. Spending 20 minutes on a single lead is the most common time black hole for beginners.

**Step 4: Find the right person on LinkedIn (get the free account working first; do not rush to pay)**

Click path: type the company name in the search box → switch to **Companies** → open the company page → click **People** → try `purchasing`, `procurement`, `import`, `sourcing`, `owner` one by one in the filter box.

```
# LinkedIn people-search syntax (type straight into the search box)
"purchasing manager" "tyre" {country}         # role + product category + country
"procurement" OR "sourcing" {company name}        # OR is a union — hits both role words at once
"import manager" -"sales" {country}            # - excludes sales roles; sales is not who you are looking for
```

- **Free account**: you can search, view, and send connection requests (with a short message attached). Get this route working first.
- **Paid Sales Navigator**: stronger filters and InMail quota. **Buy it only after you have confirmed this route actually produces people** — do not subscribe on day one.
- In the Middle East many small companies have extremely short decision chains — finding the purchasing director is basically finding the decision maker; in a small company, Owner / Founder is the person who decides.
- A connection request should state who you are and what you want in one sentence. **Do not send the product catalog in the first message.**
- When you cannot find a person, fill the gap with "company name + guessed email format + verification". For verification, only use public technical means such as **format checks and domain MX checks**; **never mass-send an email that failed verification** — the bounce rate will drag down your whole domain's reputation.

**Hard rules for email validity** (the practical version of the third hard standard):

> All email domains in the table below use the reserved domain `sample.example` as a placeholder. Replace it with the domain you actually found when recording.

| Email type | Verdict | Handling |
|---|---|---|
| Named personal email (e.g. `a.rahman@sample.example`) | **Valid** | Record it in `email`; contactable; put the matching name in `contact` |
| Department mailbox (`purchasing@sample.example` / `procurement@sample.example` / `import@sample.example`) | **Half-valid** | Record it in `email`, mark "department mailbox" in `note`; lower priority than a named email |
| Public mailbox (`info@sample.example` / `sales@sample.example` / `support@sample.example` / `contact@sample.example`) | **Does not count as having a person** | You may record it, but `note` must say "public mailbox only" — it does not enter the priority contact sequence |
| Personal free email (gmail / hotmail / yahoo) as the **only** contact method | **Suspicious** | Flag it in `note` and hand it to [03 · Due Diligence](03-due-diligence.md) for priority checking |

**Step 5: Use trade fair directories to fill gaps and verify**
Public trade fair exhibitor directories are publicly available information you can obtain legally. Two uses:
- **Gap-filling**: traders who exhibit but do not appear in customs data
- **Verification**: exhibiting for two or three years in a row means the business is still operating normally

Record the exhibitor's "country + product line + whether it is a trader".

Business cards collected at a fair get entered into `scripts/trade_show.py` the same day (`--add` one by one, or `--csv` in bulk). It ranks them by interest level into a follow-up plan within 24 hours after the fair (thank-you within 2 hours + quotation lead within 12 hours + one phone chase within 24 hours). See [docs/trade-show.md](trade-show.md) for details.

**Step 6: Build the table using the script's real column names (this step decides whether auto-grading works)**

All leads go into one CSV. **The header must strictly use these 9 column names that `scripts/lead_score.py` reads** (the script reads by column name, case-insensitive; extra columns are ignored outright):

| Column | Required? | What to fill in | How the script uses it |
|---|---|---|---|
| `company` | **Required** | Full company name | The script exits with an error if this column is missing |
| `country` | Recommended | Country | Supports the `--country` filter |
| `product` | Recommended | The product category they deal in (e.g. `TBR 12.00R20`) | Counts toward purchasing-signal keyword hits |
| `source` | Recommended | One of `referral` / `trade_show` / `customs` / `linkedin` / `search` | Source credibility, 30 points (`referral` 30 → `search` 10); **any word outside these five scores 10** |
| `email` | Optional | Email | Adds points if present; **an invalid format counts as no contact details at all**, so filling it in wrong is wasted |
| `phone` | Optional | Phone | Adds points if present; **fewer than 7 digits counts as not filled in** |
| `contact` | Optional | The contact person's **role or name** (e.g. `purchasing manager`) | Counts toward purchasing-signal hits; hitting the "decision role" group scores 3 points |
| `years` | Optional | Years since founding | A plain number is safest (`18`); `18年` and a founding year (`2010`) are also recognized. **Writing it as "ten years" with no Arabic numerals counts as 0** — 10 points thrown away |
| `note` | Optional | Remarks | The main field for purchasing signals — write brands, price bands, store counts, import records and other ammunition here |

The four easiest places to get it wrong — do it as written, do not skip:

1. **The column is `contact`, not `contact_role` / `联系人`.** Writing it under another name means the script cannot read it, the purchasing-role group never scores, and your grades will be systematically low without you knowing why.
2. **A WhatsApp number goes in the `phone` column**, with `wa` or `whatsapp` in the text (e.g. `+000 00 000 0000 (WhatsApp)`). Opening a separate `WhatsApp` column is invisible to the script, and the WA bonus never triggers.
3. **Purchasing signals go in `note` / `product` / `contact`** — the script only scans these three columns for keywords (such as `rfq`, `tender`, `container`, `purchasing manager`). Opening a separate "purchasing signal strength" column does nothing; **category words written in the `company` name do not score either** (the script deliberately does not scan company names, so a lead cannot award itself points).
4. **Placeholder words like "to be filled in", "unknown", "N/A" count as empty.** The script treats `-` / `na` / `待定` / `待补` / `未知` and similar as not filled in. Do not use them to pad cells.

Save it as `my_leads.csv` and run:

```
python scripts/lead_score.py my_leads.csv
python scripts/lead_score.py my_leads.csv --country Saudi
python scripts/lead_score.py my_leads.csv --format detail
```

**On the grading vocabulary — do not mix them up**:

- This stage (and [03 · Due Diligence](03-due-diligence.md)) grades **A/B/C customer ratings** — judging whether a company is worth investing in.
- The **T0–T3** output by `lead_score.py` is a "who to contact first" sorting tool, not a customer rating. Do not copy it into the file as A/B/C.
- The mapping from A/B/C to T0–T3 is defined solely by [04 · Outreach](04-outreach_en.md). Do not invent a separate standard in this stage.

**Step 7: Fix a daily routine (turn "finding customers" into a daily habit, not a project)**

| Item | Suggested value | Notes |
|---|---|---|
| Leads per day | **20** (split 8/6/3/2/1 across the channels in Step 1) | These are 20 **filtered** leads, not "20 company names found" |
| Time per day | **Fixed 30 minutes** (9 AM suggested) | Stop when time is up; do not stretch it because it feels good |
| Time cap per lead | **5 minutes** (see the stop-loss rule in Step 3) | Over time → mark "contact details to be filled in" and store as T3 |
| Weekly check | 5 days × 20 = **100 / week**; run the script grading once on the weekend | About 400 a month — enough to feed the due diligence stage |
| Stage target | Move on to [03 · Due Diligence](03-due-diligence.md) after **200** raw names accumulated | 200 ≈ 10 working days. Do not loosen the three hard standards just to hit the number |

Channel discipline matters more than channel cleverness: **better 30 minutes every day than one 8-hour session followed by a week off.**

## 3. Pass criteria

The hard standards for "this stage is done well":

- **At least 4 routes** from the seven-route list in Step 1 have actually been run and produced leads — no single-source betting.
- The HS code has been verified against an official source (WCO / your own country's customs / the target country's customs tariff page), not written from memory.
- Every lead has passed the three hard standards: real purchasing signs + import/export traces + a reachable contact person. Missing any one means it does not go in the table.
- There are four more gates before a lead enters the table (the door before entry): the company name is real + the city is identified + its main business matches your product + at least one **public** contact method. Missing any one goes into a separate "to be completed" pool first; it is only reviewed again once completed. **No inventing.**
- Leads where you only got a public mailbox like `info@` are marked "public mailbox only" and **not counted** as "reachable contact person obtained".
- The lead CSV header **strictly uses the script's 9 column names** (`company/country/product/source/email/phone/contact/years/note`), and `contact` has not been written under another name.
- Every lead carries an initial A/B/C rating, with the reason written in `note` so it can be traced (rating definitions and criteria: see [03 · Due Diligence](03-due-diligence.md)).
- Invalid emails and unverified emails have been removed and have not entered mass sending; negative information (closure / lawsuits / sanctions) has been checked for one round.
- **All information sources are public and legal**: no social engineering databases, no purchased private data, no impersonation to extract information.
- 30 minutes of collection at a fixed time every day has run for **10 working days** without a break (about 200 raw names).

## 4. AI prompts

**Prompt 1: Extract key information from a company website**

```
You are a B2B lead researcher. I will paste the raw text of a company website (mostly English or
Arabic). Extract ONLY facts that are explicitly stated. Never infer or guess.

Output EXACTLY this structure, and write "NOT STATED" if a field is absent:

1. Company legal name & brand names
2. HQ address + all branch addresses listed
3. Products they sell (list up to 10, with size/type if given, e.g. "TBR 12.00R20, 315/80R22.5")
4. Positioning clues: do they sell wholesale / retail / own brand / distribute others' brands?
   Quote the exact sentence as evidence.
5. Whether they mention importers, export, sourcing from Asia/China, or annual exhibitions (quote it)
6. Contacts: email, phone, WhatsApp, contact form URL, LinkedIn URL
7. Estimated company size signals (number of employees, number of locations, "leading/largest"
   claims) — quote exact wording
8. Red flags: generic mailbox only (gmail/hotmail/yahoo as sole contact), no physical address,
   site looks unfinished, brand claims unverifiable

Be strictly factual. My downstream decision is whether to invest backoffice time on this lead.
Invented details are worse than blanks.
```

Note in Chinese (translated): this prompt turns a company website's raw text into structured fields. The core is two sentences: only write what the page states in black and white; output exactly the eight fixed fields. That makes every lead the same shape, ready to go straight into the table. The red-flag field feeds directly into the next stage's due diligence.

**How the output lands in the lead table** (matching the 9 column names from Step 6):

| Prompt output item | Which column it lands in |
|---|---|
| Item 1, company name | `company` (remember to add the [Example] prefix) |
| Item 2, address → country | `country`; the full address goes in the extension table |
| Item 3, products | `product` |
| Items 4, 5, 7 (positioning / import-export / size) | Compressed into one sentence in `note` |
| Item 6, contact details | Email → `email`; phone / WhatsApp → `phone`; role → `contact`; official site → extension table |
| Item 8, red flags | Appended to `note`, handed to [03 · Due Diligence](03-due-diligence.md) |

> Do not stuff the official site address into `product` or any column other than `note` — the script does not read `website`, and stuffing it there scores nothing.

**Prompt 2: Batch-rank leads by priority**

```
You are a sales operations analyst. Below is a table of 25 potential buyers for a Chinese tire
exporter targeting {country}. Score and rank them.

For EACH company produce a one-row table with:
- Priority (A = contact within 3 days, B = within 2 weeks, C = backlog/nurture)
- Fit score 0-10 (product match + import evidence + size signals)
- Contactability 0-5 (did we get a named person or a working channel?)
- Confidence 0-1 (how sure are you that this company still trades and is a real importer)
- ONE next action, written as a concrete instruction (not "research more") —
  e.g. "Find Purchasing Manager on LinkedIn, send InMail in EN, ask for 2025 import volume"

Then output:
- TOP 5 with a 2-sentence justification each
- BOTTOM 5 with the single reason to deprioritize
- A note listing which companies had UNVERIFIED claims in their input

Rules: use only information present in my table. Do not invent company facts. If my data is
insufficient, lower Confidence rather than inventing detail.
```

Note in Chinese (translated): this prompt stops you from marking everything A just because it looks good. It forces the AI to give a confidence score, and it must give "one concrete next action" instead of vague advice. It also exposes companies with insufficient data on its own, reminding you to go fill in information rather than sending emails anyway.

**Prompt 3: Search strategy generator**

```
You are an OSINT research planner for B2B export lead generation in the tire industry
(target market: {country}).

Design 12 concrete search queries I can run, mixed deliberately across four sources:
A) Google/Bing web search  B) LinkedIn people/title search  C) trade-fair exhibitor directory
D) customs/import-data platform filters

Rules:
- Queries must be realistic, copy-paste-able strings. Use the local language where useful.
- Include at least 4 queries using import/HS/product terminology rather than generic words.
- Include at least 3 queries designed to find NEGATIVE signals (lawsuit, complaint, sanction,
  "closed", "ceased operations", "no longer active") so I can screen dead companies.
- For each query state: source, what it should surface, and how many results I should expect
  to keep (be realistic, not optimistic).

Also list 4 query patterns that are USELESS in this market and say why — I want to avoid
the search traps I am likely to fall into.
```

Note in Chinese (translated): this prompt gets you a whole search strategy in one go, and it specifically includes queries that look for "negative signals" — many people only search for good news, then treat a company that has closed, been sued or been sanctioned as a fresh lead and send it emails. That is pure waste. Part 4, "useless query patterns", tells you directly which traps not to step into.

## 5. Checklist

- [ ] **At least 4 routes** have actually been run for at least one round and produced leads — not just "customs data is switched on"
- [ ] The HS code has been verified against an official source (WCO / your own country's customs / the target country's customs tariff page)
- [ ] The lead table header strictly uses the script's 9 column names, and the `contact` column has not been written as `contact_role` or another alias
- [ ] Every row carries a `source` mark (so you can trace "where did this one come from"), with a value inside the five standard values
- [ ] `years` is all plain numbers (no writing like "ten years")
- [ ] WhatsApp numbers are written in the `phone` column with a `wa` / `whatsapp` marker — no separate column opened
- [ ] Purchasing-signal keywords are written in `note` / `product` / `contact` — no separate column opened
- [ ] Every lead has been screened against the three hard standards: real purchasing signs + import/export traces + a reachable contact person
- [ ] Leads where only a public mailbox (`info@` / `sales@` etc.) was obtained are marked "public mailbox only" and not counted as having a contact person
- [ ] Companies in the customs data that "imported a sample only once" or "switch suppliers frequently" have been downgraded with the reason written in `note`
- [ ] "Importer" and "distributor / retailer" have been distinguished, with the channel role written in `note`
- [ ] Every lead carries an initial A/B/C rating, with the rating reason in `note` rather than by feel
- [ ] 20 leads a day / 30 minutes is on the calendar and has run for 10 working days without a break
- [ ] Invalid emails have been removed; unverified emails have not entered the mass-send list
- [ ] Negative-information retrieval has been run for one round (closure / lawsuits / sanctions / ceased operations), and suspicious companies are flagged
- [ ] **All information sources are public and legal**: no social engineering databases, no purchased private data, no impersonation to extract information

## 6. Common beginner traps

**Trap 1: Only doing the customs-data route**
- What it looks like: two days pulling 300 customs records, staring at the screen feeling pleased, then getting stuck and not moving.
- Why: customs data only has company names and trade records — no emails, no people, no product details. It is only a list entry point, not the destination.
- The right move: use customs data only as the "list entry point". Per the daily quota split in Step 1, the 8 customs rows must be paired with the other 12 completion actions to count as one full round.

**Trap 2: Treating a company name as a finished lead**
- What it looks like: 300 rows in the table, all company names, the contact column completely blank — the same as not filling it in.
- Why: treating "finding the company" as the destination, without realizing that sending outreach to info@ is shouting at the company receptionist, and the receptionist has no purchasing authority.
- The right move: a specific person must be filled in before a lead enters the table. If no person can be found, downgrade it to B and mark it "person still to dig out" — do not let it occupy an A slot.

**Trap 3: Mass-sending one guessed email format**
- What it looks like: guessing 200 emails in the `firstname.lastname@sample.example` format and blasting them out at once, with a 60% bounce rate.
- Why: wrongly guessed emails sent in bulk drag your domain reputation down with them, and later emails that could genuinely get through end up in spam too — you bury yourself.
- The right move: test in small batches (10–20 at a time) to verify first, and stop immediately if the bounce rate passes 10%. Better 50 accurate sends than 200 sends with 140 fakes in them.

**Trap 4: Only checking "does it have a website", not "what does the website say"**
- What it looks like: seeing an English page and treating it as a quality customer — like assuming someone is rich because their shopfront looks grand.
- Why: most websites today are AI-generated; they look convincing but carry no purchasing signal at all.
- The right move: read the product catalog, check whether brands are listed, look for wholesale / distribution wording, check the founding year. Having a website ≠ importing. Those are two different things.

**Trap 5: Using the trade fair directory as the only source**
- What it looks like: copying one trade fair exhibitor list and starting mass outreach.
- Why: an exhibitor directory is "companies willing to pay for exposure"; the same company appears at multiple fairs, and some of them have already closed.
- The right move: a trade fair directory is only 1 of the daily 20 (about 5%), and it must pass a triple check — "consecutive exhibition years + official site activity + customs records" — before entering the table.

**Trap 6: No fixed collection schedule — three days fishing, two days drying the net**
- What it looks like: a busy week with no touching it at all, and all the feel is gone.
- Why: treating lead-finding as a project instead of a daily action.
- The right move: tie it to a fixed time slot every day. Channel discipline matters more than cleverness: better 30 minutes a day than one 8-hour push followed by a week off.

**Trap 7: Searching without recording — closing the page when done**
- What it looks like: an afternoon searching dozens of companies, closing the browser, and not remembering a single one the next day, while the lead table is still empty.
- Why: treating "having seen it" as "having got it". A lead's only home is **that row in the CSV**, not a vague impression in your head.
- The right move: the moment you find a company, open the table and fill in one row — even if it is only the four cells `company` / `country` / `source` / `note`. **Not in the table = does not exist.** Better 20 complete rows a day than having "seen" 100 companies.

**Trap 8: Going after big state-owned enterprises and big groups only**
- What it looks like: picking only the most impressive-looking companies, sending emails, hearing nothing for two weeks, and losing heart.
- Why: big groups have mature suppliers, annual tenders and layers of approval. A newcomer prying from zero basically cannot pry them open — it is not that your email was badly written, it is that the entry point is wrong.
- The right move: treat "will they even reply to you" as a filter too. Prioritize **companies with short decision chains**: small and medium traders, family businesses, small companies where the Owner decides directly. After you have 2–3 closed deals in the target country, go back and attack the big groups.

**Trap 9: Mistaking a distributor for an importer**
- What it looks like: finding a company whose website sells tires, treating it as an importer, and going straight to price and container quantities.
- Why: the channel role was never distinguished. A distributor only buys wholesale locally — it does not clear customs or book containers. Talking FOB / CIF and 40HQ loading plans with it, it simply cannot decide.
- The right move: write the channel role into `note` when the lead enters the table — **importer / distributor / retailer / end-user fleet**. Check three things: whether the website says "wholesale / distribution / agency", whether customs records show it clearing goods, and whether the competitor distributor page lists it as a distributor. Different roles mean completely different quotations and scripts later (see [06 · Quotation](06-quote.md)).

## 7. Copy-paste templates (fill in, no AI needed)

**Template 1: Lead master table `my_leads.csv` (headers exactly matching `scripts/lead_score.py` — feed it straight to the script)**

```
# All data in this table is fictional example data (for teaching demos only). Company names carry the "[Example]" prefix, emails use the reserved domain sample.example, and phone numbers are placeholders. None of them correspond to any real business or real contact. Do not contact anyone based on this.
company,country,product,source,email,phone,contact,years,note
[Example] Gulf Tire Trading,Saudi Arabia,"TBR 12.00R20, PCR tubes",customs,purchasing@sample.example,+000 00 000 0000 (WhatsApp),purchasing manager,18,"Annual RFQ for truck tyres, looking for supplier, 40HQ container regular. Importer, 3 warehouses"
[Example] Dubai Wheel House,UAE,"PCR 195/65R15, alloy rims",trade_show,,+000 00 000 0001,buyer,9,"Met at Gulf Oil Show, asked for quotation, 20GP trial order. Distributor, no import record"
[Example] Nile Trading,Egypt,"PCR tubes, motorcycle tyres",search,contact@sample.example,+000 00 000 0002,procurement,6,"Requesting quotation for 20GP mixed container. Only public mailbox info@, contact person not found"
```

Three copy points (get these wrong and the script will silently under-score):

- The headers are exactly these 9 — **do not change a single word** (especially do not write `contact` as `contact_role`).
- `source` may only be one of `referral` / `trade_show` / `customs` / `linkedin` / `search`.
- `years` takes numbers only; WhatsApp numbers go in `phone` with the word `WhatsApp` attached.

**Template 2: Extension table (fields the script does not read — open a separate table, joined by company)**

```
company,website,channel_role,priority(A/B/C),status,next_followup,language,owner
```

> Putting "follow-up status / next follow-up / official site / A-B-C" here keeps the master table in the clean structure the script can read directly. Join the two tables on `company` — do not stuff the master CSV with columns the script cannot read.

**Field-filling definitions:**

- `source`: `referral` / `trade_show` / `customs` / `linkedin` / `search`
- `priority`: A = contact within 3 days · B = within 2 weeks · C = nurture (definitions and criteria: see [03 · Due Diligence](03-due-diligence.md))
- `channel_role` (extension table): importer / distributor / retailer / end-user fleet — see Trap 9
- `note`: brands / price band / warehouse and store counts / import records / red flags — as specific as you can write them (the script looks for purchasing-signal keywords here)

**Three-hard-standards self-check (tick before each lead enters the table):**

```
Company name: ____________  Purchasing signs □   Import/export traces □   Reachable contact person □
Contact name: ________  Email type: named □ / department □ / public mailbox □
Channel role: importer □ / distributor □ / retailer □ / end user □
Is the information source public and legal: yes □ (no → do not enter the table)
```

Run it and check the result:

```
python scripts/lead_score.py my_leads.csv --format detail
```

## 8. Next stage

The list is ready — but do not send emails yet. It contains scammers, shell companies, and companies that simply do not buy. The next step is **[03 · Due Diligence](03-due-diligence.md)**: compress the 200 names into a batch of real buyers worth spending time on.

**Handover items (the three things passed to the due diligence stage):**

1. `my_leads.csv` — the raw list (around 200 rows) built on the script's 9 columns.
2. The script's grading output (T0 / T1 / T2 / T3 distribution) — used to decide who to diligence first, not the final customer rating.
3. The extension table — official site links, channel roles, initial A/B/C ratings with reasons, for due diligence to pick up directly.

After due diligence has graded A/B/C, go to [04 · Outreach](04-outreach_en.md) to convert them to T0–T3 and start first contact. **Do not send emails directly from stage 02** — sending from an unfiltered list wastes your own domain reputation.
