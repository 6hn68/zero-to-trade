# 01·选市场 Market Selection

> **本环节目标**：锁定 1 个首站市场（第一站只打一个），并写出选它的三条硬理由。
> **一句话原理**：新手不是选市场最多的人，是选市场最窄、最快能拿到第一单的人。

## 一、为什么这一步排在最前

外贸最贵的错误不是选错市场，是同时打五个市场。

同时打五个市场会发生什么？你要写五套开发信模板、查五套认证要求、记五套时差、应付五种付款习惯。做了三个月，每个市场都停在「有几个客户问了价格」，没有一个到成交。

反过来，只打一个市场：一个月能积累 200 条真线索，能搞清这个国家谁说了算、进口需要什么证、经销商从哪进、能接受什么价格。三个月能出第一单。

第一单的意义不只是钱。是它证明你的产品、你的报价、你的合同、你的单证这一整套东西是能跑通的。跑通一次，复制到第二个市场才有底。

所以第一步不是「调研十个国家」，是「砍掉九个」。

## 二、分步操作

**第 1 步：列候选池（半天）**
从你能想到的地方随手列 10-15 个国家。不用都合理，先列出来。轮胎行业的话，沙特、伊拉克、阿联酋、卡塔尔、科威特、埃及、阿尔及利亚、摩洛哥、巴西、波兰、俄罗斯、印尼、越南、泰国、墨西哥——先铺开。

**第 2 步：三维打分（1-2 天）**
每个候选国打三个分，0-5 分：
- **语言**：有没有你能读的官方/行业资料？当地人做不做英语生意？没有英语市场的先降分（巴西、西非、法国日耳纳语区降分；中东GCC降分加分）。
- **需求**：这个国家进口量有没有规模、增长有没有苗头、是不是靠进口吃饭。判断口径：看目标国海关/UN Comtrade 里 HS 编码（轮胎常用 HS 40 项下具体子目，以官方最新归类为准）对应的进口金额和来源国结构，再对照中国出口端数据交叉看。**具体数字以官方最新公告为准**，别拿三年前的文章当结论。
- **壁垒**：认证门槛、关税税率、是否需要代理、付款方式是否苛刻。壁垒高不是否决项，是「你打算用什么方式绕」的题目。

三维加总排序，取前 3。

**第 3 步：砍到 1 个（1 小时）**
对前 3 名各问自己三句话：
- 这个国家我能不能在 30 天内拿到 20 个真实可联系的买家名字？
- 这个国家有没有我能说清楚的一个「行业聚会场」？（展会、协会、批发市场）
- 这个国家有没有我认识或者能问到的人？（哪怕是同行朋友）

三句里有两句以上答「不行」，就砍掉。留一个。

**第 4 步：写三条理由（30 分钟）**
必须落到具体事实，不要写「市场大、潜力好」。比如：
- 沙特 2024 年后进入基建+工业本地化周期，轮胎替换需求上升，且 GCC 普遍无本土轮胎厂，进口依赖高（**具体增速与规模请以沙特官方统计机构与 UN Comtrade 最新数据核对**）。
- 中东客户英语流通，邮件 + WhatsApp 双通道能跑通。
- 迪拜/利雅得有成熟汽配贸易集群，展会名录和批发商名单可公开检索，线索获取成本低。

**第 5 步：立一个最小验证目标**
不是「今年做到 X 万」，是「30 天内：拿到 20 条真线索、发出 100 封开发信、拿到 5 个回复、2 个报价机会」。达不到就说明市场选错了或者打法错了，两者都比硬撑便宜。

## 三、AI 提示词

**提示词 1：市场三维打分**

```
You are an export market analyst specialized in B2B tire sales (China-based exporter).
Task: Score the following candidate markets for a NEW exporter with limited budget and no
existing relationships: {paste your country list}.

Score each country 0-5 on three dimensions:
1. Language accessibility (English usable in B2B trade? official/industry data readable?)
2. Demand size (import volume for tires HS40 subheadings; growth trend; import dependence)
3. Entry barrier (certification scheme, tariff rate, agent requirement, payment terms difficulty)

CRITICAL RULES:
- Do NOT invent numbers. If you do not have a verified figure, write "UNVERIFIED - needs Comtrade
  or official customs check".
- For certification requirements, state the scheme NAME (e.g. GSO/SABER) but never fabricate
  article numbers or clause text. Add: "confirm on the official portal".
- For tariffs, write "check current tariff schedule of the destination customs authority".

Output format: a markdown table with columns Country | Language | Demand | Barrier | Total |
One-line reason | Verification needed. Then a short "Top 3 recommendation" section with
3 bullet points each, max 40 words.
```

中文说明：让 AI 当出口市场分析师，但明确禁止它编数字——不确定的一律标 UNVERIFIED。目的是让 AI 先搭骨架、把该核实的地方标出来，你再去查官方源核实。

**提示词 2：目标市场买家画像**

