# 06 · Quotation & Negotiation

> English version of [06-quote.md](06-quote.md). Translated from the Chinese original; figures, dates, commands and file names match the original exactly.

> What this step has to hand in: a quotation, a concession ladder, and a few ready-made lines. One purpose only — so that not one of your concessions is given away for nothing.
> Memorize one sentence first: a price cut is not a concession, it is a trade. A price cut given for free stuffs profit into someone else's pocket; a price cut traded for conditions turns profit into something worth more.

## 1. Why this step comes first

The three most common ways beginners die on quotations:

**First: send the price list, then wait to be cut.** You send the catalogue price; they take it to compare prices for three weeks, then come back with "others are 8% cheaper, can you match?". You cut 8%, the order is won, the margin is thin — and you never knew how much room was in that 8% you gave away.

**Second: quote the floor price, then retreat every time you are pushed.** They press you and you give in; you reach a number you actually will not do — but you have already handed over all your price room, and in the end you can only force yourself to do it or break the deal.

**Third: concede and get nothing back.** You cut 3% and get "OK, now let's look at the shipping terms". The price cut has become a one-sided surrender.

Negotiation is not thinking on your feet with your mouth — it is laying the steps before you open it. Before the pressure arrives, think clearly: which number to open at, which step to stop at, and what each tier trades for.

Price is not the only thing to negotiate either. Quantity, payment terms, container-loading efficiency, validity period, pattern customization and target price are all chips you can trade. Trading non-price conditions for a price cut is how you keep your profit alive.

## 2. Step by step

### First, tell the trade terms apart: behind each abbreviation is "who pays + who bears the risk"

A beginner's most expensive way to die: quoting CIF but only counting the ocean freight. CIF's obligations end on board the vessel at the destination port; everything after the destination port (THC terminal handling charges, unloading, demurrage / detention, customs clearance, duties, inland delivery) is by default for the buyer's account — but the buyer often assumes you cover it, and only finds out they have to pay themselves when the goods arrive at the port. That is where the wrangling starts. So the quotation must carry one fixed line stating "what is not included".

| Term | What the seller pays for / does, and up to where | When the risk passes to the buyer | The trap beginners step into most |
|---|---|---|---|
| **EXW** (Ex Works) | Only have the goods ready at the factory; container loading, export customs declaration, ocean freight and insurance are all the buyer's | When the buyer picks the goods up | The export declaration is not in your name, so **the tax refund may not be claimable**; when the buyer is a foreign company the exit documents still need your cooperation — under EXW you take less money and save no trouble |
| **FOB** (Free on Board, must name the port, e.g. `FOB Yantian`) | Export declaration + inland transport + loading-port charges + loading the goods on board | When the goods are loaded on board | The trucking, declaration, port charges and document fees before loading are all on you — they **must be built into the cost** when you quote FOB; also keep photographic evidence of before loading, since damage after loading is no longer your responsibility |
| **CFR / CIF** (Cost and Freight / plus Insurance, must name the destination port, e.g. `CIF Dammam`) | On top of FOB, the ocean freight to the destination port (CIF also buys insurance) | Still **when loaded on board at the loading port** (not when it arrives) | ① Biggest trap: **destination-port charges are not in CIF**; ② CIF insurance is usually only the minimum cover at 110% of the CIF value, and the buyer needs to negotiate and pay extra for all-risks cover |
| **DDP** (Delivered Duty Paid) | To the buyer's door, including destination-country customs clearance, duties and VAT | When the buyer signs for it | **Do not quote it without a reliable destination-country customs agent.** Duty rates, agent fees, VAT and possible anti-dumping duties are all on you; once goods are stuck at customs, demurrage burns money by the day. Do not touch DDP on a first order |

One sentence to remember: quote as far as you can manage. If you cannot manage destination-port clearance, quote CIF and do not touch DDP.

Add this fixed line to a CIF quotation (copy the English as written):

```
CIF <destination port> (port of discharge only). Destination charges, customs clearance,
duties and inland delivery are for Buyer's account.
```

How to choose on the first order: prefer FOB (the clearest boundary of responsibility; the destination port is not your problem) → only move to CIF if the customer insists on door-to-door → DDP only when you genuinely have a reliable customs agent in hand.

### The full cost build-up of one quotation (tick it off item by item — miss one and you leak profit)

| Cost item | What it is | FOB | CIF | Matching script parameter |
|---|---|:--:|:--:|---|
| Product cost (ex-factory / EXW price) | Raw materials + processing; may include factory profit | ✓ | ✓ | `--cost` |
| Packaging | Cartons / pallets / stretch film / shipping marks; custom packaging charged separately | ✓ | ✓ | Fold into `--cost` |
| Inland freight | Factory → loading port trucking / inland transport | ✓ | ✓ | `--local` |
| Declaration and document fees | Export declaration, inspection, certificate of origin, bill of lading | ✓ | ✓ | `--local` |
| Loading-port charges | Terminal handling, seals, manifest | ✓ | ✓ | `--local` |
| Ocean freight | Loading port → destination port | ✗ | ✓ | `--freight` |
| Insurance premium | At 110% of CIF value × rate | ✗ | ✓ | `--insurance` (default 0.15) |
| Bank charges | Telegraphic transfer fees; L/C advising / negotiation / discrepancy fees | ✓ | ✓ | Fold into `--local` |
| FX and conversion loss | Difference between the settlement rate and the quoted rate | ✓ | ✓ | Via the contingency reserve |
| Contingency | FX swings / lead-time delays / customer default | ✓ | ✓ | `--contingency` (default 0.03) |
| Export tax refund | The VAT refund amount — **part of the profit (a deduction)** | ✓ | ✓ | Not built into the script; handle by hand |
| Expected profit | **Cost-plus** (quotation = cost base × (1 + markup %)) | ✓ | ✓ | `--margin` (default 15) |

