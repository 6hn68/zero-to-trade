# 04·建联客户 Outreach

> 这一步要干的事：正经做一次首次接触，交出一份带日期、带止损线的 3 触达跟进计划，把名单从「打过招呼」推到「有人在回话」。
> 一句话先说透：首触的目标不是成交，是拿到第二句对话。一封有人回的开发信，顶得上二十封进了虚空没人看的。

## 一、为什么这一步最容易翻车

从背调到成交，中间这段最易崩。

崩长一个样：发出去石沉大海，偶尔回句「send more details」，然后人又没了。你开始自我怀疑——产品不行？价格不行？还是我本人不行？先别急着否定自己。

真相有两层，顺序别搞反：

1. **第一层：邮件根本没到。** 新手最常见的失败不是文案差，是域名没配、被判垃圾、第一封还带附件直接进垃圾箱。你在等一个永远不会来的回复，还以为是自己话术不行。这一层不解决，后面怎么改文案都是白费劲（见第 2 步）。
2. **第二层：到了但没跟。** 首封有没有人回，说法差太远——品类、国家、名单质量、发送时段都能让结果天差地别，**没有哪个百分比能直接抄**。别信「回复率 X%」这种话，**自己跑 100 封测一次**（测法见第 6 步）。但有一点铁定：对话大多不是死在第一封，是死在第一封之后没第二、第三封。

海外采购每天收一堆陌生邮件。他大概率不认真看第一封，也不会回第一封。但你第二、第三封还在，而且每次都带点新东西，他会回。

所以这一步你交的不是「发了多少封」，是「**邮件真到了没** + 每封后面跟了没」。

## 二、分步操作

**第 1 步：分级 T0-T3（决定投入多少时间）**

| 级别 | 定义 | 投入 | 首触方式 |
|---|---|---|---|
| **T0** | 决策人已确认、需求明确、有采购时间表 | 最高，一对一定制 | 邮件 + LinkedIn + WhatsApp 三线同天 |
| **T1** | 大概率的采购/老板，需求待确认 | 中，模板 + 个性化开头 | 邮件 + LinkedIn 两线 |
| **T2** | 联系人不够确定，或需求不明 | 低，轻量模板 | 邮件单线 |
| **T3** | 长期养，暂时不谈单 | 极低 | 只进内容/社群，不主动推销 |

**评级桥接：02/03 的 A/B/C → 04 的 T0-T3（本环节唯一映射口径）**

背调阶段给每条线索打了 A/B/C，建联阶段用 T0-T3 决定投入。映射如下，别自己另立一套：

| 背调评级 | 建联分级 | 投入与打法 |
|---|---|---|
| **A** | **T0** | 决策人已确认、需求明确 → 三线同天，最高投入，48h 内首触 |
| **B** | **T1–T2** | 品类匹配但采购证据弱 → 两线（邮件+LinkedIn）或单线（邮件），本周内推进 |
| **C** | **T3** | 任一项 L1 不过或信息残缺 → 只养不推，低频内容，不主动推销 |

> 说明：A 不一定全是 T0、B 不一定全是 T1，还要看「决策人是否确认、需求是否明确」；但 C 一律不进主动建联序列。

T0 是你的命门。名单里 T0 通常只占一小部分（占比取决于你在 [02-find-leads.md](02-find-leads.md) 和 [03-due-diligence.md](03-due-diligence.md) 筛得严不严，没有通用数字），但值得你花最多时间的就是这一档。

**邮箱首触时机**：T0 默认邮件 + LinkedIn + WhatsApp **三线同天**（邮件为主战场）。若目标市场邮箱进垃圾箱风险高，**邮件可顺延至 D1 发出**，但必须纳入同一份跟进计划（同一 `--start` 起算日），不另起炉灶。

**第 2 步：先确认邮件能到（送达率自检）——这步不做，后面全白做**

绝大多数「开发信没人回」的案子，根子不在文案，在邮件压根没进收件箱。下面五条过一遍，哪条没过先修哪条，再谈写文案。

**2.1 用自有域名邮箱，不要用免费邮箱群发**

开发信必须用你自己域名的邮箱（`你的名字@你的公司域名.com`），别拿 `@gmail` / `@163` / `@qq` 这类免费邮箱批量外发。原因就两条：免费邮箱被拿去群发太多次，收件服务器对它们格外不客气；而且 `你的名字@gmail.com` 在采购眼里不像一家公司，像个人。

**2.2 配齐 SPF / DKIM / DMARC 三条 DNS 记录**

这三条是收件方判断「这封信是不是真的从你的域名发出」的依据，在你的域名服务商或企业邮箱后台都能配，一般不需要写代码：

| 记录 | 干什么的 | 没有会怎样 |
|---|---|---|
| **SPF** | 声明哪些服务器有权以你的域名发信 | 收件方无法确认发信方，判垃圾或直接拒收 |
| **DKIM** | 给信件加数字签名，途中被改就失效 | 信件完整性无法验证，评分降低 |
| **DMARC** | 告诉收件方：不通过验证的邮件怎么处理，并给你发报告 | 别人可以冒充你的域名发信（被冒用是外贸里真实的诈骗风险） |

