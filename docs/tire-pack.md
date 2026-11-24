# 轮胎行业包：规格 + 市场 → GCC 要点 + 清关单证 + 注意事项

> **这是什么**：轮胎是这个仓库的主营品类，但 7 个环节的骨架是通用的——具体到某个规格发往某个市场，认证、单证、注意事项都不一样。这个脚本就是把「轮胎行业」的那层细节补上：你给一个 TBR 规格 + 一个目标市场，它吐出 GCC 认证要点、目的港清关单证清单、该市场注意事项。
>
> **先说清楚**：输出里的认证、单证、市场注意事项都是**一般性提示**，不是法规原文。每份输出末尾都写着「须以官方最新要求为准、发货前复核」——发货前务必按这句去官方渠道复核一遍，别拿脚本输出当法规原文去报关。

## 用法

```bash
# 最简：规格 + 市场
python scripts/tire_pack.py --size 11.00R20 --market nigeria

# 沙特：GCC 适用，JSON 输出，方便接进你自己的表格
python scripts/tire_pack.py --size 295/80R22.5 --market saudi --format json

# 自己填载重指数 / 速度级别（不填就用该规格的常见值）
python scripts/tire_pack.py --size 315/80R22.5 --market uae --li 156/150 --speed L

# 存成文件
python scripts/tire_pack.py --size 12.00R20 --market brazil --out pack.txt

# 只核对、不出包：先看缺什么（Check first: what is missing）
python scripts/tire_pack.py --check --size 11.00R20 --market nigeria
# 只缺常见值兜底也能出包，但值没核实；缺必填项时不出包，退出码 2
# (Only common-value fallbacks missing: the pack still builds, but the values are unverified; a required input missing: no pack, exit code 2)
```

市场名中文、英文、代码都能认：`尼日利亚 / nigeria / ng`、`沙特 / saudi / ksa`、`阿联酋 / uae` 都行。`--help` 里有 3 个亲手跑过的真实例子。

## 先核对再出包：`--check` / Check first, pack second

**Check first, then quote. / 先核对，再报价。**

`--li` / `--speed` 不填时，脚本会用该规格的常见值顶上去——`--check` 就是把这层"顶上去"挑明：它只核对、不出包，告诉你这份包里缺什么、哪些值是兜底、哪些值是你填了但还没核实的。报价前先跑一遍，缺项补齐厂家数据表数值后再报价，别拿常见值当报价依据。

**What `--check` tells you / `--check` 告诉你四件事：**

| 类别 / Category | 意思 / Meaning | 堵不堵出包 / Blocks the pack? |
|---|---|---|
| `missing` / 缺项 | 必填没给：规格 / 市场 | 堵：退出码 2，不出包 |
| `assumed` / 用了常见值 | 没填，用了该规格的常见值（未按厂家数据表核实） | 不堵：退出码 0，但值没核实 |
| `unverified` / 你填的（未核实） | 你自己填了，但仍未按厂家数据表核实 | 不堵：退出码 0，但值没核实 |
| `errors` / 报错 | 格式 / 范围错（规格不在 4 个里、市场不在 8 个里、`--li` 格式不对……） | 堵：先改，退出码 2 |

**Rule of thumb / 记住一条就行：** `ready` 只有在必填齐了、又没报错时才是真——`assumed` / `unverified` 不影响 `ready`，但影响你能不能直接拿去报价。常见值永远只是参考，报价前按厂家数据表把缺项补上。

**The exit code is the answer. / 退出码就是答案：** `0` = 必填齐了，可以出包（先把下面列的缺项核实了再报）；`2` = 缺必填项或有报错，先补上再跑。`--format json` 能把四类缺项以 JSON 打出来，接进你自己的表格；`--out` 能存成文件。

**Real output / 真实输出**——命令 / Command：`python scripts/tire_pack.py --check --size 11.00R20 --market nigeria`