A few traps that are easy to step into — note them down:
1. `--cost` is the unit cost (how much per unit; the currency follows `--currency`). Domestic costs are either folded into `--cost` first or added separately with `--local` — do not count them in both places or you will double-count.
2. The tax refund and bank charges are not in the script: the refund is a deduction and the bank fees are an addition; both have to be adjusted by hand inside `--cost`.
3. `--contingency` is the risk reserve (default 3%); the script has already multiplied it in — do not multiply it again by hand.
4. `--margin` is a cost-plus markup, not a gross margin. The script calculates `quotation = cost base × (1 + markup %)`; if you want to work backwards from a gross margin (`quotation = cost ÷ (1 − gross margin)`), that is a different thing — 15% gross margin is roughly 17.6% markup. Fill in the wrong one and you earn less money.

### Run it through the script once (commands ready to copy)

In the project root. The script only uses the Python standard library; with Python 3.10+ installed it runs, with zero third-party dependencies:

```bash
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15 --local 1.2 --moq 300 --lead-time "25天" --validity 15
```

> The numbers above are all **[Example]** inputs (unit cost 28, ocean freight 6, cost-plus markup 15%, local charges 1.2, USD/piece) — replace them with your own costs.

Real output (internal view, includes costs and floor prices):

```
==================================================================
  报价引擎 (alpha) · 内部视图（含成本与底价，勿外发）
  币种: USD · 计价单位: 件 · 生成时间: 2026-10-08T23:21:20
==================================================================
  成本基数(含不可预见+本地费)    │      30.04 USD/件
  FOB 报价: 离岸价，不含运费保险 │      34.55 USD/件
  FOB 底价: 内部，再低不接       │      32.47 USD/件
  CIF 报价: 到岸价，含运费+保险  │      40.61 USD/件
  CIF 底价: 内部，再低不接       │      38.53 USD/件
  其中保险费 = CIF*110%*费率     │       0.07 USD/件
------------------------------------------------------------------
  三档让步阶梯（每降一档都必须换回条件；增量递减，底线不外露）
   第1步  本档 -2.5%  累计 -2.5%   → FOB 33.68 │ CIF 39.75 USD/件
          换回: 首单 ≥ 1 个柜（20GP/40HQ）且接受 30% 定金
   第2步  本档 -1.5%  累计 -4.0%   → FOB 33.16 │ CIF 39.22 USD/件
          换回: 由试订单升级为年度框架 / 量翻倍以上
   第3步  本档 -1.0%  累计 -5.0%   → FOB 32.82 │ CIF 38.88 USD/件
          换回: 签 1–3 年排他或独家代理（区域保护换低价）
------------------------------------------------------------------
  报价单必带字段（发出前逐项确认，缺一项都可能被客户拿去压价）
    [ ] 报价有效期 : 15 天（海运费/汇率波动大时缩到 7–15 天）
    [ ] 付款方式   : T/T 30% 定金 + 70% 见提单副本；或即期 L/C
    [ ] 最小起订量 : 300 件
    [ ] 交货期     : 25天
    [ ] 贸易术语   : 写明 Incoterms 2020 + 港口，如 FOB <装运港> / CIF <目的港>
------------------------------------------------------------------
  术语速查（完整三语术语表见 GLOSSARY.md）
   · FOB 离岸价：卖方的钱只花到货物装上船，不含海运费与保险。
   · CIF 到岸价：FOB + 海运费 + 保险费，卖方付到目的港。
   · 投保加成 110%：保险按 CIF 货值的 110% 投保，所以 CIF = (FOB+运费) ÷ (1 − 1.10×费率)，不是 FOB+运费 再乘个费率。
   · 让步阶梯：降一档价必换回一样东西（量/账期/排他/长约），不换条件的让步=送钱。
   · 计价口径：报价 = 成本基数 *(1+加成%)，这是成本加成(markup)；若按毛利率倒推，报价 = 成本 /(1-毛利率)，15% 毛利率约等于 17.6% 加成。
==================================================================
```

Parameter quick reference (real parameter names and defaults; `python scripts/quote_engine.py --help` is authoritative):

| Parameter | Default | Meaning |
|---|---|---|
| `--cost` | **Required** | Unit cost (EXW / factory price, per unit) |
| `--freight` | 0 | Ocean freight to the destination port (per unit); leave 0 when quoting FOB |
| `--margin` | 15 | **Cost-plus markup %** (not gross margin) |
| `--insurance` | 0.15 | Insurance rate, in **percent** (0.15 = 0.15%) |
| `--local` | 0 | Local charges (declaration / trucking / port charges, per unit) |
| `--contingency` | 0.03 | Contingency ratio |
| `--anchor` | none | Competitor anchor price (in the quotation currency); giving one outputs a positioning suggestion |
| `--fx` | 1.0 | Exchange rate: 1 cost currency = fx quotation currency (fill in 0.14 when costs are in CNY and the quotation is in USD), **converted once at the start only** |
| `--currency` | USD | Quotation currency symbol |
| `--unit` | 件 | Pricing unit |
| `--moq` | none | Minimum order quantity (a must-have field on the quotation) |
| `--lead-time` | none | Lead time, e.g. `"25天"` |
| `--validity` | 30 | Quotation validity in days |
| `--audience` | internal | `internal` includes costs and floor prices; `client` is the customer view, **never shows the floor price** |
| `--out` | none | Also write to a file (UTF-8), e.g. `--out quote.txt` |
| `--format` | table | `table` or `json` |
| `--insurance-rate` | none | Advanced entry, takes a **ratio** (0.0015 = 0.15%); can override `--insurance` |

