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

# 每天早上：一张清单，今天该跟谁、为什么、说什么（Daily list: who, why, what to say）
python scripts/nudge.py --list followups.json --today 2026-11-22
# JSON 输出，接进你自己的表格；--channel email 改出邮件长版
python scripts/nudge.py --list followups.json --today 2026-11-22 --format json
```

`--help` 里有上面这些能直接复制的例子。`--day` 和 `--scenario` 只在单条模式下必填（`--list` 模式不用填），缺了给人话报错，不裸奔。`--channel` 默认两者都出（`whatsapp` / `email` / `both`）。示例公司/联系人/产品全是虚构的（【示例】前缀），往外发之前必须换成真的。

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

## 每天一张清单：`--list` / One daily list

**One list each morning: who, why, what to say. / 每天早上跑一次：今天该跟谁、为什么、说什么。**

单条模式是一次拿一封；`--list` 是一次看完全部客户：给它一个 JSON 文件，里面是每个客户的 Day 0（报价/发样/谈价那天）和已经发过哪几档，它算出每个人下一档该哪天发，吐出一张今天的清单——逾期的排最前面、标 `⚠ OVERDUE`；今天到期的其次；还没到的告诉你还有几天；D30 发完仍无回音的标停手、进长名单。

**The JSON file / 清单文件长这样**（公司名、联系人、产品全是虚构示例，【示例】前缀，真用之前换成自己的；这个文件是你自己的跟进台账，真实客户信息不进仓库）：

```json
{"followups": [
{"company": "【示例】海湾轮胎贸易", "contact": "Alex",
"product": "TBR 12.00R20", "scenario": "quoted",
"day0": "2026-11-10", "sent": ["D3"],
"size": "12.00R20", "market": "saudi"},
{"company": "【示例】尼罗河商贸", "contact": "Sara",
"product": "TBR 11.00R20", "scenario": "sampled",
"day0": "2026-11-19", "sent": []}
]}
```

文件也可以直接是一个 JSON 列表（`[{...}, {...}]`，不用包 `{"followups": [...]}` 那层）。字段说明 / Fields：

| 字段 / Field | 填不填 / Required? | 说明 / Notes |
|---|---|---|
| `company` | 必填 | 客户公司名 |
| `day0` | 必填 | 报价/发样/谈价那天，`YYYY-MM-DD`；写未来日期会被跳过 |
| `scenario` | 必填 | `quoted` / `sampled` / `negotiating`（别名 `quote` / `sample` / `price` 也收） |
| `contact` / `product` | 选填 | 不填就用虚构示例值（清单里会标出来，发送前换成真的） |
| `sent` | 选填 | 已经发过的档，如 `["D3"]`；不填当没发过 |
| `size` / `market` / `li` / `speed` | 选填 | 填了就链上 `tire_pack.py`，清单里贴规格包摘要 + 缺项（见下） |

**How the list is sorted / 清单怎么排：**

| 状态 / Status | 意思 / Meaning | 位置 / Order |
|---|---|---|
| `OVERDUE` / 过期了 | 该发的档已经过了 X 天还没发 | 最前，逾期越久越靠前，标 `⚠` |
| `DUE TODAY` / 今天就发 | 该发的档就是今天 | 其次 |
| `NOT YET DUE` / 还没到 | 下一档还没到，告诉你还有几天 | 再其次 |
| `STOPPED` / 已停手，进长名单 | D3/D7/D14/D30 全发完了仍无回音 | 最后，不给话术，只给止损线 |

下一档按 D3 → D7 → D14 → D30 顺序走，不跳档：比如发过 D3，下一档就是 D7，哪怕已经过了 D7 那天，也先补 D7、不直接跳 D14。D30 发完仍无任何回应（含已读不回）就停手，进长名单，季度扫一次——跟上面止损线同口径。

**Each row says three things / 每行三句话：** 谁（公司/联系人/产品）+ 为什么（报价/发样/谈价过去 X 天，一直没回）+ 说什么（现成的 WhatsApp 短版，英文在前、中文在后，复制就能发；邮件主题行也附上）。`--channel email` 改出邮件长版；`--format json` 出整张清单的 JSON，接进你自己的表格；`--out today.txt` 存成文件；`--today 2026-11-22` 可以指定"今天是哪天"（默认就是今天，测试、补算旧账时用）。

**The daily routine / 每天的用法就两步：** (1) 早上跑一次 `python scripts/nudge.py --list followups.json`（可加 `--out today.txt` 存档）；(2) 发完一档后，把该档加进那家的 `sent`（比如发完 D7 就写成 `["D3", "D7"]`），第二天清单自动推下一档。`sent` 靠手动更新——脚本不记你发没发，它只认文件里写的。

**Chained to the spec pack / 顺带链上规格包：** 清单里每家填了规格 + 市场，就会贴上 `tire_pack.py` 出的规格包一句话摘要（规格 → 市场；GCC 适用/不适用；单证数 + 当地程序；免责句）+ 规格包缺项（哪些值用了常见值、哪些没核实）。规格写错了只记一行 `pack_error`，不拖垮整张清单；没填规格/市场的那家不贴包、不报错。

**Bad rows do not kill the list. / 坏行不炸整单：** 缺公司名、缺 `day0`、`day0` 在未来、场景写错、日期格式错的行，都进清单末尾"跳过的行"，其余家照常出——先修好那行再跑。

**Real output / 真实输出**——命令 / Command：`python scripts/nudge.py --list followups.json --today 2026-11-22`（用的就是上面那个两家客户的 JSON 文件）：

```
============================================================================
  Today's follow-ups / 今天该跟谁  (2026-11-22)
  OVERDUE 1 — act first / 先处理过期的 1 家  ·  DUE TODAY 1 / 今天到期 1 家  ·  NOT YET 0 / 还没到 0 家  ·  STOPPED 0 / 已停手 0 家
