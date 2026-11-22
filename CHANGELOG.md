# 更新日志 Changelog

## 版本表（以实测为准，2026-11-17）

| 版本 | 测试数 |
|---|---|
| V10 | 30 |
| V11 | 52 |
| V12 | 68 |
| V13 | 80 |
| V14 | 97 |
| V15 | 127 |
| V16 | 152 |
| V17 | 167 |
| V18 | 187 |
| V19 | 219 |
| V20 | 251 |

脚本数在 V19 到 12 个（11 个业务脚本 + 1 个脱敏自查脚本），V20 不变。

> 订正：V20 发版时写 250，发版后补丁多 1 个测试，2026-11-17 实测 `python3 -m unittest discover -s tests` 共 251 个全绿；219 是 V19 全库总数，不是 V12–V19 新增之和；52 是 V11 全库总数。本文以下各节保留发版时的原始数字作历史记录，当前数字以本表为准。


> 记改了什么、不记打算改什么。

## V20 · 2026-11-14

### 本地增量合并 + 10 轮打磨（本次核心）

- 合并：线上 V19（`aefce53`）为底，本地快照的增量并进 `merge/local-increments` 分支（未推）：文档“入库四标准 / 证据三档 / 谈判四招”等 7 处增量 + 6 个新文件（AGENTS.md、CLAUDE.md、docs/README.md、docs/trace-format.md、examples/README.md、scripts/README.md）+ 三个核心脚本恢复运行日志 / 单条模式 / `--start-date` 别名；219 个测试全绿。待拍板三件事：LICENSE 署名、跟进节奏、LED 示例去处（第 4 轮已解决：做成 `examples/leads_example_lighting.csv`）。
- 第 1 轮 CLI 入口统一：12 个脚本都用 `_ZhArgumentParser`（中文报错），8 个必填参数脚本无参时打印 usage + 中文提示，退出码 2；`check_private_data.py` 补 `--help`。
- 第 2 轮测试补强：单条模式、`--start-date` 别名、三个脚本的运行日志补测试，219 → 226 个。
- 第 3 轮文档数字一致性：测试数与脚本总行数同步到五版 README、ROADMAP、AGENTS.md 与 `tests/test_readme_i18n.py`（226 个测试、约 6,400 行）；FAQ 里“业务脚本不写文件”订正为“不写业务文件，三个脚本只记运行日志”。
- 第 4 轮非轮胎示例：本地 8 条 LED 灯线索做成 `examples/leads_example_lighting.csv`（新表头），分布 T0:0/T1:2/T2:2/T3:4；`examples/README.md` 说明 LED 最高只到 T1 的原因（品类词只认轮胎词，不是 bug）。
- 第 5 轮演示页与 V19 同步：`index.html` 加“载入 LED 示例”按钮与 12 脚本一览卡片；JS 计分与 Python 逐项同分（node 校验）。
- 第 6 轮输入校验与友好报错：outreach_gen 与 followup_plan 的 `--csv` 补接 `LeadDataError`（缺列 / 空文件 / 找不到文件不再 traceback）；`read_leads` 加 `strict=True`，未闭合引号报人话错；测试 230 → 237 个。
- 第 7 轮提示词对齐：P04-4 跟进命令补 `--avoid-weekend`（周五避让是可选项，不加不避，实测 D2 会落在周六）；P10-2 窗口统一 48 小时（标题 48、正文原写 24）；其余脚本引用逐条验过都是对的。
- 第 8 轮日志落地：按 `docs/trace-format.md`，三个核心脚本每次运行在 `logs/trace-YYYY-MM-DD.jsonl` 写一行（trace_id / ts / tool / input / output / duration_s / error）；输入只记文件名 basename，公司名不记；`trace-*.jsonl` 已进 `.gitignore`。
- 第 9 轮代码清理：`_ZhArgumentParser` 11 份、`setup_log` 3 份、`_width` / `_pad` / `money` / `fmt` / `_clean` / `_is_filled` 各并成一份放 `lead_score.py`，净减 151 行；due_diligence 的 parser 是特制的，留在原地；anchor_price 的 `_width` / `_pad` 与 tire_pack 的 `_width` 是死代码，直接删掉。
- 第 10 轮收尾发版：版本号升到 V20，五版 README 与 ROADMAP 数字同步（250 个测试、约 6,300 行），按 `docs/dev-flow-ai.md` 做 Final Reviewer 全量检查：全量测试 250 个全绿 + diff 逐行复查 + 验收标准打勾。

### 文档与数字