Three unit traps:
- `--insurance` takes a percent. `--insurance 0.3` = 0.3%; to write "three per mille" use `--insurance-rate 0.003`. If you enter the wrong order of magnitude (>5%) the script refuses to run with an error — it will not silently hand you a wrong price.
- When quoting FOB, do not fill in `--freight`, or you will end up quoting a CIF figure as FOB.
- `--margin` is a markup, not a gross margin (see item 4 above).

Common variants:

```bash
# 成本是人民币、报价用美元（【示例】汇率 0.14）——汇率只换算一次，不存在重复乘加成的问题
python scripts/quote_engine.py --cost 200 --currency CNY --fx 0.14 --freight 6

# 带竞品锚价，看自己贵了还是便宜了（【示例】锚价 36）
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15 --anchor 36

# 客户视图：不含成本与底价，可放心用于对外（但仍需自己排版成正式报价单）
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15 --audience client

# 输出 JSON，方便贴进表格或交给 AI 复核
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15 --format json

# 结果直接存文件
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15 --out quote_internal.txt

# 到岸全成本：先用 quote_engine 报 FOB/CIF，再用 landed_cost 算 CIF→DDP（关税 + 目的港杂费）+ 利润空间
python scripts/landed_cost.py --fob 33.17 --freight 6 --duty 10 --port-charges 2

# 报价前先锚价：海关数据竞品价区间 + 自家成本 → 进取/中位/保守三档（先用 anchor_price 定价，再用 quote_engine 出正式报价单）
python scripts/anchor_price.py --comp-low 38 --comp-high 46 --comp-median 42 --cost 28 --freight 6 --duty 10
```

> **Note**: `--audience client` only removes the costs and floor prices — **the concession ladder and the "conditions in return" are still in the output**. So the script output is always only an **internal draft** — never screenshot it or forward it to a customer as it stands; fill in your own formal quotation from it (see Template A in section 7).

**Step 1: Work out the floor first (before quoting, not after being pushed)**

Before quoting you must have three lines, written on paper:

- **Cost line**: ex-factory cost + inland freight + packaging + export-port charges + inspection / declaration + finance costs = the real cost (tick them off one by one against the list in the previous section; do not rely on memory)
- **Target line**: the price you want (the starting point for negotiation, usually above the target)
- **Floor line**: below this number, do not take the order (and this number must not be told to the customer)

The `FOB quotation` and `FOB floor` in the script output map exactly onto the **target line** and **floor line** here: `FOB quotation` is your opening price, `FOB floor` is the stop-loss the script gives you (quotation × (1−6%), and never below the cost base). The three lines do not need to be guessed by hand — one run of the script gives them to you.

**How the floor line is calculated** (structure, not numbers; the real numbers must be calculated from your own costs):
```
底价 = 真实成本 + 最低可接受利润 + 风险预留（汇率波动/交期延误/客户违约）
       - 出口退税额
```
Markets with big FX swings must have the risk reserve added in, and the tax refund must be deducted from the cost — beginners miss both of these almost every time (one understates an expense, the other understates an income).

The numbers on the quotation have to be cost + profit + risk put together — not a cost multiplied by a coefficient pulled out of thin air and sent off.

> **Iron rule: floor price, costs, gross margin and concession room must never appear in any document sent to a customer.** A quotation carries only one price + one validity period. Keep the internal costing in a separate file (with `INTERNAL` in the file name) and do not put it in the same document as the quotation — most "slipped and sent the floor line out" accidents happen because the two tables sit on the same page.

**Step 2: Must-have fields on a quotation (Quotation and Proforma Invoice are not the same thing)**

First tell two things apart; do not mix them up:

- **Quotation**: an invitation to treat. Used in the negotiation stage; it may state a "validity period" and "subject to final confirmation", and it **does not form a formal contract**. The customer uses it to compare prices, apply for an import licence, or get a bank loan.
- **Proforma Invoice (PI)**: the **quasi-contract** sent after the negotiation ends. The customer pays against it, opens a letter of credit, and clears customs with it. Once the specs, quantities, terms or amounts on a PI are wrong, the error rides all the way onto the bill of lading and the customs documents — and changing documents costs money.

The difference in must-have fields between the two is in "payment and bank information" — a Quotation may leave payment terms blank (a negotiation chip), while a PI must state them in full.

**Must-have field checklist (tick it off)**

| # | Field | Quotation | PI | Notes |
|---|---|:--:|:--:|---|
| 1 | Document type and number | ✓ | ✓ | State `QUOTATION` or `PROFORMA INVOICE` in the heading; numbers like `QT-2026-0145` / `PI-2026-0145` ([Example] numbers) so both sides can track them |
| 2 | Date + validity | ✓ | ✓ | See the "Validity and FX lock-in" section below |
| 3 | Seller heading | ✓ | ✓ | Full company name, address, contact person, email / phone |
| 4 | Buyer heading | ✓ | ✓ | **Full company name + country**, not one letter wrong (a wrong PI affects customs clearance) |
| 5 | Specification table | ✓ | ✓ | Model / pattern / ply / load index / quantity / unit price / amount, one model per line |
| 6 | **Pricing basis** of the unit price | ✓ | ✓ | `USD/pc` or `USD/set`, which `EXW/FOB/CIF` basis — a unit price without a basis is meaningless |
| 7 | Currency | ✓ | ✓ | State `Currency: USD` clearly; non-USD must come with an FX clause |
| 8 | Total price + container type + piece count | ✓ | ✓ | `Total FOB Yantian: USD xxx for 1x40HQ (480 pcs)` ([Example] quantity and container type) |
| 9 | Trade terms + named ports | ✓ | ✓ | `FOB Yantian` / `CIF Dammam`, stating the Incoterms version (**the specific applicable version is as agreed in the contract**); for CIF add the line "destination-port charges are for the buyer's account" |
| 10 | Packaging | ✓ | ✓ | How many pieces per pack, whether palletized, shipping-mark requirements; affects container loading, which directly affects the unit price |
| 11 | Lead time / production cycle | ✓ | ✓ | State the `lead time` start point (from the date the deposit arrives / from the date the contract is signed) |
| 12 | Port of loading + port of discharge | ✓ | ✓ | Consistent with item 9; a misspelled port is a free chip handed to the other side |
| 13 | Gross weight / net weight / volume | Recommended | ✓ | Affects the freight calculation and the customer's customs clearance |
| 14 | Country of origin | Recommended | ✓ | `Origin: China`; the customer needs it for the certificate of origin |
| 15 | Payment terms | May be left blank | ✓ | Blank in a Quotation is a negotiation chip; must be stated in full in a PI (ratio, method, timing) |
| 16 | Bank information | ✗ | ✓ | Beneficiary / Bank name / SWIFT / Account No. — **PI only; a Quotation does not carry them** |
| 17 | Signature and stamp | Recommended | ✓ | A PI usually needs the seller's signature and stamp |

