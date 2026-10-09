# GITHUB_LAUNCH · 上线执行清单

一步一步照做。**✅ = 已经做完，⬜ = 还没做。** 每一步要么给了能直接复制的命令，要么给了点击路径。

两个前提：

- 用户名 `6hn68`、仓库名 `zero-to-trade`，下面命令里的这两个词别改。
- 只有**第 2 步（token）**真正有风险，看清楚再做。别的步骤搞错了都能重来。

---

## 0. 用户名已锁定（P0 · ✅ 已解除阻塞）

GitHub 用户名 = **`6hn68`**，仓库名 = **`zero-to-trade`**。代码里所有 issue 链接、Pages 链接、CI badge 已全部指向 `github.com/6hn68/zero-to-trade`，无需再替换。

- 涉及文件：`README.md`、`README_EN.md`、`README_ES.md`、`CONTRIBUTING.md`、`docs/00-getting-started.md`，以及 `README.md` 顶部的 CI badge URL
- 已修好的死链：`CONTRIBUTING.md` 与 `docs/00-getting-started.md` 里的 `TODO-your-username` 已全部换成 `6hn68`，无需再改。

> 仓库名保持 `zero-to-trade`，短、好搜、品类词直给。
> CI badge 在第一次 push 后、workflow 跑过一次才会显示状态（之前是灰色 "no status"，属正常）。

---

## 1. 建仓库 + 设 Topics / About（P0 · ✅ 已完成）

> ✅ 仓库已建，代码已推到 `origin/main`。下面的命令**留作记录，不用再执行**——除非你换电脑或者重建仓库。

**建仓**：GitHub → New repository → 名字 `zero-to-trade` → 选 Public → **不要**勾 Initialize with README（本地已有）→ Create。

**本地连远程并推**（要 token，见第 2 步）：
```bash
git remote add origin https://github.com/6hn68/zero-to-trade.git
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
- 短描述：`Open-source foreign-trade workflow for starting export with zero experience — 7 stages + 4 stdlib-only Python scripts (quoting engine is alpha).`
- 长描述（About 下方的 Description 框）：`An open-source foreign-trade workflow for absolute beginners: pick a market → find/vet leads → outreach → quote → deliver. Ships 4 stdlib-only Python scripts (lead scoring, outreach copy, follow-up plan, quoting engine) and 27 copy-paste AI prompts. Anonymous, no paid course.`

---

## 2. 🔴 推代码要 token：怎么弄才不出事（P0 · ⬜）

GitHub 早就**不接受账号密码推 HTTPS** 了。`git push` 弹出要密码时，那个"密码"必须是 token，填你的账号密码没用（会报 `Authentication failed`）。

### 生成：用 fine-grained PAT（细粒度令牌），别用 classic

1. 打开 GitHub 网页 → 右上角头像 → **Settings** → 左侧最下面 **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**。
2. 按这几项填，**每一项都别图省事**：

| 填什么 | 怎么填 | 为什么 |
|---|---|---|
| Token name | `ztt-push` | 随便，自己认得就行 |
| Expiration | **90 天** | **别选 No expiration**。过期了再生成一个，30 秒的事 |
| Repository access | **Only select repositories → 只勾 `zero-to-trade`** | 这条是整套方案的核心：就算 token 漏了，也只有这一个仓库出事 |
| Permissions | 展开 **Repository permissions** → **Contents** → **Read and write** | **别的权限一个都别开**，尤其别开 Admin / Delete |

3. 点 **Generate token**。
4. **token 只在生成完那一屏出现一次**，关掉就再也看不到。当场复制。

### 用（三选一）

**A. 让 git 问你（推荐，token 不进 shell history）**

```bash
git push -u origin main
# Username: 6hn68
# Password: <粘 token，屏幕上不回显，粘完直接回车>
```

**B. 直接拼进 URL（省事，但会留在 history 里）**

```bash
git remote set-url origin https://6hn68:<TOKEN>@github.com/6hn68/zero-to-trade.git
git push -u origin main
# 推完立刻换回干净的地址
git remote set-url origin https://github.com/6hn68/zero-to-trade.git
```

**C. 用 GitHub CLI（装了 `gh` 的话最舒服）**

```bash
gh auth login
git push -u origin main
```

### 🔴 三条不许做的事

1. **不许把 token 写进任何文件**——README、脚本、`.env`、这篇文档、截图，都不行。写了再删也没用，git 历史里还在。
2. **不许把 token 贴进任何对话窗口、聊天记录、求助帖**。要贴命令求助时，先把 token 那段换成 `<TOKEN>`。
3. **不许图省事用 classic PAT 并勾满 `repo`**。那是全部仓库的权限，漏一个等于全漏。

### 万一漏了

Settings → Developer settings → Personal access tokens → 找到那个 token → **Revoke / Delete**。
**先 revoke，再查仓库有没有被塞奇怪的 commit。** 顺序别反。

> 第 1 步已经推过了的话，这步可以先跳过——下次换电脑、或者 token 过期时再回来照做。

---

## 3. 发布前最后一遍脱敏（P0 · ⬜）

公开仓库 = 全世界可见，包括搜索引擎。**发外链之前做这一遍。**

```bash
git ls-files | xargs grep -nIE "(@[a-zA-Z0-9.-]+\.[a-z]{2,})|([0-9]{7,11})" 2>/dev/null | grep -viE "6hn68|github\.com|example"
```

- 前半段抓**邮箱**，后半段抓 **7–11 位连续数字**（手机号 / 座机）。
- 后面的 `grep -v` 是排掉本来就该公开的（`6hn68`、`github.com`）和占位域名（凡是含 `example` 的都跳过）。
- 当前仓库跑这条命令，只应该剩下一两处 `你的名字@你的公司域名.com` 这类教学占位符。**有别的输出就一条条看，别批量替换。**

再单独查一遍真实公司域名：

```bash
git ls-files | xargs grep -noE "\b[a-zA-Z0-9-]+\.(com|cn|net|de|ru|br|ae|sa)\b" 2>/dev/null | grep -viE "example|github|python|shields|star-history|qq|weixin|wechat|wikipedia"
```

当前仓库跑这条，应该只剩 `gmail.com`（文档里拿它当反例）。**多出来任何一个域名都要看一眼。**

**要清的东西**：真实公司名、真实人名、邮箱、电话、WhatsApp 号、真实客户域名、后台截图里露出的账号。
文档里需要举例就用 `example.com` / `某某公司` / `buyer@example.com` 这类占位符。

> 已经推过了也能补：改掉、提交一次就行。但要明白——**git 历史里那份还在**。真有严重泄露（比如真实客户名单），只能重建仓库，别指望删文件能抹掉。

---

## 4. 开 GitHub Pages（P1 · ⬜）

入口：仓库页顶部 → **Settings**（不是头像那个 Settings，是仓库里的）→ 左侧 **Pages** → **Build and deployment** → Source 选 **Deploy from a branch** → Branch 选 `main`、目录选 `/ (root)` → **Save**。

几分钟后打开 `https://6hn68.github.io/zero-to-trade/` 就是浏览器版分级 Demo（`index.html` 已写好）。

