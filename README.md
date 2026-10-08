# zero-to-trade

**给外贸零基础新手的开源操作系统：7 个环节的完整工作流 + 一条能跑的 AI 工具链。**

> 🔥 **你发 200 封开发信 0 回复，不是英语差，是顺序错了。** 这个项目把"从选市场到收钱"拆成 7 步可执行清单 + 3 个能跑的脚本，每步告诉你今天下午打开哪个网站、填什么、看到什么算过关。

> 核心理念一句话：**AI 干重活，人做判断。**

**An open-source operating system for new foreign-trade sellers: a 7-stage workflow plus a working AI toolchain.**
> Core idea in one line: **AI does the heavy lifting, you make the calls.**

---

## 这个项目解决什么问题

你搜「外贸怎么开始」，会得到一堆东西：某大神的成功学、几百篇 SEO 软文、付费课试听片段、YouTube 标题党。看完你觉得懂了，第二天打开海关数据网站，还是不知道第一行该填什么。

问题不在信息不够，在于**信息是碎的、按成功者视角剪的、且没有下一步**。

传统教程的套路是：告诉你「要做客户背调」，然后告诉你「背调很重要」，然后没了。你依然不知道背调哪些字段、查什么网站、红旗长什么样、查到什么程度算够。

这个项目的做法是**把一件事拆到底，直到它变成一个动作**：

| 传统教程 | 本项目 |
|---|---|
| 「要做客户背调」 | L1 筛查查 3 项（官网存在性、成立年份、社媒是否活跃），任一项不过直接淘汰 |
| 「要重视客户质量」 | 8 条线索自动分成 T0/T1/T2/T3，每级写清下一步该干什么、该花多少时间 |
| 「记得跟进」 | 第 1/3/5/7 天各一次触达，每次话术不同，第 7 天给一个明确的收尾或推进动作 |
| 「AI 会改变外贸」 | 3 个 stdlib-only Python 脚本，`python scripts/lead_score.py examples/leads_example.csv` 30 秒出分级结果 |

差别不在信息量，在于**颗粒度**。这个项目的每一条结论都要能落到「今天下午打开哪个网站、填什么、看到什么算过关」。

它不是成功学，是一份**可执行清单 + 一堆能跑的脚本**。

---

## 7 环节总览

从「选国家」到「交单收钱」，一条完整链路。每环节都有文档，产出物都是可以直接用的东西。

| 环节 | 做什么 | 产出 |
|---|---|---|
| **01 选市场** | 语言-需求-壁垒三维评估 | 1 个首站市场 + 三条理由 |
| **02 找客户** | 海关数据 / 社媒 / 搜索 / 展会四路 | 每天 ≥20 条真线索 |
| **03 背调客户** | L1 筛查 / L2 标准 / L3 深度 | A/B/C 评级，过滤骗子 |
| **04 建联客户** | T0-T3 分级，三线并进首触 | 分级名单 + 7 天跟进计划 |
| **05 聊单** | 小要求先行，报价永远最后 | 规格 / 数量 / 目的港三件套 |
| **06 报价谈判** | 报价纪律，让步换条件 | 报价单 + 让步阶梯 + 话术 |
| **07 订单交付** | 合同 / 生产 / 验货 / 单证 / 收款 / 物流 | 交付闭环 + 复购计划 |

