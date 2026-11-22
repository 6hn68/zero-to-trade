# 到岸成本估算：FOB → CIF → DDP，一单到底多少钱

> **这是什么**：报价引擎（`scripts/quote_engine.py`）只算到 CIF——货到目的港为止。但客户问「DDP 到我门口多少钱」，你还得加上关税和目的港杂费。这个脚本就是把后半截补上：你给 FOB 价、海运费、保险费率、目的港杂费、关税税率，它吐出 CIF / DDP 分项 breakdown + 单条成本 +（给了售价）每条利润空间。
>
> **先说清楚**：关税税率、目的港杂费都是**估算口径**，不是法规原文。报 DDP 之前务必跟目的国清关代理核实最新税率——没有可靠清关代理就别报 DDP（见 [06-quote.md](06-quote.md) 的条款表，DDP 那一行）。CIF 的算法与 `quote_engine.py` 逐字同一条公式，同一组 FOB + 运费 + 保险费率，两边算出的 CIF 必须一致（测试里有交叉核对）。

## 用法

```bash
# 最简：FOB + 运费 + 关税 + 目的港杂费（【示例】价格全部虚构）
python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2

# 100 条 + 拟售价：一次看出 DDP 总计和每条利润空间
python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --qty 100 --sell-price 48

# 客户视图：只给 CIF/DDP 总价和分项大类，FOB 底价、保险费率、利润全砍掉
python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --audience client

# JSON 输出，方便贴进表格或交给 AI 复核
python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --format json

# 换保险费率（百分比，默认 0.15）或走比率入口
python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --insurance 0.3
python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --insurance-rate 0.003

# 存成文件
python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --out landed_internal.txt
```

`--help` 里有 4 个亲手跑过的真实例子。所有金额默认 USD/条，`--currency` / `--unit` 可改。

## 算法（跟 quote_engine.py 同一条公式）

| 步骤 | 公式 | 说明 |
|---|---|---|
| CIF | `(FOB + 海运费) ÷ (1 − 1.10 × 保险费率)` | 保险按 CIF 货值的 110% 投保 |
| 保险费 | `CIF × 1.10 × 保险费率` | 自检：CIF = FOB + 运费 + 保险费 |
| 关税 | `CIF × 关税税率` | 按 CIF 计，不是按 FOB 计 |
| DDP 单条 | `CIF + 关税 + 目的港杂费` | 完税后交货价 |
| 总计 | `单条 × 条数` | 总计按未四舍五入的原值乘，比「单条四舍五入后再乘」准 |
| 每条利润 | `拟售价 − DDP 单条` | 只有给了 `--sell-price` 才算 |

## 真实输出样例 1：【示例】FOB 30 + 运费 5 + 关税 10% + 港杂 2（表格版，内部视图）

命令：`python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2`

```
==================================================================
  到岸成本（内部视图，含 FOB 底价与利润，这版别发客户）
  币种: USD · 计价单位: 条 · 条数: 1 · 生成时间: 2026-11-07T10:45:49
==================================================================
  FOB 单价: 离岸价，不含运费保险        │      30.00 USD/条
  海运费: 装运港 → 目的港（每条）       │       5.00 USD/条
  其中保险费 = CIF×110%×费率            │       0.06 USD/条
  CIF 单条: 到岸价，含运费+保险         │      35.06 USD/条
  关税（单条）: CIF × 10.00%            │       3.51 USD/条
  目的港杂费（单条）: THC/卸货/清关代理 │       2.00 USD/条
  DDP 单条: 完税后交货价                │      40.56 USD/条
------------------------------------------------------------------
  合计（1 条）
  CIF 总计       │      35.06 USD
  关税总计       │       3.51 USD
  目的港杂费总计 │       2.00 USD
  DDP 总计       │      40.56 USD
------------------------------------------------------------------
  顺手记几个词（完整版去翻 docs/06-quote.md 的条款表）
   · CIF 到岸价：FOB + 海运费 + 保险费，卖方付到目的港。
   · DDP 完税后交货：CIF + 关税 + 目的港杂费，包到买方门口。
   · 投保加成 110%：保险按 CIF 货值的 110% 投保，所以 CIF = (FOB+运费) ÷ (1 − 1.10×费率)，与 quote_engine.py 同一条公式。
   · 关税按 CIF 计：税率、目的港杂费都是估算口径，报 DDP 前务必跟目的国清关代理核实最新税率；没有可靠清关代理就别报 DDP。
==================================================================
```

## 真实输出样例 2：【示例】同上，100 条 + 拟售价 48（JSON 版）

命令：`python scripts/landed_cost.py --fob 30 --freight 5 --duty 10 --port-charges 2 --qty 100 --sell-price 48 --format json`

```json
{
  "meta": {
    "generated_at": "2026-11-07T10:45:49",
    "currency": "USD",
    "unit": "条",
    "audience": "internal",
    "inputs": {
      "fob": 30.0,
      "freight": 5.0,
      "duty_pct": 10.0,
      "port_charges": 2.0,
      "qty": 100,
      "insurance_rate": 0.0015,
      "sell_price": 48.0
    }
  },
  "landed_cost": {
    "fob_unit": 30.0,
    "freight_unit": 5.0,
    "insurance_unit": 0.06,
    "insurance_cover_factor": 1.1,
    "insurance_rate": 0.0015,
    "cif_unit": 35.06,
    "duty_pct": 10.0,
    "duty_unit": 3.51,
    "port_charges_unit": 2.0,
    "ddp_unit": 40.56,
    "qty": 100,
    "cif_total": 3505.78,
    "duty_total": 350.58,
    "port_charges_total": 200.0,
    "ddp_total": 4056.36,
    "warnings": [],
    "sell_price": 48.0,
    "profit_unit": 7.44,
    "profit_total": 743.64,
    "profit_margin_pct": 15.49
  }
}
```

## 客户视图长什么样

同一组数字加 `--audience client`：CIF/DDP 总价和分项大类（关税、目的港杂费）都在，FOB 单价、运费、保险费、保险费率、拟售价、利润空间一行都不出现——JSON 版连 `meta.inputs` 一起删（跟 `quote_engine.py` 同一个脱敏口径）。发客户永远加 `--audience client`。

## 跟其他脚本的配合

先用 `quote_engine.py` 报 FOB/CIF（成本 + 加成 → 报价 + 三档让步阶梯），再用 `landed_cost.py` 算到岸全成本（FOB + 运费 + 保险 → CIF，再加关税 + 目的港杂费 → DDP）。顺序别反：FOB 是报价引擎的输出、是到岸成本的输入。DDP 报出去之前，先看一眼 `tire_pack.py` 的目的港清关单证——税率和单证都对上，DDP 才站得住。

## 常见报错

| 报错 | 原因 |
|---|---|
| `✗ FOB 单价必须 > 0` | 漏了 `--fob` 或填了 0/负数 |
| `✗ 海运费不能为负` | `--freight` 填了负数 |
| `✗ 关税税率不能为负` / `大得离谱（上限 1000%）` | `--duty` 填错单位：这里填百分比，10 表示 10% |
| `✗ 保险费率 30.000% 异常(>5%)` | `--insurance` 填了 30：这里填百分比数值，0.3 表示 0.3%，不是 30 |
| `✗ --qty 条数必须 ≥ 1` | `--qty` 填了 0 或负数 |
| `✗ 拟售价必须 > 0` | `--sell-price` 填了 0 或负数 |
| `usage: ... the following arguments are required: --fob` | 缺必填参数，`--fob` 是唯一必填项 |
