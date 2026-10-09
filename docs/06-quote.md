# 06·报价谈判 Quotation & Negotiation

> 这一步要交三样东西：一份报价单、一套让步阶梯、几句现成话术。目的就一个——别让你每一次松口，都白松。
> 先记一句话：降价不是让步，是买卖。白送的降价是把利润塞给别人，换条件的降价才是把利润换成更值钱的东西。

## 一、为什么这一步排在最前

新手报价最常见的三种死法：

**第一种：价格表一发，等着被砍。** 你发了目录价，对方拿着去比价三周，回来一句「others are 8% cheaper, can you match?」。你降 8% 单子成了，利润薄了，还不知道自己降的那 8% 里本来有多少水分可以留着。

**第二种：底价一报，被砍就退。** 对方一压你就让，让到某个数字你其实不干了，但你已经把价格空间全交出去了，最后只能硬着头皮做或者毁约。

**第三种：让步换不到任何东西。** 你降 3% 换来一句「好的，那再看看运输条款」。降价变成了单方面投降。

谈判不是嘴皮子临场发挥，是开口之前就把台阶铺好。压力没来之前，先想清楚：从哪个数开价、让到哪一步收手、每一档换回什么。

价格也不是唯一能谈的。数量、付款方式、装柜效率、有效期、花纹定制、目标价，全是可以拿来换的筹码。用非价格条件去换降价，才是你保住利润的活路。

## 二、分步操作

### 先分清贸易条款：缩写背后是「谁付钱 + 谁担风险」

新人最贵的一条死法：报了 CIF，却只算了海运费。CIF 的义务止于目的港船上，目的港之后的一切费用（THC 码头操作费、卸货、滞港/滞箱、清关、关税、内陆派送）默认由买方承担——但买方常常以为你包了，货到港才发现要自己掏钱，扯皮就从这里开始。所以报价单上要写死一行「不含什么」。

| 条款 | 卖方付到哪 / 办到哪 | 风险何时转移给买方 | 新人最常踩的坑 |
|---|---|---|---|
| **EXW**（工厂交货） | 只把货备好放在工厂；装柜、出口报关、海运、保险全归买方 | 买方上门提货时 | 出口报关单不在你名下，**退税可能拿不到**；买方是外国公司时出关单证仍要你配合，EXW 下你既少收钱又不省心 |
| **FOB**（装运港船上交货，须写港口，如 `FOB Yantian`） | 出口报关 + 内陆运输 + 装运港港杂 + 把货装上船 | 货物装上船 | 装船前的拖车、报关、港杂、单证费全在你身上，报 FOB 时**必须摊进成本**；另外要留装船前的照片证据，装船后破损已不是你的责任 |
| **CFR / CIF**（成本+运费 / 再加保险，须写目的港，如 `CIF Dammam`） | 在 FOB 基础上付到目的港的海运费（CIF 还要买保险） | 仍是**装运港装船时**（不是到港时） | ① 最大坑：**目的港费用不在 CIF 里**；② CIF 保险通常只按 CIF 货值 110% 投保最低险别，买方要一切险需另谈加费 |
| **DDP**（完税后交货） | 包到买方门口，含目的国清关与关税、VAT | 买方签收时 | **没有可靠的目的国清关代理就别报**。关税税率、清关代理费、VAT、可能的反倾销税全由你承担，一旦卡关，滞港费按天烧钱。新手首单不碰 DDP |

记住一句就行：你能管到哪一步，就报到哪一步。管不了目的港清关，报 CIF，别碰 DDP。

CIF 报价单上建议固定加这一行（英文照抄）：

```
CIF <目的港> (port of discharge only). Destination charges, customs clearance,
duties and inland delivery are for Buyer's account.
```

首单怎么选：优先 FOB（责任边界最清楚，目的港不用你操心）→ 客户非要门到门才上 CIF → DDP 只有你手里真有靠谱清关代理时才接。

### 一单报价的完整成本构成（照着勾，漏一项就漏利润）

