# 00·新手起步 Getting Started（零基础也能用）

> **这是什么**：一套开源的「外贸操作系统」，把从 0 到第一单拆成 **7 步**：选市场、找客户、背调、建联、聊单、报价、交付。每步配一篇文档告诉你怎么想，一个脚本替你算，一组提示词替你写——你只要会复制粘贴就成。
> **跑完这篇你能拿到**：一张**排好优先级的客户名单**（谁今天先打、谁这周打、谁暂时别碰），外加一份能直接发出去的英文开发信草稿。
> **要花多久**：**A 路**（不装任何东西，只用浏览器）约 **2 分钟**；**B 路**（装 Python、跑脚本）**首次约 20 分钟**，大半时间在等下载，装好以后每次 30 秒。

> **⏱ 只有 2 分钟？直接走这里**：解压后双击**根目录**的 `index.html` → 浏览器打开（不用联网、不用装任何东西）→ 点『**载入示例**』→ 点『**开始分级**』，立刻看到 T0–T3。**不装 Python、不碰命令行。** 看完想长期用，再回来往下读。

> **原理就一句**：文档帮你把脑子理清，脚本帮你别手算，提示词帮你不会写也能写。三样你都不用亲自动手——不对，脑子还是得你自己动。

这份文档假设你是个纯小白：Python 没装过，命令行没碰过，GitHub 是啥都不知道。这些你都会的话，直接跳 [README 的 30 秒快速上手](../README.md#30-秒快速上手)，别在这页耗着。

---

## 开始前：我需要准备什么？（先把心理负担卸掉）

| 你可能正在担心的 | 答案 |
|---|---|
| **我没有公司，能做吗** | 能。找客户、背调、写开发信这些活儿，压根不需要公司主体，个人身份一样跑。真到报价、签合同（06/07 步）再注册公司都来得及——不少人第一单都跑完了，公司还没注册呢。 |
| **要花钱吗** | 项目加自带的 4 个脚本，全免费、开源，不依赖任何第三方库，一分钱不用充。后面可能要花钱的地方（海关数据、展会、认证）都排在 01–02 步，而且每一处都给了不花钱的替代做法。 |
| **我英语差，能做吗** | 能。对外英文文案由 `scripts/outreach_gen.py` 和 `prompts/AI_PROMPTS.md` 直接出成稿，你的活是「审」不是「写」。只要能看懂 TBR / PCR / FOB / CIF 这类关键词就够，其余术语都收在 [GLOSSARY.md](../GLOSSARY.md)。 |
| **我不懂技术，能做吗** | 能。A 路全程点鼠标；B 路只要会复制粘贴，本文每条命令都给了能直接复制的版本，还按 Windows / macOS / Linux 分开列好了。 |
| **我还没有客户名单** | 不用有。项目自带一份脱敏示例数据，先拿它跑通全流程，再换成你自己的。 |

---

## 两条路径，选一条

| | **A 路 · 浏览器 Demo** | **B 路 · 本地脚本** |
|---|---|---|
| 要不要装东西 | **完全不用** | 装一次 Python（约 15–20 分钟） |
| 要不要命令行 | 不用 | 要，但只需复制粘贴 |
| 能干什么 | 只做「线索分级 T0–T3」这一件事 | 分级 + 生成开发信 + 排跟进计划 + 报价测算，共 4 个脚本 |
| 结果能存下来吗 | 看得到，不方便存 | 能存成 `.md` / `.csv` / `.json` 文件 |
| 适合谁 | 先看看这项目值不值得花时间 | 打算真的用它跑客户 |

> 两条路用的是同一套评分逻辑，结果一模一样。建议先走 A 路确认这玩意儿有用，再决定要不要花 20 分钟折腾 B 路。

---

## A 路：只用浏览器，2 分钟看到结果

1. 解压下载下来的压缩包（怎么下载见下面「B 路第一步：拿到项目文件」）。
2. 打开解压出来的文件夹，**双击 `index.html`**（它在根目录，跟 `README.md` 同一层）。会用默认浏览器打开，**不用联网、不上传任何数据**。
3. 点『**载入示例**』按钮——示例 CSV 会自动填进上面的输入框（也可以自己把 CSV 内容粘进去）。
4. 点『**开始分级**』，下方立刻出 T0–T3 分级表。

**A 路到此结束。** 想生成开发信、跟进计划、报价，就得走 B 路。

---

## B 路第一步：拿到项目文件（两种方法，选一个）

### 方法 A：下载压缩包（最简单，推荐小白）

1. 浏览器打开 <https://github.com/6hn68/zero-to-trade>。
2. 点右上角绿色按钮 **Code** → 选 **Download ZIP**。
3. 解压到任意文件夹，比如桌面。你会看到一个 **`zero-to-trade-main`** 文件夹（GitHub 默认分支叫 `main`，所以解压出来带 `-main` 后缀）。**A 路双击的 `index.html` 就在这个文件夹里，B 路的全部命令也都要在这个文件夹里执行。**

### 方法 B：用 Git（以后想跟着更新再用）

装了 Git 之后在命令行跑：

```bash
git clone https://github.com/6hn68/zero-to-trade.git
cd zero-to-trade
```

> clone 完**必须再 `cd zero-to-trade`** 进项目文件夹，不然后面每条命令都跟你报「找不到文件」。
> 小白暂时不用管方法 B，方法 A 够用。

---

## B 路第二步：装 Python（只做一次）

脚本是 Python 写的，电脑默认没有，要装一次。

1. 打开 [python.org/downloads](https://www.python.org/downloads/)，下 **3.8 或更高版本** 的安装包（macOS 用户选 macOS 版 `.pkg`）。
2. Windows 安装第一屏**务必勾上 `Add Python to PATH`**（漏了这步后面全报错，新手翻车第一原因）。macOS / Linux 不用管这步。
3. 一路 Next 装完。

### 打开命令行（三个系统各说一遍）

| 系统 | 怎么打开 |
|---|---|
| **Windows** | 按 `Win + R` → 输入 `cmd` → 回车。（也可以用 PowerShell，命令完全一样） |
| **macOS** | `Command + 空格` → 输入 `Terminal` → 回车 |
| **Linux** | `Ctrl + Alt + T` |

### 验证装没装好

在刚打开的窗口里，**依次试这三条，哪一条蹦出 `Python 3.x.x` 就用哪一条**：

```bash
python --version
```

```bash
python3 --version
```

```bash
py --version
```

**关键：记住你成功的是哪一个，本文后面所有命令里的 `python` 都换成它。**（例如你只有 `py` 能用，那 `python scripts/lead_score.py ...` 就要写成 `py scripts/lead_score.py ...`。）

三条全都不出版本号 = Python 没装上或没勾 PATH，重装一遍，记得勾 `Add Python to PATH`。

> `py` 是 Windows 自带的 Python 启动器，macOS / Linux 上没有，试不出来是正常的。
> macOS 预装的 Python 2 已淘汰，请务必自己装 3.8+；本文一律用 `python3` 指代 macOS / Linux 上的命令。

---

## B 路第三步：跑第一个脚本（看效果）

### 1. 进到项目文件夹

先说怎么判断自己在哪：命令行有个「当前目录」的概念，所有脚本命令都得在能看到 `scripts` 和 `examples` 这两个文件夹的那一层跑（就是 `zero-to-trade-main` 这层，里面应该同时有 `README.md`、`index.html`、`scripts/`、`examples/`）。

进目录的三条命令，**按你的系统挑一条**（路径中的反斜杠/正斜杠不要互换，macOS / Linux 一律用正斜杠 `/`）：

```bash
# Windows（cmd / PowerShell）—— 假设解压到了桌面
cd Desktop/zero-to-trade-main
```

```bash
# macOS —— 假设解压到了桌面，把 YourName 换成你的用户名
cd /Users/YourName/Desktop/zero-to-trade-main
```

```bash
# Linux —— 假设解压到了桌面
cd ~/Desktop/zero-to-trade-main
```

**确认自己进对了**，跑一条：

```bash
# Windows 用这条
dir
```

```bash
# macOS / Linux 用这条
ls
```

看到列表里同时出现 `scripts` 和 `examples` 就对了。没有的话，看下面的「不会 cd 怎么办」。

> **不会 `cd`？两条更省事的办法（推荐）**
> - **Windows**：打开解压后的文件夹，在**地址栏**里直接输入 `cmd` 回车，黑框就自动停在这个目录了（PowerShell 同理，输 `powershell`）。
> - **macOS / Linux**：把文件夹**直接拖进终端窗口**回车，`cd` 命令会自动填好。
> - 文件夹名以你解压出来的实际名称为准（默认 `zero-to-trade-main`，别的分支会带别的后缀）。桌面若被 OneDrive 接管，`cd Desktop/...` 可能找不到，用上面两条办法可以绕开。

### 2. 跑第一条命令

```bash
# Windows
python scripts/lead_score.py examples/leads_example.csv
```

```bash
# 如果上一条报「不是内部或外部命令」，换成启动器
py scripts/lead_score.py examples/leads_example.csv
```

```bash
# macOS / Linux
python3 scripts/lead_score.py examples/leads_example.csv
```

> 路径一律用正斜杠 `/`（`scripts/lead_score.py`）。写成 `scripts\lead_score.py` 在 macOS / Linux 的终端里直接失效。

### 3. 你会看到的真实输出（复制自实际运行结果）

```
==========================================================================
  线索分级结果  共 10 条
==========================================================================
分级   公司                         国家                得分  下一步
--------------------------------------------------------------------------
T0   【示例】海湾轮胎贸易                 Saudi Arabia      95  今天就发首触，别等
T0   【示例】三角洲轮胎                  Saudi Arabia      92  今天就发首触，别等
T1   【示例】阿曼蓝海                   Oman              77  排进本周，今天准备文案
T1   【示例】半岛汽车                   Saudi Arabia      71  排进本周，今天准备文案
T1   【示例】尼罗河商贸                  Egypt             67  排进本周，今天准备文案
T1   【示例】迪拜轮毂行                  UAE               65  排进本周，今天准备文案
T1   【示例】利雅得汽配                  Saudi Arabia      60  排进本周，今天准备文案
T2   【示例】尼日利亚先锋                 Nigeria           46  进 B 池，每天固定时段扫一遍
T3   【示例】黎凡特供配                  Lebanon           20  信息不足，先补联系方式/需求再打
T3   【示例】利雅得零件店                 Saudi Arabia      10  信息不足，先补联系方式/需求再打
--------------------------------------------------------------------------
汇总: T0:2 / T1:5 / T2:1 / T3:2

先回谁: 【示例】海湾轮胎贸易、【示例】三角洲轮胎
先打谁: 【示例】阿曼蓝海、【示例】半岛汽车、【示例】尼罗河商贸、【示例】迪拜轮毂行、【示例】利雅得汽配

下一步: 用 outreach_gen.py 按这份分级生成建联文案。
==========================================================================
```

> 上面那些带「【示例】」前缀的公司名，是项目自带的脱敏演示数据，不对应任何真实企业——你要在现实里真撞见同名，那纯属巧合。换成你自己的 CSV 后，显示的就你填的公司名，分数也跟着你的数据走。

到这步你就跑通了。T0 那两家，就是今天该先打的人。

---

## B 路第四步：填你自己的客户（真正用起来）

示例数据是用来跑通的，换成你的真线索才有意义。

1. 打开 `examples/leads_example.csv`（双击，Excel、记事本、VS Code 都能开）。
2. **文件最上面有一行 `#` 开头的注释，别删**（删了也能跑，但建议留着）；真正的表头是 `company,country,...` 那一行，**从表头下面一行开始填**。格式照抄下面这行（这是一份脱敏示例，换成你自己的真实信息）：

   ```
   company,country,product,source,email,phone,years,contact,note
   【示例】某海湾贸易公司,Saudi Arabia,TBR 12.00R20,referral,demo01@sample.example,+966 11 000 0000,18,purchasing manager,Annual RFQ for truck tyres
   ```

3. **至少填 `company` + `country` + `source` 三列**，否则分数上不去：只填 `company` 一列确实能跑通（实测两条线索都判 T3 / 10 分），但拿不到 T0/T1。
   - `country` 请填**英文国名**（`Saudi Arabia`、`UAE`、`Egypt`…）。项目里的国家筛选 `--country` 是按英文子串匹配的，填中文「沙特」会筛不出来。
   - `source` 建议从下面 5 个里挑一个填，填别的也能跑但分数不准：
     - `referral` —— 别人介绍的（最可信）
     - `trade_show` —— 展会上认识的
     - `customs` —— 海关数据查到的
     - `linkedin` —— 领英上找的
     - `search` —— 搜索引擎随便找的（最泛）

4. **另存成 `my_leads.csv`，放在项目根目录**（就是跟 `scripts` 文件夹**同级**的那层，不是放进 `examples/` 里）。放错位置会报 `can't open file`。保存时编码选 **UTF-8**。
5. 跑（同样按你的系统挑一条）：

   ```bash
   # Windows
   python scripts/lead_score.py my_leads.csv
   ```

   ```bash
   # Windows（python 不通时用）
   py scripts/lead_score.py my_leads.csv
   ```

   ```bash
   # macOS / Linux
   python3 scripts/lead_score.py my_leads.csv
   ```

---

## B 路第五步：剩下 3 个脚本（开发信 / 跟进 / 报价）

拿到 T0/T1 名单之后，下面三条按你的系统把 `python` 换成对应命令（`py` 或 `python3`），**都在项目根目录执行**：

```bash
# 2. 生成中英对照的建联文案（英文发、中文你审）
python scripts/outreach_gen.py my_leads.csv --tier T0

# 3. 生成 7 天 3 次触达的跟进计划表
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv my_leads.csv

# 4. (alpha) 报价引擎：成本 + 海运费 + 目标毛利 → FOB/CIF 区间 + 三档让步阶梯
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

- `--start` 换成你**实际发第一封的那天**，格式 `年-月-日`（上面 `2026-10-08` 只是示例日期）。
- `--cost 28 --freight 6 --margin 15` 换成你的真实成本（USD/件）、到港海运费（USD/件）、目标毛利（%）。这一步在 06 报价那篇里才用得上，现在可以先跳过。
- 想**把结果存成文件**而不是只看一眼（两条均已实测能写盘）：
  - `lead_score.py` 末尾加 `--format json --out result.json`
  - `followup_plan.py` 末尾加 `--format csv --out my_plan.csv`
  - 任何脚本想把屏幕输出存下来，还有一个通用办法：命令末尾加 ` > 文件名.md`（例如 `python scripts/outreach_gen.py my_leads.csv --tier T0 > my_outreach.md`）。

**每个脚本都支持 `--help`**，跑不通或想看全部选项，先试：

```bash
python scripts/lead_score.py --help
```

---

## B 路第六步：不会写英文？用提示词

开发信不会写、跟进不知道怎么接话，打开 [prompts/AI_PROMPTS.md](../prompts/AI_PROMPTS.md)，里面 27 条提示词，复制了贴给 ChatGPT / Claude 用就行。把客户信息填进提示词里的占位符，AI 就替你写出能用的内容——效果和脚本差不多，就是得你自己动手。

---

## 常见报错（小白急救）

| 你看到的 | 原因 | 怎么办 |
|---|---|---|
| `'python' 不是内部或外部命令` / `command not found: python` | 没装 Python，或装了没勾 PATH | `python --version`、`python3 --version`、`py --version` **三条依次试**，哪条出版本号就用哪条；都不行就重装并勾 `Add Python to PATH` |
| `can't open file '...\scripts\scripts\lead_score.py'`（注意出现两遍 `scripts`） | 多进了一层目录 | 退回上一层：Windows 用 `cd ..`，再 `dir` 确认能同时看到 `scripts` 和 `examples` |
| `can't open file '...\my_leads.csv'` | CSV 没放在根目录，或被放进了 `examples/` | 把 `my_leads.csv` 挪到跟 `scripts` 同级的项目根目录 |
| `No such file or directory` | 命令里的路径写错了，或用了反斜杠 | 路径一律用正斜杠 `/`；确认当前目录对不对（见第三步的 `dir` / `ls`） |
| 分级表里**全是 T3 / 10 分** | 只填了公司名，没填国家、来源、邮箱 | 至少补上 `country`（英文）和 `source`，见第四步第 3 点 |
| 中文公司名显示成乱码 | CSV 存成了 GBK / ANSI | 用 VS Code 或 Excel 另存为 **UTF-8**（带不带 BOM 都能正常读） |
| 用 Excel 打开 CSV 后所有列挤在一格 | Excel 按本地习惯用了 `;` 分隔 | 编辑用 VS Code 或「记事本」；Excel 导入时手动选逗号分隔 |
| `SyntaxError` | 脚本被改动过或下载不完整 | 重新下载项目，别手改 `.py` 文件 |
| Windows 上输入 `python` 弹出微软商店 | 系统没识别已安装的 Python | 改用 `py` 开头的命令；或在「设置 → 应用 → 应用执行别名」里关掉 Python 的商店别名 |

---

## 卡住了怎么办（按顺序试这三步）

1. **先问脚本自己**：跑 `python scripts/<脚本名>.py --help`，选项和用法都写在里面。
2. **再查对应文档**：命令跑通了但不知道下一步该干嘛 → 看下面的阅读顺序；不认识某个术语（TBR / FOB / 40HQ…）→ 查 [GLOSSARY.md](../GLOSSARY.md)；想看一整单从头到尾怎么串 → 看 [deal-walkthrough.md](deal-walkthrough.md)。
3. **还是不行就提 Issue**：到 <https://github.com/6hn68/zero-to-trade/issues> 提一条，把「你的系统（Windows/macOS/Linux）+ 你跑的完整命令 + 完整的报错文字」三样贴上去就够。这种「我按文档做但卡在这步」的 issue，项目其实挺欢迎的——你卡住的这步，往往就是文档该改的地方（见 [CONTRIBUTING.md](../CONTRIBUTING.md)）。**别在 issue 里贴真实客户公司名和联系方式**，不然脱敏这事儿就白做了。

---

## 下一步：我该先读哪一篇

**先建立全局感**（5 分钟）：看 [README 的「7 环节总览」表](../README.md#7-环节总览)，7 步各做什么、每步产出什么，一屏看完。

**再按这个顺序读**（跑通脚本之后）：

1. [01-market-selection.md](01-market-selection.md) —— 先选一个市场，别急着找客户
2. [02-find-leads.md](02-find-leads.md) —— 客户从哪来、怎么筛
3. [03-due-diligence.md](03-due-diligence.md) —— 怎么分辨骗子（**必读，能救钱**）
4. [04-outreach.md](04-outreach.md) → [05-negotiation.md](05-negotiation.md) → [06-quote.md](06-quote.md) → [07-order-delivery.md](07-order-delivery.md) —— 建联、聊单、报价、交付

**如果你急着想先拿到结果**，不建议按上面慢慢读，直接走 [fast-path.md](fast-path.md)（7 天，从 0 到收到第一封真人回复，每天 1–2 小时）。

提醒一句，别搞反分工：脚本只干「机器能判定的活儿」——有没有邮箱、来源可不可信、谁先打。至于值不值得花时间、怎么谈，那是文档里的，也是你自己脑子里的。脚本替不了你谈单，它连电话都不接。
