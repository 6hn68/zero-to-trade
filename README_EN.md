# zero-to-trade

**An open-source operating system for selling abroad when you have zero experience. Seven stages, from choosing a market to getting paid — plus four Python scripts (one alpha quoting engine) you can actually run.**

> The premise, in one line: **AI does the heavy lifting, you make the calls.**

> 🔥 **You sent 200 cold emails and got zero replies. It's not your English — it's your order of operations.** This repo breaks "from picking a market to getting paid" into 7 executable steps plus four Python scripts (one alpha quoting engine) you can run, so each step tells you exactly which site to open, what to type, and what "passed" looks like.

> 🔓 MIT open source · 🚫 No paid course · ✅ Scripts run with zero deps (CI passing) · 🛡️ Anonymous author — credibility comes from the content

MIT licensed · v0.1.5 · [中文版](README.md)

---

## The problem this solves

Search "how do I start exporting" and you'll get a pile of things: a success-story guru, two hundred SEO blog posts, the free preview of a paid course, a YouTube video with a thumbnail promising fast money. You read them all, you feel like you understand, you open a customs-data website the next morning and still don't know what to type in the first box.

The problem isn't a shortage of information. It's that the information comes in fragments, it's edited from the winner's perspective, and it never tells you the next action.

How most tutorials handle it: *"You should do background research on your customers."* Then nothing. You still don't know which fields to check, which sites to check them on, what a red flag looks like, or when you've checked enough.

How this repo handles it: **take one task all the way down until it becomes an action.**

| What a tutorial says | What this repo says |
|---|---|
| "Do background research" | L1 screen checks exactly three things: does the site exist, how long has the company been registered, are the social accounts active. Fail any one and the lead is dead. |
| "Quality matters more than quantity" | 10 leads get sorted into T0/T1/T2/T3, and each tier comes with its own next action and its own time budget. |
| "Follow up with them" | Day 1, 3, 5, 7. Different angle each time. Day 7 ends with either a clear close or a clear drop. |
| "AI is changing trade" | Four stdlib-only Python scripts (one alpha quoting engine). `python scripts/lead_score.py examples/leads_example.csv` gives you a full tiering in 30 seconds. |

The difference isn't the amount of information. It's the **grain size**. Every conclusion in this repo has to land on: which site do you open this afternoon, what do you type, and what result counts as passed.

This isn't motivational material. It's an executable checklist and a few scripts.

---

## The seven stages

One continuous chain, from "pick a country" to "get the money." Each stage has a doc, and each stage produces something you can hold in your hand.

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

**Total beginner?** Read [`docs/00-getting-started.md`](docs/00-getting-started.md) first — no git, no Python assumed, working in about 10 minutes. Or start with [`docs/fast-path.md`](docs/fast-path.md): five days from zero to your first reply.

---

## 30-second quickstart

**No Python?** Just open [`index.html`](index.html) in a browser — paste a CSV and see the T0-T3 tiering, zero install, zero dependencies. (Auto-hosted on GitHub Pages once pushed, so anyone can open it.)

Four scripts (one is the v0.2 alpha quoting engine). No third-party packages. Python 3.8+.

```bash
# 1. Tier your leads. CSV in, T0-T3 out, each tier with its next action.
python scripts/lead_score.py examples/leads_example.csv

# 2. Generate bilingual (EN + 中文) outreach copy for a given tier.
python scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. Build a 7-day, 3-touch follow-up plan with real dates.
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv

# 4. (alpha) Quoting engine: cost + freight + margin → FOB/CIF range + 3-step concession ladder
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

Expected output from the first command (英文翻译版，便于阅读). The script prints in Chinese; the company names below are the actual sample data (【示例】 = "sample"), and the next-action column is translated to English (10 sample leads):

| Tier | Company | Country | Score | Next action |
|---|---|---|---|---|
| T0 | 【示例】海湾轮胎贸易 | Saudi Arabia | 95 | contact today, don't wait |
| T0 | 【示例】三角洲轮胎 | Saudi Arabia | 92 | contact today, don't wait |
| T1 | 【示例】阿曼蓝海 | Oman | 77 | this week |
| T1 | 【示例】半岛汽车 | Saudi Arabia | 71 | this week |
| T1 | 【示例】尼罗河商贸 | Egypt | 67 | this week |
| T1 | 【示例】迪拜轮毂行 | UAE | 65 | this week |
| T1 | 【示例】利雅得汽配 | Saudi Arabia | 60 | this week |
| T2 | 【示例】尼日利亚先锋 | Nigeria | 46 | low-freq pool, scan daily |
| T3 | 【示例】黎凡特供配 | Lebanon | 20 | info insufficient, top up first |
| T3 | 【示例】利雅得零件店 | Saudi Arabia | 10 | info insufficient, top up first |

Summary: **T0:2 / T1:5 / T2:1 / T3:2**. Reply to first: 【示例】海湾轮胎贸易, 【示例】三角洲轮胎.

CSV header:

```
company,country,product,source,email,phone,years,contact,note
```

Only company is required; missing fields score at the floor. source matters most: referral/trade_show/customs/linkedin/search.

The scripts only handle what a machine can decide: does an email exist, does a website exist, does this lead clear the T0 threshold. Whether a lead is *worth your time* stays in the docs and in your head.

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
│   ├── followup_plan.py   # 7-day, 3-touch follow-up plan
│   └── quote_engine.py    # v0.2 quoting engine (alpha): FOB/CIF range + 3-step concession ladder
├── examples/
│   └── leads_example.csv  # Sample data, runnable as-is
├── prompts/
│   └── AI_PROMPTS.md      # 27 copy-paste English prompts, grouped by stage
└── assets/                # Screenshots, diagrams
```