Tick through this table once it is written, then send.

**Step 3: Prepare the concession ladder (the core move)**

The ladder must be written on paper in advance. The table below maps **one-to-one** onto the output of `scripts/quote_engine.py` (the script gives three tiers of price concessions; L4 is the tier of "no more price cuts"):

| Tier | Cumulative cut | Matching script output | Condition that must be traded for it ([Example] — change to your actual situation) |
|---|---|---|---|
| L0 starting point | 0 | `FOB quotation` | — |
| L1 | −2.5% (this tier −2.5%) | Step 1 `new_fob` | First order ≥ 1 container (20GP/40HQ) and accepts 30% deposit |
| L2 | −4.0% (this tier −1.5%) | Step 2 `new_fob` | Upgrade from trial order to annual framework / volume more than doubles |
| L3 | −5.0% (this tier −1.0%) | Step 3 `new_fob` | Sign 1–3 year exclusivity or sole agency (regional protection in exchange for a lower price) |
| L4 | **No more price cuts** | Already near the floor line | Only non-price chips: longer validity, priority scheduling, free inspection support, container-loading list and loading photos |
| Floor | −6% (script's `FOB floor`) | Do not take the order below this | Do not concede |

The script's three tiers are **incrementally shrinking** (2.5 → 1.5 → 1.0, 5% cumulative), one percentage point short of the floor's 6% — deliberately held back: the customer can never guess you still have one square left.

**Note: do not add a "cut 8%" tier of your own.** The script's floor is the quotation × (1−6%); any further down breaks the stop-loss. If a ladder you wrote by hand has one more tier than the script's, your opening price was set too low — **raise the opening price; do not lower the floor.**

Key rules:
- **Only ever cut one tier at a time**; do not cut twice in a row
- **Every tier must have a condition in exchange**, and the condition is spoken out loud (said, not just thought)
- **After L3, no more price concessions** — respond with non-price conditions (quantity, payment, validity, lead-time flexibility)
- **Concession size shrinks**: smaller the further you go, so they know the floor is approaching — the script's three tiers shrink 2.5 → 1.5 → 1.0
- **Run the script before fixing the ladder**: copy the script's three output numbers into the L1/L2/L3 of the table; do not hand-write percentages

**More: how to write validity, FX lock-in and MOQ tier pricing**

These three lines are the easiest to overlook on a quotation — and the easiest to argue about afterwards.

**① Validity** — not politeness, but price protection:

```
Validity: This quotation is valid for 15 days from the date of issue (until YYYY-MM-DD).
Prices are subject to re-confirmation thereafter due to raw material / freight volatility.
```

- When raw materials (rubber, steel cord) and ocean freight are volatile, shorten it to 7–10 days; when the market is steady, 15–30 days is fine.
- **Write the deadline date in full**; do not write only "15 days" — if only the number of days is written, the two sides may understand the start date differently (date of issue / date of receipt).
- Once the validity has expired and they come back asking for the price: **quote again; do not reuse the old price**, even if only a week has passed.

**② FX lock-in** — must be written for non-USD quotations; recommended for long USD orders too:

```
FX clause: Prices are based on USD/CNY = 7.10. Should the rate at the time of
payment move by more than ±2%, both parties agree to re-negotiate the USD price accordingly.
```

([Example] exchange rate and fluctuation threshold — fill in your actual settlement cost and risk tolerance.)

- The quotation **must state the exchange rate you used**; otherwise the customer assumes you bear all the FX risk.
- The threshold is usually ±1%–±3% ([Example] range): too wide is the same as no lock; too narrow and the customer will not accept it.
- The longer the period from quotation to payment (e.g. 60–90 day payment terms), the more it must be written; for cash-on-delivery it can be relaxed.

**③ MOQ and tier pricing** — write "buy more, pay less" into the quotation and save a round of haggling:

```
Price tiers (based on single shipment quantity):
  1 x 20GP  (≥ 200 pcs)  : USD ____ / pc
  1 x 40HQ  (≥ 480 pcs)  : USD ____ / pc
  2 x 40HQ  (≥ 960 pcs)  : USD ____ / pc
MOQ: 200 pcs per size / 1 x 20GP per order. Mixed sizes allowed in one container.
```

(Quantities are [Example] — replace with your actual container loading.)

Writing points:
- Tiers are counted **by "single shipment quantity"**, not by "annual cumulative quantity" — you cannot verify cumulative quantity, and the other side can chase you for it afterwards.
- Every tier states its **unit and matching container type** clearly, so there is no argument about "is 200 pieces one container or one pallet".
- State clearly **whether mixed loading is allowed** (mixed sizes in one container): allowing mixed loading significantly lowers the customer's trial-order threshold, and it is one of the cheapest chips in your hand.
- Tier pricing must not **conflict** with your Step 3 concession ladder: tier pricing is open quantity discounting; the concession ladder is room that only moves during negotiation. If the customer reaches 2 containers, give them that tier's price — do not also give the L2 discount at the same time.

**Step 4: List the non-price chips (the negotiation ammunition store)**

These are the things you can trade that cost you less — list them in advance:
- Payment terms: full prepayment, 30% deposit + 70% against B/L copy, 20% deposit
- Quantity: 2 containers to start can get a better unit price; 4 containers at once can be talked about again
- Lead time: accept the lead time you would prefer, in exchange for a little price
- Validity: stretch the validity period, in exchange for a little price (works on customers sensitive to raw-material swings)
- Pattern / packaging: custom pattern labels, custom packaging, tiered by MOQ
- Free items: container-loading list, loading photos, third-party inspection support

Remember: throw the non-price chips first; only touch price when there is nothing left.

**Step 5: Handling "others are cheaper"**

This is the most common price-pressure line. Handle it in this order:
1. Do not deny it, do not defend yourself (saying "that's not true" is losing)
2. **Ask about the difference**: "May I ask what scope the other offer covers — same size, same pattern, same packaging, same payment terms?" — much of the time the difference is in the configuration or the terms
3. **Trade a condition**: "If we can do 30% advance and 2x40HQ per shipment, let me see what I can do on price."
4. **Hold the floor**: "Our floor at this configuration is what I quoted; to go lower I would need to change the scope." — make it clear it is a configuration problem, not a sincerity problem

**Step 6: Handling "give me your lowest price first"**
- What it looks like: they want the lowest price in the first round.
- How to handle it: do not give it directly. Reply "I can sharpen the number if you confirm quantity and payment terms. Our price depends on both." — get the conditions back first.
- If you really have to push back: "Our best price for this spec starts at X, but that's tied to 1x40HQ with 30% advance. Below that I need to check with production."

**Step 7: Closing and follow-up discipline**

- After quoting, do not cut the price on your own initiative; wait for their reaction
- If they go silent for more than 5–7 days, you may follow up once — but **the follow-up carries no price cut** (carry one piece of information)
- Before the quotation goes out, have AI or a colleague pick through it for errors: figures, units, ports, Incoterms, validity, spelling
- Keep a written record of every concession: write in the email "this price is based on conditions A+B+C"

### Four negotiation moves: the psychology beyond price

Quoting is technique; negotiation is psychology. Get the technical part (cost / freight / profit) worked out, and win the psychological part in conversation:
- **Anchoring**: quote the high-spec version first, then the main model — the main model looks like great value. "The premium model is $X, but most customers pick the standard model $Y — 80% of the performance, far better value. Which suits your market?"
- **Loss aversion**: do not say "how good it is to buy"; say "how much you lose by not buying". "Raw materials rose this month; the two buyers who hesitated last week paid 4% more. Locking the price now is saving money."
- **Commitment and consistency**: get them to confirm small things first. "Specs and lead time are confirmed, right? Then I'll prepare the PI on that basis." — once something is confirmed, it costs more to go back on it.
- **Scarcity**: only ever use **real** information. "Only 3 container slots are left on this sailing; I'll hold them for you until Friday." — **inventing sailing schedules / price rises / stock grabs is a red line**.

Three red lines (if you hit one, stop and hand it to a human):
- **Quotation below the floor price** → stop; do not cut the price yourself.
- **Customer asks for payment terms / credit / open account (OA)** → a beginner must not approve this alone; this is a company-level decision.
- **Never make a promise you cannot keep**: lead time, warranty, compensation — if you cannot do it, do not say it. Every sentence you say becomes a cost later.

## 3. How to tell this step is done

Several hard bars to check against:

- Cost line / target line / floor line have been separately written down, and the floor price, costs and gross margin **have not appeared in any customer-visible document** (internal costing in a separate file).
- Costs have been ticked off item by item against the full list (product / packaging / inland freight / declaration and documents / port charges / ocean freight / insurance / bank charges / FX / contingency / tax refund / profit), with no item missed.
- The floor price already includes the risk reserve for FX swings and lead-time delays, and **the export tax refund has been deducted**.
- The trade term is one clear one of FOB / CIF / EXW / DDP, **with the named port written out**; for CIF the buyer's responsibility for destination-port charges has been stated in writing; before quoting DDP, a reliable destination-country customs agent has been confirmed.
- `scripts/quote_engine.py` has been run to produce the FOB/CIF range as the starting point, and the command genuinely executes.
- The quotation's must-have fields are complete: document type and number / date + validity / full names of buyer and seller + countries / specification table / pricing basis + currency / total price + container type + piece count / Incoterms + ports / packaging / lead time / country of origin; a PI additionally carries payment terms and bank information.
- The validity states a **deadline date** in full; non-USD quotations or long payment terms carry an FX lock-in clause (with base rate and fluctuation threshold).
- MOQ and quantity tier pricing are written out: each tier's quantity, container type, and whether mixed loading is allowed.
- The concession ladder matches the script output (L1 −2.5% / L2 −4.0% / L3 −5.0%, floor −6%), shrinking in size, each tier carrying a condition in exchange, and no more price concessions after L3 — only non-price chips.
- Non-price chips have been listed and are used first; the two scripts for "others are cheaper" and "give me the lowest price first" have been prepared in advance.

## 4. AI prompts

**Prompt 1: Quotation generation + internal costing check**

```
You are an export pricing analyst for a Chinese tire manufacturer. Build a professional
quotation document and stress-test it BEFORE it goes out.

INPUT:
- Buyer: {company, country, contact}
- Confirmed requirements (from my requirement confirmation email):
  specs {size/pattern/ply/load index/qty}, container plan, destination port, trade term
- My costs: {product cost per size, packaging, inland transport, port/inspection/finance
  charges, FX rate assumption}
- Target margin and minimum acceptable margin: {fill}

OUTPUT:
1. QUOTATION SHEET — formatted as a real quote with: quote number, date, buyer, line-item spec
   table, FOB total per container, Incoterms, payment terms (leave BLANK if not yet agreed),
   packing details, production lead time, validity period (recommend one and justify).
   Do NOT write any marketing adjectives.

2. INTERNAL COST & MARGIN BLOCK (clearly marked "INTERNAL — STRIP BEFORE SENDING"):
   per-size cost breakdown, total cost, margin %, and the MINIMUM price I can accept per
   configuration. This block must never appear in the customer version.

3. RISK BLOCK (INTERNAL):
   - FX exposure if the currency is not USD
   - what happens to margin if freight/raw material moves ±5%
   - the single most likely way this quote loses money

4. ERROR CHECK: units, currency, Incoterms named location, port spelling, container quantity
   vs piece count consistency, arithmetic. List every check performed and its result.

RULES:
- Never invent costs I did not give you — if a cost component is missing, write
  "MISSING — cannot compute margin" and list it.
- Every price must be traceable to a formula from my inputs.
- Do not use words like "best price", "competitive", "high quality" in the quotation text.
```

Note in Chinese (translated): parts 2 and 3 are for internal eyes only and must be deleted before sending. The self-check list in part 4 blocks the most embarrassing errors — quantity and container count not matching, a port misspelled. The opening line "MISSING — cannot compute margin" is the key: it forces the AI not to quietly invent a cost to fool you.

**Prompt 2: Concession ladder design**

```
You are a negotiation strategist. I need a pre-planned concession ladder for a deal.

DEAL FACTS:
- Target price: {price}   My floor: {floor}
- Buyer behavior so far: {e.g. pushed for 8% discount, asked for 60-day payment}
- My constraints: {production capacity, cash flow needs, competitor in the market}
- Non-price levers I can use: {payment advance %, order quantity tiers, lead-time flexibility,
  validity period, custom packaging, free inspection support, after-sales/warranty scope}

DESIGN:
A 5-level ladder table: Level | My price | % reduction | what I demand in return |
what I say (exact English sentence) | what I must NOT say

Then:
1. Define the ONE non-price lever that is cheapest for me to give and most valuable to them.
   Use it before touching price.
2. Flag which level I should stop at if this buyer pushes hard, and the exact sentence to close
   the negotiation politely without conceding further.
3. Write the 3 most likely buyer rebuttals to my concessions and my response to each.
4. Warn me about 2 traps in this specific ladder — e.g. a level that gives away margin without
   buying anything, or a condition the buyer can claim later without honoring.

RULES: the floor is absolute — no level below it. Conditions in "in return" must be things this
buyer can actually agree to today. Never suggest giving away the same lever twice at two levels.
```

Note in Chinese (translated): the heart of this table is part 4, "what I must NOT say" — the easiest way to slip up in a negotiation is to say the wrong thing yourself. For example, saying "this price is already the limit" to keep the customer, when there is still one tier left to go, leaves you with nothing to negotiate afterwards.

**Prompt 3: Response scripts for price pressure**

```
You are a negotiation coach. Write my response to the buyer's message below.

BUYER'S MESSAGE: {paste}
DEAL STATE: {my quote, my floor, my target, my unspent levers, my last concession offered}

DELIVER:
1. DIAGNOSE (3 bullets): what is the buyer actually doing — testing my floor / comparing with a
   real competitor / budget excuse / time pressure tactic / genuinely price-limited? Give the
   tell-tale signals in their wording.
2. MY RESPONSE (English, under 150 words) — must:
   - not argue, not apologize, not say "our price is already very low"
   - ask at least one scoping question about what the competing offer covers
   - offer exactly ONE conditional trade (something I give / something they give)
   - keep my floor unmentioned and unrevealed
3. WHAT I SHOULD NOT SAY (3 sentences) — phrases that would either reveal my floor or
   give away my next move
4. THE FOLLOW-UP I send 2 days later if they don't reply — new information, no discount

Then produce 3 alternative tones for the same response: (a) warm & relationship-first for GCC,
(b) concise & formal for Europe, (c) patient & educational for first-time buyers.
Do not change any numbers between tones — only the framing.
```

Note in Chinese (translated): the most important part of part 1 is recognizing which game the other side is playing — a "time pressure tactic" and a "budget excuse" are handled two completely different ways, and mixing up the responses is a guaranteed loss. Sweeping through part 3, "what I should not say", before every negotiation saves a lot of on-the-spot slips.

## 5. Checklist

- [] Cost line, target line and floor line have been separately calculated and written down; floor price / costs / gross margin have not appeared in any customer-visible document
- [] Costs have been ticked off item by item: product, packaging, inland freight, declaration and documents, port charges, ocean freight, insurance, bank charges, FX, contingency, tax refund, profit
- [] The floor price includes the risk reserve for FX swings and lead-time delays, and the export tax refund amount has been deducted
- [] Trade terms are clear with the named port written out; for CIF the buyer's responsibility for destination-port charges has been stated
- [] `scripts/quote_engine.py` has been run (the command genuinely executed) and the FOB/CIF range and three-tier ladder have been copied into my ladder table
- [] The quotation's must-have fields are complete: number, date + validity, full names of buyer and seller + countries, specification table, pricing basis + currency, total price + container type + piece count, Incoterms + ports, packaging, lead time, country of origin
- [] The quotation has passed an item-by-item self-check: units, currency, port spelling, Incoterms location, container count vs piece count consistency, arithmetic
- [] Validity is written as a **deadline date** (not just a number of days); an FX lock-in clause has been added where needed
- [] MOQ and quantity tier pricing state each tier's quantity, container type and whether mixed loading is allowed
- [] The concession ladder matches the script output (L0 starting point + L1 −2.5% / L2 −4.0% / L3 −5.0% + floor −6%), with no more price cuts after L3
- [] Internal cost and risk blocks have been removed (before the quotation goes to the customer; a PI additionally needs payment terms and bank information)
- [] The non-price chip list has been made, and non-price chips are used first
- [] The two scripts for "others are cheaper" and "give me the lowest price first" have been prepared in advance
- [] The exchange condition for every concession has been written in the email (not just agreed verbally)
- [] The quotation validity has been set and the deadline date written in full (the script's `--validity` defaults to 30 days; shorten to 7–15 days when ocean freight / FX is volatile)

## 6. The traps beginners step into most

**Trap 1: Writing the floor price straight onto the quotation**
- What it looks like: a line on the quotation saying "lowest price we can do", and the customer haggles straight from it.
- Why: wanting the customer to feel "I have already shown sincerity".
- What to do instead: a quotation carries only one price + one validity period. The floor price is hidden away in your own drawer, written on a separate sheet — best not kept in the same document as the quotation: nine out of ten "slipped and sent it out" accidents happen because the two tables sit next to each other.

**Trap 2: Cutting the moment they press, trading for nothing**
- What it looks like: they say "cut 3% and I'll order", you cut, and they say "in a couple of days".
- Why: treating "cutting the price" as "goodwill" rather than a "bargaining chip".
- What to do instead: state the conditions before cutting. "3% is fine, provided it is 30% prepayment, orders start at 2 containers, and validity is 10 days." Pick two of three; do not give it away for free.

**Trap 3: Cutting all the way in one go**
- What it looks like: they say "at least 5% off", and you cut 6% straight away, throwing in a little extra.
- Why: afraid of the hassle, wanting it over quickly.
- What to do instead: cut only one tier (the first tier is −2.5%) and watch the reaction. Always leave them room to feel "there is still a bit more to squeeze". A negotiation only ends when the other side feels they "might squeeze a bit more".

**Trap 4: Replying "our price is already very low"**
- What it looks like: repeating under pressure that you have already cut the price a lot.
- Why: treating "arguing your case" as defence.
- What to do instead: turn it into a question. What scope does their quotation cover? Same configuration? Same payment terms? — move the topic from "am I expensive" to "what are we comparing", and you take back the standard of comparison.

**Trap 5: Giving away the price and the credit line together**
- What it looks like: to win the first order, they ask for 90-day open-account terms and you agree.
- Why: the first order feels high-pressure; you want it closed quickly.
- What to do instead: new customers do not get open account. First order is 100% prepayment or 30% deposit + 70% against B/L copy. Payment terms are a discount bought with your cash flow — do not give them away for free.

**Trap 6: Sending a quotation you have not read yourself**
- What it looks like: sending out a quotation generated by AI as it stands, and the customer replies "your CIF Dammam says CIF Jebel Ali".
- Why: in a hurry to get it off your desk.
- What to do instead: before sending, have AI run the item-by-item self-check (the ERROR CHECK part of the prompt), then check the figures and ports yourself once more. Every error on a quotation is a free chip for the other side.

**Trap 7: Conceding without writing the condition down**
- What it looks like: the email only says "based on our discussion, we can do USD x", with no premise stated.
- Why: feeling that stating conditions looks petty.
- What to do instead: write the conditions for every concession down in writing — "this price is based on 30% prepayment + 2x40HQ order volume + validity within 10 days". Otherwise, a week later they will say "that was not the condition we talked about".

**Trap 8: Quoting CIF without working out (or stating) the destination-port charges**
- What it looks like: the customer asks "is that everything once it arrives at the port", you say "yes"; after the goods arrive the customer is charged THC, unloading fees and demurrage and comes back to you for reimbursement.
- Why: understanding CIF as "delivered to the door". In reality CIF only covers ocean freight and insurance **to the vessel at the destination port**, and the risk already passed when the goods were loaded at the loading port.
- What to do instead: add the fixed line to the quotation — `CIF <port> (port of discharge only). Destination charges, customs clearance, duties and inland delivery are for Buyer's account.`; if the customer genuinely wants door-to-door, quote DDP — but first confirm you have a reliable destination-country customs agent, or do not take it.

**Trap 9: Missing cost items — the tax refund and the bank charges**
- What it looks like: when costing, only the product price and freight are counted; the quotation looks profitable, and after finishing the order you find you worked for nothing.
- Why: the tax refund (a deduction — income) and the bank charges (L/C advising, negotiation and discrepancy fees) do not sit inside "product cost", so they are the easiest to miss.
- What to do instead: tick through the cost build-up table in section 2 one item at a time; do not skip a single one. **Deduct** the tax refund from the cost, and **add** the bank fees in.

**Trap 10: Screenshotting the script output straight to the customer**
- What it looks like: after running `quote_engine.py`, pasting a screenshot of the result into the email, thinking it looks "professional".
- Why: not realizing the default view (`--audience internal`) contains the **cost base**, the **FOB/CIF floor prices**, and the three-tier concession ladder with the "conditions in return".
- What to do instead: the script output is an **internal draft** — only copy the one number you want the customer to see (the FOB or CIF quotation) and fill it into Template A in section 7. Adding `--audience client` removes the costs and floor prices, but **the concession ladder is still there**, so it still cannot be forwarded as it stands.

**Trap 11: Treating the markup as the gross margin (`--margin` filled in with the wrong basis)**
- What it looks like: wanting a 15% gross margin, filling in `--margin 15`, and ending up with a lower gross margin than expected.
- Why: `--margin` is a **cost-plus markup**, `quotation = cost base × (1 + markup %)`; gross margin has to be worked backwards, and the two are different (15% gross margin ≈ 17.6% markup).
- What to do instead: to quote by gross margin, first convert it to a markup and then fill it in; the "pricing basis" line in the script output is there to remind you of this.

**Trap 12: Validity written as days only, FX not locked in**
- What it looks like: the quotation says `Validity: 15 days`, and three months later the customer places an order against the old quotation.
- Why: only the number of days is written, and the two sides understand the start date differently (date of issue / date of receipt); when prices rise and you want to adjust, the customer says "you said 15 days".
- What to do instead: write the deadline date in full — `valid until YYYY-MM-DD`; for non-USD quotations or payment terms over 30 days, add an FX lock-in clause (base rate + fluctuation threshold).

## 7. Copy-paste templates (fill in, no AI needed)

### Template A: Quotation skeleton for the customer

**No cost, gross margin or floor price may appear in this document.**

```
QUOTATION
Quote No.: QT-2026-____          Date: YYYY-MM-DD
Valid until: YYYY-MM-DD          Currency: USD

Seller: ______________________
Buyer:  ______________________   Country: ____________

| Size | Pattern | Ply | Load Index | Qty (pcs) | Unit Price (USD/pc) | Amount (USD) |
|------|---------|-----|-----------|-----------|--------------------|--------------|
|      |         |     |           |           |                    |              |
|      |         |     |           |           |                    |              |
|      |         |     |           |           |                    |              |

Total: USD __________  (FOB / CIF __________ port: __________)
Incoterms: ____________ (version as per contract)
Packing: ______________   Origin: China
Lead time: ____ days after receipt of deposit
Port of loading: ______   Port of discharge: ______
Gross weight / Volume: ______ / ______

Price tiers (per single shipment):
  1 x 20GP (≥ ____ pcs): USD ____ / pc
  1 x 40HQ (≥ ____ pcs): USD ____ / pc
  2 x 40HQ (≥ ____ pcs): USD ____ / pc
MOQ: ____ pcs per size / ____ per order. Mixed sizes in one container: Yes / No

Validity: This quotation is valid until YYYY-MM-DD. Prices subject to
re-confirmation thereafter due to raw material / freight volatility.

FX clause (if not USD or long payment term):
Prices are based on USD/CNY = ____. Should the rate at time of payment move
by more than ±____%, both parties agree to re-negotiate the USD price.

Note for CIF only: CIF <port> (port of discharge only). Destination charges,
customs clearance, duties and inland delivery are for Buyer's account.
```

(All figures are [Example] placeholders — replace them with your own.)

### Template B: Internal costing table (**build a separate file, with INTERNAL in the file name; never send it out**)

```
INTERNAL — STRIP BEFORE SENDING
Quote No.: QT-2026-____   对应客户版本编号

单位成本 --cost          : ____ /件    【示例】28
本地费用 --local         : ____ /件    【示例】1.2（报关/拖车/港杂）
海运费   --freight       : ____ /件    【示例】6（报 FOB 时填 0）
成本加成 --margin        : ____ %      【示例】15（是加成，不是毛利率）
不可预见 --contingency   : ____        【示例】0.03
保险费率 --insurance     : ____ %      【示例】0.15
汇率     --fx            : ____        【示例】成本 CNY 报 USD 时填 0.14
起订量   --moq           : ____        【示例】300
交货期   --lead-time     : ____        【示例】"25天"
有效期   --validity      : ____ 天     【示例】15

跑（内部视图，含底价）：
python scripts/quote_engine.py --cost __ --freight __ --margin __ --local __ \
    --moq __ --lead-time "__" --validity __

脚本输出 → 抄进下面三行：
  报价（给客户的数）: ____
  底价（止损位）    : ____    ← 绝不外发
  L1/L2/L3 三档价   : ____ / ____ / ____

手工补记（脚本不含）：
  出口退税（减项）  : ____
  银行手续费（加项）: ____

让步阶梯（抄脚本的三档，本档递减 2.5 / 1.5 / 1.0）：
  L1 累计 -2.5% → ____  换：____________
  L2 累计 -4.0% → ____  换：____________
  L3 累计 -5.0% → ____  换：____________
  底线 -6%      → ____  到此为止，不再降价格
```

To produce a version for the outside with no floor price, use `... --audience client`; but it still carries the concession ladder, so it **cannot be forwarded directly** (see the note above).

### Template C: Extra fields for the Proforma Invoice (send after the negotiation ends)

On top of Template A, **remove** the tier pricing and the "subject to final confirmation" wording, and add:

```
PROFORMA INVOICE
PI No.: PI-2026-____      Date: YYYY-MM-DD

Payment terms: ____% deposit by T/T within __ days; balance ____% against
copy of B/L / before shipment.
Bank details:
  Beneficiary: ____________
  Bank name:   ____________
  SWIFT:       ____________
  Account No.: ____________
Signed & stamped by seller: ____________
```

The specs, quantities, terms and amounts on a PI ride all the way onto the bill of lading and the customs documents — check them word for word against the final conditions confirmed with the customer before issuing.

## 8. Next stage

The quotation is out, and the back-and-forth begins. Next is **order delivery**: turning the verbal agreement into a formal contract, and moving the money and the goods safely through the whole process — see [`07-order-delivery.md`](07-order-delivery_en.md) (PI, contracts, payment, documents, logistics).

Looking back: the requirement confirmation and terms confirmation before quoting are in [`05-negotiation_en.md`](05-negotiation_en.md); the full end-to-end script walkthrough for one deal is in [`deal-walkthrough.md`](deal-walkthrough.md).