- 一直 404：等 5–10 分钟再刷，Pages 第一次构建会慢。
- 还是 404：回 Settings → Pages 看顶部有没有显示 "Your site is live at ..."，没有就是没保存成功。

---

## 5. 传 social-preview.png（P1 · ⬜）

`assets/social-preview.png` 已经在仓库里了（1280×640），但**得手动上传 GitHub 才会用**。不传的话，把链接甩到微信群/推特里，显示的是一个灰白默认图。

入口：仓库页 → **Settings** → 左侧 **General**（默认就在这页）→ 往下滚到 **Social preview** → **Edit** → 把 `assets/social-preview.png` 拖进去 → **Save**。

检查：把仓库链接粘到微信 / Slack 里看一眼预览图出来了没。

---

## 6. 发 v0.1 Release（P0 · ⬜）

这是目前**唯一确定还欠着的仓库内动作**（`git tag` 现在是空的）。发一个能被 Google 收录，也让仓库页看着像个还在维护的项目。

### A. 命令行

```bash
git tag -a v0.1 -m "v0.1: 7 步工作流 + 4 个纯标准库脚本 + 浏览器 Demo"
git push origin v0.1
gh release create v0.1 --title "v0.1 · 第一版" --notes "## 这一版有什么
- 7 步外贸工作流：选市场 → 找客户 → 背调 → 建联 → 谈判 → 报价 → 交单
- 4 个纯标准库 Python 脚本（线索分级 / 建联文案 / 跟进计划 / 报价引擎），Python 3.8+，不用 pip install
- index.html：浏览器打开就能跑的零安装 Demo
- 27 条可复制的 AI prompt
- 中 / 英 / 西 三语 README

## 还粗糙的地方
- 报价引擎是 alpha，没接真实海关数据
- 文档里的样例数据都是编的，别当行情用

MIT。匿名作者，不卖课。"
```

### B. 网页点

仓库页右侧 **Releases** → **Create a new release** → **Choose a tag** 里输入 `v0.1` 并选 "Create new tag on publish" → 标题填 `v0.1 · 第一版` → 描述框粘上面 `## 这一版有什么` 之后的内容 → 勾 **Set as the latest release** → **Publish release**。

### 自查

```bash
git tag            # 应该看到 v0.1
gh release list    # 应该看到 v0.1，Latest
```