```text
==================================================================
  Spec check / 规格核对：OK — nothing required is missing
  （必填项都齐了；下面列的是还没核实的值，报价前按厂家数据表复核）
==================================================================
  Assumed common values (not verified) / 用了常见值（未核实）（2 项）:
   1. load index: not given, using common value 150/147 for 11.00R20 (not verified against the manufacturer datasheet) / 载重指数：没填，用了 11.00R20 的常见值 150/147（未按厂家数据表核实）
   2. speed rating: not given, using common value K for 11.00R20 (not verified against the manufacturer datasheet) / 速度级别：没填，用了 11.00R20 的常见值 K（未按厂家数据表核实）
==================================================================
```

读法 / How to read it：标题写着 OK、退出码是 0——包能出；但下面 2 项明说载重指数、速度级别都用了常见值，没按厂家数据表核实。报价前先把这两个数跟厂家数据表对上。

另外两种情况 / Two more cases（都亲手跑过，退出码已核实）：

- 缺必填项：`python scripts/tire_pack.py --check --market nigeria`——标题变成 `NOT READY`，`Missing` 里写着规格没给，退出码 2。规格没给时，连常见值是多少都不知道，`assumed` 里会写 `common value unknown until the tire size is fixed / 规格定下来之前不知道常见值是多少`。
- 全给了也照样标出来：`python scripts/tire_pack.py --check --size 11.00R20 --market nigeria --li 150/147 --speed K`——退出码 0，但 `unverified` 里 2 项照列：值是你填的，仍未按厂家数据表核实。填了 ≠ 核实了。

**The pack itself says what is missing, too. / 包本身也写着缺什么：** 不用 `--check`、直接出包也行——每份包（表格版和 JSON 版）现在都自带缺项栏，表格版是 `To verify before you quote / 报价前先核实` 一节，JSON 版是 `gaps` 字段（见下面两个样例）。也就是说，缺项不会只藏在 `--check` 里，包本身就写清了哪些值是兜底、哪些没核实。

## 支持的规格与市场

| 规格 | 载重指数（常见值） | 速度级别（常见值） | 常见用途 |
|---|---|---|---|
| 11.00R20 | 150/147 | K（110 km/h） | 重载卡车、自卸车 |
| 12.00R20 | 154/151 | K（110 km/h） | 重载卡车、牵引车 |
| 295/80R22.5 | 152/148 | M（130 km/h） | 长途干线牵引车、挂车 |
| 315/80R22.5 | 156/150 | L（120 km/h） | 重载牵引车、工程车 |

| 市场 | 目的港 | GCC 适用 | 当地符合性程序 |
|---|---|---|---|
| 尼日利亚 | 拉各斯（Apapa / Tin Can Island） | 否 | SONCAP |
| 加纳 | 特马（Tema） | 否 | GSA 符合性评定 |
| 肯尼亚 | 蒙巴萨（Mombasa） | 否 | KEBS PVoC |
| 坦桑尼亚 | 达累斯萨拉姆（Dar es Salaam） | 否 | TBS PVoC |
| 哥伦比亚 | 卡塔赫纳 / 布埃纳文图拉 | 否 | 当地技术法规（出货前确认） |
| 巴西 | 桑托斯（Santos） | 否 | INMETRO 强制认证 |
| 沙特 | 吉达 / 达曼 | 是 | SASO / SABER |
| 阿联酋 | 杰贝阿里（Jebel Ali） | 是 | ECAS |

载重指数 / 速度级别表里写的是**常见值**，不是厂家数据表——最终以厂家数据表为准。`--li` / `--speed` 自己填了就按你填的走。

## 真实输出样例 1：11.00R20 → 尼日利亚（表格版）

命令：`python scripts/tire_pack.py --size 11.00R20 --market nigeria`