```
Act as a senior sales director for a Chinese tire manufacturer (exporting to {country}).
Based on the top 3 buyer segments below, produce a buyer profile card for EACH segment.

Segments: (1) independent tire importers & distributors, (2) tire dealer chains / retail groups,
(3) fleet & mining OTR tire operators, (4) tire distributors serving garages.

For each segment output EXACTLY these fields:
- Who they are (role in the import chain, who signs, who influences)
- Typical order reality: container type (20GP/40HQ), rough loaded quantity range,
  and 2-3 common specs (e.g. 12.00R20, 315/80R22.5, 7.00R16) — present as ranges/plausible
  examples, NOT as market data
- What they care about most: price / payment terms / certification / warranty claim handling /
  delivery reliability (rank top 3)
- Where they are findable: named PUBLIC sources only (customs data platforms, LinkedIn,
  trade fair exhibitor lists, chamber of commerce directories)
- The ONE question that makes them reply to a cold email
- Red flags that mean "not a real buyer" (e.g. asks for free sample of expensive goods,
  refuses video call, email domain mismatch)

Format as a markdown card per segment. Max 120 words per field. No marketing language.
```

中文说明：这段用来把「一个大市场」拆成四类不同买家。不同买家在意的东西完全不同——经销商看价差，矿山运营商看耐磨和理赔。把它们分开，你的开发信才不用一份模板打天下。

**提示词 3：进入路径体检**

```
You are a trade compliance advisor. I am a Chinese exporter of tires planning to sell into
{country}. List the practical ENTRY CHECKLIST I must complete before the first shipment.

Cover, in order:
1. Product certification schemes that apply (name them; do NOT quote clause numbers)
2. Labeling / marking requirements (language, sidewall, invoice)
3. Customs HS classification note (tire categories: passenger, truck/bus, TBR, OTR, inner tube)
4. Typical importer-of-record arrangements and whether a local agent is expected
5. Payment terms that first-time buyers usually get (T/T, L/C at sight, CAD, O/A risk)
6. 3 things I should confirm with a local customs broker BEFORE sending samples

Rules: every item must end with a "VERIFY AT:" line naming the official authority or portal
to check. If uncertain, say so explicitly. Never invent duty rates or document numbers.
```

中文说明：这段专门用来防「样品发出去才发现认证过不了」。核心是每个条目都要求 AI 写出「去哪核实」，把 AI 当线索生成器，不当答案机。

## 四、检查清单

- [ ] 候选池已列出 10-15 个国家，且每个都有一句话理由说明为什么被放进候选
- [ ] 每个候选国完成三维打分（语言/需求/壁垒），且分数背后有可查证的依据，不是感觉
- [ ] 所有引用的进口额、增速、税率数字都已标注数据来源与时间，UNVERIFIED 项已去官方源核实或已剔除
- [ ] 认证要求只写了体系名称（如 GSO/SABER），并注明「以官方最新公告为准」
- [ ] 最终只保留 1 个首站市场，另外 2 个作为「第 2 站候选」记录在案
- [ ] 三条硬理由已写完，每条都含具体事实（数字、集群名称、渠道特征），没有「潜力很大」这类空话
- [ ] 30 天最小验证目标已写成数字（线索数/发件数/回复数/报价机会数）
- [ ] 目标市场的 3 个公开展会/协会/批发市场名称已记下来，作为后续找客户和调研的入口

## 五、新手常见坑

**坑 1：选「市场最大」的那个**
- 现象：第一轮调研就锁定美国、欧盟、巴西这些大市场，本子上写满了宏观数据。
- 原因：大市场看着有前景，但买家数量多、竞争者扎堆、认证门槛高，新人没有差异化就进不去。
- 正确做法：把「市场规模」换成「我能不能在 30 天内拿到 20 条真线索」当第一筛选条件。宁可市场小一点，但要能立刻开始打电话发信。

**坑 2：三维打分打完就算选完了**
- 现象：表格做完，标了一个第一名，然后就去写开发信了。
- 原因：打分表是纸面判断，没经过任何真实接触。
- 正确做法：打分前 3 名各花一天去实际找 5-10 个潜在买家，看能不能找到、有没有人回应。找不找得到，比分数准。

**坑 3：拿三年前的报告当现状**
- 现象：引用一篇 2021 年的文章说某国需求暴涨，结论直接写进方案。
- 原因：搜索引擎排前面的还是老文章，新数据反而不显眼。
- 正确做法：所有数字标注来源 + 发布时间，超过一年的数据必须重新核实。海关数据、UN Comtrade、目标国官方统计机构是硬数字来源，行业文章只做线索。

**坑 4：认证要求「听说」一下就过**
- 现象：听说中东要认证，就没再往下查，反正还没发货。
- 原因：认证是「发货前必须做完」的事，不做不影响当下出单，所以一直往后拖。
- 正确做法：选完市场的第二天就动手查目标国的认证体系和备案入口，把「需要哪些文件、找谁办、大概周期」写成三行字贴在桌面上。

**坑 5：把「我朋友在那儿」当理由**
- 现象：因为认识一个沙特客户，就决定主攻沙特。
- 原因：朋友能开门，但开不了整扇门，市场容量和竞争状况还是空白。
- 正确做法：朋友这条线单独保留为「暖启动通道」，市场选择仍然按三维打分走。两条腿走路，别把一条腿当全部。

## 六、下一环节

市场定下来了，接下来要在这个市场里挖出具体的人。下一步是**找客户**——把「这个国家有轮胎进口」变成「这 20 个公司名和联系方式」。
