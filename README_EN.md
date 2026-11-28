# zero-to-trade

[中文](README.md) · **English** · [Español](README_ES.md) · [Português](README_PT.md) · [Français](README_FR.md) · [العربية](README_AR.md) · [Русский](README_RU.md) · [Deutsch](README_DE.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Türkçe](README_TR.md) · [Bahasa Indonesia](README_ID.md)

![CI](https://github.com/6hn68/zero-to-trade/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-306998)

**Seven stages, from "which country do I even pick" to "the money arrived." Plus fifteen Python scripts that do the boring parts, and a website with four tools that run right in your browser. No experience assumed. That's the point.**

> You sent 200 cold emails and got zero replies. That's not your English. That's your order of operations.
>
> This repo turns "start exporting" into something you can actually work: which site to open this afternoon, what to type into it, and what result means you passed.

> The one rule underneath everything here: **AI does the heavy lifting, you make the calls.**

No course to buy. No paid tier. No email wall. MIT licensed, V20.

> PRs welcome, especially from people who sell into a market this repo has never heard of. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 7-step demo: tier a real list and write your first outreach in 2 minutes

No need to read the docs first. Seven steps, one line each, one copy-paste command each — about 2 minutes end to end. All seven commands below were actually run in this repo (2026-11-24, Python 3.x, standard library only). The sample data is fictional; company names carry the 【示例】 ("sample") prefix.

| Step | In one line | Command (copy-paste) |
|---|---|---|
| 1 Get a list | Copy the sample into your own file; your real leads go only in this copy | `cp examples/leads_example.csv my_leads.csv` |
| 2 Tier it | 10 leads sorted into T0–T3; call 2 of them today | `python3 scripts/lead_score.py my_leads.csv` |
| 3 Vet the T0s | Run it with only the company name first: anything you did not provide comes back "to verify" and it lands on C — that is the demo; a real vet feeds in the facts you found before deciding | `python3 scripts/due_diligence.py --company "【示例】海湾轮胎贸易"` |
| 4 Write the first touch | Outreach draft for the T0 tier, English to send, Chinese for your own review | `python3 scripts/outreach_gen.py my_leads.csv --tier T0` |
| 5 Plan follow-ups | D0/D2/D5 rhythm: 3 touches in 6 days, stop after the third silence | `python3 scripts/followup_plan.py --tier T0 --start 2026-11-24 --csv my_leads.csv` |
| 6 Quote when they reply | Cost + freight + margin → FOB/CIF range + a three-step concession ladder | `python3 scripts/quote_engine.py --cost 28 --freight 6 --margin 15` |
| 7 Nudge when they go quiet | 7 days after the quote with no reply, ask about progress — firm, not desperate | `python3 scripts/nudge.py --day D7 --scenario quoted` |

After step 4 you hold a first-touch email you can actually send; after step 5 you know what to do each day for the next 6 days. For step 5, put the day you run it in `--start` (2026-11-24 above — swap in today); don't let D5 land on a Friday (Jumu'ah) — the script warns you to shift it if it does.

Step 3 with only a company name returns C and tells you to gather evidence before outreach — correct behaviour: with no evidence it will not invent a good rating. For a real vet, fill in the facts you found (website, years, source, customs record); the A-grade example in `python3 scripts/due_diligence.py --help` rates this same company A. Step 4 still drafts the outreach because step 2 already tiered it T0 on the CSV's source, email and years evidence.

No Python? Open the website, [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/) (or double-click [`index.html`](index.html) in a local copy). It has four tools that run in the browser — lead scoring, outreach, follow-up plan and quote — with the same rules as the scripts, and the interface comes in 12 languages (top-right menu). Load the sample list → score it and find your T0s → generate the first-touch message and copy it → replace the `[ ]` placeholders with your own name, company and WhatsApp → plan the D0/D2/D5 follow-ups → quote when they reply. Nothing is uploaded: your list never leaves the browser. The first-touch copy on the website comes in English with a Chinese reference; for Spanish, Portuguese or Arabic copy, use `outreach_gen.py --lang es/pt/ar`.