每环节文档在 `docs/`，统一采用六段结构（见 [CONTRIBUTING.md](CONTRIBUTING.md#文档规范)）：**这个环节在干什么 → 怎么做（分步） → 判断标准 → 常见坑 → 可复制模板 → 本环节的 AI 提示词**。

**完全零基础？** 先读 [`docs/00-getting-started.md`](docs/00-getting-started.md) —— 不懂 git、不懂 Python 也能在 10 分钟内跑起来。

---

## 30 秒快速上手

三个脚本，零第三方依赖，只要 Python 3.8+。

```bash
# 1. 线索自动分级：输入 CSV，输出 T0-T3 排序 + 每级下一步动作
python scripts/lead_score.py examples/leads_example.csv

# 2. 按分级生成中英对照建联文案（英文发送，中文供你审批）
python scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. 生成 7 天 3 触达跟进计划表（带具体日期）
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv
```

> 💡 不想装 Python？直接用浏览器打开 [`index.html`](index.html) 在线体验分级 Demo（推到 GitHub 后由 Pages 自动托管）。

### 第 1 条命令的真实输出

```
==========================================================================
  线索分级结果  共 10 条
==========================================================================
分级   公司                         国家                得分  下一步
--------------------------------------------------------------------------
T0   Al-Drees Tyre Co           Saudi Arabia      95  今天就发首触消息，别等
T0   Delta Tyre Group           Saudi Arabia      92  今天就发首触消息，别等
T1   Blue Ocean Trading         Oman              77  排进本周，今天准备文案
T1   East Star Auto             Saudi Arabia      71  排进本周，今天准备文案
T1   Nile Trade Group           Egypt              67  排进本周，今天准备文案
T1   Gulf Rim Trading LLC       UAE                65  排进本周，今天准备文案
T1   Al-Hoda Tires              Saudi Arabia      64  排进本周，今天准备文案
T2   Pioneer Motors Nigeria  Nigeria            46  进 B 池，每天固定时段扫一遍
T3   Levant Auto Supplies        Lebanon             20  信息不足，先补联系方式/需求再打
T3   Riyadh Auto Parts          Saudi Arabia      10  信息不足，先补联系方式/需求再打
--------------------------------------------------------------------------
汇总: T0:2 / T1:5 / T2:1 / T3:2

先回谁: Al-Drees Tyre Co、Delta Tyre Group
```

### CSV 字段

`examples/leads_example.csv` 是可直接跑的示例，表头：

```
company,country,product,source,email,phone,years,contact,note
```

只有 `company` 是必需的，其余缺省也能跑（缺项按最低分算）。`source` 建议填
`referral` / `trade_show` / `customs` / `linkedin` / `search` 之一，这项对分数影响最大。

三个脚本都支持 `--help`。`lead_score.py` 另有 `--format json` 和 `--country/--product` 过滤，
方便你接进自己的表格工具。

脚本只做**机械可判定的部分**（有没有邮箱、来源可不可信、T0 阈值）。判断「值不值得投入时间」
的部分留给文档和人——这是这个项目的基本分工。

---

## 目录结构

```
zero-to-trade/
├── README.md              # 你正在读的中文主门面
├── README_EN.md           # 完整英文版
├── index.html             # 零安装浏览器 Demo（GitHub Pages 自动托管）
├── MANIFESTO.md           # 匿名不卖课：品牌主张
├── GITHUB_LAUNCH.md       # 上线 + 推广执行清单（Topics/About/PR/Show HN）
├── CONTRIBUTING.md        # 贡献方式 + 文档/代码规范
├── LICENSE                # MIT
├── docs/                  # 7 个环节的详细文档（一个环节一个文件）
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   └── 07-order-delivery.md
├── scripts/               # 可直接跑的 Python 脚本（stdlib-only）
│   ├── lead_score.py      # 线索 T0-T3 自动分级
│   ├── outreach_gen.py    # 按分级生成中英对照建联消息
│   ├── followup_plan.py   # 7 天 3 触达跟进计划表
│   └── quote_engine.py    # v0.2 报价引擎(alpha)：FOB/CIF 区间 + 三档让步阶梯
├── examples/
│   └── leads_example.csv  # 示例数据，可直接跑
├── prompts/
│   └── AI_PROMPTS.md      # 27 条可直接粘贴的英文提示词，按环节分组
└── assets/                # 图片、截图、图表
```

---

## 为什么给 AI 工具，而不是只给一套方法论

很多「AI 提效」项目做的事是把方法论塞进 prompt。这个项目反过来：**先定纪律，再给工具**。

原因很简单——**会写 prompt 不等于会做外贸**。这个项目假设使用者缺的不是话术，缺的是判断框架。所以：

- **纪律才是价值。** T0 就该今天发邮件，T3 就该扔进池子三个月不碰。让步必须换条件，不换条件的让步叫送钱。这些是规则，不是 AI 能替你决定的。
- **AI 负责重活。** 8 条线索的批量初筛、50 家客户的三层背调草稿、7 天跟进话术的变体生成——这些耗时但不需要判断力的活，交给 AI。
- **脚本负责可重复。** 分级标准如果每次凭感觉判断，就等于没有标准。所以先把它写成一个 200 行以内、只依赖标准库的脚本，让任何人跑出的结果都一样。

分工线：**能被写成 if/else 的，写进脚本；需要权衡的，写进文档；需要对外表达的，写进 prompts。**

另外，脚本刻意不依赖 pandas / openai SDK —— 装环境这件事本身就会劝退零基础用户，而一个外贸新手卡在 `pip install` 上的时间比他花在找客户上的时间还多。

---

## 路线图

| 版本 | 状态 | 内容 |
|---|---|---|
| **v0.1.5** | ✅ 已补充 | 零安装浏览器 Demo(index.html) + v0.2 报价引擎 alpha(quote_engine.py) + 品牌主张(MANIFESTO) + 上线推广清单(GITHUB_LAUNCH) |
| **v0.1** | ✅ 已完成 | 7 环节文档骨架 + 3 个 stdlib 脚本 + 27 条提示词 + 双语 README |
| **v0.2** | 🟡 进行中(alpha) | **AI 报价引擎**：`scripts/quote_engine.py` 已落地 alpha —— 输入成本 + 市场 + 竞品锚价，输出 FOB/CIF 报价区间 + 三档让步阶梯（每步必须换条件） |
| **v0.3** | 计划中 | **客户背调 Agent**：输入公司名，输出 L1/L2/L3 三级背调草稿 + 红旗清单，带来源链接 |
| **长期** | — | 行业包（轮胎、建材、机械、五金各自的环节细节）；多语言建联消息（西/阿/法/俄）；真实线索集（脱敏后公开）；把 v0.2 的报价引擎接到海关数据上做竞品锚价自动抓取 |

v0.2 的前置条件是 v0.3 的背调数据——因为报价需要知道对方的价格带，而这个价格带最可靠的来源之一就是客户历史成交记录。所以顺序是先背调、后报价。

---

## 参与方式

这个项目最大的缺口不是文档数量，是**不同国家的实战细节**。我知道轮胎在中东怎么做第一笔单，我不知道厄瓜多尔的建材渠道长什么样，也不知道尼日利亚的清关要哪几份文件。**这些只有当地做的人能补。**

三种贡献方式，按门槛从低到高：

1. **提 issue 纠错。** 看到错字、过时信息、说不清的判断标准，直接开 issue。哪怕只有一句话也比不说好。issue 模板里问三个问题：哪一行看不懂、哪个数字没有来源、哪条你觉得不适用你所在的行业。
2. **翻译环节文档。** 西班牙语、阿拉伯语、葡萄牙语、俄语、法语、越南语——哪个语言你熟就翻哪个。文档六段结构保持不变，只换语言，术语在术语表里对齐即可。
3. **补充你所在行业 / 国家的环节细节。** 这是最缺的部分。写作要求：写你真跑过的，不写你觉得应该这样。具体到字段名、单证名、渠道结构、付款习惯、常见拒付理由。

也可以直接改代码，但硬约束是 **Python 3.8+、零第三方依赖**，理由和理由见 CONTRIBUTING。

---

## ⭐ Star History

如果这个项目帮到了你，点个 star 就是最大的支持。趋势图：

[![Star History Chart](https://api.star-history.com/svg?repos=zero-to-trade/zero-to-trade&type=Date)](https://www.star-history.com/#zero-to-trade/zero-to-trade&Date)

---

## 多语言

- 🇺🇸 [English](README_EN.md)（完整版，已就绪）
- 🇪🇸 🇸🇦 🇵🇹 🇷🇺 🇫🇷 🇻🇳 招募中 —— 任意语言熟就可以翻，结构不变、术语对齐术语表，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## License

[MIT](LICENSE) © 2026 zero-to-trade contributors

拿去用拿去改拿去商用，署名就行。免责：这套东西不保证你一定接得到单，它只保证你不会再因为「不知道下一步干什么」而停下来。

---

## 联系与提问

**请走 [GitHub Issues](https://github.com/zero-to-trade/zero-to-trade/issues)。**

包括：内容有错、指出来 · 想补你所在市场的实战细节、提 PR · 想讨论方法论、开issue 就行。

作者身份信息不在README 里公开。这是刻意的选择——**项目的可信度应该来自内容本身，而不是作者是谁。** 需要联系时请在 issue 里 @ 维护者，GitHub 会把通知送到对方邮箱。

---

## English (short version)

**zero-to-trade** is an open-source operating system for people starting in foreign trade with zero experience. Seven stages, from picking a market to shipping an order, plus three runnable Python scripts that do the boring parts.

The premise: **AI does the heavy lifting, you make the calls.** Most tutorials tell you "you should do customer background research" and stop there. This repo tells you which three fields to check, which sites to check them on, and what result makes you drop the lead.

| Stage | What you do | Output |
|---|---|---|
| **01 Pick a market** | Score language, demand, and barrier | 1 first market + 3 reasons |
| **02 Find leads** | Customs data, social media, search, trade shows | ≥20 verified leads per day |
| **03 Vet the buyer** | L1 screen / L2 standard / L3 deep dive | A/B/C rating; fraud filtered out |
| **04 Make contact** | Tier leads T0-T3; run three channels on first touch | Tiered list + 7-day follow-up plan |
| **05 Talk specs** | Small asks first, price always last | Spec / quantity / destination port |
| **06 Quote & negotiate** | Quote discipline: every concession buys something | Quote sheet + concession ladder + scripts |
| **07 Deliver the order** | Contract, production, inspection, documents, payment, freight | Closed delivery loop + repurchase plan |

**30-second demo** (Python 3.8+, no third-party packages):

```bash
python scripts/lead_score.py examples/leads_example.csv
```

Eight sample leads come back tiered T0:1 / T1:2 / T2:4 / T3:1, each with its own next action.

**What makes it different:** discipline, not tooling. The rules are what carry value — T0 gets contacted today, T3 goes in the cold pool, a concession without a condition is a donation. Anything that can be an `if/else` lives in a script, anything that needs judgment lives in the docs, anything that needs to sound like a human lives in `prompts/`.

**Roadmap:** v0.1 (docs + scripts + 21 prompts) → v0.2 AI quoting engine → v0.3 buyer background-check agent → long term: industry packs, more languages, real lead datasets.

**Contributing:** the biggest gap here is country-specific field detail. If you actually sell into a market this repo knows nothing about, that's the highest-value contribution you can make. Read [CONTRIBUTING.md](CONTRIBUTING.md).

MIT licensed. Questions, corrections, and contributions: [open an issue](https://github.com/zero-to-trade/zero-to-trade/issues).