- 五版 README 与 ROADMAP：版本表新增 V20 当前版，V19 降为已落地；测试 226 个 → **250 个**，提示词 40 条不变，脚本 12 个不变；脚本总行数约 6,400 行 → **约 6,300 行**（实测 6,320 行）；`tests/test_readme_i18n.py` 的版本号与数字同步到 V20 / 12 个脚本 / 250 个测试；`AGENTS.md` 的测试数同步到 250 个；`docs/dev-flow-ai.md` 与 `docs/decisions/ADR-001-plan-gate-downgrade.md` 的行数同步到约 6,300 行。

## V19 · 2026-11-07

### 七天快路径互动版（本次核心）

- 新增 `scripts/fast_path.py`（只用标准库，不联网）：把 `docs/fast-path.md` 的 7 天任务清单变成能打卡的脚本，任务与文档逐条对齐、不另编一套。`--day N` 打印当天任务清单（任务名 + 要产出什么 + 用哪个脚本/哪篇文档）；`--done N` 打卡（带打卡时间戳，写入 `--state` 指定的 JSON 文件，默认 `fast_path_state.json`，重复打卡提示“已打卡过”不重复记）；`--progress` 汇总已完成/待完成/逾期三数（逾期 = 计划日期早于今天且未打卡，计划日期 = `--start` 第 1 天日期 + (N-1) 天；没给 `--start` 时不算逾期，明确提示“未设开始日期”）；`--list` 列 7 天总览（每天标题 + 状态）；`--start YYYY-MM-DD` 设第 1 天日期（只给 `--start` 时只保存日期不打卡）；`--help` 带真实例子；非法天数/非法日期/没给动作都给人话报错、不裸奔。示例内容全部虚构（【示例】前缀），不含真实公司名。基准：【示例】第 1 天 2026-11-02、已打卡 Day 1–3、今天 2026-11-07 → 已完成 3 天 / 待完成 4 天 / 逾期 2 天（Day 4 计划 2026-11-05、Day 5 计划 2026-11-06）。
- 新增 `tests/test_fast_path.py`（32 个测试）：Day 1–7 各打印对应任务且标题不串、每条任务都带“产出”和“用哪处”、非法天数（0/8/非数字）与非法日期（月份/日期/自由文本）报错、打卡写入与重复打卡提示（第一次打卡时间戳不动）、进度汇总三数（用临时 state 文件，不污染仓库）、逾期判定（用 `--start` 设过去的日期：9 天前开始、只打卡 Day 1 → 逾期 6 天；今天开始 → 逾期 0 天）、`--list` 总览与打卡状态、`--help` 带真实例子、无参数给人话报错、`--day` 不凭空造出状态文件。`python3 -m unittest discover -s tests`：219 个测试全绿（原来 187 个 + 新增 32 个）。
- 新增 `docs/fast-path-interactive.md`：用法、打卡状态文件格式、逾期定义、7 天总览表（每天干什么、用哪个脚本/哪篇文档）、2 份真实输出逐字贴（【示例】`--day 1`、【示例】`--progress`，均已与脚本重新跑一遍逐字核对）、常见报错表、跟其他脚本的配合（Day 2 跑 `lead_score.py`、Day 3 跑 `outreach_gen.py`、Day 4/5/7 按 `followup_plan.py` 的 D0/D2/D5 节奏走）。

### 文档与数字

- 五版 README 与 ROADMAP：脚本文件 11 个 → **12 个**（11 个业务脚本 + 1 个脱敏自查脚本），测试 187 个 → **219 个**，提示词 40 条不变；目录结构补进 `fast_path.py`；版本表新增 V19 当前版，V18 降为已落地；“下一版”仍为方向待定（七天快路径互动版已在 V19 落地，不再占位）；五版 README 里残留的旧脚本数（英文版 “eleven scripts”、西语版 “11 scripts”、葡语版 “dez arquivos de script”、阿语版 “أحد عشر سكربتًا”等）一并同步到 12 个；英文/葡语/阿语版里残留的“十个业务脚本”一行同步到 11 个业务脚本（含 `fast_path`）；葡语版一行残留的“十个脚本文件”同步到 12 个。
- `docs/fast-path.md` 顶部补一行指向新脚本（交互版入口）；`docs/00-getting-started.md` 的 B 路第五步补上 `fast_path.py` 一行（剩下 8 个脚本 → 9 个）；`docs/learning-paths.md` 的脚本数同步到 12 个；`docs/dev-flow-ai.md` 里的脚本总行数同步（约 5,600 行 → 约 6,100 行，实测 6,084 行）；`tests/test_readme_i18n.py` 的版本号与数字同步到 V19 / 12 个脚本 / 219 个测试。

## V18 · 2026-11-07

### 竞品锚价（本次核心）

