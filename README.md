# zero-to-trade

**中文** · [English](README_EN.md) · [Español](README_ES.md) · [Português](README_PT.md) · [Français](README_FR.md) · [العربية](README_AR.md) · [Русский](README_RU.md) · [Deutsch](README_DE.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Türkçe](README_TR.md) · [Bahasa Indonesia](README_ID.md)

![CI](https://github.com/6hn68/zero-to-trade/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-306998)

**从零做外贸的开源工作流：7 步流程 + 15 个 Python 脚本 + 4 个网页工具，帮新手把找客户、背调、建联、跟单跑成可重复的动作。**

> **这是什么**：新手外贸员常卡在三件事上——不知道先找哪家客户、建联信不知道怎么写、跟进全靠记性。这个仓库把“选市场→找客户→背调→建联→聊单→报价→交付”拆成 7 步，每步落到具体动作，再用 15 个 Python 脚本替你干掉最枯燥的那部分。
>
> **怎么跑（3 条命令，30 秒看到结果）**：
>
> ```bash
> python3 scripts/lead_score.py examples/leads_example.csv        # 10 条线索出分级：T0:2 / T1:5 / T2:1 / T3:2
> python3 scripts/outreach_gen.py examples/leads_example.csv --tier T0   # 按分级生成中英对照建联文案
> python3 scripts/followup_plan.py --tier T0 --start 2026-11-24 --csv examples/leads_example.csv   # T0 跟进计划：D0/D2/D5，3 次停手
> ```
>
> **在线演示（不用装 Python）**：[https://6hn68.github.io/zero-to-trade/](https://6hn68.github.io/zero-to-trade/) ——浏览器打开就能用 4 个工具：线索分级、建联文案、跟进计划、报价，界面支持 12 种语言（右上角切换），名单不上传。
>
> **版本状态**：V20（15 个脚本、647 项测试全绿），仓库和网站都是这一版；网站有 4 个浏览器工具，界面 12 种语言；CI 在 Python 3.10–3.13 上跑。终端演示 GIF 待录制，录制脚本见 [`tape.vhs`](tape.vhs)。

## 7 步 Demo 导航：2 分钟跑通一次真实分级 + 建联消息

不用先读文档。7 步，每步一句话 + 一条能直接复制的命令，全跑通大约 2 分钟。下面 7 条命令都在仓库里实际跑过（2026-11-24，Python 3.x，零第三方依赖）；示例数据全是虚构的，公司名带【示例】前缀。

| 步 | 一句话 | 命令（复制就能跑） |
|---|---|---|
| 1 拿名单 | 把示例复制一份成自己的文件，真名单只往这份里填 | `cp examples/leads_example.csv my_leads.csv` |
| 2 分级 | 10 条线索排成 T0–T3，今天先打 2 家 | `python3 scripts/lead_score.py my_leads.csv` |
| 3 背调 | 只给公司名跑一遍：没给的项全标「待核实」，先拿 C 级——这是演示，正式背调要把查到的事实填进去再评 | `python3 scripts/due_diligence.py --company "【示例】海湾轮胎贸易"` |
| 4 建联 | 按 T0 生成中英对照首触文案，英文发、中文自己审 | `python3 scripts/outreach_gen.py my_leads.csv --tier T0` |
| 5 跟进 | D0/D2/D5 三次节奏表，6 天 3 次，第 3 次没回就停手 | `python3 scripts/followup_plan.py --tier T0 --start 2026-11-24 --csv my_leads.csv` |
| 6 报价 | 对方回了再算：成本 + 运费 + 毛利 → FOB/CIF 区间 + 三档让步阶梯 | `python3 scripts/quote_engine.py --cost 28 --freight 6 --margin 15` |
| 7 催单 | 报价 7 天没回，拿这句去问进度，不卑不亢 | `python3 scripts/nudge.py --day D7 --scenario quoted` |

第 5 步的 `--start` 填你跑的那天（上面写的是 2026-11-24，改成今天就行）；D5 别落在周五（主麻日），落上了脚本自己会提醒顺延。

第 3 步只给公司名，跑出来是 C 级、让先补证据再建联——这是对的：没给证据它不会硬编一个好评级。真背调时把查到的事实（官网、年限、来源、海关记录等）用参数填进去，同一家公司按 `python3 scripts/due_diligence.py --help` 里的 A 级例子能评到 A 级；第 4 步照发，是因为第 2 步的分级已经用了 CSV 里的来源、邮箱、年限证据。

跑完第 4 步，你手里就有一封能发的首触邮件；跑完第 5 步，你知道接下来 6 天每天该干什么。第 2 步的实际输出（一个字没改）见下面「第 1 条命令真的会打印这些」。

不想装 Python？打开[网站](https://6hn68.github.io/zero-to-trade/)（或在本地双击 [`index.html`](index.html)），浏览器里同样走一遍：点「载入轮胎示例」→ 点「打分」→ 找到 T0 → 生成首触文案并复制 → 把 `[ ]` 换成你自己的信息 → 排 D0/D2/D5 跟进 → 对方回了再报价。网页版首触文案是英文正文 + 中文对照；要西语、葡语、阿语文案，用命令行 `outreach_gen.py --lang es/pt/ar`。

- **要花多久**：不装任何东西，2 分钟能在浏览器里看到第一版分级结果；想跑脚本就装一次 Python（约 20 分钟，大半时间在等下载），之后每条命令 30 秒。7 步全走完、发出第一次真实触达，按 [`docs/fast-path.md`](docs/fast-path.md) 是 7 天、每天 1–2 小时。
- **你能得到什么**：7 个环节的清单（每步只回答"打开哪个网站、填什么、看到什么算过关"）+ 15 个脚本文件（14 个能直接跑的业务脚本 + 1 个脱敏自查脚本）+ 40 条可粘贴的 AI 提示词。

> 我第一年做外贸，开发信写了 40 封，回复 0 封。我当时的结论是"我英语太烂了"。
> 后来发现不是——是我连"这 40 家里哪 5 家值得发"都没筛过，就照着名单从上往下发了。顺序整个是反的。
> 这个仓库把我后来摸出来的顺序写下来：7 步，每步落到具体动作，外加 15 个脚本文件替你干掉最枯燥的那部分。

分工就一句话：**AI 干重活，人做判断。**

**An open-source workflow for new foreign-trade sellers: a 7-stage workflow plus 12 Python tools that turn finding leads, checking them, reaching out and following up into repeatable steps.**
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
| 「AI 会改变外贸」 | 15 个 stdlib-only Python 脚本文件（14 个业务脚本，含 1 个报价引擎；+ 1 个脱敏自查脚本），`python3 scripts/lead_score.py my_leads.csv` 30 秒出分级结果 |

信息量其实差不多，差的只是拆得够不够细。这里的每一条结论都得能落到「今天下午打开哪个网站、填什么、看到什么算过关」——落不到的，我就没往上写。

---

## 7 环节总览

从「选哪个国家」到「货上船、钱到账」，一条链路走完。每个环节一个文档，每个环节的产出都是能直接拿去用的东西——不是"认知升级"。

| 环节 | 做什么 | 产出 |
|---|---|---|
| **01 选市场** | 语言-需求-壁垒三维评估 | 1 个首站市场 + 三条理由 |
| **02 找客户** | 海关数据 / 社媒 / 搜索 / 展会四路 | 每天 ≥20 条真线索 |
| **03 背调客户** | L1 筛查 / L2 标准 / L3 深度 | A/B/C 评级，过滤骗子 |
| **04 建联客户** | T0-T3 分级，三线并进首触 | 分级名单 + D0/D2/D5 跟进计划（6 天 3 次） |
| **05 聊单** | 小要求先行，报价永远最后 | 规格 / 数量 / 目的港三件套 |
| **06 报价谈判** | 报价纪律，让步换条件 | 报价单 + 让步阶梯 + 话术 |
| **07 订单交付** | 合同 / 生产 / 验货 / 单证 / 收款 / 物流 | 交付闭环 + 复购计划 |

每个环节文档都是同一个六段结构（见 [CONTRIBUTING.md](CONTRIBUTING.md#文档规范)）：这个环节在干什么 → 怎么做（分步） → 判断标准 → 常见坑 → 可复制模板 → 本环节的 AI 提示词。

六段里我最看重「判断标准」那一段。没有判断标准的建议等于没说，你读完还是不知道自己做到没有。

**不知道先走哪条路？** 看 [三条学习路径](docs/learning-paths.md)：🌱 新手村（0 基础，01→07 按顺序，4–6 周）→ 🚀 进阶场（有线索/开过单，08→12 按需选）→ 🏆 高手营（稳定出单，13 大客户 + 回头打磨）。放量之后再看 [进阶模块 08–13](docs/advanced/08-independent-station.md)：独立站、社媒矩阵、展会、物流支付、风险合规、大客户开发。

**完全零基础？** 先读 [`docs/00-getting-started.md`](docs/00-getting-started.md)，两条路任选：A 路什么都不装，双击根目录 `index.html`，2 分钟看到 T0–T3 分级；B 路装一次 Python（首次约 20 分钟），之后每条命令 30 秒。

顺手说一句：这套流程我自己走过一遍，第 3 天就想放弃了。所以我把它写成 7 步——至少你放弃的时候，知道自己在第几步。

---

## 30 秒上手

**不想装 Python 就别装。** 打开[网站](https://6hn68.github.io/zero-to-trade/)，4 个工具（线索分级、建联文案、跟进计划、报价）直接在浏览器里跑，规则和脚本一致；粘贴 CSV 就能看到 T0–T3 分级，不装东西，名单不离开你的浏览器。界面支持 12 种语言。

愿意装的话，14 个业务脚本全是标准库写的，零第三方依赖，Python 3.10+ 就能跑；再加 1 个脱敏自查脚本 `check_private_data.py`（提交前扫一遍有没有真实客户数据）。报价引擎在 V10 已落地（FOB/CIF 区间 + 三档让步阶梯）；背调 Agent 在 V11 已落地（L1/L2/L3 三级 + A/B/C 评级 + 红旗清单）；轮胎行业包在 V12 已落地（规格 + 市场 → GCC 要点 + 清关单证 + 注意事项）；多语言建联在 V13 已落地（`--lang es/pt/ar`，西/葡/阿正文 + 英文原文对照）；到岸成本估算在 V14 已落地（FOB + 运费 + 保险 → CIF，再加关税 + 目的港杂费 → DDP）；展会实战工具在 V15 已落地（现场收的名片按兴趣度排会后 24 小时跟进计划）；催单话术库在 V16 已落地（D3/D7/D14/D30 × 已报价未回/已发样未回/已谈价未定，WhatsApp 短版 + 邮件长版，中英对照）。

**先花 10 秒做一件事**：把示例数据复制一份成自己的 `my_leads.csv`，**真名单只往这份里填**：

```bash
cp examples/leads_example.csv my_leads.csv
```

（Windows 手动做：打开 `examples` 文件夹，把 `leads_example.csv` 复制到上一层，改名叫 `my_leads.csv`。）

为什么要多这一步：`my_leads.csv` 会被自动拦住不传到网上，`examples/` 里那份是仓库自带的，改坏了会把你下次同步的代码一起搞乱。

然后跑这 4 条：

```bash
# 1. 线索自动分级：输入 CSV，输出 T0-T3 排序 + 每级下一步动作
python3 scripts/lead_score.py my_leads.csv

# 2. 按分级生成中英对照建联文案（英文发送，中文供你审批）
python3 scripts/outreach_gen.py my_leads.csv --tier T0

# 3. 生成 D0/D2/D5 跟进计划表（6 天 3 次，带具体日期）
python3 scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv my_leads.csv

# 4. 报价引擎：成本 + 海运费 + 毛利 → FOB/CIF 区间 + 三档让步阶梯
python3 scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

> 直接把 `examples/leads_example.csv` 喂给脚本也能跑。但真名单别填进那个文件——它是仓库自带的，你一改，下次同步代码就会跟它打架。

想直接开干的话，看 [`docs/fast-path.md`](docs/fast-path.md)：从 0 到第一次真实触达，7 天、每天 1–2 小时。它不保证你拿到回复——第一封回复可能第 2 天来，也可能第 8 周才来。

### 第 1 条命令真的会打印这些

下面是 `python3 scripts/lead_score.py my_leads.csv`（my_leads.csv 就是上面那份示例复制出来的）的实际输出，一个字没改：

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
  8   T2   【示例】尼日利亚先锋         Nigeria           50  进 B 池，每天固定时段扫一遍
  9   T3   【示例】黎凡特供配           Lebanon           24  信息不足，先补联系方式/需求再打
  10  T3   【示例】利雅得零件店         Saudi Arabia      17  信息不足，先补联系方式/需求再打
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

15 个脚本都有 `--help`。`lead_score.py` 另有 `--format json` 和 `--country/--product` 过滤，方便接进你自己的表格。

脚本只管机械上能判定的部分：有没有邮箱、来源可不可信、够不够 T0 线。至于「这家值不值得我花两个小时」——那是文档和你的活，我故意没写进脚本里。

---

## 几个被问过的问题

**要钱吗？**
不要。MIT 开源，没有付费版、没有进阶课、也没有"留邮箱领资料"这一步。

**完全不懂 Python 能用吗？**
能。打开网站或双击 `index.html`，浏览器里粘贴 CSV 就能看到分级结果，不装任何东西。想跑脚本再考虑装 Python，首次约 20 分钟。

**示例里的公司是真实的吗？**
全是虚构的。公司名统一带「【示例】」前缀，邮箱域名用 IANA 保留域 `sample.example`，电话是占位符。请不要照着去联系任何人。

**能保证出单吗？**
不能。这份东西解决的只是"不知道下一步干什么"。产品、市场时机、运气——那三样我给不了。

**脚本会把我的客户数据传出去吗？**
不会。15 个脚本都只用标准库、不联网；14 个业务脚本不写业务文件（除非你自己加 `--out`），其中 `lead_score` / `outreach_gen` / `followup_plan` 三个会在 `logs/` 里记一条运行日志（只记时间、参数、结果摘要，不记客户数据）；脱敏自查脚本只读不写。你喂进去的 CSV 只在你自己机器上。

**我不是做轮胎的，能用吗？**
流程能用，行业细节得你自己补。7 个环节的骨架是通用的，但具体到单证名、渠道结构、付款习惯，每个行业不一样——这也是我最希望有人来 PR 的部分。

---

## 目录结构

```
zero-to-trade/
├── README.md              # 你正在读的中文主门面
├── README_EN.md           # 完整英文版（各语种译本以它为准）
├── README_ES.md / README_PT.md / README_FR.md / README_AR.md / README_RU.md
├── README_DE.md / README_JA.md / README_KO.md / README_TR.md / README_ID.md
│                          # 西 / 葡 / 法 / 阿（RTL）/ 俄 / 德 / 日 / 韩 / 土 / 印尼语版
├── index.html             # 网站：4 个浏览器工具，界面 12 种语言，零依赖（GitHub Pages 托管）
├── MANIFESTO.md           # 匿名不卖课：品牌主张
├── GITHUB_LAUNCH.md       # 上线 + 推广执行清单（Topics/About/PR/Show HN）
├── CONTRIBUTING.md        # 贡献方式 + 文档/代码规范
├── CHANGELOG.md           # 更新日志：每次改了什么
├── ROADMAP.md             # 路线图：版本往前走的顺序
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
│   ├── deal-walkthrough.md     # 一笔真实感第一单的全流程走查（虚构示例）
│   ├── learning-paths.md       # 三条学习路径：新手村 / 进阶场 / 高手营
│   ├── troubleshooting.md      # 排障手册（亲手复现过的坑）
│   ├── dev-flow-ai.md          # 贡献者 AI 开发流程（plan 门条件触发）
│   ├── long-task-template.md   # 贡献者长任务开工模板
│   ├── decisions/              # ADR：重大决策记录
│   └── advanced/               # 进阶模块 08-13：独立站 / 社媒矩阵 / 展会 / 物流支付 / 风险合规 / 大客户
├── scripts/               # 可直接跑的 Python 脚本（stdlib-only）
│   ├── lead_score.py      # 线索 T0-T3 自动分级
│   ├── outreach_gen.py    # 按分级生成建联消息（中英对照 + 西/葡/阿 + 英文对照，V13）
│   ├── followup_plan.py   # D0/D2/D5 跟进计划表（6 天 3 次）
│   ├── quote_engine.py    # 报价引擎：FOB/CIF 区间 + 三档让步阶梯
│   ├── due_diligence.py   # V11 背调 Agent：L1/L2/L3 三级 + A/B/C 评级 + 红旗清单
│   ├── tire_pack.py       # V12 轮胎行业包：规格 + 市场 → GCC 要点 + 清关单证 + 注意事项
│   ├── landed_cost.py     # V14 到岸成本：FOB + 运费 + 保险 → CIF，再加关税 + 目的港杂费 → DDP
│   ├── trade_show.py      # V15 展会实战：现场收的名片 → 会后 24 小时跟进计划（2 小时感谢 + 12 小时报价线索 + 24 小时电话追一次）
│   ├── nudge.py           # V16 催单话术：D3/D7/D14/D30 × 已报价未回/已发样未回/已谈价未定 → WhatsApp 短版 + 邮件长版（中英对照）
│   ├── anchor_price.py    # V18 竞品锚价：海关数据竞品价区间 + 自家成本 → 进取/中位/保守三档 CIF 锚价 + 5 项复核清单
│   ├── fast_path.py     # V19 七天快路径互动版：每天 --day N 看任务，干完 --done N 打卡，--progress 看进度（与 docs/fast-path.md 逐条对齐）
│   ├── market_rules.py    # 市场规则表：目标市场、土耳其/巴西壁垒、墨西哥/美国/欧盟排除
│   ├── daily_video_list.py  # 每日 5 条视频清单：上午 3 条、下午 2 条，带规格、市场、卖点和拍摄检查项
│   ├── fulfillment_checklist.py  # 订单交付核对：PI → 定金 → 生产 → 验货 → 尾款 → 订舱 → 报关 → 提单 → 清关单据 → 售后复购，定金/放单/出运三道钱关硬拦
│   └── check_private_data.py  # 提交前自查：扫真实客户数据，抓到就挡住
├── tests/                 # 647 项标准库 unittest，`python3 -m unittest discover -s tests`
├── examples/
│   ├── leads_example.csv  # 示例数据（复制成 my_leads.csv 再填自己的）
│   ├── leads_example_lighting.csv  # 非轮胎示例：8 条 LED 灯具线索
│   └── trade_show_example.csv  # 展会示例数据（3 家，高/中/低各一）
├── prompts/
│   └── AI_PROMPTS.md      # 40 条可直接粘贴的提示词（核心 28 + 进阶 12），按环节分组
└── assets/                # 图片、截图、图表
```

---

## 为什么给 AI 工具，而不是只给一套方法论

不少「AI 提效」项目的做法是把方法论塞进 prompt。我反着来：先定纪律，再给工具。

会写 prompt 不等于会做外贸。我默认你缺的不是话术——话术网上一抓一把——你缺的是一套判断框架，用来决定今天这 3 小时该花在哪 5 家公司身上。所以：

- 值钱的是纪律。T0 今天就发，T3 扔进池子三个月别碰。让步必须换条件，不换条件的让步那叫送钱。这些是规则，AI 替你决定不了。
- 重活扔给 AI。10 条线索的批量初筛、50 家客户的三层背调草稿、D0/D2/D5 跟进话术的变体——费时间但不需要判断力的活，都给它。
- 要重复的就写进脚本。分级标准如果每次都凭感觉，那就等于没有标准。所以先写成只依赖标准库的脚本，谁跑结果都一样。

分工线：能写成 if/else 的进脚本，需要权衡的进文档，需要说人话的进 `prompts/`。

另外，脚本刻意不依赖 pandas / openai SDK。装环境这件事本身就会劝退零基础用户——外贸新手卡在 `pip install` 上的时间，经常比他花在找客户上的还多。

---

## 路线图

> 详细路线见 [ROADMAP.md](ROADMAP.md)；每次改动见 [CHANGELOG.md](CHANGELOG.md)。

| 版本 | 状态 | 内容 |
|---|---|---|
| **V13** | ✅ 已落地（2026-11-07） | 多语言建联（`scripts/outreach_gen.py --lang es/pt/ar`：西/葡/阿正文 + 每条后附英文原文；模板与英文 T0/T1/T2 一一对应，脚本内嵌字典单份来源）+ `docs/04-outreach.md` 新一节（用法 + 3 份真实输出逐字贴）+ `tests/` 80 个标准库测试 + 提示词 40 条不变（核心 28 + 进阶 12）+ 7 个脚本文件 |
| **V18** | ✅ 已落地（2026-11-07） | 竞品锚价（`scripts/anchor_price.py`：海关数据竞品价区间 + 自家成本 → 进取/中位/保守三档 CIF 锚价，每档毛利、毛利率、FOB 对等价、隐含加成与适用场景；报价前先过成本/运费/汇率/付款条件/有效期 5 项复核清单，任一项待核就提醒；低于成本警告“低于成本，别接单或先谈量换价”；缺中位价按（最低+最高）/2 估算并注明；`--format json` / `--audience client`）+ `docs/anchor-price.md`（用法 + 锚价指南 + 2 份真实输出逐字贴）+ `docs/06-quote.md` 补一行（报价前先锚价）+ `tests/` 187 个标准库测试 + 提示词 40 条不变（核心 28 + 进阶 12）+ 11 个脚本文件 |
| **V20** | ✅ 当前版（2026-11-14） | 本地增量合并 + 10 轮打磨：CLI 入口统一（中文报错、退出码对齐）+ 测试补强（单条模式、`--start-date` 别名、运行日志）+ 文档数字对齐 + LED 灯具非轮胎示例（8 条）+ 演示页与 V19 同步 + 坏 CSV 人话报错（缺列/空文件/未闭合引号不再 traceback）+ 提示词对齐（P04-4 跟进命令补 `--avoid-weekend`、P10-2 窗口统一 48 小时）+ 操作日志落地（`logs/trace-YYYY-MM-DD.jsonl`，三个核心脚本每次运行写一行）+ 代码清理（共用函数只留一份，净减 151 行；anchor_price/tire_pack 两处死代码顺手清掉）+ `tests/` 647 个标准库测试 + 提示词 40 条不变（核心 28 + 进阶 12）+ 15 个脚本文件 |
| **V19** | ✅ 已落地（2026-11-07） | 七天快路径互动版（`scripts/fast_path.py`：每天 `--day N` 看任务清单（任务名 + 要产出什么 + 用哪个脚本/哪篇文档）、干完 `--done N` 打卡（带打卡时间戳，写 `--state` JSON 文件，重复打卡提示已打卡过不重复记）、`--progress` 汇总已完成/待完成/逾期三数（逾期 = 计划日期早于今天且未打卡，计划日期 = `--start` 第 1 天 + (N-1) 天；没给 `--start` 时不算逾期，明确提示未设开始日期）、`--list` 列 7 天总览；任务清单与 `docs/fast-path.md` 逐条对齐，不另编一套；`--help` 带真实例子，非法天数/非法日期给人话报错）+ `docs/fast-path-interactive.md`（用法 + 打卡状态格式 + 逾期定义 + 7 天总览表 + 2 份真实输出逐字贴）+ `docs/fast-path.md` 顶部补一行（交互版入口）+ `docs/00-getting-started.md` B 路第五步补一行（剩下 8 个脚本 → 9 个）+ `tests/` 226 个标准库测试 + 提示词 40 条不变（核心 28 + 进阶 12）+ 12 个脚本文件 |
| **V17** | ✅ 已落地（2026-11-07） | 葡语/阿语完整版 README（新增 `README_PT.md`（巴西葡语完整版）与 `README_AR.md`（阿语完整版，RTL 排版），内容与英文版对齐：章节结构、表格、代码命令、脚本名、文件名、版本号、数字全部一致；示例公司/价格/联系方式全是虚构的（【示例】前缀、sample.example 保留域）；`tests/` 167 个标准库测试 + 提示词 40 条不变（核心 28 + 进阶 12）+ 10 个脚本文件 |
| **V16** | ✅ 已落地（2026-11-07） | 催单话术库（`scripts/nudge.py`：D3/D7/D14/D30 × 已报价未回/已发样未回/已谈价未定共 12 条话术，WhatsApp 短版 + 邮件长版，中英对照；语气分档 D3 轻提醒、D7 问进度、D14 给台阶（降价/换规格/延账期三选一）、D30 最后通牒但留后路；Day 0 是报价/发样/谈价那天，与 followup_plan 的首触节奏锚点不同，同一客户同一线程只走一条线；`--channel whatsapp/email/both` / `--format json` / `--out`）+ `docs/nudge.md`（用法 + 跟进节奏衔接表 + 2 份真实输出逐字贴）+ `docs/00-getting-started.md` 的脚本清单补一行（剩下 6 个脚本 → 7 个）+ `tests/` 152 个标准库测试 + 提示词 40 条不变（核心 28 + 进阶 12）+ 10 个脚本文件 |
| **V15** | ✅ 已落地（2026-11-07） | 展会实战工具（`scripts/trade_show.py`：现场收的名片按兴趣度排会后 24 小时跟进计划——2 小时感谢 + 12 小时报价线索 + 24 小时电话追一次；`--add` 逐条加 + `--csv` 批量读，`--format json` / `--out`；首触草稿按 outreach_gen 的 T0/T1/T2 模板口径）+ `docs/trade-show.md`（用法 + 1 份真实输出逐字贴）+ `examples/trade_show_example.csv`（3 家示例，高/中/低各一）+ `docs/00-getting-started.md` 的脚本清单与 `docs/02-find-leads.md` 各补一行（展会收线索后的处理）+ `tests/` 127 个标准库测试 + 提示词 40 条不变（核心 28 + 进阶 12）+ 9 个脚本文件 |
| **V14** | ✅ 已落地（2026-11-07） | 到岸成本估算（`scripts/landed_cost.py`：FOB + 运费 + 保险 → CIF，再加关税 + 目的港杂费 → DDP；单条成本 + 总计 + 拟售价利润空间；`--qty` / `--format json` / `--audience client`）+ `docs/landed-cost.md`（用法 + 算法表 + 2 份真实输出逐字贴）+ `docs/00-getting-started.md` 与 `docs/06-quote.md` 各补一行（先用 quote_engine 报 FOB/CIF，再用 landed_cost 算到岸全成本）+ `tests/` 97 个标准库测试 + 提示词 40 条不变（核心 28 + 进阶 12）+ 8 个脚本文件 |
| **V12** | ✅ 已落地（2026-11-07） | 轮胎行业包（`scripts/tire_pack.py`：规格 + 市场 → GCC 认证要点 + 目的港清关单证 + 市场注意事项；4 个 TBR 规格 × 8 个市场）+ `docs/tire-pack.md`（用法 + 2 份真实输出逐字贴）+ `docs/00-getting-started.md` 补上脚本清单一行 + `tests/` 68 个标准库测试 + 提示词 40 条（核心 28 + 进阶 12）+ 7 个脚本文件 |
| **V11** | ✅ 已落地（2026-11-07） | 客户背调 Agent（`scripts/due_diligence.py`：L1/L2/L3 三级 + A/B/C 评级 + 红旗清单 + 客户视图 + JSON 输出）+ `docs/03-due-diligence.md` 十三节（真实输出逐字贴）+ 提示词 P03-5 + `tests/` 52 个标准库测试 + 提示词 40 条（核心 28 + 进阶 12）+ 6 个脚本文件 |
| **V10** | ✅ 已落地（2026-11-07） | 6 个进阶模块（08 独立站 / 09 社媒矩阵 / 10 展会 / 11 物流支付 / 12 风险合规 / 13 大客户）+ 三条学习路径 + 排障手册与贡献者协作流程 + 报价引擎加固（客户视图隔离、边界校验）+ `tests/` 30 个标准库测试 + 提示词 39 条（核心 27 + 进阶 12）+ 浏览器 Demo 打分与 Python 对齐 |
| **v0.1.5** | ✅ 已补充 | 零安装浏览器 Demo(index.html) + v0.2 报价引擎 alpha(quote_engine.py) + 品牌主张(MANIFESTO) + 上线推广清单(GITHUB_LAUNCH) |
| **v0.1** | ✅ 已完成 | 7 环节文档骨架 + 4 个 stdlib 业务脚本 + 27 条提示词 + 双语 README |
| **v0.2** | ✅ 已落地（alpha） | **AI 报价引擎**：`scripts/quote_engine.py` 已落地 —— 输入成本 + 市场 + 竞品锚价，输出 FOB/CIF 报价区间 + 三档让步阶梯（每步必须换条件）；客户视图隔离与边界校验已加固（见 `tests/test_quote_engine.py`） |
| **下一版** | 待定 | 下一版方向待定（七天快路径互动版已在 V19 落地） |
| **长期** | — | 行业包（轮胎、建材、机械、五金各自的环节细节）；多语言建联消息（法/俄，西/葡/阿已在 V13 落地）；真实线索集（脱敏后公开）；把报价引擎接到海关数据上做竞品锚价自动抓取 |

V20 不等下一版：10 轮打磨已经能直接用（坏 CSV 给人话报错不再 traceback、每次运行写一行 trace 日志、共用函数只留一份）。想跑不用等下一版——脚本已经在仓库里，647 个测试全绿。

---

## 参与方式

缺的不是文档数量，是不同国家的实战细节。轮胎在中东怎么跑第一笔单我写得出来；厄瓜多尔的建材渠道长什么样，我不知道；尼日利亚清关要哪几份文件，我不敢瞎写。这些只有当地做的人能补。

三种贡献方式，门槛从低到高：

1. 提 issue 纠错。看到错字、过时信息、说不清的判断标准，直接开 issue。一句话也行，比不说强。issue 模板会问你三个问题：哪一行看不懂、哪个数字没有来源、哪条在你所在的行业不适用。
2. 翻译环节文档。西班牙语、阿拉伯语、葡萄牙语、俄语、法语、越南语——你会哪个就翻哪个。六段结构别动，只换语言，术语在 [GLOSSARY.md](GLOSSARY.md) 里对齐就行。
3. 补你所在行业 / 国家的环节细节。这是最缺的。要求只有一条：写你真跑过的，别写你觉得应该这样的。具体到字段名、单证名、渠道结构、付款习惯、常见拒付理由。

代码也可以直接改，但硬约束是 Python 3.10+、零第三方依赖，理由见 CONTRIBUTING。

---

## 给开发者：可 hack、零依赖

14 个业务脚本（`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine` / `due_diligence` / `tire_pack` / `landed_cost` / `trade_show` / `nudge` / `anchor_price` / `fast_path` / `market_rules` / `daily_video_list` / `fulfillment_checklist`，再加脱敏自查脚本 `check_private_data.py`）只用 Python 标准库，一个第三方包都没有，你随便改、随便嵌：

- 想换打分权重？改 `lead_score.py` 顶部的 `CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W` 四个常量，满分还是 100。
- 想接自己的海关数据？CSV 表头对齐 `company,country,product,source,email,phone,years,contact,note`，直接喂进去。
- 想嵌进自己的工具链？每个脚本都能 `import`，`score_lead()` / `render()` / `plan_followups()` / `build_quote()` 都是纯函数，返回字典或列表，不碰网络、不写文件。
- CI 在 GitHub Actions 上跑 `py_compile` + 全部测试（Python 3.10–3.13）+ 脱敏门禁，改完提 PR 不会悄悄坏掉。

> 你不用信我说的。复制一份示例数据，跑一遍 `python3 scripts/lead_score.py my_leads.csv` 自己看结果——这玩意儿好不好使，30 秒就能验证，用不着我在这儿吹。

---

## 点个 star，当书签用也行

仓库还在更新（最后一次提交看下面的 badge）。觉得有用就点右上角 star——最大的用处其实是下次你想找的时候能翻出来。

我不群发、不私信、不要邮箱，也不会因为你点了 star 就给你发任何东西。

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[查看完整 Star History 趋势图](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## 多语言

README 有 12 种语言，网站界面也是这 12 种。各译本以英文版为准。

- [English](README_EN.md)（英语，完整版）
- [Español](README_ES.md)（西班牙语，starter，招募校对）
- [Português](README_PT.md)（巴西葡语，完整版）
- [Français](README_FR.md)（法语，完整版）
- [العربية](README_AR.md)（阿拉伯语，完整版，RTL 排版）
- [Русский](README_RU.md)（俄语，完整版）
- [Deutsch](README_DE.md)（德语，完整版）
- [日本語](README_JA.md)（日语，完整版）
- [한국어](README_KO.md)（韩语，完整版）
- [Türkçe](README_TR.md)（土耳其语，完整版）
- [Bahasa Indonesia](README_ID.md)（印尼语，完整版）

`docs/` 里的环节文档目前只有中文。你会哪种语言就翻哪篇，结构不变、术语对齐 [GLOSSARY.md](GLOSSARY.md)；母语者帮忙校对 README 也非常欢迎，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

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

**zero-to-trade** is an open-source workflow for people starting in foreign trade with zero experience. Seven stages, from picking a market to shipping an order, plus 15 Python script files — 14 business scripts and one privacy guard — that do the boring parts. Two minutes in a browser if you install nothing; about seven days at 1–2 hours a day to make your first real contact.

The premise: **AI does the heavy lifting, you make the calls.** Most tutorials tell you "you should do customer background research" and stop there. This repo tells you which three fields to check, which sites to check them on, and what result makes you drop the lead.

| Stage | What you do | Output |
|---|---|---|
| **01 Pick a market** | Score language, demand, and barrier | 1 first market + 3 reasons |
| **02 Find leads** | Customs data, social media, search, trade shows | ≥20 verified leads per day |
| **03 Vet the buyer** | L1 screen / L2 standard / L3 deep dive | A/B/C rating; fraud filtered out |
| **04 Make contact** | Tier leads T0-T3; run three channels on first touch | Tiered list + D0/D2/D5 follow-up plan (3 touches in 6 days) |
| **05 Talk specs** | Small asks first, price always last | Spec / quantity / destination port |
| **06 Quote & negotiate** | Quote discipline: every concession buys something | Quote sheet + concession ladder + scripts |
| **07 Deliver the order** | Contract, production, inspection, documents, payment, freight | Closed delivery loop + repurchase plan |

**30-second demo** (Python 3.10+, no third-party packages):

```bash
cp examples/leads_example.csv my_leads.csv
python3 scripts/lead_score.py my_leads.csv
```

Copy the sample data to your own file first — the `.example` suffix is there so nobody accidentally publishes their real customer list. Fill `my_leads.csv`, never the example file.

Ten sample leads come back tiered T0:2 / T1:5 / T2:1 / T3:2, each with its own next action.

**What makes it different:** discipline, not tooling. The rules are what carry value — T0 gets contacted today, T3 goes in the cold pool, a concession without a condition is a donation. Anything that can be an `if/else` lives in a script, anything that needs judgment lives in the docs, anything that needs to sound like a human lives in `prompts/`.

**Roadmap:** v0.1 (docs + scripts + 27 prompts) → v0.2 AI quoting engine → V19 (advanced modules, learning paths, 226 tests, 40 prompts, background-check agent, tire industry pack, multilingual outreach, landed cost estimation, trade show follow-up, nudge library, full Portuguese and Arabic READMEs, competitor anchor pricing, interactive 7-day fast path) → V20 (647 tests, local-increment merge, 10 hardening rounds: unified CLI, bad-CSV friendly errors, run tracing, shared helpers) → next: to be decided → long term: industry packs, more languages, real lead datasets.

**Contributing:** the biggest gap here is country-specific field detail. If you actually sell into a market this repo knows nothing about, that's the highest-value contribution you can make. Read [CONTRIBUTING.md](CONTRIBUTING.md).

MIT licensed. Questions, corrections, and contributions: [open an issue](https://github.com/6hn68/zero-to-trade/issues).
