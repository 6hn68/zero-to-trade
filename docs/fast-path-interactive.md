# 7 天快路径互动版：看任务、打卡、看进度

> **这是什么**：`docs/fast-path.md` 那篇 7 天快路径是纸上的清单，这个脚本是它的互动版——
> 每天跑一条命令看当天要干什么，干完打一次卡，进度随时能汇总。
> 任务清单与 `docs/fast-path.md` 逐条对齐，脚本没有另编一套任务。
>
> **先说清楚**：脚本只管「动作有没有做」——打卡、算进度、提醒逾期。
> 它不负责「回复来了没有」，那是结果，不是动作。收到回复这事看产品、看时机、还得看运气，
> 7 天跑完的交付物还是 `docs/fast-path.md` 最后那份可验收清单（≥20 行 CSV、分级表、
> 至少 5 封已发出的首触、跟进计划表、三个数字 + 3 行复盘、一份档案）。

## 用法

```bash
# 看当天任务：任务名 + 要产出什么 + 用哪个脚本/哪篇文档
python scripts/fast_path.py --day 1

# 列 7 天总览：每天标题 + 状态（已打卡 / 逾期 / 待完成）
python scripts/fast_path.py --list

# 设第 1 天日期，再给第 1 天打卡（日期是【示例】，换成你自己的开始日期）
python scripts/fast_path.py --start 2026-11-09 --done 1

# 只打卡（第 1 天日期已设过就不用再给 --start）
python scripts/fast_path.py --done 3

# 看进度：已完成几天 / 待完成几天 / 逾期几天
python scripts/fast_path.py --progress

# 进度 + 设第 1 天（没设过开始日期时，先给 --start 再看进度才有逾期数）
python scripts/fast_path.py --progress --start 2026-11-02

# 打卡状态换个文件存（默认 fast_path_state.json，当前目录）
python scripts/fast_path.py --done 3 --state /tmp/fast_path_state.json
```

`--help` 里有上面这些真实例子。所有命令都在仓库根目录跑（能同时看到 `scripts/` 和 `examples/` 的那一层）。
示例里的日期全部虚构，不含真实公司名。

## 打卡状态存在哪

默认写当前目录的 `fast_path_state.json`，长这样（`--state` 可换路径）：

```json
{
  "start": "2026-11-02",
  "done": {
    "1": "2026-11-07T19:30:00",
    "2": "2026-11-07T19:30:01",
    "3": "2026-11-07T19:30:02"
  }
}
```

- `start`：第 1 天日期（`--start YYYY-MM-DD` 设的；只给 `--start` 时只保存日期，不打卡）。
- `done`：键是天数（"1"–"7"），值是打卡时间戳。
- 同一天重复打卡会提示「已打卡过」，不重复记，第一次的打卡时间戳不动。
- `--day` / `--list` / `--progress` 只读不写，不会凭空造出状态文件；`--day` 看的那天没打卡过就显示「未打卡」。

## 逾期是怎么算的

第 N 天的计划日期 = 第 1 天日期 + (N-1) 天。计划日期早于今天且未打卡，就是逾期。
没给 `--start` 时不算逾期，`--progress` 会明确提示「未设开始日期」——先跑
`python scripts/fast_path.py --start 2026-11-09`（换成你自己的第 1 天）再看进度。

逾期不是失败，是提醒：先把逾期那天的任务补上，再往下走，别跳过。

## 7 天总览：每天干什么、用哪处

| 天 | 干什么 | 用哪个脚本 / 哪篇文档 |
|---|---|---|
| Day 1 | 定 1 个市场 + 找 10–15 条线索 | `docs/01-market-selection.md`、`docs/02-find-leads.md` |
| Day 2 | 背调 + 补联系方式 + 自动分级 | `docs/03-due-diligence.md`、`scripts/lead_score.py` |
| Day 3 | 首触（硬底线，必须发出去） | `scripts/outreach_gen.py`、`docs/04-outreach.md` |
| Day 4 | 探渠道 + 继续补线索，今天不发正式消息 | `scripts/followup_plan.py`、`docs/04-outreach.md` |
| Day 5 | 第 2 次触达（D2）+ 给新冒出来的 T0/T1 发一轮 | `scripts/followup_plan.py`、`scripts/lead_score.py`、`scripts/outreach_gen.py` |
| Day 6 | 写好第 3 封信 + 收尾复盘 | `docs/04-outreach.md`、`docs/fast-path.md` |
| Day 7 | 收官：发第 3 次触达（D5）+ 把结果存成档案 | `scripts/followup_plan.py`、`scripts/lead_score.py`、`docs/fast-path.md` |