| 成本项 | 说明 | FOB | CIF | 对应脚本参数 |
|---|---|:--:|:--:|---|
| 产品成本（出厂/EXW 价） | 原材料 + 加工，可含工厂利润 | ✓ | ✓ | `--cost` |
| 包装费 | 纸箱/托盘/缠膜/唛头；定制包装另计 | ✓ | ✓ | 摊进 `--cost` |
| 国内运费 | 工厂 → 装运港的拖车/内陆运输 | ✓ | ✓ | `--local` |
| 报关与单证费 | 出口报关、商检、产地证、提单 | ✓ | ✓ | `--local` |
| 装运港港杂 | 码头操作、铅封、舱单 | ✓ | ✓ | `--local` |
| 海运费 | 装运港 → 目的港 | ✗ | ✓ | `--freight` |
| 保险费 | 按 CIF 货值 110% × 费率 | ✗ | ✓ | `--insurance`（默认 0.15） |
| 银行手续费 | 电汇手续费；L/C 的通知费/议付费/不符点费 | ✓ | ✓ | 摊进 `--local` |
| 汇率与换汇损失 | 结汇价与报价汇率之差 | ✓ | ✓ | 走风险预留 |
| 不可预见费 | 汇率波动 / 交期延误 / 客户违约 | ✓ | ✓ | `--contingency`（默认 0.03） |
| 出口退税 | 增值税退税额，**是利润的一部分（减项）** | ✓ | ✓ | 脚本未内置，手工处理 |
| 预期利润 | **成本加成**（报价 = 成本基数 ×(1+加成%)） | ✓ | ✓ | `--margin`（默认 15） |

几个容易踩的坑，记一下：
1. `--cost` 是单位成本（每单位多少钱，币种看 `--currency`）。国内费用要么先摊进 `--cost`，要么用 `--local` 单加，别两处都算，算重了。
2. 退税和银行手续费脚本里没有：退税是减项、银行费是加项，都得你自己在 `--cost` 里手调。
3. `--contingency` 就是风险预留（默认 3%），脚本已经乘过了，你别手贱再乘一遍。
4. `--margin` 是成本加成（markup），不是毛利率。脚本算的是 `报价 = 成本基数 ×(1+加成%)`；你要按毛利率倒推（`报价 = 成本 ÷(1−毛利率)`），两码事——15% 毛利率约等于 17.6% 加成。填反了，钱就少赚了。

### 用脚本跑一遍（命令可直接复制）

在项目根目录执行。脚本只用 Python 标准库，装了 Python 3.8+ 就能跑，无任何第三方依赖：

```bash
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15 --local 1.2 --moq 300 --lead-time "25天" --validity 15
```

> 上面数字均为**【示例】**输入（单位成本 28、海运费 6、成本加成 15%、本地费用 1.2，USD/件），请替换成你自己的成本。

真实输出（内部视图，含成本与底价）：

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

参数速查（真实参数名与默认值，以 `python scripts/quote_engine.py --help` 为准）：

| 参数 | 默认值 | 含义 |
|---|---|---|
| `--cost` | **必填** | 单位成本（EXW/工厂价，每单位） |
| `--freight` | 0 | 到目的港海运费（每单位）；报 FOB 时留 0 |
| `--margin` | 15 | **成本加成 %**（不是毛利率） |
| `--insurance` | 0.15 | 保险费率，单位是**百分数**（0.15 = 0.15%） |
| `--local` | 0 | 本地费用（报关/拖车/港杂，每单位） |
| `--contingency` | 0.03 | 不可预见费比例 |
| `--anchor` | 无 | 竞品锚价（报价币种），给了会输出定位建议 |
| `--fx` | 1.0 | 汇率：1 成本币种 = fx 报价币种（成本 CNY、报价 USD 时填 0.14），**只在开头换算一次** |
| `--currency` | USD | 报价币种符号 |
| `--unit` | 件 | 计价单位 |
| `--moq` | 无 | 最小起订量（报价单必带字段） |
| `--lead-time` | 无 | 交货期，如 `"25天"` |
| `--validity` | 30 | 报价有效期天数 |
| `--audience` | internal | `internal` 含成本与底价；`client` 客户视图，**绝不出现底价** |
| `--out` | 无 | 同时写入文件（UTF-8），如 `--out quote.txt` |
| `--format` | table | `table` 或 `json` |
| `--insurance-rate` | 无 | 高级入口，收**比率**（0.0015 = 0.15%），可覆盖 `--insurance` |

