# 你改了啥

一句话说清，顺手写上动过的文件。例：`docs/06-quote.md` 第 3 节的 CIF 例子算错了。

> 只改了一个错别字？很好，那也请提交。错别字也是贡献，我们不挑食。

## 先勾类型（勾一个就够，勾错了没人罚你）

- [ ] **改错别字 / 措辞** —— 那你只看下面「通用」那三条，代码那堆直接跳过，一条都不用跑
- [ ] **补内容**（某个国家 / 行业的实战细节）
- [ ] **翻译**（语种：______ ｜ 六段结构没动，顺序没变）
- [ ] **改文档**（docs/、README）
- [ ] **改代码**（scripts/ 下的 Python）

## 你从哪儿知道的（补内容必填）

这条决定别人敢不敢信你写的。

- [ ] 我自己干过 / 踩过坑
- [ ] 公开文件（政策、海关公告、平台规则）—— 出处：______
- [ ] 听说的 / 我推测的 —— 正文里已经标了「推测，待验证」

## 通用自检（改啥都看一眼，就三条）

- [ ] **没有真实客户数据。** 公司名改【示例】，邮箱域名改 `sample.example`，电话 / WhatsApp 用 `+000` 占位。真名、真公司、真报价，一个都别留。
- [ ] 链接点得开，没指向不存在的页面。
- [ ] 署名是 zero-to-trade，不是我的真名 / 公司名 / 微信号。

## 改代码的，再跑一遍

先编译。四个文件名打全，Windows 的 cmd 和 PowerShell 不认 `*.py` 这种写法：

```bash
python -m py_compile scripts/lead_score.py scripts/outreach_gen.py scripts/followup_plan.py scripts/quote_engine.py
```

再冒烟，四条都得有输出，不能只有一行报错：

```bash
python scripts/lead_score.py examples/leads_example.csv
python scripts/outreach_gen.py examples/leads_example.csv --tier T0
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

- [ ] 上面五条命令我跑过，没报错
- [ ] **只用 Python 标准库**。没有 `pandas` / `requests` / `openpyxl` 之类，脚本也不发任何网络请求。
- [ ] 改了输出的话，README 里的预期输出也一起改了（两处不一致会被打回）

## 改文档 / 翻译的，再看两条

- [ ] 术语对着 [GLOSSARY.md](../GLOSSARY.md) 对齐了（FOB / CIF / L/C / MOQ 这些别意译）
- [ ] 六段结构没拆，顺序没变

---

拿不准该不该改，或者改之前想吵一架：先开个 issue 聊聊。开 issue 不要钱，改错了要花我一整天。

更细的规矩在 [CONTRIBUTING.md](../CONTRIBUTING.md)。