- 新增 `scripts/anchor_price.py`（只用标准库，不联网）：输入海关数据竞品价区间（最低价 `--comp-low`、最高价 `--comp-high`、中位价 `--comp-median`）+ 自家 FOB 成本 `--cost` + 运费 `--freight`（可选关税率 `--duty`），输出进取/中位/保守三档 CIF 锚价（中位价 × 97% / 100% / 103%），每档写清毛利、毛利率、FOB 对等价、隐含加成与适用场景；报出去之前先过成本、运费、汇率、付款条件、有效期 5 项复核清单（`--verified cost,freight,fx,payment,validity` 逐项打勾，任一项待核就标出来提醒）。口径与 `quote_engine.py` / `landed_cost.py` 逐字同一套（成本基数 = FOB 成本 × (1 + 不可预见费 3%)，保本 CIF = (成本基数 + 运费) ÷ (1 − 1.10 × 保险费率)，毛利率按售价算），同一组数字三边算出的 CIF 必须一致，测试里有交叉核对。竞品价低于自家成本时明确警告“低于成本，别接单或先谈量换价”；缺中位价时按（最低+最高）/2 估算并注明是估算值；`--format json` / `--audience client`（客户版只给三档报价与适用场景，不露成本、毛利、FOB 对等价、复核清单；JSON 版连 `meta.inputs` 一起删，跟 `quote_engine.py` / `landed_cost.py` 同一个脱敏口径）；`--help` 带 5 个亲手跑过的真实例子；缺参数/非法输入给人话报错、不裸奔。示例价格全部虚构（【示例】前缀）。基准：【示例】竞品 38–46 / 中位 42、成本 28 + 运费 6 + 关税 10% → 三档 CIF 40.74 / 42.00 / 43.26，保本 CIF 34.90，中位价毛利 7.10、毛利率 16.91%、隐含加成 24.59%。
- 新增 `tests/test_anchor_price.py`（20 个测试）：两组数字手算逐项核对（三档价格/毛利/毛利率/FOB 对等价/隐含加成/DDP 价）、三档全低于成本与仅进取价低于成本两档警告、缺中位价估算（中位价 50.00 是估算值）、复核清单 5 项齐全（默认全待核、部分打勾、全部打勾、中文别名、非法项报错）、JSON 双视图隔离、表格客户视图不露成本/毛利/复核清单、与 `quote_engine` / `landed_cost` 的 CIF 交叉核对（中位价档 FOB 35.93 经 `landed_cost` 得 CIF 42.00，经 `quote_engine` 加成 24.59% 得 FOB 35.93 / CIF 42.00）、缺参数/非法输入给人话报错、`--help` 带真实例子。`python3 -m unittest discover -s tests`：187 个测试全绿（原来 167 个 + 新增 20 个）。
- 新增 `docs/anchor-price.md`：用法、算法表、锚价指南（什么时候用中位价、什么时候用进取价、低于成本怎么办）、2 份真实输出逐字贴（【示例】正常锚价表格版内部视图、【示例】低于成本警告表格版内部视图，均已与脚本重新跑一遍逐字核对）、客户视图说明、跟其他脚本的配合（先用 `anchor_price.py` 定三档，再用 `quote_engine.py` 出正式报价单，最后用 `landed_cost.py` 算到岸全成本）、常见报错表。

### 文档与数字

- 五版 README 与 ROADMAP：脚本文件 10 个 → **11 个**（10 个业务脚本 + 1 个脱敏自查脚本），测试 167 个 → **187 个**，提示词 40 条不变；目录结构补进 `anchor_price.py`；版本表新增 V18 当前版，V17 降为已落地；“下一版”仍为方向待定（竞品锚价已在 V18 落地，不再占位）；五版 README 里残留的旧脚本数（英文版 “ten scripts”、西语版 “10 scripts”、葡语版 “dez scripts”、阿语版 “عشرة سكربتات”等）一并同步到 11 个；英文/葡语/阿语版里残留的“六个业务脚本”一行同步到 10 个业务脚本（含 `landed_cost` / `trade_show` / `nudge` / `anchor_price`）。
- `docs/06-quote.md` 补一行指向新脚本（报价前先锚价）；`docs/learning-paths.md` 的脚本数同步到 11 个；`docs/dev-flow-ai.md` 里的脚本总行数同步（约 5,100 行 → 约 5,600 行，实测 5,624 行）；`tests/test_readme_i18n.py` 的版本号与数字同步到 V18 / 11 个脚本 / 187 个测试。

## V17 · 2026-11-07

### 葡语/阿语完整版 README（本次核心）

