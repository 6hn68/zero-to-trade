# 催单话术库：报价/发样/谈价之后，对方不回，你说什么

> **这是什么**：报价发出去了、样品寄出去了、价格谈到一半了——然后对方没了动静。这个脚本只干一件事：按「过去了几天 × 卡在哪一步」给你一封现成的话术，WhatsApp 短版 + 邮件长版，中英对照（英文发、中文你审）。
>
> **先说清楚**：Day 0 是报价发出去、样品寄出去、或者价格谈起来的那一天，不是首触那天。D3/D7/D14/D30 四档语气一天比一天重，但 D30 也不撕破脸——明说这是最后一封，同时留一句「以后有需要随时找我」。

## 用法

```bash
# 报价发出去 3 天没回：轻提醒（只确认收到没有，不问决定）
python scripts/nudge.py --day D3 --scenario quoted

# 样品寄出去 7 天没回：问进度（只出 WhatsApp 短版）
python scripts/nudge.py --day D7 --scenario sampled --channel whatsapp

# 价格谈了 14 天没定：给台阶（三选一），填上自己的客户和产品
python scripts/nudge.py --day D14 --scenario negotiating --company "【示例】海湾轮胎贸易" --contact Alex --product "TBR 12.00R20"

# 30 天没回：最后通牒但不撕破脸；JSON 输出，存成文件
python scripts/nudge.py --day D30 --scenario quoted --format json --out nudge.json
```

`--help` 里有上面这些能直接复制的例子。`--day` 和 `--scenario` 必填，缺了给人话报错，不裸奔。`--channel` 默认两者都出（`whatsapp` / `email` / `both`）。示例公司/联系人/产品全是虚构的（【示例】前缀），往外发之前必须换成真的。

## 四档语气（一天比一天重）

| 天数 | 语气 | 这封在干什么 |
|---|---|---|
| D3 | 轻提醒 | 只确认对方收到没有（报价/样品有没有到），不问决定、不施压 |
| D7 | 问进度 | 问进展到哪一步，给对方一个「一句话就能回」的口子 |
| D14 | 给台阶 | 降价 / 换规格 / 延账期三选一，对方不用自己想办法下台 |
| D30 | 最后通牒但不撕破脸 | 明说这是最后一封，之后停手；同时留一句「以后有需要随时找我」 |

## 三个场景（卡在哪一步）

| 场景 | 意思 | 话术盯着什么问 |
|---|---|---|
| `quoted` | 已报价未回 | 报价收到了吗、价格/规格要不要改 |
| `sampled` | 已发样未回 | 样品到了吗、测试得怎么样 |
| `negotiating` | 已谈价未定 | 价格谈到哪一步、差在哪一项 |

## 跟 followup_plan.py 怎么分工（两套节奏不打架）

| 脚本 | 管哪一段 | Day 0 是哪天 |
|---|---|---|
| `followup_plan.py` | 报价之前：首触后的触达表 | 首触发出去那天（T0 D0/D2/D5、T1 D0/D3/D6、T2 D0/D7/D14） |
| `nudge.py` | 报价/发样/谈价之后：催单话术 | 报价发出去、样品寄出去、价格谈起来那天 |

同一客户同一线程只走一条线：报价前走 `followup_plan.py`，报价后走 `nudge.py`，别两边同时发。D3 对上 T1 的 D3、D7 对上 T2 的 D7 只是天数巧合——锚点不同（首触日 vs 报价日），不要把两个 D3 当成同一天。T2 的 D14 是归档日（那天不发信），`nudge.py` 的 D14 只发给已经报价/发样/谈价过的客户，不发给冷线索。

**止损线**：D30 发完仍无任何回应（含已读不回）→ 停手，进长名单，季度扫一次（跟 `followup_plan.py` 的止损线同口径）。

## 真实输出（逐字贴，下面两份都是脚本亲手跑出来的）

第一份：`python scripts/nudge.py --day D3 --scenario quoted`