---

## What this actually fixes

Google "how do I start exporting." You get one guy's success story, two hundred SEO posts, the free preview of a paid course, and a YouTube thumbnail promising money fast. You read all of it, you feel informed, and the next morning you're staring at a customs-data site with no idea what goes in the first field.

That's not a shortage of information. It's information in the wrong shape: chopped into fragments, written from the winner's point of view, and stopping right before the part where you do something.

Here's how most tutorials handle it. *"You should do background research on your customers."* Then: *"Background research is important."* Then nothing. You still don't know which fields, which websites, what a red flag looks like, or when you've checked enough.

This repo does the opposite: **take one task and keep breaking it down until it's an action.**

| What a tutorial says | What this repo says |
|---|---|
| "Do background research" | L1 screen, three checks: does the site exist, how long has the company been registered, are the social accounts alive. Fail any one and the lead is dead. |
| "Quality matters more than quantity" | 10 leads get sorted into T0/T1/T2/T3, each tier with its own next move and its own time budget. |
| "Follow up with them" | Day 0, day 2, day 5 — three touches, a different angle each time, and the day-5 note closes it; after that, stop. |
| "AI is changing trade" | Fifteen stdlib-only Python scripts (fourteen business scripts, one of them a quoting engine, plus one privacy guard). `python3 scripts/lead_score.py examples/leads_example.csv` and you have the full tiering in about thirty seconds. |

Same information. Different **grain size**. That's the entire difference. Every claim in here has to survive one question: what do I open this afternoon, and what do I type?

So no, this isn't motivation. It's a checklist and fifteen script files (fourteen business scripts + one privacy guard).

---

## The seven stages

One chain, start to finish: pick a country, end with money in the bank. One doc per stage, and every doc ends with something you can actually use.

| Stage | What you do | Output |
|---|---|---|
| **01 Pick a market** | Score it on language, demand, and barrier | 1 first market + 3 reasons to defend it |
| **02 Find leads** | Four routes: customs data, social, search, trade shows | ≥20 verified leads per day |
| **03 Vet the buyer** | L1 screen → L2 standard → L3 deep dive | A/B/C rating; scammers filtered out |
| **04 Make contact** | Tier leads T0-T3; run three channels on first touch | Tiered list + D0/D2/D5 follow-up plan (3 touches in 6 days) |
| **05 Talk specs** | Small asks first. Price is always last | Spec / quantity / destination port |
| **06 Quote & negotiate** | Quote discipline: every concession buys something in return | Quote sheet + concession ladder + talk tracks |
| **07 Deliver the order** | Contract, production, inspection, documents, payment, freight | Closed delivery loop + repurchase plan |

Stage docs live in `docs/`, one file per stage, all following the same six-part structure (see [CONTRIBUTING.md](CONTRIBUTING.md)): **what this stage is for → how to do it, step by step → the pass/fail criteria → the classic mistakes → copy-paste templates → the AI prompts for this stage.**

**Never done this before?** [`docs/00-getting-started.md`](docs/00-getting-started.md) assumes no git and no Python: about 2 minutes in the browser with nothing to install, or about 20 minutes the first time if you install Python. In a hurry instead? [`docs/fast-path.md`](docs/fast-path.md) is seven days from zero to your first reply.

---

## 30-second quickstart

**Don't want to install Python?** Open the website: [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/). Four browser tools — lead scoring, outreach, follow-up plan and quote — in 12 interface languages. Paste a CSV, get the T0-T3 tiering, then the first touch, the follow-up dates and the quote. Nothing to install, and nothing leaves your browser.

Fifteen script files: fourteen business scripts, one of them the quoting engine, plus a privacy guard script (`check_private_data.py`, scans for real customer data before you commit). Standard library only. Python 3.10+.