- 新增 `README_PT.md`（巴西葡语完整版，284 行）与 `README_AR.md`（阿语完整版，288 行，RTL 排版）：内容与 `README_EN.md` 全文对齐——章节结构、表格、代码命令、脚本名、文件名、版本号、数字（脚本 10 个、测试 167 个、提示词 40 条）全部一致；阿语版文件顶部加 `dir="rtl"` 方向说明，代码块、命令、文件名、数字保持 LTR 不翻；葡语版按巴西葡语口径（目标市场含巴西）；两版示例公司/价格/联系方式全是虚构的（【示例】前缀、sample.example 保留域），不含真实公司名；两版各含快速开始、脚本清单、7 步流程、FAQ 关键章节。
- 新增 `tests/test_readme_i18n.py`（15 个测试）：五版 README 的版本号都是 V17、V17 行为当前版、脚本数/测试数/提示词数三处数字一致、PT/AR 两版含关键章节标题（快速开始、脚本清单、7 步流程、FAQ）、阿语版含 RTL 标记、两版含【示例】标记与 sample.example、README.md 语言导航含 PT/AR 链接。`python3 -m unittest discover -s tests`：167 个测试全绿（原来 152 个 + 新增 15 个）。

### 文档与数字

- 五版 README 与 ROADMAP：README 由三版 → **五版**（新增葡语/阿语完整版），测试 152 个 → **167 个**，提示词 40 条不变；版本表新增 V17 当前版，V16 降为已落地；“下一版”仍为方向待定（葡语/阿语完整版 README 已在 V17 落地，不再占位）；README.md 语言导航新增 PT/AR 两版；英文版 Translations 一节同步列出 PT/AR 已就绪。
- `docs/learning-paths.md` 的脚本数仍是 10 个、`docs/dev-flow-ai.md` 的脚本总行数仍约 5,100 行（实测 5,118 行），两处均未过期，无需改。

## V16 · 2026-11-07

### 催单话术库（本次核心）

- 新增 `scripts/nudge.py`（只用标准库，不联网）：报价/发样/谈价之后对方不回，按天数 × 场景给现成话术——D3/D7/D14/D30 × 已报价未回（quoted）/已发样未回（sampled）/已谈价未定（negotiating）共 12 条，每条 WhatsApp 短版 + 邮件长版，中英对照（英文在前、中文在后）。语气分档：D3 轻提醒（只确认收到没有，不问决定、不施压）、D7 问进度（给对方一个一句话就能回的口子）、D14 给台阶（降价/换规格/延账期三选一，两版都齐）、D30 最后通牒但不撕破脸（明说这是最后一封，同时留一句“以后有需要随时找我”）；D30 之后停手，进长名单季度扫一次。Day 0 是报价/发样/谈价那天，不是首触那天——与 `followup_plan.py` 的首触节奏（T0 D0/D2/D5、T1 D0/D3/D6、T2 D0/D7/D14）锚点不同，同一客户同一线程只走一条线，两套节奏不打架；`--channel whatsapp/email/both`（默认两者都出）、`--format json` / `--out`；`--help` 带 4 个亲手跑过的真实例子；缺参数/非法输入给人话报错、不裸奔。示例公司/联系人/产品全是虚构的（【示例】前缀）。
- 新增 `tests/test_nudge.py`（25 个测试）：12 条组合齐全、每条 WhatsApp + 邮件两版中英对照齐全且占位符已填、D3 两版无施压词（英文 urgent/deadline/final/last chance/must/asap、中文 最后/催/必须/赶紧/截止/通牒）、D30 两版是最后一封且留后路句（英文 reach out any time、中文 以后有需要随时找我）、D14 两版三选一齐全（降价/换规格/延账期）、D7 问进度、别名归一（3/d30、quote/sample/price/谈价）与非法天数/场景报错、JSON 输出可解析且渠道过滤生效、表格版含止损线与 followup_plan 衔接说明、CLI 四档真实例子/--out 写盘/缺参数与非法输入给人话报错、`--help` 带真实例子。`python3 -m unittest discover -s tests`：152 个测试全绿（原来 127 个 + 新增 25 个）。
- 新增 `docs/nudge.md`：用法、四档语气表、三个场景表、跟 `followup_plan.py` 的分工衔接表（报价前走跟进计划、报价后走催单话术）、止损线、2 份真实输出逐字贴（D3 已报价未回、D14 已谈价未定，均已与脚本重新跑一遍逐字核对）、常见报错表。

### 文档与数字

- 三版 README 与 ROADMAP：脚本文件 9 个 → **10 个**（9 个业务脚本 + 1 个脱敏自查脚本），测试 127 个 → **152 个**，提示词 40 条不变；目录结构补进 `nudge.py`；版本表新增 V16 当前版，V15 降为已落地；“下一版”仍为方向待定（催单话术库已在 V16 落地，不再占位）；三版 README 里残留的旧脚本数（英文版 “nine scripts”、西语版 “9 scripts” 等）一并同步到 10 个。
- `docs/00-getting-started.md` 的 B 路第五步补上 `nudge.py` 一行（剩下 6 个脚本 → 7 个）；`docs/learning-paths.md` 的脚本数同步到 10 个；`docs/dev-flow-ai.md` 里的脚本总行数同步（约 4,500 行 → 约 5,100 行，实测 5,118 行）。