三个单位陷阱：
- `--insurance` 收百分数。`--insurance 0.3` = 0.3%；想写「千分之三」请用 `--insurance-rate 0.003`。输错量级（>5%）脚本会直接报错拒绝执行，不会静默给你一个错价。
- 报 FOB 时不要填 `--freight`，否则你会拿到一个 CIF 数字当 FOB 报出去。
- `--margin` 是加成不是毛利率（见上面第 4 条）。

常用变体：

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
```

> **注意**：`--audience client` 只去掉成本与底价，**让步阶梯和"换回条件"仍在输出里**。所以脚本输出永远只是**内部草稿**，不要原样截图或转发给客户——照着它填你自己的报价单（见第七节模板 A）。

**第 1 步：算到底线（报价之前，不是被砍之后）**

报价前必须有三条线，写在纸上：

- **成本线**：出厂成本 + 内陆运费 + 包装 + 出口港费用 + 商检/报关 + 财务成本 = 真实成本（按上一节的清单逐项勾，别凭记忆）
- **目标线**：你想拿的价格（谈判起点，通常高于目标）
- **底价线**：低于这个数就不做（这个数不能告诉客户）

脚本输出里的 `FOB 报价` 和 `FOB 底价` 正好对应这里的**目标线**和**底价线**：`FOB 报价` 是你的开价，`FOB 底价` 是脚本给的止损位（报价 ×(1−6%)，且永不低于成本基数）。三条线不用自己拍，跑一次脚本就有了。

**底价线的算法**（结构，不是数字；实际数字必须用自己的成本算）：
```
底价 = 真实成本 + 最低可接受利润 + 风险预留（汇率波动/交期延误/客户违约）
       - 出口退税额