配完别以为就生效了，去验一下：拿公开的 SPF/DKIM 检测工具查你域名记录，或者直接给自己在不同服务商（Gmail、Outlook、本地企业邮）的邮箱各发一封，看邮件原文里的验证结果。

**2.3 新域名要预热，不要第一天上量**

刚注册、刚配好邮箱的域名，在收件方眼里是白纸一张，没有任何信誉记录。稳妥做法：

- 先用它做几周**正常往来邮件**（和同事、和已有客户），让域名有正常的收发行为；
- 开发信从小量起步，**逐日递增**（例如个位数 → 十几封 → 几十封），不要第一天就拉到几百封；
- 观察退信和进箱情况，一旦出现成批进垃圾箱，立刻降量、排查内容；
- 具体「每天几封安全」没有统一标准（取决于域名年龄、收件方、内容），**用你自己的 seed list 试出来**，别照抄别人的数字。

**2.4 首封不带附件、不带链接**

附件是垃圾过滤器的强信号，也是对方公司 IT 网关的常见拦截对象；首封里放多个链接同样拉低评分。项目脚本 `scripts/outreach_gen.py` 生成的首触文案里，正文是纯文本、无任何附件和链接——照这个形态发。

要给的规格表、目录、报价单，**等对方回了再给**（也正好成为你第二封信的「新信息」）。

**2.5 避开 spam 触发面与发送节奏**

- 内容面：全大写单词、连续多个感叹号、`free` / `cheapest` / `100% guaranteed` / `best price` / `urgent` 这类词堆砌、整段红色大字、花哨 HTML 模板、正文用一张图片代替文字。**首触一律用纯文本。**
- 节奏面：不要一分钟群发几百封。错开时段、随机间隔、按对方当地时间的工作日上午发。整点整批、同一秒几百封，本身就是机器行为特征。
- 名单面：**硬退信（地址不存在）必须立刻从名单删除**。退信率一高，域名信誉掉得比什么都快。用 [03-due-diligence.md](03-due-diligence.md) 核过的邮箱，退信会少很多。
- 自测面：准备一个 **seed list**（你自己在 3-5 个不同邮件服务商的测试邮箱），每次改模板先发给自己看进箱还是进垃圾，再对外发。

**第 3 步：三线并进首触（同一客户，同一天做）**

- **邮件线**：正式、可转发给同事、留书面记录。这是主战场。
- **LinkedIn 线**：找到人，加好友或发 InMail。作用是**提高你在他那里的可信度**——他点开你的主页能看到你是谁、做什么的。
- **即时通讯线**（中东、东南亚、非洲非常关键）：WhatsApp、WeChat、LinkedIn 直聊。**发第一条消息前先看他有没有设公司 WhatsApp 商务号**，个人号别乱打。

三线的分工要明确：
- 邮件 = 讲清楚价值、给可回复的理由
- LinkedIn = 建立身份感，让他记住你是谁
- WhatsApp = 制造「有人在跟进」的紧迫感，尤其在 WhatsApp 为主的市场

有个反直觉的点：有些市场里，WhatsApp 先发、邮件后发，反而更好——对方先在轻通道见过你一次，收到邮件时已经不是陌生人了。

**第 4 步：写第一封邮件（结构固定，别每次重想）**

**主题行先定**（决定他开不开，比正文重要）

- 短、具体、像一封工作邮件，不像广告。目标 **40 个字符以内**——`scripts/outreach_gen.py` 的发送前自查清单就是按这条卡的，超了改短。
- 带上他的公司名或一个具体品类，形态参考脚本生成的样子：`TBR 12.00R20 supply — 【示例】海湾轮胎贸易`。
- 不写 `Cooperation` / `Best price` / `Hello` 这种空词，不用全大写，不用感叹号，不写 `Re:` 假装是回复（第一次就被识破，且是欺骗）。
- 主题行只承诺正文里真的有的东西。

**正文五段，130-170 词**

1. **第一句必须是关于他，不是关于你。** 采购看第一句，判断的是「这封信跟我有关系吗」。你开头写「我是 XX 公司的 XX」，等于让他先读一句广告再决定要不要继续。把「为什么是他」提到最前：`I noticed ...（他公司的一件具体的事）`，再用半句带出你是谁。
2. **身份半句**：你是谁、做什么的、供哪个市场。一句话带过，不写成立年份、厂房面积、认证清单。
3. **一个具体的、小的、可验证的价值**：不是「我们是专业制造商」，而是「我们做 12.00R20 和 315/80R22.5 全花纹，包装按中东客户习惯做了英文+阿拉伯语双标」，或者「我们整理了贵国 TBR 进口主力规格清单，可以发你参考」。
4. **一个具体的、容易回答的问题**：能一句话回答。「你们目前 TBR 走哪个渠道？车队还是批发？」比「有兴趣合作吗」好十倍。
5. **一个明确的下一步（一封信只能一个 CTA）**：「二选一」指的是同一个动作的两种形式——「我把规格表发你，还是你直接给型号？」两个选项都指向「我给你发资料」，这还是一个 CTA。而「要不你看报价 / 要不约电话 / 要不加我 WhatsApp」是三个动作，结果等于零个回复。

