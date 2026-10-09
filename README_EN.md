# zero-to-trade

![CI](https://github.com/6hn68/zero-to-trade/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.8%2B-306998)

**Seven stages, from "which country do I even pick" to "the money arrived." Plus four Python scripts that do the boring parts. No experience assumed. That's the point.**

> You sent 200 cold emails and got zero replies. That's not your English. That's your order of operations.
>
> This repo turns "start exporting" into something you can actually work: which site to open this afternoon, what to type into it, and what result means you passed.

> The one rule underneath everything here: **AI does the heavy lifting, you make the calls.**

No course to buy. No paid tier. No email wall. MIT licensed, v0.1.5 · [中文版](README.md)

> PRs welcome, especially from people who sell into a market this repo has never heard of. See [CONTRIBUTING.md](CONTRIBUTING.md).

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
| "Follow up with them" | Day 1, 3, 5, 7. A different angle each time, and day 7 ends with a decision: push or drop. |
| "AI is changing trade" | Four stdlib-only Python scripts (one alpha quoting engine). `python scripts/lead_score.py examples/leads_example.csv` and you have the full tiering in about thirty seconds. |

Same information. Different **grain size**. That's the entire difference. Every claim in here has to survive one question: what do I open this afternoon, and what do I type?

So no, this isn't motivation. It's a checklist and four scripts.

---

## The seven stages

One chain, start to finish: pick a country, end with money in the bank. One doc per stage, and every doc ends with something you can actually use.

| Stage | What you do | Output |
|---|---|---|
| **01 Pick a market** | Score it on language, demand, and barrier | 1 first market + 3 reasons to defend it |
| **02 Find leads** | Four routes: customs data, social, search, trade shows | ≥20 verified leads per day |
| **03 Vet the buyer** | L1 screen → L2 standard → L3 deep dive | A/B/C rating; scammers filtered out |
| **04 Make contact** | Tier leads T0-T3; run three channels on first touch | Tiered list + 7-day follow-up plan |
| **05 Talk specs** | Small asks first. Price is always last | Spec / quantity / destination port |
| **06 Quote & negotiate** | Quote discipline: every concession buys something in return | Quote sheet + concession ladder + talk tracks |
| **07 Deliver the order** | Contract, production, inspection, documents, payment, freight | Closed delivery loop + repurchase plan |

Stage docs live in `docs/`, one file per stage, all following the same six-part structure (see [CONTRIBUTING.md](CONTRIBUTING.md)): **what this stage is for → how to do it, step by step → the pass/fail criteria → the classic mistakes → copy-paste templates → the AI prompts for this stage.**

**Never done this before?** [`docs/00-getting-started.md`](docs/00-getting-started.md) assumes no git and no Python, and gets you moving in about 10 minutes. In a hurry instead? [`docs/fast-path.md`](docs/fast-path.md) is seven days from zero to your first reply.

---

## 30-second quickstart

**Don't want to install Python?** Open [`index.html`](index.html) in a browser. Paste a CSV, get the T0-T3 tiering. Nothing to install. (Once it's pushed, GitHub Pages hosts it, so you can send the link to someone else.)

Four scripts, one of them the v0.2 alpha quoting engine. Standard library only. Python 3.8+.

```bash
# 1. Tier your leads. CSV in, T0-T3 out, each tier with its next move.
python scripts/lead_score.py examples/leads_example.csv

# 2. Draft outreach copy for one tier, English and 中文 side by side.
python scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. Build the follow-up plan. Three touches, real dates.
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv

# 4. (alpha) Quote: cost + freight + margin -> FOB/CIF range + a 3-step concession ladder.
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
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
| T2 | 【示例】尼日利亚先锋 | Nigeria | 46 | cold pool, sweep it once a day |
| T3 | 【示例】黎凡特供配 | Lebanon | 20 | not enough info, go find contact + need first |
| T3 | 【示例】利雅得零件店 | Saudi Arabia | 10 | not enough info, go find contact + need first |

Summary: **T0:2 / T1:5 / T2:1 / T3:2**. Contact today: 【示例】海湾轮胎贸易, 【示例】三角洲轮胎. This week: 【示例】阿曼蓝海, 【示例】半岛汽车, 【示例】尼罗河商贸, 【示例】迪拜轮毂行, 【示例】利雅得汽配. Leave alone for now: 【示例】黎凡特供配, 【示例】利雅得零件店.

CSV header:

```
company,country,product,source,email,phone,years,contact,note
```

Only `company` is required. Everything else can be blank, and blanks score at the floor. `source` moves the needle most: `referral` / `trade_show` / `customs` / `linkedin` / `search`.

All four scripts take `--help`. `lead_score.py` also has `--format json` and `--country` / `--product` filters, if you want to pipe it into a spreadsheet.

The scripts only decide what a machine can decide: is there an email, is there a website, does this clear the T0 bar. Whether a lead deserves your afternoon lives in the docs, and in your head.

---

## Repository layout

```
zero-to-trade/
├── README.md              # Full Chinese version
├── README_EN.md           # This file
├── index.html             # Zero-install browser demo (GitHub Pages)
├── MANIFESTO.md           # Anonymous, no paid course: the brand stance
├── GITHUB_LAUNCH.md       # Launch + promo checklist (Topics/About/PR/Show HN)
├── CONTRIBUTING.md        # How to contribute + doc and code conventions
├── LICENSE                # MIT
├── docs/                  # One file per stage
│   ├── 00-getting-started.md
│   ├── fast-path.md       # 5 days from zero to first reply
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
│   ├── outreach_gen.py    # Bilingual outreach copy per tier
│   ├── followup_plan.py   # 3-touch follow-up plan with real dates
│   └── quote_engine.py    # v0.2 quoting engine (alpha): FOB/CIF range + 3-step concession ladder
├── examples/
│   └── leads_example.csv  # Sample data, runnable as-is
├── prompts/
│   └── AI_PROMPTS.md      # 27 copy-paste English prompts, grouped by stage
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

