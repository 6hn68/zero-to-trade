# 00·新手起步 Getting Started（零基础也能用）

> **本环节目标**：你不懂 git、不懂 Python，照这篇也能在 10 分钟内把项目跑起来、拿到第一份客户分级名单。
> **一句话原理**：文档负责「想清楚」，脚本负责「别手算」，提示词负责「不会写也能写」。

> **完全不想装 Python？** 项目里有个 `index.html`，**双击用浏览器打开**，把 CSV 粘进去点『开始分级』就能看 T0-T3，零安装零命令行。想本地跑脚本再往下看。

这份文档假设你是**完全的小白**：没装过 Python、没用过命令行、不知道 GitHub 是啥。会这些的可以直接跳到 [README](../README.md) 的 30 秒快速上手。

---

## 第一步：拿到项目文件（两种方法，选一个）

### 方法 A：下载压缩包（最简单，推荐小白）

1. 打开这个项目的 GitHub 页面（地址见仓库首页）。
2. 点右上角绿色按钮 **Code** → 选 **Download ZIP**。
3. 解压到任意文件夹，比如桌面。你会看到一个 `zero-to-trade-main` 文件夹（GitHub 默认分支叫 `main`，所以解压出来带 `-main` 后缀）。

### 方法 B：用 Git（以后想跟着更新再用）

装了 Git 之后在命令行跑：

```bash
git clone https://github.com/6hn68/zero-to-trade.git
```

> 小白暂时不用管方法 B。方法 A 够用。

---

## 第二步：装 Python（只做一次）

脚本是 Python 写的，电脑默认没有，要装一次。

1. 打开 [python.org](https://www.python.org/downloads/)，下 **3.8 或更高版本** 的安装包。
2. **安装时第一屏务必勾选 `Add Python to PATH`**（这步漏了，后面全报错，是最常见的新手坑）。
3. 一路 Next 装完。

验证装没装好：按 `Win + R`，输入 `cmd` 回车，在黑框里输：

```bash
python --version
```

跳出一行 `Python 3.x.x` 就是成功了。没跳出就重装一遍，记得勾 PATH。

> 如果 `python` 提示「不是内部或外部命令」，Windows 上往往只有微软商店版 `py`，那就改用 `py --version` 验证；后面所有命令里的 `python` 也都换成 `py` 即可。

---

## 第三步：跑第一个脚本（看效果）

1. 在刚才那个 `cmd` 黑框里，进到你解压的文件夹。比如你放桌面了：

   ```bash
   cd Desktop\zero-to-trade-main
   ```

   > 不会 `cd`？桌面路径不会错的话，也可以直接在文件夹地址栏输 `cmd` 回车，自动就在这个目录了。
   > 文件夹名以你解压出来的实际文件夹名为准（默认是 `zero-to-trade-main`，如果你下的是别的版本分支，名字会带对应后缀）。

2. 跑这条命令：

   ```bash
   python scripts/lead_score.py examples/leads_example.csv
   ```

3. 屏幕会吐出一张表，大概长这样（数字可能略有不同，公司名以你实际数据为准）：

   ```
   分级   公司                         国家                得分  下一步
   T0   【示例】海湾轮胎贸易                 Saudi Arabia      95  今天就发首触消息，别等
   T0   【示例】三角洲轮胎                  Saudi Arabia      92  今天就发首触消息，别等
   T1   【示例】阿曼蓝海                   Oman              77  排进本周，今天准备文案
   ...
   汇总: T0:2 / T1:5 / T2:1 / T3:2
   先回谁: 【示例】海湾轮胎贸易、【示例】三角洲轮胎
   ```

   > 上面表格里的公司名带「【示例】」前缀，是项目自带的脱敏演示数据。你跑自己 CSV 时，显示的就是你填的真公司名，数字也会随你的数据变化。

   到这步你就跑通了。**T0 那两家，就是今天该先打的人。**

---

## 第四步：填你自己的客户（真正用起来）

示例数据是公司编的，没用。换成你的真线索：

1. 打开 `examples/leads_example.csv`（双击，用 Excel 或记事本都能开）。
2. **文件最上面可能有一行 `#` 开头的注释别删**；真正的表头是 `company,country,...` 那一行，从表头**下面一行**开始填。只需要填 `company`（公司名）这一列就能运行，其他列有就填、没有空着。

   ```
   company,country,product,source,email,phone,years,contact,note
   张三贸易有限公司,沙特,truck tyres,search,zhang@xxx.com,+966...,8,采购经理,官网找到
   ```

3. `source` 这一列建议从下面 5 个里挑一个填，填别的也能跑但分数不准：
   - `referral` —— 别人介绍的（最可信）
   - `trade_show` —— 展会上认识的
   - `customs` —— 海关数据查到的
   - `linkedin` —— 领英上找的
   - `search` —— 搜索引擎随便找的（最泛）

4. 把文件另存成你的名字，比如 `my_leads.csv`，放在同一个文件夹里。
5. 跑：

   ```bash
   python scripts/lead_score.py my_leads.csv
   ```

---

## 第五步：生成开发信 + 排跟进

拿到 T0/T1 名单之后：

```bash
# 生成中英对照的建联文案（英文发、中文你审）
python scripts/outreach_gen.py my_leads.csv --tier T0

# 生成 7 天 3 次触达的跟进计划表
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv my_leads.csv
```

`--start` 换成你**实际发第一封的那天**，日期格式是 `年-月-日`。

每条脚本都支持 `--help`，输 `python scripts/lead_score.py --help` 能看到全部选项。

---

## 第六步：不会写英文？用提示词

开发信不会写、跟进不知道怎么接话，打开 `prompts/AI_PROMPTS.md`，里面 27 条提示词**直接复制粘贴给 ChatGPT / Claude 用**。把你的客户信息填进提示词里的占位符，AI 就替你写出可用的内容——效果和脚本差不多，只是手动。

---

## 常见报错（小白急救）

| 你看到的 | 原因 | 怎么办 |
|---|---|---|
| `'python' 不是内部或外部命令` | 没装 Python 或没勾 PATH | 重装，勾 Add to PATH |
| `can't open file` / `No such file` | 命令行不在项目目录 | 用 `cd` 进到项目文件夹，或地址栏输 `cmd` |
| `SyntaxError` | 脚本坏了（不太可能，除非你改过） | 重新下载项目 |
| 中文乱码 | 记事本存成了别编码 | 用 VS Code 或 Excel 开 CSV |

---

## 下一步

跑通之后，按这个顺序读文档，把方法吃透：

1. `docs/01-market-selection.md` —— 先选一个市场，别急着找客户
2. `docs/02-find-leads.md` —— 客户从哪来、怎么筛
3. `docs/03-due-diligence.md` —— 怎么分辨骗子（必读，能救钱）
4. `docs/04-outreach.md` 到 `07-order-delivery.md` —— 建联、聊单、报价、交付

**一句提醒**：脚本只帮你做「机械能判定的事」（有没有邮箱、来源可不可信、谁先打）。**值不值得花时间、怎么谈**，那部分在项目文档里，也在你自己脑子里。这分工别搞反了。