```
汇率波动大的市场必须加进风险预留，退税必须从成本里减掉——这两条新人基本都会漏（一个少算支出，一个少算收入）。

报价单上的数，得是 成本 + 利润 + 风险 凑出来的，不是拿成本乘个拍脑袋的系数就发出去了。

> **铁律：底价、成本、毛利率、让步空间，一律不得出现在任何发给客户的文件里。** 报价单上永远只出现一个价格 + 一个有效期。内部核算单独建一个文件（文件名带 `INTERNAL`），别和报价单放在同一个文档里——很多「手滑把底线发出去」的事故，根源就是两张表在同一页上。

**第 2 步：报价单必填字段（Quotation 与 Proforma Invoice 不是一回事）**

先分清两个东西，别混用：

- **Quotation / 报价单**：要约邀请。用于谈判阶段，可以写"有效期"和"以最终确认为准"，**不构成正式合同**。客户拿它去比价、去申请进口许可、去银行贷款。
- **Proforma Invoice / 形式发票（PI）**：谈判结束后发的**准合同**。客户凭它付款、开信用证、报关。PI 上的规格、数量、条款、金额一旦出错，会一路带到提单和清关单据上，改单要花钱。

两者的必填字段差别就在"付款与银行信息"上——Quotation 里付款条件可以留空（谈判筹码），PI 里必须写死。

**必填字段清单（照着勾）**

| # | 字段 | Quotation | PI | 说明 |
|---|---|:--:|:--:|---|
| 1 | 单据类型与编号 | ✓ | ✓ | 抬头写清 `QUOTATION` 还是 `PROFORMA INVOICE`；编号如 `QT-2026-0145` / `PI-2026-0145`（【示例】编号），便于双方追踪 |
| 2 | 日期 + 有效期 | ✓ | ✓ | 见下方「有效期与汇率锁定」一节 |
| 3 | 卖方抬头 | ✓ | ✓ | 公司全称、地址、联系人、邮箱/电话 |
| 4 | 买方抬头 | ✓ | ✓ | **公司全称 + 国家**，一个字母都不能错（PI 错了会影响清关） |
| 5 | 规格表 | ✓ | ✓ | 型号 / 花纹 / 层级 / 载重指数 / 数量 / 单价 / 金额，一行一个型号 |
| 6 | 单价的**计价基准** | ✓ | ✓ | `USD/pc` 还是 `USD/set`、`EXW/FOB/CIF` 哪个口径——不写基准的单价是废话 |
| 7 | 币种 | ✓ | ✓ | 明确 `Currency: USD`，非美元必须配汇率条款 |
| 8 | 总价 + 柜型 + 件数 | ✓ | ✓ | `Total FOB Yantian: USD xxx for 1x40HQ (480 pcs)`（【示例】数量与柜型） |
| 9 | 贸易条款 + 指定港口 | ✓ | ✓ | `FOB Yantian` / `CIF Dammam`，写明 Incoterms 版本（**具体适用版本以合同约定为准**）；CIF 加那行"目的港费用归买方" |
| 10 | 包装方式 | ✓ | ✓ | 几件一包、是否托盘、唛头要求；影响装柜量，直接影响单价 |
| 11 | 交货期 / 生产周期 | ✓ | ✓ | 写 `lead time` 起算点（定金到账日起 / 合同签订日起） |
| 12 | 装运港 + 目的港 | ✓ | ✓ | 与第 9 条一致，拼错港口是免费送给对手的筹码 |
| 13 | 毛重 / 净重 / 体积 | 建议 | ✓ | 影响运费核算与客户清关 |
| 14 | 原产国 | 建议 | ✓ | `Origin: China`，客户办产地证要用 |
| 15 | 付款条件 | 可留空 | ✓ | Quotation 里留空是谈判筹码；PI 里必须写死（比例、方式、时点） |
| 16 | 银行信息 | ✗ | ✓ | Beneficiary / Bank name / SWIFT / Account No. —— **PI 才有，Quotation 不要放** |
| 17 | 签字盖章 | 建议 | ✓ | PI 通常需要卖方签章 |

写完对照这张表勾一遍，再发。

**第 3 步：准备让步阶梯（核心动作）**

阶梯要提前写在纸上。下面这张表和 `scripts/quote_engine.py` 的输出**一一对应**（脚本给三档价格让步，L4 是「不再降价格」这一档）：

| 层级 | 累计降幅 | 对应脚本输出 | 必须换回的条件（【示例】，按你的实际情况改） |
|---|---|---|---|
| L0 起点 | 0 | `FOB 报价` | — |
| L1 | −2.5%（本档 −2.5%） | 第 1 步 `new_fob` | 首单 ≥ 1 个柜（20GP/40HQ）且接受 30% 定金 |
| L2 | −4.0%（本档 −1.5%） | 第 2 步 `new_fob` | 由试订单升级为年度框架 / 量翻倍以上 |
| L3 | −5.0%（本档 −1.0%） | 第 3 步 `new_fob` | 签 1–3 年排他或独家代理（区域保护换低价） |
| L4 | **不再降价格** | 已接近底价线 | 只给非价格筹码：更长有效期、优先排产、免费验货支持、装柜清单与装箱照片 |
| 底线 | −6%（脚本 `FOB 底价`） | 低于此数不做 | 不让 |

脚本的三档是**增量递减**（2.5 → 1.5 → 1.0，累计 5%），比底价的 6% 少一个百分点——这是故意留的一手：客户永远猜不到你还有最后一格。

**注意：不要自己加「降 8%」这一档。** 脚本的底价是报价 ×(1−6%)，再往下就跌破止损位了。你手写的阶梯如果比脚本多出一档，说明你的开价定低了——**往上调开价，不要往下调底线。**

关键规则：
- **每次只降一级**，不连续降
- **每一级必须有交换条件**，且条件写在话里（说出来，不是心里想）
- **L3 之后不再让价格**，用非价格条件回应（数量、付款、有效期、交期灵活度）
- **让步幅度递减**：越往后越小，让对方知道底在接近——脚本的三档增量就是 2.5 → 1.5 → 1.0
- **先跑脚本再定阶梯**：把脚本输出的三个数字抄进表里的 L1/L2/L3，别手写百分比

**补充内容：有效期、汇率锁定、MOQ 阶梯价怎么写**

这三行是报价单上最容易被忽略、但事后最容易吵架的地方。

**① 有效期**——不是礼貌，是价格保护：

```
Validity: This quotation is valid for 15 days from the date of issue (until YYYY-MM-DD).
Prices are subject to re-confirmation thereafter due to raw material / freight volatility.
```

- 原材料（橡胶、钢帘线）和海运费波动大时缩到 7-10 天；行情平稳可给 15-30 天。
- **写死截止日期**，不要只写「15 days」——只写天数，双方对起算日（发出日 / 收到日）的理解可能不同。
- 有效期过期后对方回头要价：**重新报，不要沿用旧价**，哪怕只过了一周。

**② 汇率锁定**——非美元报价必写，美元长单也建议写：

```
FX clause: Prices are based on USD/CNY = 7.10. Should the rate at the time of
payment move by more than ±2%, both parties agree to re-negotiate the USD price accordingly.
```

（【示例】汇率与浮动阈值，按你的实际结汇成本和风险承受度填。）

- 报价单上**必须写出你用的汇率数字**，否则客户以为你承担了全部汇率风险。
- 阈值一般 ±1%~±3%（【示例】区间）：给太宽等于没锁，给太窄客户不接受。
- 从报价到收款周期越长（比如 60-90 天账期），越要写；现款现货可以放宽。

**③ MOQ 与阶梯价**——把"多买便宜"写进报价单，省掉一轮讨价还价：

```
Price tiers (based on single shipment quantity):
  1 x 20GP  (≥ 200 pcs)  : USD ____ / pc
  1 x 40HQ  (≥ 480 pcs)  : USD ____ / pc
  2 x 40HQ  (≥ 960 pcs)  : USD ____ / pc