首发在 Day 3，之后按「首发当天 / 首发后第 2 天 / 首发后第 5 天」触达 3 次，落到 Day 3 / Day 5 / Day 7。
Day 4 只探渠道不发正式消息，D2 是 Day 5；Day 7 发完第 3 次就停手，不要发第 4 次。

## 真实输出样例 1：【示例】`--day 1`（还没打卡）

命令：`python scripts/fast_path.py --day 1 --state /tmp/fast_path_state.json`

```
Day 1 · 定 1 个市场 + 找 10-15 条线索（≤2 小时）
内容来源：docs/fast-path.md Day 1，任务清单与它逐条对齐。
状态：未打卡
1. 定 1 个首站：照三维法（语言 / 需求 / 壁垒）挑 1 个国家，写 3 条理由
   产出：1 个国家 + 3 条理由
   用哪处：docs/01-market-selection.md
2. 按四路（海关数据 / 社媒 / 搜索 / 展会）找线索，今天只要 10-15 条；先攒公司名 + 国家 + 来源就成，邮箱电话 Day 2 再补
   产出：10-15 条线索
   用哪处：docs/02-find-leads.md
3. 整理成 CSV 存仓库根目录：表头 company,country,product,source,email,phone,years,contact,note；source 只能填 referral / trade_show / customs / linkedin / search 其中一个
   产出：my_leads.csv（≥10 行，每行 company 都有值）
   用哪处：docs/02-find-leads.md
过关标准：一个 ≥10 行的 CSV，company 列每行都有值，source 列每行都是上面五个合法值之一。
```

## 真实输出样例 2：【示例】`--progress`（第 1 天 2026-11-02，已打卡 Day 1–3，今天 2026-11-07）

命令：`python scripts/fast_path.py --progress --state /tmp/fast_path_state.json`
（打卡前先跑了 `--start 2026-11-02 --done 1`、`--done 2`、`--done 3`）

```
7 天快路径进度（今天：2026-11-07）
第 1 天：2026-11-02
已完成 3 天 / 待完成 4 天 / 逾期 2 天
已打卡：Day 1、Day 2、Day 3
逾期：Day 4（计划 2026-11-05）、Day 5（计划 2026-11-06）
逾期不是失败，是提醒：先把逾期那天的任务补上，再往下走，别跳过。
```

Day 4、Day 5 的计划日期（2026-11-05、2026-11-06）早于今天且未打卡，所以逾期 2 天；
Day 6 的计划日期就是今天（2026-11-07），还没过期，不算逾期。

## 常见报错

| 报错 | 意思 | 怎么办 |
|---|---|---|
| `天数不对：第 0 天不存在。7 天快路径只有 Day 1 到 Day 7` | `--day` / `--done` 给了 1–7 以外的数 | 换成 1–7，比如 `--day 1` |
| `天数不对：「abc」不是数字。7 天快路径只有 Day 1 到 Day 7` | 天数不是数字 | 换成数字，比如 `--done 3` |
| `日期不对：「2026-13-01」不是 YYYY-MM-DD 格式` | `--start` 的日期写错了 | 换成真实日期，比如 `--start 2026-11-09` |
| `没给动作：加 --day N 看当天任务……` | 一个动作参数都没给 | 加 `--day N`、`--list` 或 `--progress`；先看 `--help` 也行 |
| `打卡状态文件 …… 读不出来` | `--state` 指定的文件损坏了 | 删掉它重打一次卡就行，任务清单不受影响 |

## 跟其他脚本的配合

先用这个脚本认领每天的任务，再用当天那行写明的脚本干活：
Day 2 跑 `lead_score.py` 分级、Day 3 跑 `outreach_gen.py` 生成首触文案、
Day 4、Day 5、Day 7 按 `followup_plan.py` 的 D0/D2/D5 节奏走。
Day 3 有人回复、开始谈价要报价时，读 `docs/05-negotiation.md`，报价前先跑
`scripts/anchor_price.py` 锚价（见 `docs/06-quote.md`）。