## V15 · 2026-11-07

### 展会实战工具（本次核心）

- 新增 `scripts/trade_show.py`（只用标准库，不联网）：展会现场收的名片按兴趣度排会后 24 小时跟进计划——会后 2 小时内发感谢 + 展会资料、会后 12 小时内发报价线索（先确认规格与月用量再给报价区间意向，不报具体价格数字）、会后 24 小时内电话/WhatsApp 追一次；时间点只写相对时间（T+2h / T+12h / T+24h），不编具体日期。两种录入：`--add` 逐条加（公司/国家/产品/兴趣度 + 邮箱/电话/WhatsApp 至少留一个，一次命令加一家）+ `--csv` 批量读（列名 company/country/product/contact/interest，与 examples/leads_example.csv 的 9 列口径对齐，email/phone 列也认；contact 列只有长得像邮箱/电话时才当联系方式，写职位的不算）；兴趣度 高/中/低（或 high/medium/low），不填按「低」处理，同级按录入顺序；兴趣度 → outreach_gen 分级（高→T0 / 中→T1 / 低→T2），每家输出按该分级的首触模板写的草稿 + 拿完整中英对照版的命令（`python scripts/outreach_gen.py <CSV> --tier T0`，CSV 里 source 填 trade_show）；`--format json` / `--out`；`--help` 带 4 个亲手跑过的真实例子；缺参数/非法输入/没留联系方式给人话报错、不裸奔。基准：【示例】3 家（高/中/低各一）→ 高 1 家先打、中 1 家本周内、低 1 家只确认，每家三档齐全。
- 新增 `tests/test_trade_show.py`（30 个测试）：兴趣度排序（高/中/低）、英文别名归一、同级按录入顺序、T0/T1/T2 映射、24 小时三档齐全（窗口与 offset 逐字核对）、第 3 步渠道优先电话、首触草稿引用 outreach_gen 模板与命令、CSV 批量读、 bundled 示例 CSV、leads_example.csv 无 interest 列全按「低」处理且 contact 职位词不算联系方式、缺 company 列/空表/文件不存在报错、空名单/没留联系方式/邮箱格式错/电话太短/兴趣度乱填报错、空兴趣度默认「低」、JSON 输出可解析且排序与三档一致、CLI 单条录入/CSV+JSON/CSV+--add 混用/无参数与非法输入给人话报错、`--help` 带真实例子。`python3 -m unittest discover -s tests`：127 个测试全绿（原来 97 个 + 新增 30 个）。
- 新增 `docs/trade-show.md`：用法、展商 CSV 列名表、会后 24 小时三档表、兴趣度 → 首触模板映射表、1 份真实输出逐字贴（`--csv examples/trade_show_example.csv`，已与脚本重新跑一遍逐字核对）、跟其他脚本的配合、常见报错表。
- 新增 `examples/trade_show_example.csv`：3 家虚构展商（【示例】前缀、sample.example 保留域、+000 占位电话），高/中/低各一；因 `.gitignore` 挡了 `examples/*`，本次用 `git add -f` 入库（与 `leads_example.csv` 同一口径）。

### 文档与数字

- 三版 README 与 ROADMAP：脚本文件 8 个 → **9 个**（8 个业务脚本 + 1 个脱敏自查脚本），测试 97 个 → **127 个**，提示词 40 条不变；目录结构补进 `trade_show.py` 与 `trade_show_example.csv`；版本表新增 V15 当前版，V14 降为已落地；“下一版”仍为方向待定（展会实战工具已在 V15 落地，不再占位）；三版 README 里残留的旧脚本数（英文版 “five/six scripts”、西语版 “5 archivos” 等）一并同步到 9 个。
- `docs/00-getting-started.md` 的 B 路第五步补上 `trade_show.py` 一行（剩下 5 个脚本 → 6 个），两处残留的“4 个脚本”同步到 8 个业务脚本；`docs/02-find-leads.md` 第 5 步补一行指向新脚本（展会收线索后的处理）；`docs/learning-paths.md` 的脚本数同步到 9 个；`docs/dev-flow-ai.md` 里的脚本总行数同步（约 4,000 行 → 约 4,500 行，实测 4,522 行）。

## V14 · 2026-11-07

### 到岸成本估算（本次核心）