MOQ: 200 pcs per size / 1 x 20GP per order. Mixed sizes allowed in one container.
```

（数量为【示例】，按你的实际装柜量替换。）

写法要点：
- 阶梯**按"单次出货量"计**，不按"年度累计量"——累计量你没法验证，也容易被对方事后追讨。
- 每档写清**单位和对应柜型**，避免"200 件是一个柜还是一托"的争议。
- 明确**是否允许混装**（mixed sizes in one container）：允许混装能显著降低客户试单门槛，是你手上最便宜的筹码之一。
- 阶梯价要和你第 3 步的让步阶梯**不冲突**：阶梯价是明码标价的数量折扣，让步阶梯是谈判时才动的空间。客户够到 2 个柜，你就走阶梯价那一档，不要同时再给 L2 折扣。

**第 4 步：把非价格筹码列出来（谈判弹药库）**

这些是你能交换、成本更低的东西，提前列好：
- 付款方式：全款预付、30% 定金 + 70% 见提单副本、20% 定金
- 数量：2 个柜起订可以给更好的单价；一次 4 个柜可以再谈
- 交期：接受你更希望的交期，换一点价格
- 有效期：拉长有效期，换一点价格（对原材料波动敏感的客户有效）
- 花纹/包装：定制花纹标签、定制包装，按 MOQ 分档
- 免费项：提供装柜清单、装箱照片、第三方验货支持

记住：先甩非价格筹码，实在没招了再动价格。

**第 5 步：应对「别人更便宜」**

这是最常见的压价话术。处理顺序：
1. 不否认，不辩护（说「that's not true」是输）
2. **问差异**：「May I ask what scope the other offer covers — same size, same pattern, same packaging, same payment terms?」—— 很多时候差异在配置或条款
3. **换条件**：「If we can do 30% advance and 2x40HQ per shipment, let me see what I can do on price.」
4. **守底线**：「Our floor at this configuration is what I quoted; to go lower I would need to change the scope.」—— 说清是配置问题不是诚意问题

**第 6 步：应对「先给个最低价」**
- 现象：第一轮就要 lowest price。
- 处理：不直接给。回「I can sharpen the number if you confirm quantity and payment terms. Our price depends on both.」—— 先把条件拿回来。
- 实在要挡回去：「Our best price for this spec starts at X, but that's tied to 1x40HQ with 30% advance. Below that I need to check with production.」

**第 7 步：收尾和跟进纪律**

- 报价后不主动降价，等对方反应
- 对方沉默超过 5-7 天，可以跟进一次，但**跟进不带降价**（带一个信息点）
- 报价发出前让 AI 或同事挑一遍错：数字、单位、港口、Incoterms、有效期、拼写
- 每次让价都留书面记录：邮件里写清「这个价格是基于 A+B+C 条件」

## 三、怎么算这步过关了

几个硬杠杠，对着查：

- 成本线 / 目标线 / 底价线三者已分开写下，底价、成本、毛利率**未出现在任何客户可见文件**（内部核算单独建文件）。
- 成本已按完整清单逐项勾过（产品 / 包装 / 国内运费 / 报关单证 / 港杂 / 海运费 / 保险 / 银行手续费 / 汇率 / 不可预见费 / 退税 / 利润），无漏项。
- 底价已含汇率波动与交期延误的风险预留，且**已扣减出口退税**。
- 贸易条款是 FOB / CIF / EXW / DDP 中明确的一个，且**写清了指定港口**；报 CIF 时已书面声明目的港费用由买方承担；报 DDP 前已确认有可靠的目的国清关代理。
- 已用 `scripts/quote_engine.py` 跑出 FOB/CIF 区间作为起点，命令能真实执行。
- 报价单必填字段已齐全：单据类型与编号 / 日期+有效期 / 买卖双方全称+国家 / 规格表 / 计价基准+币种 / 总价+柜型+件数 / Incoterms+港口 / 包装 / 交期 / 原产国；PI 另补付款条件与银行信息。
- 有效期写死了**截止日期**；非美元报价或长账期已附汇率锁定条款（含基准汇率与浮动阈值）。
- MOQ 与数量阶梯价已写明：每档对应单次出货量与柜型、是否允许混装。
- 让步阶梯与脚本输出一致（L1 −2.5% / L2 −4.0% / L3 −5.0%，底价 −6%），幅度递减、每级带交换条件，L3 之后不再让价格，只用非价格筹码回应。
- 非价格筹码已列出并优先使用；「别人更便宜」「先给最低价」两套话术已提前备好。

## 四、AI 提示词

**提示词 1：报价单生成 + 内部核算校验**

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

中文说明：第 2、3 部分是给内部看的，必须在发送前删掉。第 4 部分的自检清单能挡掉最丢人的错误——数量和柜数不一致、港口拼错。开头那句「MISSING — cannot compute margin」是关键，它逼着 AI 不能闷声编个成本骗你。

**提示词 2：让步阶梯设计**

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

中文说明：这张表的核心是第 4 部分「必须不说的话」——谈判中最容易失手的是自己说漏嘴。比如你为了留住客户说了句「这个价格已经是极限了」，其实还有一级没走完，后面就没得谈了。

**提示词 3：压价应对话术生成**

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

中文说明：第 1 部分最关键的是认出对方在玩哪套话术——「time pressure tactic」和「budget excuse」应对完全两码事，混着接招准吃亏。第 3 部分「不该说的话」每次谈之前扫一遍，能省掉不少临场说漏嘴的尴尬。

## 五、检查清单

- [ ] 成本线、目标线、底价线三者已分开计算并写下，底价/成本/毛利率未出现在任何客户可见文件
- [ ] 成本已按完整清单逐项勾过：产品、包装、国内运费、报关单证、港杂、海运费、保险、银行手续费、汇率、不可预见费、退税、利润
- [ ] 底价已包含汇率波动与交期延误的风险预留，并已扣减出口退税额
- [ ] 贸易条款已明确并写清指定港口；报 CIF 时已声明目的港费用由买方承担
- [ ] `scripts/quote_engine.py` 已跑通（命令真实执行过），FOB/CIF 区间与三档阶梯已抄进我的阶梯表
- [ ] 报价单必填字段已齐全：编号、日期+有效期、买卖双方全称+国家、规格表、计价基准+币种、总价+柜型+件数、Incoterms+港口、包装、交期、原产国
- [ ] 报价单已通过逐项自检：单位、货币、港口拼写、Incoterms 地点、柜数与件数一致性、算术
- [ ] 有效期写的是**截止日期**（不是只写天数）；汇率锁定条款已按需附加
- [ ] MOQ 与数量阶梯价已写明每档的数量、柜型、是否允许混装
- [ ] 让步阶梯与脚本输出一致（L0 起点 + L1 −2.5% / L2 −4.0% / L3 −5.0% + 底线 −6%），L3 之后不再降价格
- [ ] 内部成本与风险块已删除（报价单发给客户前；PI 另需补付款条件与银行信息）
- [ ] 非价格筹码清单已列出，并明确优先用非价格筹码
- [ ] 应对「别人更便宜」「先给最低价」的两套话术已提前备好
- [ ] 每次让价的交换条件已在邮件中书面写明（不只是口头交换）
- [ ] 报价有效期已设置并写死截止日期（脚本 `--validity` 默认 30 天；海运费/汇率波动大时缩到 7–15 天）

## 六、新手常见坑

**坑 1：底价直接写在报价单上**
- 现象：报价单里有一行「最低可做价格」，客户直接照着还价。
- 原因：想让客户觉得「我已经给了诚意」。
- 正确做法：报价单上永远只挂一个价格 + 一个有效期。底价是你被窝里藏的，写在另一张纸上，最好别和报价单放在同一个文档——手滑发出去的事故，十个有九个都是两张表挨一起。

**坑 2：对方一压就降，没换任何东西**
- 现象：对方说「降 3% 我就下单」，你降了，他说过两天。
- 原因：把「让价」当成「善意」，而不是「交易筹码」。
- 正确做法：降价前先说条件。「降 3% 可以，前提是预付 30%、订量 2 个柜起、有效期 10 天。」三选二，不白给。

**坑 3：一次降到位**
- 现象：对方说「至少降 5%」，你直接降 6%，还多送了一点。
- 原因：怕麻烦，想快点结束。
- 正确做法：只降一级（第一档是 −2.5%），看反应。你永远要给对方留「可以再谈」的空间。谈判在对方觉得「还能再挤一点」的时候才结束。

**坑 4：回复「我们价格已经很低了」**
- 现象：被压价时反复强调自己已经降价很多。
- 原因：把「辩解」当防守。
- 正确做法：换成问句。对方的报价覆盖了什么范围？配置一样吗？付款条件一样吗？—— 把话题从「我贵不贵」转到「我们比的是什么」，你就重新拿回了比较标准。

**坑 5：把价格和信用额度一起送出去**
- 现象：为了拿下首单，对方要 90 天 O/A 账期，你答应了。
- 原因：首单压力大，想赶紧成。
- 正确做法：新客户不给 O/A。首单 100% 预付或 30% 定金 + 70% 见提单副本。账期是用你的现金流换来的折扣，不能白给。

**坑 6：报价单自己都没看就发**
- 现象：把 AI 生成的报价单直接发出去，客户回「CIF Dammam 写的是 CIF Jebel Ali」。
- 原因：急着交差。
- 正确做法：发之前让 AI 逐项自检（提示词里的 ERROR CHECK 段落），再自己核一遍数字和港口。报价单上的每一个错，都是对手方免费的筹码。

**坑 7：让步不写条件**
- 现象：邮件里只说「based on our discussion, we can do USD x」，没说前提是什么。
- 原因：觉得说条件显得斤斤计较。
- 正确做法：每次让价都书面写清条件——「该价格基于 30% 预付 + 2x40HQ 订量 + 10 天有效期内」。否则一周后他会说「当时谈的不是这个条件」。

**坑 8：报了 CIF，却没算清（也没说清）目的港费用**
- 现象：客户问「是不是到港就完事了」，你说「是」；货到港后客户被收 THC、卸货费、滞港费，回头找你报销。
- 原因：把 CIF 理解成「包到门」。实际上 CIF 只覆盖到**目的港船上**的运费和保险，风险也在装运港装船时就转移了。
- 正确做法：报价单固定加一行 `CIF <港> (port of discharge only). Destination charges, customs clearance, duties and inland delivery are for Buyer's account.`；客户真要门到门，就报 DDP，但先确认你有可靠的目的国清关代理，否则别接。