**签名档该有啥**：名字 + 公司 + 一句职责就行。脚本 `--sender` 默认值就是 `[Your Name] | [Company]` 这种一行式（可用 `--sender "Li | 【示例】远东轮胎 | Export"` 覆盖）。首封别堆一串电话、三个邮箱、官网链接、WhatsApp、公司 slogan 和 banner 图——链接图片拉低垃圾评分，还会把一封 150 词的信变成 400 词的广告。完整联系方式等他回了再给。

**首封三不带**：不带附件、不带链接、不带价格。前两条的原因见第 2 步，报价为什么现在不能给见 [05-negotiation.md](05-negotiation.md) 与 [06-quote.md](06-quote.md)。不写公司宣传册。

> **跟脚本一处已知的冲突（照下面处理）**：`scripts/outreach_gen.py` 的 T0 / T1 模板里带 `price list`（价格单）和 FOB/CIF 条款，但同一份脚本的自查清单又写「全文有没有价格？没有 = 正确」——脚本自己打架了。**本项目以「首封不报价」为准**：脚本生成草稿后，手动删掉价格单那句，换成规格或配柜量。这冲突已记下，后续会修脚本。

**第 5 步：多渠道第一句话（每个渠道的口径都不一样）**

邮件之外还有四个入口。它们的**第一句话不是邮件的缩写版**，各有各的规矩。

**LinkedIn 连接请求（note 有字符上限，写 2 句就够）**

```
Hi {Name} — I supply {product} to buyers in {country}. Saw you handle {他的品类/品牌}.
Would like to connect and follow what you're doing there.

中文对照：{Name} 你好，我给 {country} 的买家供 {product}，看到贵司在做 {品类/品牌}。想加个好友，跟进一下你们那边的动向。
```
要点：连接请求里**不要推销**。你的目的只是让他通过；通过之后才有资格发消息。对方资料里没东西可引用时，宁可不发。

**LinkedIn 首条消息（他通过之后再发，≤ 50 词）**

```
Thanks for connecting, {Name}. Quick context: we make {product} and currently ship to
{country}. Not pitching — I'd like to know whether you source {product} from Asia this year.
One word is enough.

中文对照：谢谢通过。简单说下背景：我们做 {product}，目前在供 {country}。不是推销——想确认贵司今年是否从亚洲采购 {product}，回一个词就行。
```

**WhatsApp 首条（≤ 25 词，手机上看，且对方可能在忙）**

```
Hi {Name}, {Your Name} from {Company} ({product}). Saw you import from Asia —
OK if I send the size list? One line is enough.

中文对照：{Name} 你好，我是 {Company} 的 {Your Name}，做 {product}。看到贵司从亚洲进货——发份规格表给你行吗？回一句就行。
```
要点：发之前先确认他用的是**公司商务号**还是私人号（个人号别乱打）；不连发第二条；不发语音；不发链接；不发在对方深夜；他回了「thanks」就停下来，把有实质内容的那句挪到下一轮。

**电话（冷 call 的前 20 秒）**

```
Hello, may I speak to {Name}?
… Hi {Name}, {Your Name} calling from {Company}. We supply {product} to {country}.
I'm calling because {一句为什么是他}.
Is now a bad time for two minutes?

中文对照：你好，请找 {Name}。…… {Name} 你好，我是 {Company} 的 {Your Name}，我们给 {country} 供 {product}。打这个电话是因为 {为什么是他}。现在方便讲两分钟吗？
```
要点：先确认找对了人，再自报家门，再给理由，最后**先问方不方便**。对方说不方便就约时间——这是冷 call 唯一的礼貌，也是你唯一能拿到第二次机会的方式。被明确拒绝一次，当天不要再打。

**官网表单（Contact form）——优先级最低**

表单通常进 `info@`，由市场部或没人管，回复率显著低于找对人。只在**完全找不到任何联系人**时才用：

```
Subject: For the purchasing team — {product} supply enquiry

Please forward this to whoever handles {product} sourcing.
We manufacture {product} and supply {country}. {一句为什么是他}.
If you already have a supplier for this, a one-word reply is enough and I'll stop here.

中文对照：请转给负责 {product} 采购的同事。我们生产 {product} 并供应 {country}。{为什么是他}。如已有供应商，回一个词即可，我不再打扰。
```
要点：第一句就说清你要找**哪个部门/哪个人**（否则这封信会在 info@ 里死掉）；字数压到表单上限内；不要贴大段公司介绍。

**四渠道的同一条铁律**：四个渠道说的是同一件事、同一个人设、同一个诉求，但**文案不能是同一段**。一个采购同日在四个通道看到四段一模一样的话，只会得出一个结论——群发。一致性校验见提示词 3。

**第 6 步：做 A/B 测试（分名单测，不是给同一个人发三遍）**

同一批线索、不同切入角度各写一版：
- 版本 A：规格/产品角度（强调你能做什么型号）
- 版本 B：成本角度（强调柜型效率、混装，不提底价）
- 版本 C：市场角度（强调你看到的他所在市场的变化）

**怎么测才有效：**