```
============================================================================
  催单话术  D3 · quoted（已报价未回）  ·  语气：轻提醒
  客户：【示例】海湾轮胎贸易（联系人 Alex）· 产品：TBR 12.00R20
============================================================================

[WhatsApp 短版 — 直接复制发]

  EN:
  Hi Alex, just checking in — did the quote for TBR 12.00R20 reach you all right? Happy to resend it or adjust the sizes if anything looks off.

  中文对照:
  Alex 你好，冒昧打扰一下——TBR 12.00R20 的报价收到没有？要是没收到或者规格想调整，我再发你一版。

[邮件长版 — 主题行 + 正文]

  Subject: Quick check — your TBR 12.00R20 quote from 【示例】海湾轮胎贸易
  主题（中文对照）: 确认一下——【示例】海湾轮胎贸易 发的 TBR 12.00R20 报价收到了吗

  EN:
  Hi Alex,
  
  Hope you are doing well. I sent over the quote for TBR 12.00R20 a few days ago and wanted to make sure it landed in the right inbox — sometimes attachments get caught in spam.
  
  If the prices or sizes need tweaking, just tell me which line and I will rework it. No rush at all.
  
  Best regards

  中文对照:
  Alex 你好，
  
  前几天发了 TBR 12.00R20 的报价，想确认一下有没有收到——附件有时会被当成垃圾邮件。
  
  价格或规格想改的话，告诉我是哪一行，我重新给你算一版。不着急，等你方便的时候回就行。
  
  祝好

----------------------------------------------------------------------------
  止损线：D30 发完仍无任何回应（含已读不回）→ 停手，进长名单，季度扫一次。
  衔接：Day 0 是报价/发样/谈价那天，不是首触那天。报价前走 followup_plan.py （T0 D0/D2/D5、T1 D0/D3/D6、T2 D0/D7/D14），报价后走本脚本，同一客户同一线程只走一条线，别两边同时发。
  复现：python scripts/nudge.py --day D3 --scenario quoted --company '【示例】海湾轮胎贸易' --contact Alex --product TBR 12.00R20
============================================================================
```

第二份：`python scripts/nudge.py --day D14 --scenario negotiating --company "【示例】海湾轮胎贸易" --contact Alex --product "TBR 12.00R20"`

```
============================================================================
  催单话术  D14 · negotiating（已谈价未定）  ·  语气：给台阶（降价 / 换规格 / 延账期三选一）
  客户：【示例】海湾轮胎贸易（联系人 Alex）· 产品：TBR 12.00R20
============================================================================

[WhatsApp 短版 — 直接复制发]

  EN:
  Hi Alex, we have been going back and forth on TBR 12.00R20 for two weeks, so let me put three options on the table: (1) a lower price if the first order is smaller, (2) a different size/spec at a lower cost, or (3) longer payment terms while the price stays. Pick one, or tell me what would actually close it.

  中文对照:
  Alex 你好，TBR 12.00R20 的价格来回谈了两周，我把三个选择摆出来：(1) 首单小一点、价格降一点；(2) 换规格、换个成本低的型号；(3) 价格不动、账期放长。你选一个，或者直接告诉我怎样才算谈成。

[邮件长版 — 主题行 + 正文]

  Subject: Three options to close the TBR 12.00R20 price
  主题（中文对照）: 谈成 TBR 12.00R20 的价格，三个选择

  EN:
  Hi Alex,
  
  We have been going back and forth on the TBR 12.00R20 price for two weeks, so let me put three options on the table:
  
  1. Lower price — a smaller first order at a lower unit price; you test us small, we earn the bigger orders later.
  2. Different size/spec — swap to a size or spec that costs less; I will re-quote the same day.
  3. Longer payment terms — the price stays where it is, but the payment terms stretch out.
  
  Pick one, or tell me plainly what would actually close it — a straight answer helps us both more than another round.
  
  Best regards

  中文对照:
  Alex 你好，
  
  TBR 12.00R20 的价格来回谈了两周，我把三个选择摆出来：
  
  1. 降价——首单小一点、单价降一点，先小批量试试，大单以后再说。
  2. 换规格——换个成本低的规格或型号，我当天重新报价。
  3. 延账期——价格不动，账期给你放长一点。
  
  你选一个，或者直接告诉我怎样才算谈成——一句实在话，比再绕一圈对两边都有用。
  
  祝好

----------------------------------------------------------------------------
  止损线：D30 发完仍无任何回应（含已读不回）→ 停手，进长名单，季度扫一次。
  衔接：Day 0 是报价/发样/谈价那天，不是首触那天。报价前走 followup_plan.py （T0 D0/D2/D5、T1 D0/D3/D6、T2 D0/D7/D14），报价后走本脚本，同一客户同一线程只走一条线，别两边同时发。
  复现：python scripts/nudge.py --day D14 --scenario negotiating --company '【示例】海湾轮胎贸易' --contact Alex --product TBR 12.00R20
============================================================================
```

## 常见报错

| 你看到的 | 原因 | 怎么办 |
|---|---|---|
| `天数只能是 D3 / D7 / D14 / D30` | `--day` 填了 D5 之类的值 | 只填 D3 / D7 / D14 / D30（`3`、`d7` 这种写法也收） |
| `场景只能是 quoted / sampled / negotiating` | `--scenario` 拼错了 | 三个场景：`quoted`（已报价未回）/ `sampled`（已发样未回）/ `negotiating`（已谈价未定）；别名 `quote` / `sample` / `price` 也收 |
| 缺 `--day` / `--scenario` 被拦住 | 这两个是必填的 | 照 `--help` 里的例子抄一条，两个都填上 |