**坑 9：成本漏项——漏退税、漏银行手续费**
- 现象：算成本时只算了产品价和运费，报价看着有利润，做完一单发现白干。
- 原因：退税（减项，是收入）和银行手续费（L/C 的通知费、议付费、不符点费）不在"产品成本"里，最容易漏。
- 正确做法：按第二节的成本构成表逐项勾，一项都别跳。退税从成本里**减掉**，银行费**加进去**。

**坑 10：把脚本输出直接截图发给客户**
- 现象：跑完 `quote_engine.py`，把结果截图贴进邮件，觉得"专业"。
- 原因：没意识到默认视图（`--audience internal`）里同时含**成本基数**、**FOB/CIF 底价**，还有三档让步阶梯和"换回条件"。
- 正确做法：脚本输出是**内部草稿**，只抄你要给客户的那一个数字（FOB 或 CIF 报价），然后填进第七节模板 A。加 `--audience client` 能去掉成本与底价，但**让步阶梯仍在**，仍不能原样转发。

**坑 11：把加成当毛利率（`--margin` 填错口径）**
- 现象：想要 15% 毛利率，填 `--margin 15`，结果实际毛利率低于预期。
- 原因：`--margin` 是**成本加成（markup）**，`报价 = 成本基数 ×(1+加成%)`；毛利率要倒推，两者不同（15% 毛利率 ≈ 17.6% 加成）。
- 正确做法：想按毛利率报价，先换算成加成再填；脚本输出的"计价口径"那一行就是提醒你这件事的。