- **按名单分组，不按同一个人轮发。** 把同一 tier 的线索随机分成两组，一组 A 一组 B，其余条件（发送时段、签名、跟进节奏）完全一致。**不要给同一个客户连发三个不同角度的版本**——他三封都收到，一眼看穿是群发，而且三封信互相打架，可信度归零。变体是**名单维度**的（这一组用 A，那一组用 B），不是**同一人维度**的。
- **一次只改一个变量。** 只改「为什么是他」那一句，或只改给的价值点，其他全不动。同时改两处，你永远不知道是哪个起了作用。
- **样本要够。** 每版各十几封的结果基本是噪音。**目标每版各 50-100 封**再下结论；没到这个量之前，不要因为「A 今天回了两个」就宣布 A 胜出。
- **只测一个指标：有没有收到回复。** 这一环不测点击、不测报价、不测成交。
- **自测方法（替代任何现成百分比）**：发 100 封 → 记下回了几个、回的是哪一版、哪一版在第几次触达时回的 → 换一个变量再跑 100 封 → 两轮对比。这就是你自己的基准，也只有这个数字对你有效。

**第 7 步：排 3 触达跟进计划（写进日历，不是写进脑子）**

项目脚本 `scripts/followup_plan.py` 的真实节奏是：**每个 tier 各 3 次触达，之后停手**。没有 D7/D14/D30 一路排下去的无限序列——`T2` 的 D14 是「归档」，是第 3 次触达，不是第四次跟进。文档口径以脚本为准：

| 层级 | D0 首触 | 第二次 | 第三次 | 停手规则（脚本口径） |
|---|---|---|---|---|
| **T0** <br>D0/D2/D5 | 首触邮件：直接 + 一句只对他成立的话 | **D2** 换渠道（同一诉求转到 WhatsApp / 领英，主题不变），带配柜量参考 | **D5** 给台阶「这条路先放着，你随时找我」，带一条行业信息 | D0 明确拒绝 → 立刻停手；第 3 次触达后仍无回应（含已读不回）→ **无条件停手**，进长名单，季度扫一次 |
| **T1** <br>D0/D3/D6 | 首触邮件：轻、具体、给一个容易回应的理由，含一个具体数字 | **D3** 换渠道（领英 / WhatsApp，不重复全文），带配柜量参考 | **D6** 问「现在不是时候？」这类二选一 | 同上；第 3 次后无回应 → 无条件停手，进长名单，季度扫一次（本级停手后降进低频池） |
| **T2** <br>D0/D7/D14 | 确认信息：只问是否还在采购，不求回复 | **D7** 仅在有行情时发（行情 / 涨价 / 认证通知）；**无行情可发就跳过这一步**，不要为了凑次数而发 | **D14** 归档 | 归档，移出主动触达名单 |
| **T3** | 不排触达 | — | — | 本级止损线就是 0 次：信息不足，先补信息 |

**T3 不排触达**（脚本 `--tier T3` 支持，但输出是「不排触达」）。三条层级线的跨度本来就不一样，脚本注释说得很清楚：**不是都叫「7 天」**——T0/T1 在首周内跑完，T2 跨到 D14。

生成命令（`--start` 必填，填你**实际首发当天**的日期 `YYYY-MM-DD`，脚本不接受本机日期，为的是结果可复现）：

```bash
# 表格版（默认 gcc 市场规则，会提示周末/节假日）
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv my_leads.csv

# 把落在周末的触达自动顺延到下一个工作日
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --avoid-weekend

# 导出进表格 / CRM
python scripts/followup_plan.py --tier T1 --start 2026-10-08 --csv my_leads.csv --format csv --out plan.csv
python scripts/followup_plan.py --tier T2 --start 2026-10-08 --market gcc --avoid-weekend --format json --out plan.json
```

脚本另外三条内建约束，写文档不如直接照它做：
- **最小间隔**：相邻两次触达至少间隔 `MIN_GAP_DAYS` 个自然日，别一天一封连着轰。
- **不许群发同文案**：`ANTI_SPAM` 明确写着「同一批线索绝不用同一份文案群发」——同文案群发会被判垃圾邮件，**域名进黑名单后受影响的不是这一家客户，是你所有客户**。
- **时区与节假日**：发送按对方当地时间上午 9-11 点，不是你的上午 9 点；海湾客户周五是主麻日基本不看邮件，沙特周末周五+周六、阿联酋已改周六+周日；斋月/开斋节/宰牲节、8 月欧洲假期、12 月圣诞、中国春节与国庆，回复会骤降或停摆，**不要在那些时候做「最后一次」催单**。具体节假日按当年日历自行核对（脚本不联网，只给提示）。

记牢一点：每次跟进必须带新信息，不能只来一句「跟进一下」「Any update?」。跟进的价值就在那一句新东西里。脚本每步都列了「必须带」啥，照填。

> 注：脚本 T0 的 D0 标着「规格与报价区间（不含底价）」。本项目主张**首封一个价格数字都不出现**，所以把这一项换成「规格 + 配柜量」；「报价区间」留到 05 聊完之后再用。

**第 8 步：0 回复时的动作序列（按顺序做，不靠意志力硬撑）**

「没回」不是一种情绪，是一个需要处理的流程状态。三次触达都无回应后，按这个顺序执行：