```text
==================================================================
  轮胎行业包：11.00R20 → 尼日利亚（Nigeria）
  目的港：拉各斯（Lagos，Apapa / Tin Can Island）
==================================================================
  规格：11.00R20 · 全钢子午线 TBR · 断面 11.00 英寸（约 279 mm） · 轮辋 20 英寸
  载重指数：150/147 · 速度级别：K（约 110 km/h，常见值）
  常见用途：重载卡车、自卸车：驱动轮与转向轮都常见
  （载重指数/速度级别是常见值，最终以厂家数据表为准）
------------------------------------------------------------------
  To verify before you quote / 报价前先核实（2 项）
   1. load index: not given, using common value 150/147 for 11.00R20 (not verified against the manufacturer datasheet) / 载重指数：没填，用了 11.00R20 的常见值 150/147（未按厂家数据表核实）
   2. speed rating: not given, using common value K for 11.00R20 (not verified against the manufacturer datasheet) / 速度级别：没填，用了 11.00R20 的常见值 K（未按厂家数据表核实）
------------------------------------------------------------------
  GCC 认证要点（不适用）
   1. 本市场不在海湾合作委员会（GCC）成员国之列，GCC 认证不适用；走当地符合性评定程序（见下方市场注意事项）。
------------------------------------------------------------------
  目的港清关单证清单（5 项，当地符合性程序：SONCAP）
   1. 原产地证（Certificate of Origin）
   2. 商业发票（Commercial Invoice）
   3. 装箱单（Packing List）
   4. 提单（Bill of Lading）
   5. SONCAP 符合性证书（PC 产品证书 + SC 装运证书）
------------------------------------------------------------------
  该市场注意事项
   1. SONCAP 是尼日利亚的装运前符合性评定程序：PC（产品证书）先行，每批货再凭 PC 申请 SC（装运证书），没 SC 到港清不了关。
   2. 轮胎属 SONCAP 管制产品，申请前确认本规格是否在当批管制清单里；清单会变，别拿上个月的清单当这批的依据。
   3. 发票金额、品名、规格要跟 SONCAP 证书逐字对得上，对不上就扣货补材料。
------------------------------------------------------------------
  须以官方最新要求为准、发货前复核。
==================================================================
```

读法：尼日利亚不在 GCC 成员国之列，所以 GCC 那节只有一句话「不适用」；重点在 SONCAP——PC 产品证书先行，每批货再凭 PC 申请 SC 装运证书，没 SC 到港清不了关。单证 5 项里第 5 项就是 SONCAP 符合性证书。表格里现在还多了一节「To verify before you quote / 报价前先核实」——这份包的 2 项缺项（载重指数、速度级别都用了常见值）直接写在包里，报价前先按厂家数据表核实。

## 真实输出样例 2：295/80R22.5 → 沙特（JSON 版）

命令：`python scripts/tire_pack.py --size 295/80R22.5 --market saudi --format json`

```json
{
  "pack": {
    "size": "295/80R22.5",
    "kind": "全钢子午线 TBR",
    "rim_in": 22.5,
    "section": "295 mm，扁平比 80",
    "load_index": "152/148",
    "speed_rating": "M（约 130 km/h，常见值）",
    "typical_use": "长途干线牵引车、挂车：高速路为主",
    "market": "沙特",
    "market_en": "Saudi Arabia",
    "port": "吉达（Jeddah）/ 达曼（Dammam）",
    "gcc_applies": true,
    "gcc_points": [
      "GSO 标志：海湾标准化组织（GSO）符合性标志；出货前确认标志样式与贴标位置（胎侧 / 包装）符合 GSO 当时的要求，别凭印象贴。",
      "检测报告：须由认可实验室出具，覆盖本规格、载重指数、速度级别；报告须在有效期内，过期报告等于没报告。",
      "GCC 符合性证书：凭检测报告向发证机构申请，出货前拿到手，随货走；到港查验时拿不出，柜子就得在港里等。"
    ],
    "program": "SASO / SABER",
    "docs": [
      "原产地证（Certificate of Origin）",
      "商业发票（Commercial Invoice）",
      "装箱单（Packing List）",
      "提单（Bill of Lading）",
      "GCC 符合性证书 + SABER 平台登记"
    ],
    "notes": [
      "沙特是 GCC 成员国，轮胎须过 GCC 认证（见上方要点），同时走 SASO 的 SABER 平台登记：产品先注册、再申请符合性证书。",
      "SABER 平台上产品分类、规格填错会导致证书无效，填之前跟买家逐项对一遍。",
      "沙特对轮胎标签、胎侧标识有专门要求，标签内容出货前按当时法规核对。"
    ],
    "gaps": [
      "load index: not given, using common value 152/148 for 295/80R22.5 (not verified against the manufacturer datasheet) / 载重指数：没填，用了 295/80R22.5 的常见值 152/148（未按厂家数据表核实）",
      "speed rating: not given, using common value M for 295/80R22.5 (not verified against the manufacturer datasheet) / 速度级别：没填，用了 295/80R22.5 的常见值 M（未按厂家数据表核实）"
    ],
    "disclaimer": "须以官方最新要求为准、发货前复核。"
  }
}
```

