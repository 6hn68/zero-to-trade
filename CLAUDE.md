# CLAUDE.md — zero-to-trade 第二大脑

> 给 AI 的项目速查手册。全局规则在 `~/AGENTS.md`，本文件只写本项目的事。
> 2026-10-31 从 easy-vibe"第二大脑"抄来。

## 这是什么
"从零做外贸"7 环节工作流 + AI 工具链，给纯新手看的开源项目（MIT，作者署名刘生）。终态：AI 自动完成找客户到收款全流程。

## 目录地图
- `scripts/`：15 个脚本（14 个业务脚本 + 1 个脱敏自查脚本），只用标准库
- `docs/01-07`：7 环节文档；`docs/dev-flow-ai.md`：开发流程；`docs/long-task-template.md`：长任务模板
- `prompts/`：可复制的 AI 提示词总库（`AI_PROMPTS.md`，40 条）；`examples/`：虚构示例数据；`logs/`：运行日志

## 技术栈
Python 3，只用标准库，零依赖。无数据库（现阶段 CSV/日志文件）。

## 常见任务命令
```bash
python3 scripts/lead_score.py      # 线索分级
python3 scripts/outreach_gen.py    # 建联消息
python3 scripts/followup_plan.py   # 跟进计划
python3 -m unittest discover -s tests  # 全部测试
git log --oneline -5               # 最近改动
```

## 开发规范
1. plan 门条件触发（见 AGENTS.md），不是默认。
2. 改完即验；Final Reviewer 按 🟢/🟡/🔴 分档。
3. 示例数据必须虚构；真实公司名/价格/联系方式永不进仓库。

## 注意事项
- 报价引擎已在 V10 落地（`scripts/quote_engine.py`），客户视图与内部视图隔离。
- 对外发布（push 公开仓库/发版）必须 John 逐条批。
- 坑位：见 `docs/troubleshooting.md`；教训沉淀在 skill 的 `insights/`。

## 当前状态
当前版 V20（本地增量合并 + 10 轮打磨）；详见 CHANGELOG.md 与 ROADMAP.md。