1. **先排除技术问题（这是第一步，不是最后一步）**：用你自己的 seed list 检查有没有进垃圾箱；检查有没有硬退信（地址不存在——有就**立刻从名单删掉**，退信率一高域名信誉就没了）。邮件没到 = 不是文案问题，改文案无效。
2. **换人**：同一家公司换另一个入口——采购之外还有运营、物流、销售负责人，或者官网 `info@` / 总台。找到人再走一轮 3 触达，但「为什么是他」必须重写。
3. **换渠道**：邮件三次没回，就改用电话或 WhatsApp 问一句「这块采购现在是谁在跟？」。这一句的目的不是卖货，是问出正确的人名。
4. **换角度**：前三封都讲规格，下一轮换市场角度（行情 / 认证 / 交期风险）。换的是切入角度，不是措辞。
5. **降级，不要删除**：T0 → T1/T2 节奏，进长名单，按季度扫一次。换季、涨价、新认证、展会前后，都是再触的正当理由。进长名单不等于永远不联系，等于不再按周投入。
6. **停手线**：同一个人在同一个角度上，三次无回应（含已读不回）就该停。继续发不会提高回复概率，只会消耗域名信誉和你在这一市场仅有的几次露脸机会。脚本把这条写成了硬止损线（`MAX_TOUCHES`），原文理由：「继续发只会拉低域名信誉，而且对方已经用行为告诉你答案了」。D0 就被明确拒绝的，当场停手，不用等第三次。
7. **回头改上游**：如果一个市场**整批**线索都 0 回复，问题大概率不在 04，在 02（名单不准）或 03（背调没做实）。回 [02-find-leads.md](02-find-leads.md) 和 [03-due-diligence.md](03-due-diligence.md) 重来，不要在 04 里死磕文案。

**第 9 步：记录响应并复盘**

每天记录：发了什么、走哪个渠道、哪个变体、对方回没回、回的是啥内容、停留在哪一步。**每周只做一次结论**，且样本累积到每版 50-100 封才下——把胜出的那个固定下来，把输的角度记进 notes，别下周又凭感觉换回去。

## 三、判断标准

本环节「做好了」的硬标准：

- **送达率已自检**：用的是自有域名邮箱，SPF / DKIM / DMARC 已配置并验证通过，首封无附件、无链接、无价格，seed list 自测能进箱。
- 所有 A 类已按映射表转为 **T0** 并三线同天首触（或按市场风险 D1 补发邮箱，仍属同一计划）。
- 每封首触邮件：**首句是关于对方**（不是自我介绍），含一句「为什么是他」并引用背调核实信息，**全篇只有一个 CTA**，主题行 40 字符内且带公司名/品类，**未报价、未发报价单、未带附件**。
- 多渠道首触各用了该渠道的第一句话模板（LinkedIn ≤ 50 词、WhatsApp ≤ 25 词），三线说法一致但文案不雷同。
- A/B 是**按名单分组**测的，一次只改一个变量，目标每版 50-100 封；结论基于自己的 100 封实测，不是网传百分比。
- 跟进计划已进日历，且与 `scripts/followup_plan.py` 的 3 触达节奏一致（T0 = D0/D2/D5，T1 = D0/D3/D6，T2 = D0/D7/D14），每次跟进带新信息点。
- 三次无回应已按第 8 步序列处理（查送达 → 换人 → 换渠道 → 换角度 → 降级），不是原角度继续硬发。
- 响应状态已记录（含渠道 + 变体编号 + 第几次触达），可周度复盘。

## 四、AI 提示词

**提示词 1：首封开发信生成器**

```
You are an export sales writer for a Chinese tire manufacturer. Write a cold outreach email.

MY INPUT:
- Target country: {country}
- Buyer: {name}, {role}, {company}
- What I know about them: {paste verified intel from due diligence, e.g. "carries
  Goodyear/Bridgestone, distributes to garages in Riyadh, importing TBR regularly"}
- Our products: {e.g. TBR 12.00R20, 315/80R22.5, 7.00R16; Tread pattern options;
  OEM and export packaging; MOQ}
- Verified selling points: {only things I can prove}

RULES — non-negotiable:
1. Language: English, 130-170 words, plain text, no Chinglish, no translated-from-Chinese phrasing.
2. SUBJECT LINE: under 40 characters, concrete, must contain their company name or a specific
   product/category. No "Cooperation", no "Best price", no ALL CAPS, no exclamation marks,
   no fake "Re:".
3. STRUCTURE (5 parts, label nothing):
   (a) FIRST SENTENCE MUST BE ABOUT THEM — one specific fact about their business, from MY INPUT.
       Never open with who I am. Open with what I noticed about them.
   (b) half a sentence of who I am and what we make (no founding year, no factory size,
       no certificate list)
   (c) ONE concrete small value offer tied to our products (NOT "high quality", NOT "best price")
   (d) ONE easy-to-answer question they can reply to in a few words
   (e) ONE CTA only. A "this or that" choice is allowed only if both options lead to the SAME
       action. Never ask for a call, a quote and a WhatsApp add in the same email.
4. DO NOT include prices, quote sheets, MOQ numbers, any attachment, or any link.
5. DO NOT write: "we are a leading manufacturer", "factory direct", "best quality",
   "looking forward to your reply", "our company was established in...",
   no spam-trigger stacking (free / urgent / 100% guaranteed / cheapest).
6. End with a ONE-LINE signature: name | company | one role phrase. No phone list, no website
   link, no banner, no slogan.
7. No emojis, no more than one exclamation mark.

OUTPUT:
- The subject line
- The email body
- Then a 3-line note: the ONE variable I should test next, the risk of this angle, and which
  spam-trigger words (if any) I should re-read for.

Then write ONE follow-up version (Day 4) that adds a NEW piece of information and does NOT
say "just following up" or "any update".
```

