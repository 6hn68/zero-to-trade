# 展会实战：名片收进来，会后 24 小时跟进计划排出去

> **这是什么**：展会结束不是结束，是 24 小时倒计时开始。展会上换的名片，拖过三天再联系，对方连你长什么样都忘了。这个脚本只干一件事：把展会上收到的展商按「兴趣度」排好队，每家给一张会后 24 小时跟进表（2 小时感谢 + 12 小时报价线索 + 24 小时电话追一次），并按 `outreach_gen.py` 的首触模板把第一封消息的草稿写出来。
>
> **先说清楚**：时间点只写相对时间（会后 2/12/24 小时），不编具体日期——展会哪天结束，你哪天跑脚本，T+0 就是那一天。第一封不报具体价格数字，报价线索那步也只给「确认规格再报价」的口子。

## 用法

```bash
# 展会现场收了一张名片，当场逐条加（一次命令加一家）
python scripts/trade_show.py --add "【示例】海湾轮胎贸易" --country "Saudi Arabia" --product "TBR 12.00R20" --interest 高 --email demo01@sample.example

# 回来批量读：展商 CSV（3 家示例，高/中/低各一）
python scripts/trade_show.py --csv examples/trade_show_example.csv

# 也可以直接拿线索示例 CSV 跑（没有 interest 列的行全按「低」处理）
python scripts/trade_show.py --csv examples/leads_example.csv

# JSON 输出，方便贴进表格或交给 AI 复核；--out 存成文件
python scripts/trade_show.py --csv examples/trade_show_example.csv --format json --out plan.json

# --csv 和 --add 可以混着用：先读 CSV，再补一家现场后补的名片
python scripts/trade_show.py --csv examples/trade_show_example.csv --add "【示例】后补的" --country Nigeria --product "TBR 11.00R20" --interest 高 --email extra@sample.example
```

`--help` 里有上面这些能直接复制的例子。联系方式邮箱/电话/WhatsApp 至少留一个，没留的排不进表（CSV 里这种行会被跳过并报出来，不是悄悄丢掉）。

## 展商 CSV 怎么填

列名与 `examples/leads_example.csv` 的 9 列口径对齐（`email`/`phone` 列也认）：

| 列名 | 必填？ | 填什么 |
|---|---|---|
| `company` | **必填** | 公司全名 |
| `country` | 建议填 | 国家（英文，如 Saudi Arabia） |
| `product` | 建议填 | 对方问过的产品（如 TBR 12.00R20） |
| `contact` | 建议填 | 联系方式（邮箱或电话）；**只写职位（如 purchasing manager）不算**，那是角色不是联系方式 |
| `interest` | 建议填 | 兴趣度：高/中/低（或 high/medium/low）；**不填按「低」处理**，宁可排后不硬抬优先级 |

现场填表只求快：公司名 + 一个联系方式 + 兴趣度三样齐了就能排；国家、产品回来再补也行。

## 会后 24 小时三档（每家都一样，缺一不可）

| 时间点 | 做什么 | 渠道 |
|---|---|---|
| 会后 2 小时内（T+2h） | 发感谢 + 展会资料（产品单页/规格表） | 有邮箱走邮箱，没邮箱走 WhatsApp/电话 |
| 会后 12 小时内（T+12h） | 发报价线索：请对方确认规格与月用量，再给报价区间意向 | 同上 |
| 会后 24 小时内（T+24h） | 电话/WhatsApp 追一次：只问一个 20 秒能答的问题（规格/用量/目的港） | 优先电话/WhatsApp，没留电话只能邮件追一次 |

只发感谢不跟报价等于白聊，只报价格不打电话等于等对方想起你。**止损线**：第 3 步追完仍无任何回应 → 停手，进长名单，季度扫一次；同一家 24 小时内别追两次。

## 兴趣度 → 首触模板（跟 outreach_gen 同一套话术）

| 兴趣度 | 分级 | 首触语气 |
|---|---|---|
| 高 | T0（立即建联） | 直接、具体，问规格和月用量 |
| 中 | T1（本周首触） | 轻、短，只问一个问题（今年还采不采购） |
| 低 | T2（低频培育） | 更轻，只求确认信息，不求回复 |

每家输出里都带两样东西：按这个模板写的首触草稿（主题行 + 英文正文），以及拿完整中英对照版的命令——`python scripts/outreach_gen.py <你的线索 CSV> --tier T0`（CSV 里 source 填 trade_show），完整版末尾还有发送前自查清单，先把 ✗ 项清掉再发。

## 真实输出样例：【示例】3 家展商（高/中/低各一）

命令：`python scripts/trade_show.py --csv examples/trade_show_example.csv`

