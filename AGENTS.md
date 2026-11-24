# AGENTS.md — zero-to-trade

> 项目级 agent 协作规则。全局规则在 `~/AGENTS.md`，本文件只写本项目的事。
> 开发流程（plan 门/验收/红线）见 `docs/dev-flow-ai.md`，长任务见 `docs/long-task-template.md`。

## How to run

```bash
python3 scripts/lead_score.py      # 线索 T0-T3 分级
python3 scripts/outreach_gen.py    # 生成中英对照建联消息
python3 scripts/followup_plan.py   # 跟进计划表（T0 为 D0/D2/D5）
```

- 全部 15 个脚本（14 个业务脚本 + 1 个脱敏自查脚本）见 `scripts/README.md`。
- 只用 Python 标准库，零依赖。`pip install` 之前先过 plan 门。
- 跑测试：`python3 -m unittest discover -s tests`（586 个测试）+ 三个核心脚本各跑一遍冒烟。

## 协作规则

1. 动手前读 `~/workspace/custom-skills/zero-to-trade/SKILL.md`（30 秒建立上下文）。
2. plan 门是条件触发（≥3 文件 / 动数据密钥 / 范围模糊 / 不熟悉模块），不是默认。
3. 一个 AI turn 一个 commit；commit 信息写人话（改了什么+为什么）。
4. 大重构前 `git tag good-<日期>`；开工前工作树必须干净。
5. 密钥、支付、生产数据：不碰、不读、不写。API Key 永不进仓库。

## Stop conditions（命中立刻停手，等人）

- 要引入新依赖 / 改动超 5 个文件
- 连续 2 次排错失败（第 3 次不许自己再试）
- 要删库 / 发版 / 对外发布
- 发现 plan 要改：先停下来同步，不许悄悄偏离

## MCP（如自研 MCP server）

- STDIO 日志走 stderr，stdout 是协议通道，混入 print 直接断连。
- 新 MCP 接入先过 7 问：读写边界 / 权限范围 / 网络行为 / 敏感距离 / 审计日志 / 重试风险 / 供应链。答不上来不上线。
- 最小权限：写操作只落 `src/`/`tmp/`，碰不到 `.env`。
