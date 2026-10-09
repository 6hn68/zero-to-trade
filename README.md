# zero-to-trade

![CI](https://github.com/6hn68/zero-to-trade/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.8%2B-306998)

**外贸零基础，7 步跑到第一单。**

- **要花多久**：不装任何东西，2 分钟能在浏览器里看到第一版分级结果；想跑脚本就装一次 Python（约 20 分钟，大半时间在等下载），之后每条命令 30 秒。7 步全走完、发出第一次真实触达，按 [`docs/fast-path.md`](docs/fast-path.md) 是 7 天、每天 1–2 小时。
- **你能得到什么**：7 个环节的清单（每步只回答"打开哪个网站、填什么、看到什么算过关"）+ 4 个能直接跑的 Python 脚本 + 27 条可粘贴的 AI 提示词。

> 我第一年做外贸，开发信写了 40 封，回复 0 封。我当时的结论是"我英语太烂了"。
> 后来发现不是——是我连"这 40 家里哪 5 家值得发"都没筛过，就照着名单从上往下发了。顺序整个是反的。
> 这个仓库把我后来摸出来的顺序写下来：7 步，每步落到具体动作，外加 4 个脚本替你干掉最枯燥的那部分。

分工就一句话：**AI 干重活，人做判断。**

**An open-source operating system for new foreign-trade sellers: a 7-stage workflow plus a working AI toolchain.**
> Core idea in one line: **AI does the heavy lifting, you make the calls.**

> MIT 开源 · 不卖课 · 不收费 · 不要你留邮箱 · 脚本零依赖、跑得通（CI 已在跑）· 作者匿名，可信度靠内容本身

> 欢迎各路江湖大佬提 PR / 补你所在市场的实战细节 / 翻译成你的母语 —— 详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 这个项目解决什么问题

你搜「外贸怎么开始」，会得到一堆东西：某大神的成功学、几百篇 SEO 软文、付费课试听片段、以及一堆标题写着"2026 最新玩法"点进去内容是 2019 年的文章。看完你觉得懂了，第二天打开海关数据网站，还是不知道第一行该填什么。

信息不是不够，是碎的、按成功者的视角剪过的、而且没有下一步。

传统教程的套路一般是这样：告诉你「要做客户背调」，再告诉你「背调很重要」，然后没了。你依然不知道查哪几个字段、上哪个网站查、红旗长什么样、查到什么程度算够。

我的做法是把一件事往下拆，拆到它变成一个动作才算完：

| 传统教程 | 本项目 |
|---|---|
| 「要做客户背调」 | L1 筛查查 3 项（官网存在性、成立年份、社媒是否活跃），任一项不过直接淘汰 |
| 「要重视客户质量」 | 10 条线索自动分成 T0/T1/T2/T3，每级写清下一步该干什么、该花多少时间 |
| 「记得跟进」 | 首发当天、第 2 天后、第 5 天后各触达一次，共 3 次，每次话术不同；第 5 天那次是收尾信，发完就停手 |
| 「AI 会改变外贸」 | 4 个 stdlib-only Python 脚本（含 1 个 alpha 报价引擎），`python scripts/lead_score.py my_leads.csv` 30 秒出分级结果 |

信息量其实差不多，差的只是拆得够不够细。这里的每一条结论都得能落到「今天下午打开哪个网站、填什么、看到什么算过关」——落不到的，我就没往上写。

---

## 7 环节总览

从「选哪个国家」到「货上船、钱到账」，一条链路走完。每个环节一个文档，每个环节的产出都是能直接拿去用的东西——不是"认知升级"。

| 环节 | 做什么 | 产出 |
|---|---|---|
| **01 选市场** | 语言-需求-壁垒三维评估 | 1 个首站市场 + 三条理由 |
| **02 找客户** | 海关数据 / 社媒 / 搜索 / 展会四路 | 每天 ≥20 条真线索 |
| **03 背调客户** | L1 筛查 / L2 标准 / L3 深度 | A/B/C 评级，过滤骗子 |
| **04 建联客户** | T0-T3 分级，三线并进首触 | 分级名单 + 7 天跟进计划 |
| **05 聊单** | 小要求先行，报价永远最后 | 规格 / 数量 / 目的港三件套 |
| **06 报价谈判** | 报价纪律，让步换条件 | 报价单 + 让步阶梯 + 话术 |
| **07 订单交付** | 合同 / 生产 / 验货 / 单证 / 收款 / 物流 | 交付闭环 + 复购计划 |

每个环节文档都是同一个六段结构（见 [CONTRIBUTING.md](CONTRIBUTING.md#文档规范)）：这个环节在干什么 → 怎么做（分步） → 判断标准 → 常见坑 → 可复制模板 → 本环节的 AI 提示词。

六段里我最看重「判断标准」那一段。没有判断标准的建议等于没说，你读完还是不知道自己做到没有。

**完全零基础？** 先读 [`docs/00-getting-started.md`](docs/00-getting-started.md)，两条路任选：A 路什么都不装，双击根目录 `index.html`，2 分钟看到 T0–T3 分级；B 路装一次 Python（首次约 20 分钟），之后每条命令 30 秒。

顺手说一句：这套流程我自己走过一遍，第 3 天就想放弃了。所以我把它写成 7 步——至少你放弃的时候，知道自己在第几步。

---

## 30 秒上手

**不想装 Python 就别装。** 双击 [`index.html`](index.html)，浏览器里粘贴 CSV 就能看到 T0–T3 分级，不联网、不装东西。（推到 GitHub 后由 Pages 自动托管，别人也能直接打开。）

愿意装的话，下面 4 个脚本全是标准库写的，零第三方依赖，Python 3.8+ 就能跑。第 4 个还是 v0.2 alpha，别直接拿它去报真实价格。

**先花 10 秒做一件事**：把示例数据复制一份成自己的 `my_leads.csv`，**真名单只往这份里填**：

```bash
cp examples/leads_example.csv my_leads.csv
```

（Windows 手动做：打开 `examples` 文件夹，把 `leads_example.csv` 复制到上一层，改名叫 `my_leads.csv`。）

为什么要多这一步：`my_leads.csv` 会被自动拦住不传到网上，`examples/` 里那份是仓库自带的，改坏了会把你下次同步的代码一起搞乱。

然后跑这 4 条：

```bash
# 1. 线索自动分级：输入 CSV，输出 T0-T3 排序 + 每级下一步动作
python scripts/lead_score.py my_leads.csv

# 2. 按分级生成中英对照建联文案（英文发送，中文供你审批）
python scripts/outreach_gen.py my_leads.csv --tier T0

# 3. 生成 7 天 3 触达跟进计划表（带具体日期）
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv my_leads.csv

# 4. (alpha) 报价引擎：成本 + 海运费 + 毛利 → FOB/CIF 区间 + 三档让步阶梯
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

> 直接把 `examples/leads_example.csv` 喂给脚本也能跑。但真名单别填进那个文件——它是仓库自带的，你一改，下次同步代码就会跟它打架。

想直接开干的话，看 [`docs/fast-path.md`](docs/fast-path.md)：从 0 到第一次真实触达，7 天、每天 1–2 小时。它不保证你拿到回复——第一封回复可能第 2 天来，也可能第 8 周才来。

### 第 1 条命令真的会打印这些

下面是 `python scripts/lead_score.py my_leads.csv`（my_leads.csv 就是上面那份示例复制出来的）的实际输出，一个字没改：

```
====================================================================================
  线索分级结果   共 10 条 · 今天先打 2 家 · 本周再加 5 家
====================================================================================
  #   分级 公司                         国家            得分  今天/本周该做什么
------------------------------------------------------------------------------------
  1   T0   【示例】海湾轮胎贸易         Saudi Arabia      95  今天就发首触，别等
  2   T0   【示例】三角洲轮胎           Saudi Arabia      88  今天就发首触，别等
  3   T1   【示例】阿曼蓝海             Oman              77  排进本周，今天准备文案
  4   T1   【示例】半岛汽车             Saudi Arabia      71  排进本周，今天准备文案
  5   T1   【示例】尼罗河商贸           Egypt             67  排进本周，今天准备文案
  6   T1   【示例】迪拜轮毂行           UAE               65  排进本周，今天准备文案
  7   T1   【示例】利雅得汽配           Saudi Arabia      60  排进本周，今天准备文案
  8   T2   【示例】尼日利亚先锋         Nigeria           46  进 B 池，每天固定时段扫一遍
  9   T3   【示例】黎凡特供配           Lebanon           20  信息不足，先补联系方式/需求再打
  10  T3   【示例】利雅得零件店         Saudi Arabia      10  信息不足，先补联系方式/需求再打
------------------------------------------------------------------------------------
  汇总: T0:2 / T1:5 / T2:1 / T3:2  （T0 20% · T1 50% · T2 10% · T3 20%）

  今天先打: 【示例】海湾轮胎贸易、【示例】三角洲轮胎
  本周跟进: 【示例】阿曼蓝海、【示例】半岛汽车、【示例】尼罗河商贸、【示例】迪拜轮毂行、【示例】利雅得汽配
  先别碰  : 【示例】黎凡特供配、【示例】利雅得零件店（信息不全，补完再说）

  下一步: 用 outreach_gen.py 按这份分级生成建联文案。
====================================================================================
```

10 条线索里只有 2 条是"今天就该发"的。剩下 8 条，你要是把 40 封开发信的时间平均分给它们，就是在用最贵的时间做最便宜的事。

### CSV 字段

`my_leads.csv`（从 `examples/leads_example.csv` 复制来的那份）的表头长这样：

```
company,country,product,source,email,phone,years,contact,note
```

只有 `company` 这一列是必需的，其余空着也能跑——缺项按最低分算，不会报错。`source` 建议填 `referral` / `trade_show` / `customs` / `linkedin` / `search` 之一，这一项对分数影响最大：展会和海关数据来的线索，天然比搜索搜出来的高一截。

4 个脚本都有 `--help`。`lead_score.py` 另有 `--format json` 和 `--country/--product` 过滤，方便接进你自己的表格。

脚本只管机械上能判定的部分：有没有邮箱、来源可不可信、够不够 T0 线。至于「这家值不值得我花两个小时」——那是文档和你的活，我故意没写进脚本里。

---

## 几个被问过的问题

**要钱吗？**
不要。MIT 开源，没有付费版、没有进阶课、也没有"留邮箱领资料"这一步。

**完全不懂 Python 能用吗？**
能。双击 `index.html`，浏览器里粘贴 CSV 就能看到分级结果，不装任何东西。想跑脚本再考虑装 Python，首次约 20 分钟。

**示例里的公司是真实的吗？**
全是虚构的。公司名统一带「【示例】」前缀，邮箱域名用 IANA 保留域 `sample.example`，电话是占位符。请不要照着去联系任何人。

**能保证出单吗？**
不能。这份东西解决的只是"不知道下一步干什么"。产品、市场时机、运气——那三样我给不了。

**脚本会把我的客户数据传出去吗？**
不会。4 个脚本都是纯函数 + 标准库，不联网、不写文件（除非你自己加 `--out`）。你喂进去的 CSV 只在你自己机器上。

**我不是做轮胎的，能用吗？**
流程能用，行业细节得你自己补。7 个环节的骨架是通用的，但具体到单证名、渠道结构、付款习惯，每个行业不一样——这也是我最希望有人来 PR 的部分。

---

## 目录结构

```
zero-to-trade/
├── README.md              # 你正在读的中文主门面
├── README_EN.md           # 完整英文版
├── README_ES.md           # 西班牙语版（starter，招募校对）
├── index.html             # 零安装浏览器 Demo（GitHub Pages 自动托管）
├── MANIFESTO.md           # 匿名不卖课：品牌主张
├── GITHUB_LAUNCH.md       # 上线 + 推广执行清单（Topics/About/PR/Show HN）
├── CONTRIBUTING.md        # 贡献方式 + 文档/代码规范
├── LICENSE                # MIT
├── docs/                  # 7 个环节的详细文档（一个环节一个文件）
│   ├── 00-getting-started.md   # 完全零基础：A 路不装东西 2 分钟 / B 路首次约 20 分钟
│   ├── fast-path.md            # 7 天从零到第一封客户回复（新手最快路径）
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   ├── 07-order-delivery.md
│   └── deal-walkthrough.md     # 一笔真实感第一单的全流程走查（虚构示例）
├── scripts/               # 可直接跑的 Python 脚本（stdlib-only）
│   ├── lead_score.py      # 线索 T0-T3 自动分级
│   ├── outreach_gen.py    # 按分级生成中英对照建联消息
│   ├── followup_plan.py   # 7 天 3 触达跟进计划表
│   └── quote_engine.py    # v0.2 报价引擎(alpha)：FOB/CIF 区间 + 三档让步阶梯
├── examples/
│   └── leads_example.csv  # 示例数据（复制成 my_leads.csv 再填自己的）
├── prompts/
│   └── AI_PROMPTS.md      # 27 条可直接粘贴的英文提示词，按环节分组
└── assets/                # 图片、截图、图表
```

---

## 为什么给 AI 工具，而不是只给一套方法论

不少「AI 提效」项目的做法是把方法论塞进 prompt。我反着来：先定纪律，再给工具。

会写 prompt 不等于会做外贸。我默认你缺的不是话术——话术网上一抓一把——你缺的是一套判断框架，用来决定今天这 3 小时该花在哪 5 家公司身上。所以：

- 值钱的是纪律。T0 今天就发，T3 扔进池子三个月别碰。让步必须换条件，不换条件的让步那叫送钱。这些是规则，AI 替你决定不了。
- 重活扔给 AI。10 条线索的批量初筛、50 家客户的三层背调草稿、7 天跟进话术的变体——费时间但不需要判断力的活，都给它。
- 要重复的就写进脚本。分级标准如果每次都凭感觉，那就等于没有标准。所以先写成 200 行以内、只依赖标准库的脚本，谁跑结果都一样。

分工线：能写成 if/else 的进脚本，需要权衡的进文档，需要说人话的进 `prompts/`。

另外，脚本刻意不依赖 pandas / openai SDK。装环境这件事本身就会劝退零基础用户——外贸新手卡在 `pip install` 上的时间，经常比他花在找客户上的还多。

---

## 路线图

| 版本 | 状态 | 内容 |
|---|---|---|
| **v0.1.5** | ✅ 已补充 | 零安装浏览器 Demo(index.html) + v0.2 报价引擎 alpha(quote_engine.py) + 品牌主张(MANIFESTO) + 上线推广清单(GITHUB_LAUNCH) |
| **v0.1** | ✅ 已完成 | 7 环节文档骨架 + 4 个 stdlib 脚本 + 27 条提示词 + 双语 README |
| **v0.2** | 🟡 进行中(alpha) | **AI 报价引擎**：`scripts/quote_engine.py` 已落地 alpha —— 输入成本 + 市场 + 竞品锚价，输出 FOB/CIF 报价区间 + 三档让步阶梯（每步必须换条件） |
| **v0.3** | 计划中 | **客户背调 Agent**：输入公司名，输出 L1/L2/L3 三级背调草稿 + 红旗清单，带来源链接 |
| **长期** | — | 行业包（轮胎、建材、机械、五金各自的环节细节）；多语言建联消息（西/阿/法/俄）；真实线索集（脱敏后公开）；把 v0.2 的报价引擎接到海关数据上做竞品锚价自动抓取 |

v0.2 的前置条件是 v0.3 的背调数据——因为报价需要知道对方的价格带，而这个价格带最可靠的来源之一就是客户历史成交记录。所以顺序是先背调、后报价。

---

## 参与方式

缺的不是文档数量，是不同国家的实战细节。轮胎在中东怎么跑第一笔单我写得出来；厄瓜多尔的建材渠道长什么样，我不知道；尼日利亚清关要哪几份文件，我不敢瞎写。这些只有当地做的人能补。

三种贡献方式，门槛从低到高：

1. 提 issue 纠错。看到错字、过时信息、说不清的判断标准，直接开 issue。一句话也行，比不说强。issue 模板会问你三个问题：哪一行看不懂、哪个数字没有来源、哪条在你所在的行业不适用。
2. 翻译环节文档。西班牙语、阿拉伯语、葡萄牙语、俄语、法语、越南语——你会哪个就翻哪个。六段结构别动，只换语言，术语在 [GLOSSARY.md](GLOSSARY.md) 里对齐就行。
3. 补你所在行业 / 国家的环节细节。这是最缺的。要求只有一条：写你真跑过的，别写你觉得应该这样的。具体到字段名、单证名、渠道结构、付款习惯、常见拒付理由。

代码也可以直接改，但硬约束是 Python 3.8+、零第三方依赖，理由见 CONTRIBUTING。

---

## 给开发者：可 hack、零依赖

4 个脚本（`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine`）只用 Python 标准库，一个第三方包都没有，你随便改、随便嵌：

- 想换打分权重？改 `lead_score.py` 顶部的 `CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W` 四个常量，满分还是 100。
- 想接自己的海关数据？CSV 表头对齐 `company,country,product,source,email,phone,years,contact,note`，直接喂进去。
- 想嵌进自己的工具链？每个脚本都能 `import`，`score_leads()` / `build_message()` / `plan_followups()` / `quote_range()` 都是纯函数，返回字典或列表，不碰网络、不写文件。
- CI 在 GitHub Actions 上跑 `py_compile` + 冒烟测试（py3.8 / 3.11 / 3.13），改完提 PR 不会悄悄坏掉。

> 你不用信我说的。复制一份示例数据，跑一遍 `python scripts/lead_score.py my_leads.csv` 自己看结果——这玩意儿好不好使，30 秒就能验证，用不着我在这儿吹。

---

## 点个 star，当书签用也行

仓库还在更新（最后一次提交看下面的 badge）。觉得有用就点右上角 star——最大的用处其实是下次你想找的时候能翻出来。

我不群发、不私信、不要邮箱，也不会因为你点了 star 就给你发任何东西。

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[查看完整 Star History 趋势图](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## 多语言

- 🇺🇸 [English](README_EN.md)（完整版，已就绪）
- 🇪🇸 [Español](README_ES.md)（starter，招募校对）· 🇸🇦 🇵🇹 🇷🇺 🇫🇷 🇻🇳 招募中 —— 任意语言熟就可以翻，结构不变、术语对齐 [GLOSSARY.md](GLOSSARY.md)，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## License

[MIT](LICENSE) © 2026 zero-to-trade contributors

拿去用、拿去改、拿去商用，署名就行。

一句免责：这套东西不保证你接得到单。它只解决一种卡壳——坐在电脑前，不知道下一个动作该干什么。别的我帮不上。

---

## 联系与提问

**请走 [GitHub Issues](https://github.com/6hn68/zero-to-trade/issues)。**

内容有错、想补你所在市场的细节、想提 PR、想跟我吵方法论，都是开 issue。

作者身份不在 README 里公开，这是故意的：项目的可信度应该来自内容本身，不是来自"作者是某某公司的某某"。有事在 issue 里 @ 维护者，GitHub 会把通知送到对方邮箱。

---

## English (short version)

**zero-to-trade** is an open-source operating system for people starting in foreign trade with zero experience. Seven stages, from picking a market to shipping an order, plus four runnable Python scripts (one alpha quoting engine) that do the boring parts. Two minutes in a browser if you install nothing; about seven days at 1–2 hours a day to make your first real contact.

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
cp examples/leads_example.csv my_leads.csv
python scripts/lead_score.py my_leads.csv
```

Copy the sample data to your own file first — the `.example` suffix is there so nobody accidentally publishes their real customer list. Fill `my_leads.csv`, never the example file.

Ten sample leads come back tiered T0:2 / T1:5 / T2:1 / T3:2, each with its own next action.

**What makes it different:** discipline, not tooling. The rules are what carry value — T0 gets contacted today, T3 goes in the cold pool, a concession without a condition is a donation. Anything that can be an `if/else` lives in a script, anything that needs judgment lives in the docs, anything that needs to sound like a human lives in `prompts/`.

**Roadmap:** v0.1 (docs + scripts + 27 prompts) → v0.2 AI quoting engine → v0.3 buyer background-check agent → long term: industry packs, more languages, real lead datasets.

**Contributing:** the biggest gap here is country-specific field detail. If you actually sell into a market this repo knows nothing about, that's the highest-value contribution you can make. Read [CONTRIBUTING.md](CONTRIBUTING.md).

MIT licensed. Questions, corrections, and contributions: [open an issue](https://github.com/6hn68/zero-to-trade/issues).