读法：沙特是 GCC 成员国，GCC 那节是 3 条实的——GSO 标志、检测报告、GCC 符合性证书；同时还要走 SASO 的 SABER 平台登记。JSON 版跟表格版是同一份数据，字段名见上，方便接进表格或别的脚本。`gaps` 字段就是这份包的缺项栏：这次 2 项都是常见值兜底（载重指数 152/148、速度级别 M 都没填），自己填了 `--li` / `--speed` 的话，这里列的就是你填的值、仍未核实。

## 常见报错

| 你看到的 | 原因 | 怎么办 |
|---|---|---|
| `✗ 规格 13.00R24 不在支持范围` | 只支持 4 个常见 TBR 规格 | 换表里的规格；别的规格确认厂家数据表后，等脚本加支持再跑 |
| `✗ 市场 mexico 不在支持范围` | 只支持 8 个市场 | 换表里的市场；墨西哥在永久排除名单里（反倾销税至 2029），本来也不做 |
| `✗ 载重指数 abc 格式不对` | `--li` 只认 `150` 或 `150/147` 这种 | 去掉字母，按格式重填 |
| `✗ 速度级别 KK 格式不对` | `--speed` 只认一个字母 | 写一个字母，如 K、L、M |
| `✗ 没给规格：--size 后面要跟一个规格……` | 少了 `--size`（退出码 1） | 补上规格；不知道怎么填就跑 `--help` |
| `✗ 没给市场：--market 后面要跟一个市场……` | 少了 `--market`（退出码 1） | 补上市场；`--size` / `--market` 不再是 argparse 层面的必填项，缺了给人话报错 |
| `Spec check / 规格核对：NOT READY`（退出码 2） | `--check` 时缺必填项或有报错 | 按下面列的缺项 / 报错补上；只有 `assumed` / `unverified` 时退出码是 0，包能出但值没核实 |

## 跟其他脚本怎么配合

- 先跑 `lead_score.py` 分级，再对 T0/T1 的客户跑 `tire_pack.py`：知道对方市场要什么证，开发信里才能写对一句——比如尼日利亚的客户，第一句就该问 SONCAP 的 PC 办了没有，而不是先报价格。
- 报价前跑一遍：巴西的 INMETRO 认证周期长、反倾销税要算进到岸成本，`quote_engine.py` 的 `--freight` / `--margin` 填之前，先看这份输出里的注意事项，别按裸价报。
- 背调时对照着看：`due_diligence.py` 的 L2「合规」那维，拿这份输出里的当地程序去核——客户说「证都齐了」，齐的是哪几项，对着清单一项项问。
- 每天跟进时顺带核对：`nudge.py --list` 的清单里，每家填了规格 + 市场，就会贴上这份包的一句话摘要 + 缺什么没核实——见 `docs/nudge.md` 的「每天一张清单」一节，两个工具一次跑通。