---

## 7. 检查 badge（P1 · ⬜）

README 顶部那个 CI badge，要等 workflow 第一次跑完才有状态。**一直是灰色 "no status" 是正常的，不是坏了。**

```bash
gh run list --limit 5    # 看 workflow 跑没跑、绿没绿
```

或者：仓库页 → **Actions** → 点最新一条 → 看是不是绿色对勾。

- 绿了 → badge 自己会变，等几分钟刷新 README 页面。
- 红了 → 点进去看日志。脚本是纯标准库的，失败最常见的原因是 Python 版本（要 3.8+）。
- 一直灰 → 确认 workflow 文件真推上去了：`git ls-files .github/workflows/`（应该看到 `ci.yml`）。

---

## 8. 借流量：PR 到 awesome 列表（P2 · ⬜，先验证再提）

> ⚠️ **先搜再提**。之前记过几个"外贸 awesome 列表"的名字，后来核不实，`foreign-trade` 这个主题下真正活跃的集合很少。提 PR 之前自己搜一遍确认它还活着，别对着一个不存在的仓库忙活。

```bash
gh search repos --topic foreign-trade --limit 20
gh search repos --topic export --limit 20
```

三条路，按顺序试：

1. 上面搜出来有活跃的 `awesome-*` 集合 → 提 PR。
2. 没有 → 改投相关项目的 README「相关项目」区，或者去外贸论坛发帖（`STAR-GROWTH.md` 4.3 的知乎那条也能用）。
3. 都没有 → 就别在这上面耗了，靠 Show HN + 博主（第 9、10 步）就行。

若确实有合适的 awesome 列表，PR 加一行：

```markdown
- [zero-to-trade](https://github.com/6hn68/zero-to-trade) - 开源外贸工作流：7 环节 + 4 个零依赖可跑脚本（线索分级/建联文案/跟进计划/报价引擎），给零基础新手，匿名不卖课。
```

PR 标题建议：`add zero-to-trade: open-source foreign trade workflow for beginners`

---

## 9. 点火：Show HN（P1 · ⬜，技术背书 / 外链，非主引擎）

> 优先级：0→1 的主引擎是中文社媒 + 中腰部博主（STAR-GROWTH 第二节，P0）。Show HN 只是顺手发一次，别指望它。完整文案（含周日 12–14 UTC 的发帖时段、首发评论）在 `STAR-GROWTH.md` 4.4，这里不重复。

入口：打开 `news.ycombinator.com` → **Submit** → 把 `STAR-GROWTH.md` 4.4 里的标题和正文**原样**粘进去（别自己改写，那版是按 HN 的口味调过的）→ 提交完立刻发那条首发评论 → 蹲 2–6 小时回评论，包括骂你的。

想配图就用 `index.html` 跑出来的分级表截图，或者录 30 秒 GIF。

**UTM** 统一按 `STAR-GROWTH.md` 4.6 那张表来，Show HN 用的是：

```
https://github.com/6hn68/zero-to-trade?utm_source=hn&utm_medium=news&utm_campaign=launch
```

GitHub 自己不解析 UTM，光加参数没用，得自己记一张表（`STAR-GROWTH.md` 第五节）。

---

## 10. 投中腰部外贸博主（P2 · ⬜）

目标：抖音 / 小红书 / 视频号上 **3–5 个**"外贸实操"中腰部博主，几万粉就够——大 V 不看私信，别浪费时间。

完整筛选标准、暖场节奏和私信模板在 `STAR-GROWTH.md` 4.5，这里只记两条：

- **先在他评论区认真留 3–5 天言，再私信。** 上来就私信 = 广告 = 不回。
- 素材包就两样：Pages 的 Demo 链接（第 4 步那个）+ README 截图 2 张。别发长文件。

---

## 11. 养趋势：Star History（P2 · ⬜）

README 里已经嵌了 Star History 图，放着就行。等 30 天闸门过了（`STAR-GROWTH.md` 3.1），拿它对齐一下"哪天涨了一波"和"那天发了什么"，比看总数有用。

---

## 12. 扩面：多语言（P3 · ⬜，30 天内别做）

中 / 英 / 西三语 README 已经在了。下一个要不要上阿拉伯语，等 30 天结果出来再说。

真要做：保持六段结构、术语对齐 `GLOSSARY.md`，流程见 `CONTRIBUTING.md`。

---

## 13. 长大：把 v0.2 报价引擎做扎实（P3 · ⬜）

`scripts/quote_engine.py` 现在是 alpha。下一步是让它接真实的海关数据做锚价——这是整个项目里最可能真的有用的部分，比发 10 条视频号有用。

但它是"做给需要它的人"，不是"做给 star"。顺序别搞反。