```
============================================================================
  会后 24 小时跟进计划   共 3 家 · 高 1 家先打 · 中 1 家本周内 · 低 1 家只确认
  时间点是相对时间（T+0 = 展会结束那一刻）：T+2h / T+12h / T+24h
============================================================================

[1] 【示例】海湾轮胎贸易（Saudi Arabia）· 兴趣度 高 → T0（立即建联）· 联系：邮箱 demo01@sample.example
    产品：TBR 12.00R20
    会后 2 小时内（T+2h）· 邮箱：第 1/3 步
      做什么：发感谢 + 展会资料（产品单页/规格表）
      记住：一句话提展会上聊过的具体产品/规格，别群发同一版
    会后 12 小时内（T+12h）· 邮箱：第 2/3 步
      做什么：发报价线索：请对方确认规格与月用量，再给报价区间意向
      记住：只给「确认规格再报价」的口子，不报具体价格数字、不发价单
    会后 24 小时内（T+24h）· 邮箱（没留电话，只能邮件追一次）：第 3/3 步
      做什么：电话/WhatsApp 追一次：只问一个 20 秒能答的问题（规格/用量/目的港）
      记住：对方明确说不需要就停手，别在 24 小时内连追两次
    首触草稿（outreach_gen.py --tier T0 的首触模板（高→T0 / 中→T1 / 低→T2））：Subject: TBR 12.00R20 supply — 【示例】海湾轮胎贸易
      Hello,
      
      We met at the trade show and you asked about TBR 12.00R20. We make TBR 12.00R20 and ship to Saudi Arabia on a regular basis.
      
      What sizes and monthly volume are you running on TBR 12.00R20 at the moment?
    完整中英对照版：python scripts/outreach_gen.py examples/trade_show_example.csv --tier T0（CSV 里 source 填 trade_show）

[2] 【示例】迪拜轮毂行（UAE）· 兴趣度 中 → T1（本周首触）· 联系：电话 +000 00 000 0000
    产品：PCR 195/65R15
    会后 2 小时内（T+2h）· 电话/WhatsApp：第 1/3 步
      做什么：发感谢 + 展会资料（产品单页/规格表）
      记住：一句话提展会上聊过的具体产品/规格，别群发同一版
    会后 12 小时内（T+12h）· 电话/WhatsApp：第 2/3 步
      做什么：发报价线索：请对方确认规格与月用量，再给报价区间意向
      记住：只给「确认规格再报价」的口子，不报具体价格数字、不发价单
    会后 24 小时内（T+24h）· 电话/WhatsApp：第 3/3 步
      做什么：电话/WhatsApp 追一次：只问一个 20 秒能答的问题（规格/用量/目的港）
      记住：对方明确说不需要就停手，别在 24 小时内连追两次
    首触草稿（outreach_gen.py --tier T1 的首触模板（高→T0 / 中→T1 / 低→T2））：Subject: PCR 195/65R15 — one quick question
      Hello,
      
      We met at the trade show and talked about PCR 195/65R15. One quick question: is PCR 195/65R15 still something you source from Asia this year?
    完整中英对照版：python scripts/outreach_gen.py examples/trade_show_example.csv --tier T1（CSV 里 source 填 trade_show）

[3] 【示例】尼罗河商贸（Egypt）· 兴趣度 低 → T2（低频培育）· 联系：电话 +000 00 000 0000
    产品：PCR tubes
    会后 2 小时内（T+2h）· 电话/WhatsApp：第 1/3 步
      做什么：发感谢 + 展会资料（产品单页/规格表）
      记住：一句话提展会上聊过的具体产品/规格，别群发同一版
    会后 12 小时内（T+12h）· 电话/WhatsApp：第 2/3 步
      做什么：发报价线索：请对方确认规格与月用量，再给报价区间意向
      记住：只给「确认规格再报价」的口子，不报具体价格数字、不发价单
    会后 24 小时内（T+24h）· 电话/WhatsApp：第 3/3 步
      做什么：电话/WhatsApp 追一次：只问一个 20 秒能答的问题（规格/用量/目的港）
      记住：对方明确说不需要就停手，别在 24 小时内连追两次
    首触草稿（outreach_gen.py --tier T2 的首触模板（高→T0 / 中→T1 / 低→T2））：Subject: 【示例】尼罗河商贸 — PCR tubes sourcing check
      Hello,
      
      We met at the trade show. I am updating my notes on Egypt importers of PCR tubes — is 【示例】尼罗河商贸 still sourcing PCR tubes from Asia this year? One word is enough.
    完整中英对照版：python scripts/outreach_gen.py examples/trade_show_example.csv --tier T2（CSV 里 source 填 trade_show）

  止损线：第 3 步（T+24h）追完仍无任何回应 → 停手，进长名单，季度扫一次；同一家 24 小时内别追两次。
  下一步：T+2h 那封发出去后，按 followup_plan.py 排 D0/D2/D5 的后续节奏。
============================================================================
```

## 跟其他脚本的配合

- **展会收线索**：先按 [02·找客户](02-find-leads.md) 第 5 步从展会名录筛一遍，现场收到的名片当天就用本脚本录进去，别等回公司再凭记忆补。
- **首触全文**：本脚本给的是草稿 + 命令；完整中英对照版跑 `outreach_gen.py`（见上表），CSV 里 source 填 trade_show。
- **24 小时之后**：T+2h 那封发出去后，按 `followup_plan.py` 排 D0/D2/D5 的后续节奏（`--tier T0 --start <首触实际发送日>`）。
- **不是展会来的线索**：走 `lead_score.py` 分级（T0–T3），别硬塞进本脚本——本脚本的排序只认展会现场的兴趣度。

## 常见报错

| 你看到的 | 原因 | 怎么办 |
|---|---|---|
| `错误：名单是空的。` | 既没给 `--csv` 也没给 `--add` | 逐条加一家，或批量读一个 CSV（例子在 `--help` 里） |
| `错误：「XX」没留任何联系方式……` | 这家邮箱/电话/WhatsApp 一个都没留 | 展会现场当场补一个再记；CSV 里这种行会被跳过并报出来 |
| `错误：兴趣度只能填 高/中/低……` | 填了认不出的词（如「很高」「urgent」） | 改成 高/中/低（或 high/medium/low）；不填按「低」处理 |
| `错误：邮箱格式不对……` | 邮箱缺 @ 或缺域名后缀 | 改成 someone@sample.example 这种样子 |
| `错误：找不到文件「XX」。` | CSV 路径拼错了 | 检查路径；Windows 上可以直接把文件拖进终端 |
| `提示：X 条没填 interest，按「低」处理` | CSV 里有行没填 interest 列 | 不是报错；想提优先级就回去把 interest 补成 高/中 |
| `跳过一行：……没留任何联系方式` | CSV 里有行没留联系方式 | 不是报错；那行没进表，补上联系方式再跑 |