============================================================================

⚠ OVERDUE 5 days / 过期了 5 天 — 【示例】海湾轮胎贸易 (contact Alex) · TBR 12.00R20
  Next / 下一步：D7 · 问进度
  Why / 为什么：Quote sent 12 days ago, no reply since / 报价发出 12 天，一直没回
  Spec pack / 规格包：12.00R20 → 沙特 (Saudi Arabia); GCC applies / 适用; 5 docs (SASO / SABER); 须以官方最新要求为准、发货前复核。
  Pack gaps / 规格包缺项：load index: not given, using common value 154/151 for 12.00R20 (not verified against the manufacturer datasheet) / 载重指数：没填，用了 12.00R20 的常见值 154/151（未按厂家数据表核实）; speed rating: not given, using common value K for 12.00R20 (not verified against the manufacturer datasheet) / 速度级别：没填，用了 12.00R20 的常见值 K（未按厂家数据表核实）
  Say this on WhatsApp / WhatsApp 这样发：
  EN: Hi Alex, following up on the TBR 12.00R20 quote — has anything changed on your side, or is there a question I can answer? If the timing is not right, just say so and I will check back later.
  中文对照：Alex 你好，跟进一下 TBR 12.00R20 的报价——你那边有什么新情况，或者有什么问题我可以解答？要是现在时机不对，直说就行，我过段时间再来问。
  Email subject / 邮件主题：Any update on the TBR 12.00R20 quote?

DUE TODAY (D3) / 今天就发（D3） — 【示例】尼罗河商贸 (contact Sara) · TBR 11.00R20
  Next / 下一步：D3 · 轻提醒
  Why / 为什么：Sample sent 3 days ago, no feedback since / 样品寄出 3 天，一直没反馈
  Say this on WhatsApp / WhatsApp 这样发：
  EN: Hi Sara, just checking in — has the TBR 11.00R20 sample arrived? Keen to hear how it looks and feels on your side.
  中文对照：Sara 你好，TBR 11.00R20 的样品到了吗？想听听你那边看上去、手感怎么样。
  Email subject / 邮件主题：Did the TBR 11.00R20 sample arrive?

----------------------------------------------------------------------------
  Stop rule / 止损线：D30 发完仍无任何回应（含已读不回）→ 停手，进长名单，季度扫一次。
  Day 0 is the day the quote went out / sample shipped / price talk started — not the first-touch day. / Day 0 是报价/发样/谈价那天，不是首触那天。
============================================================================
```

读法 / How to read it：顶部四类计数先告诉你今天的盘子——过期 1 家、今天到期 1 家。`【示例】海湾轮胎贸易` 报价 12 天前发出，只发过 D3，所以下一档 D7 已经过期 5 天，`⚠` 置顶，话术是 D7 的"问进度"，还顺带贴了沙特规格包摘要 + 2 项缺项（载重指数、速度级别都用了常见值）。`【示例】尼罗河商贸` 样品寄出刚好 3 天，D3 今天到期。发完记得把档位写进 `sent`，不然明天它还在同一档上。

停手的那家这样显示 / What a stopped row looks like（同一份清单里加一家 D3/D7/D14/D30 全发完的，亲手跑过）：

```
STOPPED — long list / 已停手，进长名单 — 【示例】大西洋轮胎 (contact Musa) · TBR 11.00R20
  Next / 下一步：— · —
  Why / 为什么：Quote sent 38 days ago, no reply since / 报价发出 38 天，一直没回
  Stop / 停手：D30 发完仍无任何回应（含已读不回）→ 停手，进长名单，季度扫一次。
```

没有话术、没有"下一步"——这家已经发完四档，清单只提醒你别再发了，季度扫一次就行。

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
| 缺 `--day` / `--scenario` 被拦住 | 单条模式下这两个必填 | 照 `--help` 里的例子抄一条，两个都填上；要每天一张清单就跑 `--list followups.json`（清单模式不用填这两个） |
| `错误：打不开「…」：No such file or directory` | `--list` 指的文件不存在（退出码 1） | 先确认文件在不在、路径写没写对 |
| `错误：「…」不是合法 JSON` | 清单文件不是合法 JSON（退出码 1） | 修好 JSON 再跑；报错里写了第几行、错在哪 |
| `错误：「…」里没找到 followups 列表` | 文件里没有 `followups` 键（退出码 1） | 文件该是 `{"followups": [...]}`，或者直接是一个 JSON 列表 `[{...}]` |
| `Rows skipped / 跳过的行`（清单末尾） | 某行缺公司名 / 缺 `day0` / `day0` 在未来 / 场景写错 / 日期格式错 | 坏行只进末尾清单，其余家照常出；按提示修好那行再跑 |
