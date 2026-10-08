# 02·找客户 Find Leads

> **本环节目标**：建立一条能每天稳定吐出 20 条真实线索的渠道组合，形成 200 条以上的原始名单。
> **一句话原理**：客户不是「找到」的，是「筛出来」的；四路并行才够量，单路依赖必断粮。

## 一、为什么这一步排在最前

新手最大的幻觉，是以为自己需要「客户资源」。

真实情况是：任何一个有进口量的行业，一个国家里几百上千家有真实采购行为的贸易商、经销商、连锁店、车队运营方都不在LinkedIn 上等你私信。绝大部分公司没有任何人把「找中国供应商」这件事挂在网上。

所以找客户不是搜索，是筛。从一堆公司名单里，筛出那些「真的在买、真的买得动、真的能联系上」的。

三个硬标准，缺一条就是假线索：
1. **有真实采购迹象**——网站上有产品目录、有批发价目、有业务联系页，不是只有一张首页图的公司。
2. **有进出口相关痕迹**——做过进口、挂过展会、写过跟供应商合作的内容。
3. **有可触达的联系人**——能拿到姓名 + 邮箱或 WhatsApp/电话。只拿到公司名不算线索。

一天 20 条，不是一天发 20 封开发信。一天 20 条**筛过的**线索，发出去的成功率会差出十倍。

## 二、分步操作

**第 1 步：铺渠道（四路并行，别押单一渠道）**

| 渠道 | 能拿到什么 | 怎么用 |
|---|---|---|
| 海关数据 | 真实在进口的公司名 + 品类 + 体量 | 第一主力，最直接证明「这家在买」 |
| 搜索 + 官网 | 官网产品线、批发政策、联系方式 | 补齐海关数据里查不到的邮箱和电话 |
| LinkedIn | 采购负责人姓名和职位 | 找对人，别群发公司通用邮箱 |
| 展会名录 | 常年参展的活跃买家名单 | 筛「真在花钱买流量」的人 |

四路的比例建议：**海关数据 40%、搜索 30%、LinkedIn 20%、展会 10%**。任何一路断了，其余三路还能顶上。

**第 2 步：海关数据挖第一层（最耗时，但最值）**
按 HS 编码（轮胎常见归在 HS 40 章下，具体子目以官方归类为准）拉目标国进口记录。重点看三列：
- **谁在进口**：公司名 → 这就是名单主体
- **进口量级**：从高到低排，大概率是你的目标客户
- **来源国结构**：如果大量从中国进口，说明他们对中国货熟，门槛低

拉一批出来后做初筛：一次进口量小到只做样品、频繁换供应商、名字里带「 trading only 批发部」但没实体地址的，降低优先级。

**第 3 步：官网+搜索补全信息（每条线索 3-5 分钟）**
拿到公司名之后，搜官网。重点看三处：
- `/contact`、`/about`、`/products` 页面——找邮箱、电话、WhatsApp、地址
- 产品目录里有没有你要卖的品类（比如 TBR 商用胎、OTR 工程胎）
- 有没有「批发/经销/代理商」相关表述——决定他是渠道商还是终端用户

顺手记一条「情报」：对方主打什么品牌、价位带大概在哪、有没有提到自己的仓库或门店数量。这些是后面写开发信和报价时的弹药。

**第 4 步：LinkedIn 找对的人**
搜索公司名 → 进公司主页 → 找采购/采购经理/进口经理/老板（Owner 在小国很常见，就是他本人）。
- 发 InMail 或加好友，请求语一句说清身份和来意，不要一上来发产品目录。
- 中东很多小公司决策链极短，能找到采购总监基本就等于找到决策人。
- 找不到人时，用「公司名 + 邮箱格式猜测 + 验证」补，但**验证不过的邮箱不要群发**，退信率会拖垮整个域名信誉。

**第 5 步：展会名录做补漏和校验**
公开的展会参展商名录是可以合法获取的公开资料。用途有两个：
- **补漏**：不在海关数据里但参展过的贸易商
- **校验**：连续两三年参展的，说明还在正常经营

把参展商的「国家 + 产品线 + 是否贸易商」记下来。

**第 6 步：进名单表，做初评级**
所有线索统一进一张表，字段最少要有：
公司名 / 国家 / 官网 / 来源渠道 / 联系人+职位 / 邮箱 / WhatsApp或电话 / 品类线索 / 采购迹象强度 / 语言 / 初步评级（A/B/C） / 跟进状态 / 下次跟进日期