- 新增 `scripts/landed_cost.py`（只用标准库，不联网）：输入 FOB 单价 + 海运费 + 保险费率 + 目的港杂费 + 关税税率，输出 CIF / DDP 分项 breakdown（FOB、海运费、保险费、CIF 小计、关税、目的港杂费、DDP 总计）+ 单条成本 + 总计 +（给了 `--sell-price`）每条利润空间。CIF 口径与 `quote_engine.py` 逐字同一条公式（CIF = (FOB+运费) ÷ (1 − 1.10×费率)，保险按 CIF 货值 110% 投保），同一组 FOB + 运费 + 保险费率，两边算出的 CIF 必须一致，测试里有交叉核对。`--qty` 条数（默认 1）、`--format json`、`--audience client`（客户版只给 CIF/DDP 总价和分项大类，不露 FOB 底价、保险费率、利润空间；JSON 版连 `meta.inputs` 一起删，跟 `quote_engine.py` 同一个脱敏口径）；`--help` 带 4 个亲手跑过的真实例子；缺参数/非法输入给人话报错、不裸奔。基准：【示例】FOB 30 + 运费 5 + 关税 10% + 港杂 2 → CIF 单条 35.06、DDP 单条 40.56；100 条 + 拟售价 48 → DDP 总计 4056.36、每条利润 7.44、利润率 15.49%。
- 新增 `tests/test_landed_cost.py`（17 个测试）：两组数字手算逐项核对（CIF/DDP/保险费/关税/利润）、关税 0% 边界、海运费 0 边界、利润与亏本提醒、JSON 双视图隔离、表格客户视图不露底价与利润、与 `quote_engine` 的 CIF 交叉核对（FOB 33.17 + 运费 6 → 两边 CIF 都是 39.23）、缺参数/非法输入给人话报错。`python3 -m unittest discover -s tests`：97 个测试全绿（原来 80 个 + 新增 17 个）。
- 新增 `docs/landed-cost.md`：用法、算法表、2 份真实输出逐字贴（【示例】表格版内部视图、100 条 + 拟售价 JSON 版）、客户视图说明、跟其他脚本的配合（先用 `quote_engine.py` 报 FOB/CIF，再用 `landed_cost.py` 算到岸全成本）、常见报错表。

### 文档与数字

- 三版 README 与 ROADMAP：脚本文件 7 个 → **8 个**（7 个业务脚本 + 1 个脱敏自查脚本），测试 80 个 → **97 个**，提示词 40 条不变；目录结构补进 `landed_cost.py`；版本表新增 V14 当前版，V13 降为已落地；“下一版”仍为方向待定（到岸成本估算已在 V14 落地，不再占位）。
- `docs/00-getting-started.md` 与 `docs/06-quote.md` 各补一行指向新脚本（报价流程：先用 quote_engine 报 FOB/CIF，再用 landed_cost 算到岸全成本）；`docs/learning-paths.md` 的脚本数同步到 8 个；`docs/dev-flow-ai.md` 里的脚本总行数同步（约 3,700 行 → 约 4,000 行）。

## V13 · 2026-11-07

### 多语言建联（本次核心）

- `scripts/outreach_gen.py` 新增 `--lang es/pt/ar`（只用标准库，不联网）：西语/葡语/阿语建联消息，模板与英文 T0/T1/T2 一一对应（同一段落结构、同样的两个要点、同一个 CTA、不报价、不带附件）；模板只在脚本里一份内嵌字典，`prompts/` 不另建副本；每条非英语消息后附英文原文（`[EN — English original, for approval]`），自查清单走英文、长度类检查以真正会发的那版为准；主题行同样卡 40 字符，超了自动降级到更短的写法；`--help` 带 3 个亲手跑过的真实例子（es/pt/ar 各一）；非法 `--lang` 报 argparse 错、缺文件报人话错，不裸奔。基准：es T0【示例】海湾轮胎贸易 / pt T1【示例】阿曼蓝海 / ar T2【示例】尼日利亚先锋，三例实测通过。
- 新增 `tests/test_outreach_i18n.py`（12 个测试）：es/pt/ar 各一例完整消息、非法语言参数报错、每种语言输出都含英文对照行、与现有英文输出不冲突（英文输出不含西/葡/阿标记）、无占位符残留、职位联系人降级为不带名字的招呼、`--help` 带三语真实例子、T3 多语言模式不写文案。`python3 -m unittest discover -s tests`：80 个测试全绿（原来 68 个 + 新增 12 个）。
- `docs/04-outreach.md` 新增“第 5 步（附）：多语言建联”：用法、跟英文版相同的四条规矩、3 份真实输出逐字贴（2026-11-07 实测）。

### 文档与数字

- 三版 README 与 ROADMAP：脚本文件 7 个不变（6 个业务脚本 + 1 个脱敏自查脚本，无新脚本，只是扩展 `outreach_gen.py`），测试 68 个 → **80 个**，提示词 40 条不变；目录结构里 `outreach_gen.py` 注释同步；版本表新增 V13 当前版，V12 降为已落地；“下一版”仍为方向待定（多语言建联已在 V13 落地，不再占位）；长期规划里西/葡/阿从待办划掉，只剩法/俄。
- `docs/dev-flow-ai.md` 里的脚本总行数同步（约 3,400 行 → 约 3,700 行）；`docs/learning-paths.md` 的脚本数仍是 7 个，无需改。

