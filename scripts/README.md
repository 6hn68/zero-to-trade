# scripts

可直接跑的工具脚本，每个脚本独立做一件事，新 Agent 不用读全项目就能用。只用 Python 标准库，零依赖。

- `lead_score.py`：输入客户 CSV（列见 `examples/leads_example.csv`），输出 T0–T3 分级。用法：`python3 scripts/lead_score.py examples/leads_example.csv`
- `market_rules.py`：目标市场与贸易壁垒规则表（土耳其/巴西壁垒、墨西哥/美国/欧盟排除），供 `lead_score.py` 分级时查；改规则只改这张表。用法：`python3 scripts/market_rules.py --country Turkey`
- `outreach_gen.py`：按分级批量生成建联文案（中英对照，另有西/葡/阿语）；也可以 `--company` 单条生成，不用先建 CSV。
- `followup_plan.py`：按分级排出带日期的跟进节奏表（T0 为 D0/D2/D5）。
- `quote_engine.py`：报价引擎：成本 + 运费 + 毛利 → FOB/CIF 区间 + 三档让步阶梯。
- `due_diligence.py`：背调 Agent：L1/L2/L3 三级 + A/B/C 评级 + 红旗清单。
- `tire_pack.py`：轮胎行业包：规格 + 市场 → GCC 要点 + 清关单证 + 注意事项。
- `landed_cost.py`：到岸成本：FOB + 运费 + 保险 → CIF，再加关税 + 目的港杂费 → DDP。
- `trade_show.py`：展会实战：现场名片 → 会后 24 小时跟进计划。
- `nudge.py`：催单话术库：D3/D7/D14/D30 × 三种场景，中英对照。
- `anchor_price.py`：竞品锚价：海关数据竞品价区间 + 自家成本 → 三档 CIF 锚价。
- `fast_path.py`：七天快路径互动版：每天 `--day N` 看任务，干完 `--done N` 打卡。
- `daily_video_list.py`：每日 5 条视频清单：上午 3 条 + 下午 2 条，每条带规格、市场、一句话卖点和 3 项拍摄检查项。用法：`python3 scripts/daily_video_list.py`
- `check_private_data.py`：提交前自查：扫真实客户数据，抓到就挡住。

日志：`lead_score.py` / `outreach_gen.py` / `followup_plan.py` 每次运行都会在项目根目录 `logs/` 下追加一条记录（`lead_score.log` / `outreach_gen.log` / `followup_plan.log`），含运行时间、参数和结果摘要，屏幕输出不变。`logs/` 已加入 `.gitignore`，不进版本库，里面可能含客户名，只留在本地。