| Version | Status | Contents |
|---|---|---|
| **v0.1.5** | Shipped | Zero-install browser demo (index.html) + v0.2 quoting engine alpha (quote_engine.py) + brand manifesto (MANIFESTO) + launch/promo checklist (GITHUB_LAUNCH) + Fast Path + deal walkthrough |
| **v0.1** | Shipped | 7 stage docs, 4 stdlib scripts, 27 prompts, bilingual README |
| **v0.2** | 🟡 In progress (alpha) | **AI quoting engine**: `scripts/quote_engine.py` is live in alpha — input costs + market + competitor anchor price → FOB/CIF range + a three-step concession ladder (each step must buy something) |
| **v0.3** | Planned | **Buyer background-check agent**: input a company name → L1/L2/L3 research draft + red-flag checklist, with source links |
| **Long term** | — | Industry packs (tyres, building materials, machinery, hardware); outreach copy in Spanish/Arabic/French/Russian; public de-identified lead datasets; wiring v0.2's quoting engine to customs data for automatic competitor anchor pricing |

v0.3 is deliberately ahead of v0.2. To quote well you need the buyer's price band, and the best source for that is their own order history. Vet first, quote second.

---

## Contributing

The hole here isn't docs. It's **country-specific field detail.** I know how the first tyre order into the Middle East goes. I have no idea how building-materials distribution works in Ecuador, or which documents Nigerian customs actually wants. Only people selling there can fill that in.

Three ways in, cheapest first:

1. **Fix something.** Typo, stale fact, a rule that reads like mush. Open an issue. One sentence beats silence. The template asks three things: which line lost you, which number has no source, which rule doesn't hold in your industry.
2. **Translate a stage.** Spanish, Arabic, Portuguese, Russian, French, Vietnamese — whatever you actually speak. Keep the six-part structure, swap the language, match terms against [GLOSSARY.md](GLOSSARY.md).
3. **Add your country or industry.** This is the missing part. Write what you've done, not what you think should be done. Field names, document names, how the channel is built, how people pay, and why they refuse to pay.

Code too, with one hard rule: **Python 3.8+, standard library only.** The reasoning is in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## For developers: hackable, and it has no dependencies

All four scripts (`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine`) are standard library only. There is no `pip install`. Fork it, change it, drop it into your own stuff:

- Weights feel wrong? Four constants at the top of `lead_score.py` (`CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W`). Still caps at 100.
- Got your own customs data? Match the header (`company,country,product,source,email,phone,years,contact,note`) and feed it in.
- Want it inside your own tool? Every script imports clean. `score_leads()`, `build_message()`, `plan_followups()`, `quote_range()` are pure functions returning dicts and lists. No network, no files written.
- CI runs `py_compile` plus smoke tests (py3.8/3.11/3.13) on every PR, so a bad edit doesn't sneak through.

> The bias here is **verifiable over clever.** Don't take my word for it: run `python scripts/lead_score.py examples/leads_example.csv` and read what comes out.

---

## If this saved you a wrong turn

Star it. Top-right corner. That's the whole ask. It's also how you find this again in six months, when you've forgotten the name and need the follow-up plan at 11pm.

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[View the full Star History chart](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Translations

- 🇨🇳 [中文版](README.md) (full, ready)
- 🇪🇸 🇸🇦 🇵🇹 🇷🇺 🇫🇷 🇻🇳 wanted — translate any stage doc you're fluent in; keep the six-part structure and align terms against the [GLOSSARY.md](GLOSSARY.md). See [CONTRIBUTING.md](CONTRIBUTING.md). A Spanish starter lives at [README_ES.md](README_ES.md).

---

## License

[MIT](LICENSE) © 2026 zero-to-trade contributors

Use it, change it, sell with it. Keep the credit line. One caveat: none of this guarantees you'll land a deal. What it does guarantee is that you won't grind to a halt because you didn't know the next step.

---

## Questions & contributions

**Open an issue: https://github.com/6hn68/zero-to-trade/issues**

Something in here wrong? Say so, that counts as a contribution. Selling into a market this repo has never heard of? That's a PR I actually want. Think the whole method is off? Argue with me in an issue, I'd rather be wrong out loud.

No author bio, on purpose. **The content should be what convinces you, not who wrote it.** Need to reach me: @ the maintainer in an issue. GitHub puts it in their inbox.