中文说明：这套提示词最值钱的是禁令清单和第 3(a) 条。它把 AI 从「生成一封很客气的废话」拽回具体信息上，还逼着第一句写对方而不是写自己——这一句就是回不回的分水岭。第 2 条把主题行 40 字符上限和「必须带公司名/品类」写成硬规则，跟 `scripts/outreach_gen.py` 的自查清单一个口径。

**提示词 2：跟进消息生成器（防「只是催」）**

```
You are writing follow-up messages for a B2B tire export sale. My previous email to
{buyer} sent on {date} got {reply status: no reply / polite brush-off / asked for more info}.

RULES:
1. Each follow-up MUST contain at least one piece of genuinely NEW information the earlier
   messages did not contain. Possible new-value types: a specific size list, a container load
   plan, a packing-mark note, a market observation, an answer to an objection, a specific question
   they have not been asked before.
2. Never write: "just following up", "any update", "bumping this up", "did you see my email",
   "waiting for your reply", "please let me know".
3. Never apologize for following up.
4. Never repeat the same pitch. Each message should feel like a different person with something
   to say, or the same person who had something new to add.
5. Keep it under 90 words. English.
6. Match the politeness level of their market: GCC = warm and conversational with light
   honorifics; Europe = concise and formal; Latin America = warmer and more relational.
7. If the previous message asked for something and they went silent, the follow-up should
   lower the ask (from "quote for 3 sizes" to "shall I just send the spec sheet first?").

OUTPUT: the message body, plus one line stating which new-value type I used and why it's
relevant to a tire buyer.

Then write a Day-7 "clear ask" message that makes responding trivially easy (yes/no question).
```

中文说明：跟进信最大的失败模式是「换个说法重复第一封」。这个提示词把「必须含新信息」写成硬规则，还给了五种新信息类型当菜单，你只要挑一个塞进去。

**提示词 3：三线内容一致性检查**

```
You are an outreach strategist. Below are three messages I plan to send to the SAME buyer on the
SAME day: an email, a LinkedIn InMail, and a WhatsApp first message.

Check and fix. Output each channel revised, with a one-line reason for each change.

REQUIREMENTS:
- All three must say the same thing about WHO I AM and WHAT I WANT. A buyer who gets three
  different pitches in one day will distrust at least two of them.
- But they must NOT be identical texts: WhatsApp max 25 words, LinkedIn max 50 words,
  email can be longer. Same message, different shape — never copy-paste the same paragraph.
- Each message carries exactly ONE CTA, and it is the same CTA across all three channels.
- Channel behaviour: WhatsApp = assume they will read it on a phone while busy; be warm,
  extremely short, one clear ask. LinkedIn = short, professional, mention why I'm contacting
  them through this channel specifically (their profile/company). Email = the full substance.
- No channel may promise something the others don't, and none may mention a price the others hide.
- No attachments and no links in any first-touch message (deliverability).
- Do not use "Dear Sir/Madam" in WhatsApp. Do not use all-caps. Do not exceed word limits.

Then flag any place where the three channels could contradict each other.
```

中文说明：三线同天发最常见的事故，一是三个版本说法不一致，二是三个版本**一字不差**（客户一看就知道是群发模板）。这段做一致性校验、字数压缩，并把「每个渠道只有一个 CTA、且三个渠道是同一个 CTA」写成硬规则；还把「不同市场的礼貌等级」参数化（GCC 热络、欧洲简洁、拉美关系导向）。

## 五、检查清单

- [ ] **送达率**：自有域名邮箱；SPF / DKIM / DMARC 已配且验证通过；seed list 自测能进箱；首封纯文本，无附件、无链接
- [ ] 所有 A 类客户已标为 T0，明确了决策人和需求点
- [ ] 每封首触邮件首句是关于对方，且「为什么是他」引用了背调阶段核实的真实信息（换成同行还成立就重写）
- [ ] 全篇只有一个 CTA（二选一可以，三个动作不行）；主题行 40 字符内、带公司名或品类、非空词
- [ ] 全程未发送价格、报价单、MOQ 数字；签名档只有一行，没有堆电话/链接/banner
- [ ] A/B 按名单分组，一次只改一个变量，每版目标 50-100 封
- [ ] T0 客户三线同天完成（或按市场风险邮件顺延 D1 但仍属同一跟进计划），且三线说法一致、文案不雷同
- [ ] 跟进计划已进日历，与脚本 3 触达节奏一致，每条跟进都预置了「新信息点」，不是空催
- [ ] 发送前确认过：邮件无错别字、无 spam 触发词、纯文本、无附件
- [ ] 发送节奏已做节流（错开时段、逐日增量），不是一分钟几百封；硬退信已从名单删除
- [ ] 发送时段按**对方当地时间上午 9-11 点**，不是你的上午 9 点；海湾客户避开周五（主麻日），沙特周末周五+周六、阿联酋周六+周日（或用 `--avoid-weekend` / `--market` 让脚本替你顺延）
- [ ] 本轮不落在斋月、开斋节、宰牲节、8 月欧洲假期、12 月圣诞、春节国庆这些回复停摆期；**不在这类时段做「最后一次」催单**
- [ ] 每条线索的响应状态已记录，含渠道 + 变体编号 + 第几次触达，便于周度复盘
- [ ] 三次无回应的线索已走第 8 步序列（查送达 → 换人 → 换渠道 → 换角度 → 降级），不是继续硬发