```bash
# 1. Tier your leads. CSV in, T0-T3 out, each tier with its next move.
python3 scripts/lead_score.py examples/leads_example.csv

# 2. Draft outreach copy for one tier, English and 中文 side by side.
python3 scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. Build the follow-up plan. Three touches, real dates.
python3 scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv

# 4. Quote: cost + freight + margin -> FOB/CIF range + a 3-step concession ladder.
python3 scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

What that first command actually prints, on 10 sample leads. The script outputs in Chinese; 【示例】 is just a marker meaning "sample", and the last column is translated here:

| Tier | Company | Country | Score | Next action |
|---|---|---|---|---|
| T0 | 【示例】海湾轮胎贸易 | Saudi Arabia | 95 | send first touch today, don't wait |
| T0 | 【示例】三角洲轮胎 | Saudi Arabia | 88 | send first touch today, don't wait |
| T1 | 【示例】阿曼蓝海 | Oman | 77 | this week; draft the copy today |
| T1 | 【示例】半岛汽车 | Saudi Arabia | 71 | this week; draft the copy today |
| T1 | 【示例】尼罗河商贸 | Egypt | 67 | this week; draft the copy today |
| T1 | 【示例】迪拜轮毂行 | UAE | 65 | this week; draft the copy today |
| T1 | 【示例】利雅得汽配 | Saudi Arabia | 60 | this week; draft the copy today |
| T2 | 【示例】尼日利亚先锋 | Nigeria | 50 | cold pool, sweep it once a day |
| T3 | 【示例】黎凡特供配 | Lebanon | 24 | not enough info, go find contact + need first |
| T3 | 【示例】利雅得零件店 | Saudi Arabia | 17 | not enough info, go find contact + need first |

Summary: **T0:2 / T1:5 / T2:1 / T3:2**. Contact today: 【示例】海湾轮胎贸易, 【示例】三角洲轮胎. This week: 【示例】阿曼蓝海, 【示例】半岛汽车, 【示例】尼罗河商贸, 【示例】迪拜轮毂行, 【示例】利雅得汽配. Leave alone for now: 【示例】黎凡特供配, 【示例】利雅得零件店.

CSV header:

```
company,country,product,source,email,phone,years,contact,note
```

Only `company` is required. Everything else can be blank, and blanks score at the floor. `source` moves the needle most: `referral` / `trade_show` / `customs` / `linkedin` / `search`.

All fifteen scripts take `--help`. `lead_score.py` also has `--format json` and `--country` / `--product` filters, if you want to pipe it into a spreadsheet.

The scripts only decide what a machine can decide: is there an email, is there a website, does this clear the T0 bar. Whether a lead deserves your afternoon lives in the docs, and in your head.

---

## Repository layout

```
zero-to-trade/
├── README.md              # Full Chinese version
├── README_EN.md           # This file (the reference for every translation)
├── README_ES.md / README_PT.md / README_FR.md / README_AR.md / README_RU.md
├── README_DE.md / README_JA.md / README_KO.md / README_TR.md / README_ID.md
│                          # Spanish, Portuguese, French, Arabic (RTL), Russian, German, Japanese, Korean, Turkish, Indonesian
├── index.html             # The website: 4 browser tools, 12 interface languages, zero dependencies (GitHub Pages)
├── MANIFESTO.md           # Anonymous, no paid course: the brand stance
├── GITHUB_LAUNCH.md       # Launch + promo checklist (Topics/About/PR/Show HN)
├── CONTRIBUTING.md        # How to contribute + doc and code conventions
├── CHANGELOG.md           # Changelog: what changed each time
├── ROADMAP.md             # Roadmap: where versions go next
├── LICENSE                # MIT
├── docs/                  # One file per stage
│   ├── 00-getting-started.md
│   ├── fast-path.md       # 7 days from zero to first reply
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   ├── 07-order-delivery.md
│   └── deal-walkthrough.md # A realistic first-deal worked example
├── scripts/               # Runnable Python, standard library only
│   ├── lead_score.py      # Tier leads T0-T3
│   ├── outreach_gen.py    # Outreach copy per tier (EN/ZH + ES/PT/AR with English reference, V13)
│   ├── followup_plan.py   # D0/D2/D5 follow-up plan (3 touches in 6 days)
│   ├── quote_engine.py    # Quoting engine: FOB/CIF range + 3-step concession ladder
│   ├── due_diligence.py   # V11 background-check agent: L1/L2/L3 + A/B/C rating + red flags
│   ├── tire_pack.py       # V12 tire industry pack: size + market → GCC points + clearance docs + market notes
│   ├── landed_cost.py     # Landed cost, V14: FOB + freight + insurance → CIF, plus duty + destination charges → DDP
│   ├── trade_show.py      # Trade show, V15: exhibitors collected at the show → 24-hour follow-up plan (thanks in 2h, quote lead in 12h, call/WhatsApp chase in 24h)
│   ├── nudge.py           # Nudge library, V16: D3/D7/D14/D30 × quoted/sampled/negotiating → short WhatsApp version + longer email version (English + Chinese)
│   ├── anchor_price.py    # Competitor anchor pricing, V18: customs-data competitor price range + your own cost → aggressive/median/conservative CIF tiers + 5-item checklist
│   ├── fast_path.py     # V19 interactive 7-day fast path: --day N shows tasks, --done N checks off, --progress totals (aligned with docs/fast-path.md)
│   ├── market_rules.py    # Market rules: target markets, Turkey/Brazil barriers, Mexico/US/EU exclusions
│   ├── daily_video_list.py  # Daily list of 5 videos (3 in the morning, 2 in the afternoon) with size, market, selling point and shot checks
│   ├── fulfillment_checklist.py  # Order fulfillment checklist: PI → deposit → production → inspection → balance → booking → customs → B/L → clearance docs → after-sales, hard money gates on deposit/release/shipping
│   └── check_private_data.py  # Privacy guard: scans for real customer data before commit
├── examples/
│   ├── leads_example.csv  # Sample data, runnable as-is
│   ├── leads_example_lighting.csv  # Non-tyre sample: 8 LED lighting leads
│   └── trade_show_example.csv  # Sample exhibitors, one per interest level
├── tests/                 # 680 standard-library tests
├── prompts/
│   └── AI_PROMPTS.md      # 40 copy-paste prompts (28 core + 12 advanced), grouped by stage
└── assets/                # Screenshots, diagrams
```

---

## Why scripts, and not just a method doc

Most "AI for business" repos do the same thing: take the methodology, paste it into a prompt, ship it. This one runs backwards. **Discipline first, tools second.**

Here's why: **being good at prompts is not the same as being good at trade.** My bet is that you're not short of wording. You're short of a way to decide. So:

- **The rules are the product here.** T0 gets an email today. T3 sits in a drawer for three months. A concession that buys nothing back is a gift, not a negotiation. No model gets to make those calls for you.
- **Volume goes to AI.** Screening 8 leads in one pass, drafting three levels of background research on 50 companies, spinning out seven days of follow-up variants. Hours of work, almost no judgement in it.
- **Anything repeatable gets scripted.** If tiering is a feeling, it isn't a standard. So it's a script under 200 lines with zero dependencies, and two people running it land on the same answer.

Where the line sits: **can it be an `if/else`? Into a script. Does it need a trade-off? Into the docs. Does it have to sound like a human wrote it? Into `prompts/`.**

No pandas, no OpenAI SDK, on purpose. Environment setup is where beginners quit. Someone new to export will lose more hours to `pip install` than to finding customers, and that's a stupid place to lose them.

---

## Roadmap

> Full roadmap: [ROADMAP.md](ROADMAP.md); change history: [CHANGELOG.md](CHANGELOG.md).

| Version | Status | Contents |
|---|---|---|
| **V13** | ✅ Landed (2026-11-07) | Multilingual outreach (`scripts/outreach_gen.py --lang es/pt/ar`: Spanish/Portuguese/Arabic copy + English original after every draft; templates mirror the English T0/T1/T2 one-to-one, single inline dict in the script) + `docs/04-outreach.md` new section (usage + 3 real outputs pasted verbatim) + `tests/` 80 stdlib tests + 40 prompts unchanged (28 core + 12 advanced) + 7 script files |
| **V18** | ✅ Landed (2026-11-07) | Competitor anchor pricing (`scripts/anchor_price.py`: customs-data competitor price range + your own cost → aggressive/median/conservative CIF tiers, each with profit room, margin, FOB equivalent, implied markup and when to use it; a 5-item checklist — cost, freight, FX, payment terms, validity — before you quote, any unchecked item flagged; below-cost warning “below cost, don't take the order, negotiate volume for price first”; missing median estimated as (low + high) / 2 and marked as an estimate; `--format json` / `--audience client`) + `docs/anchor-price.md` (usage + anchor guide + 2 real outputs pasted verbatim) + one line in `docs/06-quote.md` (anchor before you quote) + `tests/` 187 stdlib tests + 40 prompts unchanged (28 core + 12 advanced) + 11 script files |
| **V20** | ✅ Current (2026-11-14) | Local-increment merge + 10 hardening rounds: unified CLI entries (plain-language errors, aligned exit codes) + stronger tests (single-message mode, `--start-date` alias, run logs) + doc numbers aligned + non-tyre example (8 LED lighting leads) + demo page synced with V19 + friendly errors for bad CSVs (missing column / empty file / unclosed quote no longer traceback) + prompt alignment (P04-4 follow-up command gains `--avoid-weekend`, P10-2 window unified at 48 hours) + run tracing landed (`logs/trace-YYYY-MM-DD.jsonl`, one line per run of the three core scripts) + code cleanup (shared helpers kept in one place, net −151 lines; two dead helpers removed) + `tests/` 680 stdlib tests + 40 prompts unchanged (28 core + 12 advanced) + 15 script files |
| **V19** | ✅ Landed (2026-11-07) | Interactive 7-day fast path (`scripts/fast_path.py`: `--day N` shows the day's tasks — task name + what to produce + which script/doc to use; `--done N` checks a day off with a timestamp, written to the `--state` JSON file, a repeat check-in says already checked in and is not recorded twice; `--progress` totals done / remaining / overdue (overdue = planned date earlier than today and not checked off, planned date = `--start` day 1 + (N-1) days; no `--start` means no overdue count, stated plainly); `--list` shows all 7 days; tasks aligned line by line with `docs/fast-path.md`, no second list invented; `--help` carries real examples, a bad day or date gets a plain-language error) + `docs/fast-path-interactive.md` (usage + state-file format + overdue rule + 7-day overview + 2 real outputs pasted verbatim) + one line at the top of `docs/fast-path.md` (interactive entry) + one line in `docs/00-getting-started.md` step B5 (8 remaining scripts → 9) + `tests/` 226 stdlib tests + 40 prompts unchanged (28 core + 12 advanced) + 12 script files |
| **V17** | ✅ Landed (2026-11-07) | Full Portuguese and Arabic READMEs (new `README_PT.md` in Brazilian Portuguese and `README_AR.md` in Arabic with RTL layout, both translated in full and aligned with README_EN.md: same sections, tables, commands, script names, file names, version and numbers; all sample companies/prices/contacts are fictional, marked 【示例】 with the sample.example reserved domain) + `tests/` 167 stdlib tests + 40 prompts unchanged (28 core + 12 advanced) + 10 script files |
| **V16** | ✅ Landed (2026-11-07) | Nudge library (`scripts/nudge.py`: D3/D7/D14/D30 × quoted/sampled/negotiating, 12 drafts in total, short WhatsApp version + longer email version, English first with Chinese translation after every draft; tone ladder — D3 light reminder, D7 ask for progress, D14 three options to save face (lower price / different spec / longer payment terms), D30 final note that leaves the door open; Day 0 is the day the quote/sample/price talk went out, a different anchor from followup_plan's first-touch cadence, one thread follows one line only; `--channel whatsapp/email/both` / `--format json` / `--out`) + `docs/nudge.md` (usage + how it lines up with followup_plan + 2 real outputs pasted verbatim) + one line in `docs/00-getting-started.md` (script list 6 → 7) + `tests/` 152 stdlib tests + 40 prompts unchanged (28 core + 12 advanced) + 10 script files |
| **V15** | ✅ Landed (2026-11-07) | Trade-show follow-up (`scripts/trade_show.py`: exhibitors collected at the show ranked by interest into a 24-hour follow-up plan — thanks + materials in 2h, quote lead in 12h, call/WhatsApp chase in 24h; `--add` one by one + `--csv` batch, `--format json` / `--out`; first-touch draft follows the outreach_gen T0/T1/T2 template) + `docs/trade-show.md` (usage + 1 real output pasted verbatim) + `examples/trade_show_example.csv` (3 sample exhibitors, one per interest level) + one line each in `docs/00-getting-started.md` and `docs/02-find-leads.md` (what to do with leads after the show) + `tests/` 127 stdlib tests + 40 prompts unchanged (28 core + 12 advanced) + 9 script files |
| **V14** | ✅ Landed (2026-11-07) | Landed cost estimation (`scripts/landed_cost.py`: FOB + freight + insurance → CIF, plus duty + destination-port charges → DDP; per-unit cost + totals + profit room when a sell price is given; `--qty` / `--format json` / `--audience client`) + `docs/landed-cost.md` (usage + formula table + 2 real outputs pasted verbatim) + one line each in `docs/00-getting-started.md` and `docs/06-quote.md` (quote FOB/CIF with quote_engine first, then work out the full landed cost with landed_cost) + `tests/` 97 stdlib tests + 40 prompts unchanged (28 core + 12 advanced) + 8 script files |
| **V12** | ✅ Landed (2026-11-07) | Tire industry pack (`scripts/tire_pack.py`: size + market → GCC certification points + destination-port clearance documents + market notes; 4 TBR sizes × 8 markets) + `docs/tire-pack.md` (usage + 2 real outputs pasted verbatim) + `docs/00-getting-started.md` script list updated + `tests/` 68 stdlib tests + 40 prompts (28 core + 12 advanced) + 7 script files |
| **V11** | ✅ Landed (2026-11-07) | Background-check agent (`scripts/due_diligence.py`: L1/L2/L3 + A/B/C rating + red-flag checklist + client view + JSON output) + `docs/03-due-diligence.md` section 13 (real output pasted verbatim) + prompt P03-5 + `tests/` 52 stdlib tests + 40 prompts (28 core + 12 advanced) + 6 script files |
| **V10** | ✅ Landed (2026-11-07) | 6 advanced modules (08 standalone site / 09 social matrix / 10 trade shows / 11 logistics & payment / 12 risk & compliance / 13 key accounts) + 3 learning paths + troubleshooting & contributor workflow + quoting engine hardened (client-view isolation, boundary checks) + `tests/` 30 stdlib tests + 39 prompts (27 core + 12 advanced) + browser demo scoring aligned with Python |
| **v0.1.5** | Shipped | Zero-install browser demo (index.html) + v0.2 quoting engine alpha (quote_engine.py) + brand manifesto (MANIFESTO) + launch/promo checklist (GITHUB_LAUNCH) + Fast Path + deal walkthrough |
| **v0.1** | Shipped | 7 stage docs, 4 stdlib business scripts, 27 prompts, bilingual README |
| **v0.2** | ✅ Landed (alpha) | **AI quoting engine**: `scripts/quote_engine.py` is live — input costs + market + competitor anchor price → FOB/CIF range + a three-step concession ladder (each step must buy something); client-view isolation and boundary checks hardened (see `tests/test_quote_engine.py`) |
| **Next version** | To be decided | Next direction to be decided (interactive 7-day fast path landed in V19) |
| **Long term** | — | Industry packs (tyres, building materials, machinery, hardware); outreach copy in French/Russian (Spanish, Portuguese and Arabic landed in V13); public de-identified lead datasets; wiring the quoting engine to customs data for automatic competitor anchor pricing |

V20 does not wait for the next version: the 10 hardening rounds are ready to use now (bad CSVs get plain-language errors instead of tracebacks, every run writes one trace line, shared helpers live in one place). No need to wait for the next version — the scripts are already in the repo, with 680 tests all green.

---

## Contributing

The hole here isn't docs. It's **country-specific field detail.** I know how the first tyre order into the Middle East goes. I have no idea how building-materials distribution works in Ecuador, or which documents Nigerian customs actually wants. Only people selling there can fill that in.

Three ways in, cheapest first:

1. **Fix something.** Typo, stale fact, a rule that reads like mush. Open an issue. One sentence beats silence. The template asks three things: which line lost you, which number has no source, which rule doesn't hold in your industry.
2. **Translate a stage.** Spanish, Arabic, Portuguese, Russian, French, Vietnamese — whatever you actually speak. Keep the six-part structure, swap the language, match terms against [GLOSSARY.md](GLOSSARY.md).
3. **Add your country or industry.** This is the missing part. Write what you've done, not what you think should be done. Field names, document names, how the channel is built, how people pay, and why they refuse to pay.

Code too, with one hard rule: **Python 3.10+, standard library only.** The reasoning is in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## For developers: hackable, and it has no dependencies

All fourteen business scripts (`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine` / `due_diligence` / `tire_pack` / `landed_cost` / `trade_show` / `nudge` / `anchor_price` / `fast_path` / `market_rules` / `daily_video_list` / `fulfillment_checklist`, plus the privacy guard `check_private_data.py`) are standard library only. There is no `pip install`. Fork it, change it, drop it into your own stuff:

- Weights feel wrong? Four constants at the top of `lead_score.py` (`CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W`). Still caps at 100.
- Got your own customs data? Match the header (`company,country,product,source,email,phone,years,contact,note`) and feed it in.
- Want it inside your own tool? Every script imports clean. `score_lead()`, `render()`, `plan_followups()`, `build_quote()` are pure functions returning dicts and lists. No network, no files written.
- CI runs `py_compile` plus the test suite (Python 3.10–3.13) plus a privacy gate on every PR, so a bad edit doesn't sneak through.

> The bias here is **verifiable over clever.** Don't take my word for it: run `python3 scripts/lead_score.py examples/leads_example.csv` and read what comes out.

---

## If this saved you a wrong turn

Star it. Top-right corner. That's the whole ask. It's also how you find this again in six months, when you've forgotten the name and need the follow-up plan at 11pm.

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[View the full Star History chart](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Translations

The README comes in 12 languages, and so does the website's interface. English is the reference text.

- [中文](README.md) (Chinese, full)
- [Español](README_ES.md) (Spanish, starter, looking for reviewers)
- [Português](README_PT.md) (Brazilian Portuguese, full)
- [Français](README_FR.md) (French, full)
- [العربية](README_AR.md) (Arabic, full, RTL)
- [Русский](README_RU.md) (Russian, full)
- [Deutsch](README_DE.md) (German, full)
- [日本語](README_JA.md) (Japanese, full)
- [한국어](README_KO.md) (Korean, full)
- [Türkçe](README_TR.md) (Turkish, full)
- [Bahasa Indonesia](README_ID.md) (Indonesian, full)

The stage docs in `docs/` are still Chinese only. Translate any stage you're fluent in; keep the six-part structure and align terms against the [GLOSSARY.md](GLOSSARY.md). Native speakers who can review a README are very welcome too. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

[MIT](LICENSE) © 2026 zero-to-trade contributors

Use it, change it, sell with it. Keep the credit line. One caveat: none of this guarantees you'll land a deal. What it does guarantee is that you won't grind to a halt because you didn't know the next step.

---

## Questions & contributions

**Open an issue: https://github.com/6hn68/zero-to-trade/issues**

Something in here wrong? Say so, that counts as a contribution. Selling into a market this repo has never heard of? That's a PR I actually want. Think the whole method is off? Argue with me in an issue, I'd rather be wrong out loud.

No author bio, on purpose. **The content should be what convinces you, not who wrote it.** Need to reach me: @ the maintainer in an issue, or leave a message through the form at the bottom of the website. Either way, it reaches the author.