## V12 · 2026-11-07

### 轮胎行业包（本次核心）

- 新增 `scripts/tire_pack.py`（只用标准库，不联网）：输入一个 TBR 规格 + 一个目标市场，输出 GCC 认证要点 + 目的港清关单证清单 + 该市场注意事项。4 个常见 TBR 规格（11.00R20、12.00R20、295/80R22.5、315/80R22.5）× 8 个市场（尼日利亚、加纳、肯尼亚、坦桑尼亚、哥伦比亚、巴西、沙特、阿联酋）。GCC 认证只对沙特/阿联酋适用（GSO 标志 + 检测报告 + GCC 符合性证书）；非 GCC 市场走当地程序（尼日利亚 SONCAP、沙特 SASO/SABER、阿联酋 ECAS、肯尼亚/坦桑尼亚 PVoC、巴西 INMETRO）。每份输出都带「须以官方最新要求为准、发货前复核」，不编死条款；载重指数/速度级别默认该规格常见值，最终以厂家数据表为准。`--help` 带 3 个亲手跑过的真实例子；`--format json`（跟 `lead_score.py` 一个信封口径）；`--li` / `--speed` 可覆盖常见值。基准：11.00R20→尼日利亚、295/80R22.5→沙特、315/80R22.5→阿联酋三例实测通过。
- 新增 `tests/test_tire_pack.py`（16 个测试）：4 规格各一例、8 市场全覆盖、GCC 适用/不适用分流、SONCAP/SASO 点名、非法规格与市场报错、JSON 输出可解析且与表格版同数据。`python3 -m unittest discover -s tests`：68 个测试全绿（原来 52 个 + 新增 16 个）。
- 新增 `docs/tire-pack.md`：用法、规格/市场两张表、2 份真实输出逐字贴（11.00R20→尼日利亚表格版、295/80R22.5→沙特 JSON 版）、常见报错表、跟其他脚本的配合（先分级再跑行业包、报价前先看注意事项、背调时对照清单核合规）。

### 文档与数字

- 三版 README 与 ROADMAP：脚本文件 6 个 → **7 个**（6 个业务脚本 + 1 个脱敏自查脚本），测试 52 个 → **68 个**，提示词 40 条不变；目录结构补进 `tire_pack.py`；版本表新增 V12 当前版，V11 降为已落地；"下一版"仍为方向待定（轮胎行业包已在 V12 落地，不再占位）。
- `docs/00-getting-started.md` 的 B 路第五步补上 `tire_pack.py` 一行（剩下 3 个脚本 → 4 个）。

## V11 · 2026-11-07

### 客户背调 Agent（本次核心）

- 新增 `scripts/due_diligence.py`（只用标准库，不联网）：输入一家公司的公开信息，输出 L1/L2/L3 三级背调报告 + A/B/C 评级 + 红旗清单 + 下一步。L1 是 `docs/03` 第五节的四问（官网存在性 / 联系方式 / 贸易属性 / 规模迹象）；L2 六维（身份 / 规模 / 信誉 / 采购力 / 付款习惯 / 合规），每维只给通过 / 待核实 / 红旗；L3 只列"查什么、去哪查"，不替用户编结果。评级：A = L1 全过 + 有进口记录 + 品类匹配 + 找到具体采购人且零红旗；B = 证据弱或 1 项降级红旗；C = L1 不过或 ≥2 项红旗；制裁名单 / 货款付给第三方账户 = 立即终止。评级映射 T0/T1/T2/T3。`--format json`（跟 `lead_score.py` 一个信封口径）；`--audience client` 只给已核实的公开事实 + 待补材料，评级、红旗、内部判断一律不带出门；`--help` 带 5 个亲手跑过的真实例子。基准：A 级【示例】海湾轮胎贸易 / B 级【示例】半岛汽车 / C 级【示例】黎凡特供配，三例实测通过。
- 新增 `tests/test_due_diligence.py`（22 个测试）：L1 淘汰（官网缺失 / 免费邮箱 / 同行 / 待核实降 C）、A/B/C 各一例、1 项红旗降级、2 项红旗降 C、制裁与收款账户终止、域名不一致红旗、缺公司名报错、JSON 内部与客户视图隔离、L3 只列来源不编结果、CSV note 只写已核实事实。`python3 -m unittest discover -s tests`：52 个测试全绿（原来 30 个 + 新增 22 个）。
- `docs/03-due-diligence.md` 新增十三节：脚本用法、5 个真实例子、A/B/C 三份输出逐字贴（2026-11-07 实测）、读报告的三个要点、常见报错表。口径说明：脚本的 L1 按本页第五节四问走（任务简报里一度写的三项已按文档口径纠正，见十三节开头）。
- `prompts/AI_PROMPTS.md` 新增 P03-5（背调报告复核：让 AI 验算脚本的评级，不许改评级），提示词从 39 条涨到 **40 条**（核心 28 + 进阶 12）。