## 六、新手最容易踩的坑

**坑 1：第一封信就报价**
- 啥样：怕客户不来，第一封直接把价格表塞进去。
- 为啥：新手把「给点东西」当成礼貌。
- 咋办：第一封的价值不是价格，是「值得回你一句的理由」。报价是聊完单之后的事，原因见 05、06。提前报价，谈判空间当场归零。

**坑 2：开发信写成公司宣传册**
- 啥样：成立年份、厂房面积、产线数量、拿过的认证，全写。
- 为啥：把自己的介绍当成对方的关切。
- 咋办：把「我多大」换成「你能拿到啥」。采购不关心你几条产线，只关心他要的型号能不能做、能不能按时到、价对不对。

**坑 3：跟进只会说「Any update?」**
- 啥样：D2、D4、D7 各发一句「Gentle reminder」，然后被拉黑。
- 为啥：把跟进当提醒，不是当提供新价值。
- 咋办：每次跟进带个「新东西」——一份规格表、一个柜型方案、一个你看到的市场变化。那次没新东西，就别发。

**坑 4：只发邮件不碰即时通讯**
- 啥样：邮件发了，等三天没动静就当他没兴趣。
- 为啥：没搞清市场习惯。中东、南亚、非洲大量决策靠 WhatsApp 完成，邮件只是留档。
- 咋办：目标市场靠即时通讯做决策，首触当天就发一条极短的 WA。不回也别连发，等 D7 再碰。

**坑 5：一天发 200 封**
- 啥样：拿工具批量发，盯着发送量看。
- 为啥：把发送量当 KPI，而且新域名第一天就上量。
- 咋办：先小批量验证（比如先发 20-30 封），确认能进箱、有回复，再**逐日递增**。新域名第一天群发几百封，是最快毁掉域名的方式。回得好不好，自己跑 100 封统计一次（发 100 封、记回几个、哪版回的），拿这个当基准；别把网上流传的百分比当真，也别样本不够就下结论。继续堆量不解决问题，只会先把域名信誉烧光。

**坑 6：群发同一封信只换公司名**
- 啥样：模板里把 {company name} 一换，发出去 300 封。
- 为啥：以为个性化就是改个公司名。
- 咋办：真个性化是第二段那句「为什么是他」——他卖啥品牌、主推哪个型号、在哪个城市、官网有啥特点。做不到这点的，宁可只发 A/B 类。

**坑 7：发完就不动了**
- 啥样：首触发完，等十天没回就当这条路走不通。
- 为啥：跟进计划存脑子里，第二天一忙就忘。
- 咋办：跟进任务进日历，每条带时间。但**跟进有上限**：3 次触达后无回应就走第 8 步——换人、换渠道、换角度，最后降级进长名单。同一个人不是唯一入口，也不是个能无限发下去的入口。

**坑 8：第一封就带附件或链接**

- 啥样：为显得专业，首封塞份 PDF 目录、一个官网链接、一张产品图。
- 为啥：把「给点东西」等同于「显得有实力」。
- 咋办：附件和多链接是垃圾过滤器的强信号，也是对方 IT 网关的常见拦截对象，还会让你在出现在他邮箱前先被判死。**首封纯文本，一个附件都不带**。目录、规格表是你第二封信最好的「新信息」，留到那时候再给。

**坑 9：用免费邮箱群发 / 没配 SPF-DKIM-DMARC**

- 啥样：用 `@gmail` / `@163` / `@qq` 批量发开发信，或者用了公司域名但从没配过 DNS，然后抱怨「一封都没人回」。
- 为啥：不知道邮件可能根本没到，以为发出去就是到了。
- 咋办：见第 2 步。先确认 SPF / DKIM / DMARC 三条都在并验证通过，用 seed list 自测进箱，再谈文案。**没解决送达率就改文案，是在给一个没人看得到的东西做优化。**

**坑 10：一封信里塞三个请求**

- 啥样：结尾写「要不发报价？要不约电话？要不加我 WhatsApp？」
- 为啥：怕错过，把所有可能性列上，把选择权丢给对方。
- 咋办：列三个请求等于让对方做三个决定，结果通常一个都不做。**一封信一个 CTA**。可以「二选一」，但两个选项必须指向同一个动作（发规格表 / 给型号后我报价），不是两个不同动作。

