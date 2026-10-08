# zero-to-trade

**An open-source operating system for selling abroad when you have zero experience. Seven stages, from choosing a market to getting paid — plus three Python scripts you can actually run.**

> The premise, in one line: **AI does the heavy lifting, you make the calls.**

MIT licensed · v0.1 · [中文版](README.md)

---

## The problem this solves

Search "how do I start exporting" and you'll get a pile of things: a success-story guru, two hundred SEO blog posts, the free preview of a paid course, a YouTube video with a thumbnail promising fast money. You read them all, you feel like you understand, you open a customs-data website the next morning and still don't know what to type in the first box.

The problem isn't a shortage of information. It's that the information comes in fragments, it's edited from the winner's perspective, and it never tells you the next action.

How most tutorials handle it: *"You should do background research on your customers."* Then nothing. You still don't know which fields to check, which sites to check them on, what a red flag looks like, or when you've checked enough.

How this repo handles it: **take one task all the way down until it becomes an action.**

| What a tutorial says | What this repo says |
|---|---|
| "Do background research" | L1 screen checks exactly three things: does the site exist, how long has the company been registered, are the social accounts active. Fail any one and the lead is dead. |
| "Quality matters more than quantity" | 8 leads get sorted into T0/T1/T2/T3, and each tier comes with its own next action and its own time budget. |
| "Follow up with them" | Day 1, 3, 5, 7. Different angle each time. Day 7 ends with either a clear close or a clear drop. |
| "AI is changing trade" | Three stdlib-only Python scripts. `python scripts/lead_score.py examples/leads_example.csv` gives you a full tiering in 30 seconds. |

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

---

## 30-second quickstart

Three scripts. No third-party packages. Python 3.8+.

```bash
# 1. Tier your leads. CSV in, T0-T3 out, each tier with its next action.
python scripts/lead_score.py examples/leads_example.csv

# 2. Generate bilingual (EN + 中文) outreach copy for a given tier.
python scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. Build a 7-day, 3-touch follow-up plan with real dates.
python scripts/followup_plan.py --tier T0 --start 2026-10-08
```

Expected output from the first command:

```
Read 8 leads
  T0: 1    contact today, three channels in parallel
  T1: 2    first touch within 3 days
  T2: 4    low-frequency pool, prep material first
  T3: 1    no time investment
→ examples/leads_example_scored.csv
```

CSV header:

```
company_name,country,website,contact_name,contact_title,email,linkedin,source,last_contact_date,notes
```

The scripts only handle what a machine can decide: does an email exist, does a website exist, does this lead clear the T0 threshold. Whether a lead is *worth your time* stays in the docs and in your head.

---

## Repository layout

```
zero-to-trade/
├── README.md              # This file
├── README_EN.md           # Full English version
├── CONTRIBUTING.md        # How to contribute + doc and code conventions
├── LICENSE                # MIT
├── docs/                  # One file per stage
│   ├── 01-pick-a-market.md
│   ├── 02-find-leads.md
│   ├── 03-vet-the-buyer.md
│   ├── 04-make-contact.md
│   ├── 05-talk-specs.md
│   ├── 06-quote-negotiate.md
│   └── 07-delivery.md
├── scripts/               # Runnable Python, standard library only
│   ├── lead_score.py      # Tier leads T0-T3
│   ├── outreach_gen.py    # Bilingual outreach copy per tier
│   └── followup_plan.py   # 7-day, 3-touch follow-up plan
├── examples/
│   └── leads_example.csv  # Sample data, runnable as-is
├── prompts/
│   └── AI_PROMPTS.md      # 21+ copy-paste English prompts, grouped by stage
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
| **v0.1** | Shipped | 7 stage docs, 3 stdlib scripts, 21+ prompts, bilingual README |
| **v0.2** | Planned | **AI quoting engine**: input costs + market + competitor anchor price → FOB/CIF range + a three-step concession ladder |
| **v0.3** | Planned | **Buyer background-check agent**: input a company name → L1/L2/L3 research draft + red-flag checklist, with source links |
| **Long term** | — | Industry packs (tyres, building materials, machinery, hardware); outreach copy in Spanish/Arabic/French/Russian; public de-identified lead datasets; wiring v0.2's quoting engine to customs data for automatic competitor anchor pricing |

v0.3 comes before v0.2 on purpose: quoting needs to know the buyer's price band, and the most reliable source of a price band is the buyer's own order history. Vetting first, then quoting.

---

## Contributing

The gap in this repo is not a shortage of docs. It's the absence of **country-specific field detail.** I know how the first tyre order into the Middle East goes. I don't know how building-materials distribution works in Ecuador, or which documents Nigerian customs actually demands. Only people selling there can fill that in.

Three ways in, ordered by how little you need to know:

1. **Open an issue to fix something.** Typos, outdated facts, judgment calls that read as mush. One sentence beats silence. The template asks three things: which line confused you, which number has no source, which rule doesn't apply to your industry.
2. **Translate a stage doc.** Spanish, Arabic, Portuguese, Russian, French, Vietnamese — whatever you're fluent in. Keep the six-part structure, swap the language, align terms against the glossary.
3. **Add the stage detail for your industry or country.** This is the missing part. Write what you've actually done, not what you think should be done. Down to field names, document names, channel structure, payment habits, and the reasons buyers refuse to pay.

Code contributions welcome too, with one hard constraint: **Python 3.8+, standard library only.** Reasoning in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

[MIT](LICENSE) © 2026 zero-to-trade contributors

Use it, change it, sell with it — just keep the credit. Disclaimer: none of this guarantees you'll land a deal. What it does guarantee is that you won't stop because you didn't know the next step.

---

## Questions & contributions

**Open an issue: https://github.com/TODO-your-username/zero-to-trade/issues**

Spot an error? Say so. Have field detail from a market this repo knows nothing about? Send a PR. Want to argue about the method? Open an issue.

The author's personal details are deliberately not listed here. **Credibility should come from the content, not from who wrote it.** Tag the maintainer in an issue and GitHub will route the notification.
