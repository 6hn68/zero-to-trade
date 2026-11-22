# TRACE_FORMAT — 操作日志规范

> 2026-10-31 从 1EchA《04》抄来。多路并行时强制带 trace_id，否则分不清上下游。
>
> 状态（2026-11-14 落地）：三个核心脚本（`lead_score.py`、`outreach_gen.py`、`followup_plan.py`）每次运行都在 `logs/trace-YYYY-MM-DD.jsonl` 写一行，字段就按下面记；`*.log` 旧格式保持不动。`trace-*.jsonl` 已进 `.gitignore`，不进仓库。

## 字段（JSONL，一行一条）

```json
{"trace_id": "uuid", "ts": "2026-10-31T13:00:00+08:00", "tool": "lead_score.py",
 "input": "leads_example.csv（脱敏摘要）", "output": "T0:2 T1:5（摘要）",
 "duration_s": 3, "error": ""}
```

- `trace_id`：一次任务一个，多路并行时每路独立 id，汇总时可串。
- 输入/输出只记摘要，**绝不记密钥、真实客户信息、完整 PII**。
- 看四个指标：通过率 / 耗时 / Token / 卡点。

## 存放
`logs/` 下按日期记 JSONL，如 `logs/trace-2026-10-31.jsonl`。
现有 `*.log` 保持不动，新任务用新格式。