**坑 12：有效期只写天数、汇率不写死**
- 现象：报价单写 `Validity: 15 days`，三个月后客户拿着旧报价单来下单。
- 原因：只写天数，双方对起算日（发出日 / 收到日）理解不同；行情涨了你想调价，客户说"你说过 15 天"。
- 正确做法：写死截止日期 `valid until YYYY-MM-DD`；非美元报价或账期超过 30 天，加汇率锁定条款（基准汇率 + 浮动阈值）。

## 七、可复制模板（照填，不依赖 AI）

### 模板 A：给客户的报价单骨架（Quotation）

**这一份里不许出现任何成本、毛利、底价。**

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

（所有数字均为【示例】占位，替换成你自己的。）

### 模板 B：内部成本核算表（**单独建文件，文件名带 INTERNAL，绝不外发**）

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

要对外出一份不含底价的版本，用 `... --audience client`；但它仍带让步阶梯，**不能直接转发**（见上文提示）。

### 模板 C：Proforma Invoice 的补充字段（谈判结束后发）

在模板 A 的基础上**删掉**阶梯价与"以最终确认为准"的表述，补上：

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

PI 上的规格、数量、条款、金额会一路带到提单和清关单据，签发前必须与客户确认过的最终条件逐字核对。

## 八、下一环节

报价发出去了，开始来回谈。下一步是**订单交付**：把口头共识变成正式合同，把钱和货安全地走完整个流程 —— 见 [`07-order-delivery.md`](07-order-delivery.md)（PI、合同、收款、单证、物流）。

往回看：报价前的需求确认与条款确认在 [`05-negotiation.md`](05-negotiation.md)；完整一单的脚本串联见 [`deal-walkthrough.md`](deal-walkthrough.md)。