**坑 11：开头先介绍自己**

- 啥样：第一句「I am XX from XX company, we are a professional manufacturer of...」。
- 为啥：以为礼貌得先自报家门。
- 咋办：采购看第一句判断的是「跟我有关吗」。先写关于他的一句具体事实（你看到他做了啥），半句带出你是谁。**第一句讲自己，等于把最值钱的一句浪费在自己身上。**

## 七、可复制模板（照填，不依赖 AI）

**模板 A：首封开发信（中英对照，照填即可）**

规则回顾：首句关于他 · 一个 CTA · 纯文本 · 不带附件/链接/价格 · 签名一行。

```
Subject: {品类/规格} supply — {他的公司名}          ← 40 字符以内
主题：{品类/规格} 供应 — {他的公司名}

Hi {联系人名},

I noticed {为什么是他：他公司的一件具体事实，一句}. I'm {你的名字} at {公司名} —
we make {品类} and ship to {他的国家} regularly.

One thing that may be useful to you: {一个具体可验证的点，如规格清单 / 双语包装 / 配柜量}.

{一个一句话能回答的问题，如 "Are you supplying fleets or wholesale on this?"}

Want me to send the size list, or would you rather give me the sizes you need?

Best regards,
{你的名字} | {公司名} | {一句职责，如 Export}

—— 中文对照（仅供你核对，客户不收）——

{联系人名} 你好，

我注意到 {为什么是他}。我是 {公司名} 的 {你的名字}，我们做 {品类}，长期发 {他的国家}。

有一件事可能对你有用：{具体可验证的点}。

{一句话能回的问题，如「你们这块是供车队还是走批发？」}

我把规格表发你，还是你直接给需要的型号？

顺祝商祺，
{你的名字} | {公司名} | 外贸
```

**填表时的三个硬检查**（脚本 `outreach_gen.py` 每份草稿末尾也带这三条）：
1. 「为什么是他」换成同行还成立吗？成立 = 重写。
2. 全文有没有出现价格数字？有 = 删掉（脚本 T0/T1 草稿自带 price list 句，务必手动删）。
3. 主题行超 40 字符了吗？超了 = 改短。

生成草稿：

```bash
python scripts/outreach_gen.py my_leads.csv --tier T0                 # 中英对照
python scripts/outreach_gen.py my_leads.csv --tier T1 --lang en --out drafts.md   # 只要英文
```

**模板 B：LinkedIn 连接请求 / 首条消息**

```
连接请求（note，2 句）:
Hi {Name} — I supply {品类} to buyers in {国家}. Saw you handle {他的品类/品牌}.
Would like to connect and follow what you're doing there.
中文：{Name} 你好，我给 {国家} 供 {品类}，看到贵司在做 {品类/品牌}，想加个好友跟进一下。

通过后的首条（≤ 50 词）:
Thanks for connecting, {Name}. Quick context: we make {品类} and ship to {国家}.
Not pitching — are you sourcing {品类} from Asia this year? One word is enough.
中文：谢谢通过。我们做 {品类}，发 {国家}。不是推销——贵司今年还从亚洲采购 {品类} 吗？回一个词就行。
```

**模板 C：WhatsApp 首条（≤ 25 词）**

```
Hi {Name}, {你的名字} from {公司名} ({品类}). Saw you import from Asia —
OK if I send the size list? One line is enough.
中文：{Name} 你好，我是 {公司名} 的 {你的名字}，做 {品类}。看到贵司从亚洲进货——发份规格表行吗？回一句就行。
```

**模板 D：电话开场（20 秒）**

```
Hello, may I speak to {Name}? … Hi {Name}, {你的名字} from {公司名}. We supply {品类} to {国家}.
I'm calling because {为什么是他}. Is now a bad time for two minutes?
中文：你好，请找 {Name}。…… {Name} 你好，我是 {公司名} 的 {你的名字}，我们给 {国家} 供 {品类}。
打电话是因为 {为什么是他}。现在方便讲两分钟吗？
```

**模板 E：官网表单（找不到联系人时才用）**

```
Subject: For the purchasing team — {品类} supply enquiry
Please forward this to whoever handles {品类} sourcing. We manufacture {品类} and supply {国家}.
{为什么是他}. If you already have a supplier, a one-word reply is enough and I'll stop here.
中文：请转给负责 {品类} 采购的同事。我们生产 {品类} 并供应 {国家}。{为什么是他}。
如已有供应商，回一个词即可，我不再打扰。
```

> 所有模板里的公司名一律带 **【示例】** 前缀，邮箱域名一律用 **sample.example**，电话一律用占位符（如 `+000-0000-0000`）。真实客户数据只进你本地的 CSV，不进仓库。

## 八、下一环节

有人回话了——问价的、要样品的都算——对话打开了。下一步是**聊单** [05-negotiation.md](05-negotiation.md)：报价之前，先把需求问清楚。

如果三次触达后仍然 0 回复，先回到第 8 步走动作序列；整批线索都没回，问题在 [02-find-leads.md](02-find-leads.md) 或 [03-due-diligence.md](03-due-diligence.md)，不在这一篇。
