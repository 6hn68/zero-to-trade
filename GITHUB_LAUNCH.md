# GITHUB_LAUNCH · 上线 + 推广执行清单

本文件是"从本地仓库到高星"的一站式执行单。所有动作按 P0→P3 排序，能本地做的已经做完，剩下需要你点几下或贴几行。

---

## 0. 改用户名（P0，阻塞推送）

代码里所有 issue 链接现在指向 `github.com/zero-to-trade/zero-to-trade`。
如果你的 GitHub 用户名不是 `zero-to-trade`，做一次全局替换即可：

- 把 `zero-to-trade/zero-to-trade` 换成 `你的用户名/zero-to-trade`
- 涉及文件：`README.md`、`README_EN.md`（共 3 处 issue 链接 + 文中若干处）

> 仓库名建议保持 `zero-to-trade`，短、好搜、品类词直给。

---

## 1. 建仓库 + 设 Topics / About（P0）

**建仓**：GitHub → New repository → 名字 `zero-to-trade` → 选 Public → **不要**勾 Initialize with README（本地已有）→ Create。

**本地连远程并推**：
```bash
git remote add origin https://github.com/你的用户名/zero-to-trade.git
git branch -M main
git push -u origin main
```

**GitHub Topics（仓库页右侧 Topics 里填，决定别人搜不搜得到你）**：
```
foreign-trade
import-export
cold-email
lead-generation
b2b
sales
crm
python
beginners
export
```

**About 描述（仓库页右上 About 里填，带关键词）**：
- 短描述：`Open-source operating system for starting foreign trade with zero experience — 7 stages + runnable scripts.`
- 长描述（About 下方的 Description 框）：`An open-source foreign-trade workflow for absolute beginners: pick a market → find/vet leads → outreach → quote → deliver. Ships 4 stdlib-only Python scripts (lead scoring, outreach copy, follow-up plan, quoting engine) and 27 copy-paste AI prompts. Anonymous, no paid course.`

---

## 2. 开 GitHub Pages（P1，零安装 Demo）

Settings → Pages → Source 选 `main` / `/root` → Save。
几分钟后 `https://你的用户名.github.io/zero-to-trade/` 就是浏览器版分级 Demo（已写好 `index.html`）。

---

## 3. 借流量：PR 到 awesome-foreign-trade（P1）

它是一个 187★ 的链接集合，不是竞品。提一个 PR，加一行：

```markdown
- [zero-to-trade](https://github.com/你的用户名/zero-to-trade) - 开源外贸操作系统：7 环节工作流 + 4 个零依赖可跑脚本（线索分级/建联文案/跟进计划/报价引擎），给零基础新手，匿名不卖课。
```

PR 标题建议：`add zero-to-trade: open-source foreign trade workflow for beginners`

---

## 4. 点火：Show HN（P2）

Hacker News → Submit → Title：
`Zero-to-Trade: an open-source "operating system" for starting export with zero experience`

正文（贴一段，别长）：
```
Most "how to start exporting" content tells you to "do background research" and stops.
This repo takes one task down until it's an action: which 3 fields to check, which
sites, what result drops the lead. Seven stages, from picking a market to getting paid,
plus 4 stdlib-only Python scripts you can run in 30s (no pip install). 27 copy-paste
AI prompts. Anonymous, no paid course. Feedback welcome — especially from people
selling into markets the docs don't cover yet.
```
配一张 `index.html` 跑出来的分级表截图（或录 30 秒 GIF）。

---

## 5. 投中腰部外贸博主（P2）

目标：抖音 / 小红书 / 视频号 上 5–10 个"外贸实操"中腰部博主（几万粉即可，比大 V 更易理）。
私信/评论模板（口语化，别像广告）：

```
老师好，我做了一份开源的外贸新手操作系统，把"选市场→找客户→背调→建联→报价→交单"
拆成能直接照做的清单，还带了 4 个能跑的 Python 小工具（不用装环境，浏览器也能跑分级）。
完全免费、MIT、不卖课。觉得对你的粉丝有用我就把链接发你，随便用随便改。
```

给的素材包：`index.html` 在线 Demo 链接 + README 截图 2 张。

---

## 6. 养趋势：Star History（P2）

README 已嵌入 Star History 图。拿到前 100 个 star 后，看"谁带来的"——
如果前 100 来自 3 个以内来源（某个博主 / 某个 list），说明点火成功，乘胜加投那几个渠道。

---

## 7. 扩面：多语言（P3）

英语已就绪。下一个性价比最高的是**西班牙语 / 阿拉伯语**（覆盖拉美 + 中东两大外贸市场）。
翻译只需保持六段结构、术语对齐术语表，详见 `CONTRIBUTING.md`。

---

## 8. 长大：把 v0.2 报价引擎做扎实（P3）

`scripts/quote_engine.py` 已是 alpha。下一步让它"会接海关数据做竞品锚价自动抓取"，
是让项目持续被关注的关键——人们会回来 star 一个"还在长"的项目。