### 文档与数字

- 三版 README 与 ROADMAP：脚本文件 5 个 → **6 个**（5 个业务脚本 + 1 个脱敏自查脚本），测试 30 个 → **52 个**，提示词 39 条 → **40 条**；目录结构补进 `due_diligence.py`；版本表新增 V11 当前版，V10 降为已落地；"下一版"改为方向待定（背调 Agent 已在 V11 落地，不再占位）。
- `docs/00-getting-started.md`、`docs/learning-paths.md`、`docs/dev-flow-ai.md` 里的现行数量同步（脚本 6 个、提示词 40 条）；`GITHUB_LAUNCH.md`、`STAR-GROWTH.md` 里的提示词数同步到 40。`docs/decisions/ADR-001` 是带日期的决策记录，原文不动。

## V10 · 2026-11-07

### 进阶模块

- 新增 `docs/advanced/` 6 个模块：08 独立站 / 09 社媒矩阵 / 10 展会 / 11 物流支付 / 12 风险合规 / 13 大客户。按线上口径适配：CSV 是 9 列，跟进是 D0/D2/D5 三次；模块内链逐个验过。

### 学习路径

- 新增 `docs/learning-paths.md`：三条路径（零基础 / 7 天最快 / 进阶），脚本名和数字按 7 环节 + 进阶模块 + 5 脚本文件写；README 补了入口。

### 排障与协作

- 新增 `docs/troubleshooting.md`（4 个亲手验过的真坑）、`docs/dev-flow-ai.md`、`docs/long-task-template.md`、`docs/decisions/ADR-001-plan-gate-downgrade.md`。作者保持匿名，公开文档正文不出现真实姓名。

### 报价引擎

- `scripts/quote_engine.py` 堵住两处泄漏：JSON 客户视图不再带 `meta.inputs`（成本/运费/加成等输入全删），表格客户视图不再打印锚价定位行；客户视图从此算不出底价。补边界校验：缺成本、负数、超大数（>1000 万）、加成 >1000%、MOQ ≤ 0、有效期超出 1–365 天，全部给一句人话报错、不抛 traceback。`--help` 补了 3 个亲手跑过的真实例子。基准数字不变：`--cost 28 --freight 6 --margin 15` 仍出 FOB 33.17 / CIF 39.23。

### 测试

- 新增 `tests/`（只用标准库 `unittest`，30 个测试）：报价基准/阶梯/客户视图隔离/边界、线索打分、跟进节奏、开发信双语输出、脱敏检查、5 个脚本 CLI 冒烟。`python3 -m unittest discover -s tests` 一键全绿。

### 文档与数字

- `README.md` / `README_EN.md` / `README_ES.md` 的数字与真实输出逐字对上：脚本是 5 个文件、跟进是 D0/D2/D5（6 天 3 次）；开发示例里的函数名改成真实存在的；CI 矩阵改成 py3.8–3.13；目录结构补进新增的文档和 `tests/`；死链全验。
- 新增本文件（`CHANGELOG.md`）和 `ROADMAP.md`。

### 提示词

- `prompts/AI_PROMPTS.md` 从 27 条涨到 **39 条**（核心 27 + 进阶 12）。新章节 08–13 进阶（P08-1 … P13-2），每条补了 STOP 字数上限和防幻觉条款；拆分版 13 文件不并入（避免两套提示词分叉），只挑了两句好句子补进总库。三版 README、STAR-GROWTH、GITHUB_LAUNCH、00-getting-started 里的现行数量同步到 39；v0.1 历史行留 27（那时确实只有 27 条）。

### 浏览器 Demo

- `index.html` 的打分逻辑与 `lead_score.py` 逐项对齐：修了 5 处分差（采购信号不再扫公司名、电话带 WA 加 4 分、格式错的邮箱按没填算、电话少于 7 位数字按没填算、仅备注里有社媒账号不给分）；兜底示例数据修成与 `examples/leads_example.csv` 逐字节同源。验证：10 条示例 + 7 个边界用例，浏览器 JS 与 Python 分数/分级全部相等；全库扫查无真实邮箱/电话/公司名混入。

## 更早

- **v0.2**：AI 报价引擎（`scripts/quote_engine.py`，alpha）：输入成本 + 市场 + 竞品锚价，输出 FOB/CIF 报价区间 + 三档让步阶梯。
- **v0.1.5**：零安装浏览器 Demo（`index.html`）+ 报价引擎 alpha + 品牌主张（MANIFESTO）+ 上线推广清单（GITHUB_LAUNCH）。
- **v0.1**：7 环节文档骨架 + 4 个 stdlib 业务脚本 + 27 条提示词 + 双语 README。
