# GITHUB_LAUNCH · 上线 + 推广执行清单

本文件是"从本地仓库到高星"的一站式执行单。所有动作按 P0→P3 排序，能本地做的已经做完，剩下需要你点几下或贴几行。

---

## 0. 改用户名（P0，阻塞推送）

代码里所有 issue 链接、Pages 链接、CI badge 现在都指向 `github.com/zero-to-trade/zero-to-trade`。
如果你的 GitHub 用户名不是 `zero-to-trade`，做一次全局替换即可：

- 把 `zero-to-trade/zero-to-trade` 换成 `你的用户名/zero-to-trade`
- 涉及文件：`README.md`、`README_EN.md`、`README_ES.md`、`CONTRIBUTING.md`、`docs/00-getting-started.md`，以及 `README.md` 顶部的 CI badge URL
- 已修好的死链：`CONTRIBUTING.md` 与 `docs/00-getting-started.md` 里的 `TODO-your-username` 已全部换成 `zero-to-trade`，无需再改。

> 仓库名建议保持 `zero-to-trade`，短、好搜、品类词直给。
> CI badge 在第一次 push 后、workflow 跑过一次才会显示状态（之前是灰色 "no status"，属正常）。

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

> ⚠️ **别用 `os` / `operating-system` 当 Topic**：这个词已被 `TradeOS` 等项目占住，搜这个词刷不到你。本项目自称"操作系统"是比喻（一套工作流/清单），搜索优化靠上面的品类词（`foreign-trade`/`export`/`b2b`/`cold-email`/`lead-generation`）才精准。About 里也用 "workflow / checklist / system" 而不是反复强调 OS。

**About 描述（仓库页右上 About 里填，带关键词）**：
- 短描述：`Open-source operating system for starting foreign trade with zero experience — 7 stages + runnable scripts.`
- 长描述（About 下方的 Description 框）：`An open-source foreign-trade workflow for absolute beginners: pick a market → find/vet leads → outreach → quote → deliver. Ships 4 stdlib-only Python scripts (lead scoring, outreach copy, follow-up plan, quoting engine) and 27 copy-paste AI prompts. Anonymous, no paid course.`

---

## 2. 开 GitHub Pages（P1，零安装 Demo）

Settings → Pages → Source 选 `main` / `/root` → Save。
几分钟后 `https://你的用户名.github.io/zero-to-trade/` 就是浏览器版分级 Demo（已写好 `index.html`）。

---

## 3. 借流量：PR 到 awesome 列表（P1，先验证再提）

> ⚠️ **核实后再 PR**：之前记录的 "awesome-foreign-trade 187★" 未经核实，GitHub 上 `foreign-trade` 主题下相关集合很少，**这个仓库可能不存在**。提 PR 前先搜一下确认它还活着，否则白费功夫。

可选项（按可行性排序）：
1. 搜 `topic:foreign-trade` / `topic:export` 下有没有活跃的 `awesome-*` 集合，有就提 PR。
2. 没有合适 awesome 列表时，**改投相关项目的 README「友链 / 相关项目」区**，或在外贸论坛/社群发帖（见第 5 步）。
3. 退路：不依赖外部 list，靠 Show HN + 博主（第 4、5 步）点火，这些更可控。

若确实有合适的 awesome 列表，PR 加一行：

```markdown
- [zero-to-trade](https://github.com/你的用户名/zero-to-trade) - 开源外贸工作流：7 环节 + 4 个零依赖可跑脚本（线索分级/建联文案/跟进计划/报价引擎），给零基础新手，匿名不卖课。
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

**首发评论（提交后立刻自己沙发，回答最高频问题 + 引流到 Demo）**：
```
Self-plug follow-up. The thing most people miss: it's not a course, it's a checklist + 4 scripts.

- No install needed: open index.html, paste a CSV, see T0-T3 tiering in the browser.
- Total beginner? docs/fast-path.md gets you from zero to your first reply in ~5 days.
- All scripts are stdlib-only Python 3.8+, run in 30s, no pip.
- Anonymous, MIT, no paid upsell. Happy to take feedback, especially from people selling into markets the docs don't cover yet.
```

**UTM 追踪（GitHub 不会告诉你 star 来自哪个渠道）**：在不同渠道发链接时带上不同 UTM 参数，方便事后看哪路点火最有效。例如：
- 微信/视频号：`?utm_source=wechat&utm_medium=social&utm_campaign=launch`
- Show HN：`?utm_source=news&utm_medium=hn&utm_campaign=launch`
- 博主 A：`?utm_source=bloggerA&utm_medium=collab&utm_campaign=launch`

GitHub 自身不解析 UTM，所以请**配合一张自建计数表**（Google Sheet / 飞书多维表），记录"哪天、哪个渠道、发了什么、当天新增 star"，累计到 100 个 star 后看来源集中度，集中处加投。

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