---

## Why AI tools, and not just methodology

A lot of "AI for business" projects take one approach: dump the methodology into a prompt. This one does the reverse — **set the discipline first, then hand out the tools.**

The reason is simple: **being good at prompts is not the same as being good at trade.** This repo assumes what you lack isn't wording, it's a framework for deciding. So:

- **Discipline is the value.** T0 gets an email today. T3 goes in a drawer for three months. A concession without something in return is a giveaway, not a negotiation. These are rules, and no model should be making them for you.
- **AI takes the heavy lifting.** Batch-screening 8 leads, drafting three levels of background research on 50 companies, generating variants of seven days of follow-up copy — high effort, low judgement. Hand it over.
- **Scripts make it repeatable.** If tiering is done by feel each time, it isn't a standard. So it becomes a script under 200 lines with zero dependencies, and two people running it get the same answer.

The dividing line: **if it can be an `if/else`, it goes in a script; if it needs a trade-off, it goes in the docs; if it has to sound like a human on the other end, it goes in `prompts/`.**

The scripts also deliberately avoid pandas and the OpenAI SDK. Environment setup alone turns away beginners, and a beginner who exports loses more time to `pip install` than to finding customers.

---

## Roadmap

| Version | Status | Contents |
|---|---|---|
| **v0.1.5** | Added | Zero-install browser demo (index.html) + v0.2 quoting engine alpha (quote_engine.py) + brand manifesto (MANIFESTO) + launch/promo checklist (GITHUB_LAUNCH) + Fast Path + deal walkthrough |
| **v0.1** | Shipped | 7 stage docs, 4 stdlib scripts, 27 prompts, bilingual README |
| **v0.2** | 🟡 In progress (alpha) | **AI quoting engine**: `scripts/quote_engine.py` is live in alpha — input costs + market + competitor anchor price → FOB/CIF range + a three-step concession ladder (each step must buy something) |
| **v0.3** | Planned | **Buyer background-check agent**: input a company name → L1/L2/L3 research draft + red-flag checklist, with source links |
| **Long term** | — | Industry packs (tyres, building materials, machinery, hardware); outreach copy in Spanish/Arabic/French/Russian; public de-identified lead datasets; wiring v0.2's quoting engine to customs data for automatic competitor anchor pricing |

v0.3 comes before v0.2 on purpose: quoting needs to know the buyer's price band, and the most reliable source of a price band is the buyer's own order history. Vetting first, then quoting.

---

## Contributing

The gap in this repo is not a shortage of docs. It's the absence of **country-specific field detail.** I know how the first tyre order into the Middle East goes. I don't know how building-materials distribution works in Ecuador, or which documents Nigerian customs actually demands. Only people selling there can fill that in.

Three ways in, ordered by how little you need to know:

1. **Open an issue to fix something.** Typos, outdated facts, judgment calls that read as mush. One sentence beats silence. The template asks three things: which line confused you, which number has no source, which rule doesn't apply to your industry.
2. **Translate a stage doc.** Spanish, Arabic, Portuguese, Russian, French, Vietnamese — whatever you're fluent in. Keep the six-part structure, swap the language, align terms against the [GLOSSARY.md](GLOSSARY.md).
3. **Add the stage detail for your industry or country.** This is the missing part. Write what you've actually done, not what you think should be done. Down to field names, document names, channel structure, payment habits, and the reasons buyers refuse to pay.

Code contributions welcome too, with one hard constraint: **Python 3.8+, standard library only.** Reasoning in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🛠️ For developers: hackable, zero-dependency

All four scripts (`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine`) use the Python standard library only — **no third-party dependencies**. Fork it, tweak it, embed it:

- Change scoring weights? Edit the four constants at the top of `lead_score.py` (`CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W`); the max stays 100.
- Plug in your own customs data? Align your CSV header to `company,country,product,source,email,phone,years,contact,note` and feed it in.
- Embed in your own toolchain? Each script is importable — `score_leads()`, `build_message()`, `plan_followups()`, `quote_range()` are pure functions returning dicts/lists. No network, no file writes.
- CI runs `py_compile` + smoke tests (py3.8/3.11/3.13) on every PR, so your edits won't silently break.

> Design philosophy: **verifiable > flashy.** You don't have to trust me — run `python scripts/lead_score.py examples/leads_example.csv` and see for yourself.

---

## ⭐ Like it? Drop a star

zero-to-trade is **actively maintained** (recent commits in the repo history). If it saved you from a wrong turn, a star in the top-right corner is the best feedback — and the easiest way to find it again.

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[View the full Star History chart](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Translations

- 🇨🇳 [中文版](README.md) (full, ready)
- 🇪🇸 🇸🇦 🇵🇹 🇷🇺 🇫🇷 🇻🇳 wanted — translate any stage doc you're fluent in; keep the six-part structure and align terms against the [GLOSSARY.md](GLOSSARY.md). See [CONTRIBUTING.md](CONTRIBUTING.md). A Spanish starter lives at [README_ES.md](README_ES.md).

---

## License

[MIT](LICENSE) © 2026 zero-to-trade contributors

Use it, change it, sell with it — just keep the credit. Disclaimer: none of this guarantees you'll land a deal. What it does guarantee is that you won't stop because you didn't know the next step.

---

## Questions & contributions

**Open an issue: https://github.com/6hn68/zero-to-trade/issues**

Spot an error? Say so. Have field detail from a market this repo knows nothing about? Send a PR. Want to argue about the method? Open an issue.

The author's personal details are deliberately not listed here. **Credibility should come from the content, not from who wrote it.** Tag the maintainer in an issue and GitHub will route the notification.