最后做一件事：**每天固定时间（比如早上 9 点）做 30 分钟采集**，雷打不动。渠道纪律比渠道聪明更重要。

## 三、AI 提示词

**提示词 1：从公司官网提取关键信息**

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

中文说明：这段用来把一个官网正文变成结构化字段。关键是「只准写页面上明确写了的内容」和「8 个字段固定输出」——这样每条线索的记录格式一致，可以直接进表。红旗字段专门用来给下一步背调做输入。

**提示词 2：线索优先级批量排序**

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

中文说明：这段用来避免「看着顺眼就都标 A」。它强制 AI 给置信度，并且必须给「下一步具体动作」而不是空泛建议。同时把数据不足的公司主动暴露出来，提醒你要去补信息而不是硬发。

**提示词 3：搜索策略生成器**

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

中文说明：这段用来一次性拿到一整套搜索策略，特别包含「找负面信号」的查询——很多人只搜好话，搜到已停业、被告、被制裁的公司还当新线索发信，这是纯浪费。第 4 部分「无效查询模式」能直接告诉你哪些坑别踩。

## 四、检查清单

- [ ] 四条渠道都已开通并实际跑过至少一轮，不是只开通了海关数据
- [ ] 线索表字段固定，每条都有来源渠道标记（能追溯「这条是哪来的」）
- [ ] 每条线索都经过三条硬标准筛查：有真实采购迹象 + 有进出口痕迹 + 有可触达联系人
- [ ] 海关数据里对「一次只进口样品」「频繁换供应商」的公司已做降级处理
- [ ] 每条线索都标了 A/B/C 初评级，评级理由写进备注而不是凭感觉
- [ ] 每天固定 30 分钟采集已排进日程，连续执行 7 天不断档
- [ ] 无效邮箱已剔除，未验证邮箱未进入群发名单
- [ ] 负向信息检索已跑过一轮（停业/诉讼/制裁/停止经营），标记出可疑公司

## 五、新手常见坑

**坑 1：只做海关数据一条路**
- 现象：花两天拉了 300 条海关记录，然后卡住不动了。
- 原因：海关数据只有公司名和贸易记录，没有邮箱、没有联系人、没有产品细节。
- 正确做法：海关数据只当「名单入口」，每拉出 20 条就必须配 20 条官网检索补全信息。40% 海关 + 60% 补充信息，才是完整一轮。

**坑 2：拿到公司名就算完成线索**
- 现象：表里 300 行，全是公司名，联系人栏大面积空白。
- 原因：把「找到公司」当终点，没意识到开发信发到 info@ 是最低效的选择。
- 正确做法：入库前必须填联系人。找不到具体人的，降级为 B 类并标「待挖人」，不要占用 A 类名额。

**坑 3：群发同一个邮箱格式**
- 现象：猜了 200 个 firstname.lastname@company.com，一次性发出去，退信率 60%。
- 原因：猜错的邮箱被硬发，域名信誉被拖，后续真发得进的邮件也会进垃圾箱。
- 正确做法：小批量试（每次 10-20 个）先验证，退信率超过 10% 立即停。宁可发 50 个准的，不要发 200 个里的 140 个假的。

**坑 4：只看「有没有网站」，不看「网站说什么」**
- 现象：看到网站有英文页面就判定为优质客户。
- 原因：现在的网站大量 AI 生成，看着完整，其实零采购信号。
- 正确做法：看产品目录、看是否列了品牌、看有没有批发/经销表述、成立年份。有网站 ≠ 在做进口。

**坑 5：靠展会名录当唯一来源**
- 现象：抄了一份展会参展商名单就开始群发。
- 原因：参展商名录是「愿意花钱曝光的公司」，同一家公司会出现在多个展会，且部分公司已停业。
- 正确做法：展会名录只占 10% 权重，且必须用「连续参展年份 + 官网活跃度 + 海关记录」三重校验后再入库。

**坑 6：不定时采集，三天打鱼两天晒网**
- 现象：忙的时候一个礼拜没碰，手感全无。
- 原因：把找客户当项目而不是当日常动作。
- 正确做法：把它绑死在每天固定时间段。渠道纪律 > 渠道聪明。宁可每天只做 30 分钟，也别做一次 8 小时然后停一周。

## 六、下一环节

名单有了，但不能直接发信——里面有骗子、有皮包、有根本不买货的。下一步是**背调客户**：把 200 条名单压缩成一批值得投入时间的真买家。
