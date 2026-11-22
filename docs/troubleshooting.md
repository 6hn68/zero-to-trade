# 排障手册 Troubleshooting

> 每条按"问题 / 现象 / 原因 / 解法"四段写。只写亲手复现过的坑，没复现的写"未核实"，不写"我觉得"。
> 2026-11-07 并入公开仓库：下面 4 条全部在 2026-11-07 当天亲手跑过，命令和输出都对得上。
> 2026-11-14 并入本地快照的三条（5–7 条，2026-10-31 前后亲手踩过，格式与上面一致）。

## 1. 线索全被打成 T3，脚本好像坏了

- **问题**：`python scripts/lead_score.py my_leads.csv` 跑完，10 条里 9 条是 T3。
- **现象**：输出正常、不报错，但"今天先打"一家都没有，得分全在 10–20 分。
- **原因**：CSV 缺列不报错，只按最低分算。`lead_score.py` 只认 9 列：`company,country,product,source,email,phone,years,contact,note`。实测：只给 `company,country` 两列的 1 条线索，得 10 分、判 T3——脚本没坏，是数据没给够。
- **解法**：先对表头，再跑脚本。`company` 是唯一必填列，其余空着也能跑，但空一项就少一项分；`source` 填 `referral` / `trade_show` / `customs` / `linkedin` / `search` 之一，对分数影响最大。

## 2. 真客户名单差点被提交到 GitHub

- **问题**：往 `examples/leads_example.csv` 里填了真客户，`git status` 显示它要被提交。
- **现象**：`.gitignore` 里明明写了 `*.csv`，却一点没拦。
- **原因**：`examples/leads_example.csv` 是"已被 git 跟踪"的文件，`.gitignore` 只对还没被跟踪的文件生效，对它完全无效。
- **解法**：真名单永远先 `cp examples/leads_example.csv my_leads.csv`，只往 `my_leads.csv` 里填（`*.csv` 那条会挡住它）；提交前跑一遍 `python scripts/check_private_data.py`，它扫真实邮箱域名和真电话，抓到就退出码 1 挡住提交，CI 里同一关也会挂掉。

## 3. 报价单发出去了，客户看到了底价

- **问题**：用 `quote_engine.py` 出的报价单发给客户，对方直接按底价还价。
- **现象**：报价单里有"FOB 底价 / CIF 底价"两行。
- **原因**：`quote_engine.py` 默认是内部视图（`--audience internal`），含成本与底价；客户视图要显式加 `--audience client`。实测 `--cost 28 --freight 6 --margin 15`：内部视图 FOB 报价 33.17、底价 31.18；客户视图只有 FOB 报价 33.17、CIF 报价 39.23，底价数字（31.18/37.24）和成本基数（28.84）一行都不出现。
- **解法**：发给客户的一律加 `--audience client`；内部视图只留在自己机器上。发出前对一遍"报价单这几样得补齐"清单（有效期、付款方式、最小起订量、交货期），漏了客户正好拿缺的来压价。

## 4. 跟进日期或分级参数报错，不知道错在哪

- **问题**：`followup_plan.py` 或 `outreach_gen.py` 一跑就报错。
- **现象**：`followup_plan.py --start 2026-13-40` 报"错误：--start 日期格式应为 YYYY-MM-DD（例 2026-10-08），收到的是 '2026-13-40'"；`outreach_gen.py --tier T9` 报"invalid choice: 'T9' (choose from 'T0', 'T1', 'T2', 'T3', 'all')"。
- **原因**：这两个都是参数错，不是脚本坏了。日期必须是真实存在的 `YYYY-MM-DD`；分级只有 T0–T3 和 all 五个值。跟进节奏是 D0/D2/D5（首发当天、第 2 天后、第 5 天后，6 天 3 次），别按"第 1/4/7 天"填。
- **解法**：照报错里给的格式改：日期写 `2026-10-08` 这种真实日期，分级写 T0–T3。Windows 上 `python` 命令可能不存在，改用 `python3` 或 `py` 再试。先跑 `python scripts/lead_score.py --help` 看一眼参数，别凭记忆填。

## 5. /tmp 下的构建脚本中途消失

- **问题**：放 `/tmp` 的构建脚本跑着跑着没了。
- **现象**：脚本执行到一半报 file not found。
- **原因**：运行环境会清理 `/tmp`。
- **解法**：所有构建脚本、中间产物一律放 workspace 持久目录（如 goal 的 hidden_files）；`/tmp` 只放一次性抽帧/临时文件。

## 6. browser 上传多文件顺序错位

- **问题**：一次传两个视频，标题和内容对不上。
- **现象**：YouTube Studio 里标题 A 配了视频 B 的封面。
- **原因**：browser 的 files 参数实际按逆序上传。
- **解法**：所有多文件上传任务，必须加「打开公开页逐条核对标题与内容一致」的硬性验收；错位直接在 Studio 改标题。

## 7. 云电脑 git 走代理失败

- **问题**：`git clone/push` 连不上。
- **现象**：timeout / connection reset。
- **原因**：直连被墙，需走代理。
- **解法**：`git config --global http.proxy http://127.0.0.1:3129`（云电脑代理端口）；SSH 走 `~/.ssh/config` 配 ProxyCommand。

<!-- 新坑按四段式追加：问题 / 现象 / 原因 / 解法，缺一不可 -->
