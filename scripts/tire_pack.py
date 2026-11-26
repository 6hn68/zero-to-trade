#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轮胎行业包。给你一个 TBR 规格 + 一个目标市场，它吐出三样东西：
GCC 认证要点、目的港清关单证清单、该市场注意事项。

只用了标准库，Python 3.10 往上都能直接跑，不联网，不写文件（除非你自己加 --out）。

用法:
    python scripts/tire_pack.py --size 11.00R20 --market nigeria
    python scripts/tire_pack.py --size 295/80R22.5 --market saudi --format json
    python scripts/tire_pack.py --size 315/80R22.5 --market uae --li 156/150 --speed L
    python scripts/tire_pack.py --size 12.00R20 --market brazil --out pack.txt

    # 只核对、不出包：先看缺什么（Check first: what is missing）
    python scripts/tire_pack.py --check --size 11.00R20 --market nigeria
    python scripts/tire_pack.py --check --market nigeria --li 150/147
    # 第一行缺了规格，第二行缺了规格、速度级别用了常见值——都明说，不悄悄兜底。
    # --check 只列缺项：必填没给的叫 missing，空着用了常见值的叫 assumed，
    # 自己填了但还没按厂家数据表核实的叫 unverified。缺必填项时退出码是 2；
    # 只有 assumed / unverified 时退出码是 0（包能出，但值没核实）。

参数:
    --size          轮胎规格，必填。只支持 4 个常见 TBR 规格：
                    11.00R20 / 12.00R20 / 295/80R22.5 / 315/80R22.5
    --market        目标市场，必填。8 个市场：尼日利亚 / 加纳 / 肯尼亚 / 坦桑尼亚 /
                    哥伦比亚 / 巴西 / 沙特 / 阿联酋（中文名、英文名、代码都能认）
    --li            载重指数，如 150/147。不填就用该规格的常见值（见下表）
    --speed         速度级别，如 K。不填就用该规格的常见值（见下表）
    --format        table(默认) / json
    --out           同时写入文件（UTF-8），不指定则只打印

常见值（只是常见值，不是厂家数据表）:
    规格            载重指数    速度级别    常见用途
    11.00R20       150/147     K(110km/h)  重载卡车、自卸车
    12.00R20       154/151     K(110km/h)  重载卡车、牵引车
    295/80R22.5    152/148     M(130km/h)  长途干线牵引车、挂车
    315/80R22.5    156/150     L(120km/h)  重载牵引车、工程车

三条规矩：
    认证、单证、市场注意事项都是「一般性提示」，不是法规原文——
    每份输出末尾都写着「须以官方最新要求为准、发货前复核」，发货前务必按这句去做。
    载重指数/速度级别以厂家数据表为准，这里只给常见值做参考。
    示例里不出现任何真实公司、真实价格、真实联系方式。
"""

import argparse
import json
import re
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lead_score import _ZhArgumentParser  # noqa: E402

DISCLAIMER = "须以官方最新要求为准、发货前复核。"

# 4 个常见 TBR 规格：载重指数/速度级别是「常见值」，不是厂家数据表
TIRE_SIZES = {
    "11.00R20": {
        "display": "11.00R20",
        "kind": "全钢子午线 TBR",
        "rim_in": 20,
        "section": "11.00 英寸（约 279 mm）",
        "common_li": "150/147",
        "common_speed": "K",
        "speed_kmh": 110,
        "typical_use": "重载卡车、自卸车：驱动轮与转向轮都常见",
    },
    "12.00R20": {
        "display": "12.00R20",
        "kind": "全钢子午线 TBR",
        "rim_in": 20,
        "section": "12.00 英寸（约 305 mm）",
        "common_li": "154/151",
        "common_speed": "K",
        "speed_kmh": 110,
        "typical_use": "重载卡车、牵引车：比 11.00R20 再大一号",
    },
    "295/80R22.5": {
        "display": "295/80R22.5",
        "kind": "全钢子午线 TBR",
        "rim_in": 22.5,
        "section": "295 mm，扁平比 80",
        "common_li": "152/148",
        "common_speed": "M",
        "speed_kmh": 130,
        "typical_use": "长途干线牵引车、挂车：高速路为主",
    },
    "315/80R22.5": {
        "display": "315/80R22.5",
        "kind": "全钢子午线 TBR",
        "rim_in": 22.5,
        "section": "315 mm，扁平比 80",
        "common_li": "156/150",
        "common_speed": "L",
        "speed_kmh": 120,
        "typical_use": "重载牵引车、工程车：载重最大的一档",
    },
}

# GCC（海湾合作委员会）认证要点：只适用于 GCC 成员国市场（本表里的沙特、阿联酋）
GCC_POINTS = [
    "GSO 标志：海湾标准化组织（GSO）符合性标志；出货前确认标志样式与贴标位置"
    "（胎侧 / 包装）符合 GSO 当时的要求，别凭印象贴。",
    "检测报告：须由认可实验室出具，覆盖本规格、载重指数、速度级别；"
    "报告须在有效期内，过期报告等于没报告。",
    "GCC 符合性证书：凭检测报告向发证机构申请，出货前拿到手，随货走；"
    "到港查验时拿不出，柜子就得在港里等。",
]

NON_GCC_POINT = ("本市场不在海湾合作委员会（GCC）成员国之列，GCC 认证不适用；"
                 "走当地符合性评定程序（见下方市场注意事项）。")

# 每个市场都有的 4 项基础单证；第 5 项是各市场的符合性证书
COMMON_DOCS = [
    "原产地证（Certificate of Origin）",
    "商业发票（Commercial Invoice）",
    "装箱单（Packing List）",
    "提单（Bill of Lading）",
]

MARKETS = {
    "nigeria": {
        "code": "nigeria",
        "name": "尼日利亚",
        "name_en": "Nigeria",
        "port": "拉各斯（Lagos，Apapa / Tin Can Island）",
        "gcc": False,
        "program": "SONCAP",
        "cert_doc": "SONCAP 符合性证书（PC 产品证书 + SC 装运证书）",
        "notes": [
            "SONCAP 是尼日利亚的装运前符合性评定程序：PC（产品证书）先行，"
            "每批货再凭 PC 申请 SC（装运证书），没 SC 到港清不了关。",
            "轮胎属 SONCAP 管制产品，申请前确认本规格是否在当批管制清单里；"
            "清单会变，别拿上个月的清单当这批的依据。",
            "发票金额、品名、规格要跟 SONCAP 证书逐字对得上，对不上就扣货补材料。",
        ],
    },
    "ghana": {
        "code": "ghana",
        "name": "加纳",
        "name_en": "Ghana",
        "port": "特马（Tema）",
        "gcc": False,
        "program": "GSA 符合性评定",
        "cert_doc": "加纳标准局（GSA）符合性证书",
        "notes": [
            "加纳对进口轮胎有符合性评定要求，出货前向加纳标准局（GSA）"
            "或其授权机构确认本规格的评定流程与所需文件。",
            "目的港查验较严，单证上的规格、数量、唛头要跟实货一致。",
        ],
    },
    "kenya": {
        "code": "kenya",
        "name": "肯尼亚",
        "name_en": "Kenya",
        "port": "蒙巴萨（Mombasa）",
        "gcc": False,
        "program": "KEBS PVoC",
        "cert_doc": "PVoC 符合性证书（CoC，肯尼亚标准局 KEBS）",
        "notes": [
            "肯尼亚实行装运前符合性验证（PVoC）：出货前须取得 CoC，"
            "没 CoC 到港要补检，费用和时间都翻倍。",
            "轮胎须符合肯尼亚标准局（KEBS）当时的技术要求，"
            "新旧胎政策、胎龄限制出货前先确认。",
        ],
    },
    "tanzania": {
        "code": "tanzania",
        "name": "坦桑尼亚",
        "name_en": "Tanzania",
        "port": "达累斯萨拉姆（Dar es Salaam）",
        "gcc": False,
        "program": "TBS PVoC",
        "cert_doc": "PVoC 符合性证书（CoC，坦桑尼亚标准局 TBS）",
        "notes": [
            "坦桑尼亚同样实行装运前符合性验证（PVoC），出货前须取得 CoC。",
            "达累斯萨拉姆港是东非内陆国家的转口门户，单证上写清最终目的地，"
            "避免转口环节被当成当地货扣下。",
        ],
    },
    "colombia": {
        "code": "colombia",
        "name": "哥伦比亚",
        "name_en": "Colombia",
        "port": "卡塔赫纳（Cartagena）/ 布埃纳文图拉（Buenaventura）",
        "gcc": False,
        "program": "当地技术法规（出货前确认）",
        "cert_doc": "符合性证书（按哥伦比亚当时要求，出货前确认是否需要）",
        "notes": [
            "哥伦比亚对进口轮胎的技术要求以其当时的技术法规为准，"
            "出货前向买家或当地代理确认是否需要符合性证书、贴什么标签。",
            "反倾销是拉美轮胎的老话题：出货前确认本规格、本原产地"
            "是否在反倾销措施范围内，别等到港才发现要补税。",
        ],
    },
    "brazil": {
        "code": "brazil",
        "name": "巴西",
        "name_en": "Brazil",
        "port": "桑托斯（Santos）",
        "gcc": False,
        "program": "INMETRO 强制认证",
        "cert_doc": "INMETRO 认证证书（轮胎属强制认证产品）",
        "notes": [
            "巴西对轮胎实行 INMETRO 强制认证：没认证的轮胎进不了巴西市场，"
            "认证周期长，第一次做要提前几个月启动。",
            "巴西对华卡客车胎反倾销税是按生产商分档的从量税 US$1.05–2.59/kg"
            "（Gecex 198/2021 号决议）；日落复审已于 2026-03-20 启动（Circular SECEX 20/2026），"
            "复审期间税照收，结论期限延至 12 个月（约 2027-03-20），结果未定，出货前查官方原文。"
            "报价前先把税算进到岸成本，别按裸价报。",
            "清关单证须葡萄牙语或附葡语翻译件，品名、规格翻译要跟认证证书一致。",
        ],
    },
    "saudi": {
        "code": "saudi",
        "name": "沙特",
        "name_en": "Saudi Arabia",
        "port": "吉达（Jeddah）/ 达曼（Dammam）",
        "gcc": True,
        "program": "SASO / SABER",
        "cert_doc": "GCC 符合性证书 + SABER 平台登记",
        "notes": [
            "沙特是 GCC 成员国，轮胎须过 GCC 认证（见上方要点），"
            "同时走 SASO 的 SABER 平台登记：产品先注册、再申请符合性证书。",
            "SABER 平台上产品分类、规格填错会导致证书无效，"
            "填之前跟买家逐项对一遍。",
            "沙特对轮胎标签、胎侧标识有专门要求，标签内容出货前按当时法规核对。",
        ],
    },
    "uae": {
        "code": "uae",
        "name": "阿联酋",
        "name_en": "United Arab Emirates",
        "port": "杰贝阿里（Jebel Ali）",
        "gcc": True,
        "program": "ECAS",
        "cert_doc": "GCC 符合性证书 + ECAS 注册",
        "notes": [
            "阿联酋是 GCC 成员国，轮胎须过 GCC 认证（见上方要点），"
            "同时走 ECAS（阿联酋符合性评定体系）注册。",
            "杰贝阿里是中东转口枢纽：货是当地卖还是转口第三国，"
            "单证与认证要求不一样，出货前跟买家确认清楚再走。",
            "阿联酋对轮胎胎龄、仓储条件有要求，长期露天堆存会影响查验结果。",
        ],
    },
}

# 市场别名：中文名、英文名、常见代码都能认
MARKET_ALIASES = {
    "nigeria": "nigeria", "尼日利亚": "nigeria", "ng": "nigeria",
    "ghana": "ghana", "加纳": "ghana", "gh": "ghana",
    "kenya": "kenya", "肯尼亚": "kenya", "ke": "kenya",
    "tanzania": "tanzania", "坦桑尼亚": "tanzania", "tz": "tanzania",
    "colombia": "colombia", "哥伦比亚": "colombia", "co": "colombia",
    "brazil": "brazil", "巴西": "brazil", "br": "brazil",
    "saudi": "saudi", "沙特": "saudi", "沙特阿拉伯": "saudi",
    "saudi arabia": "saudi", "ksa": "saudi", "sa": "saudi",
    "uae": "uae", "阿联酋": "uae", "united arab emirates": "uae", "ae": "uae",
}


def normalize_size(size):
    """规格归一化：去空格、转大写；只认 4 个常见 TBR 规格，别的直接报错。"""
    if size is None:
        raise ValueError("没给规格：--size 后面要跟一个规格，如 11.00R20")
    s = str(size).strip().upper().replace(" ", "")
    if s in TIRE_SIZES:
        return s
    raise ValueError(
        "规格 %s 不在支持范围：本脚本只支持 4 个常见 TBR 规格——"
        "11.00R20、12.00R20、295/80R22.5、315/80R22.5。"
        "别的规格先别硬套，确认厂家数据表后再加。" % (size,))


def normalize_market(market):
    """市场归一化：中文名、英文名、代码都能认；认不出就报 8 个市场给你挑。"""
    if market is None:
        raise ValueError("没给市场：--market 后面要跟一个市场，如 nigeria 或 尼日利亚")
    m = str(market).strip().lower()
    if m in MARKET_ALIASES:
        return MARKET_ALIASES[m]
    raise ValueError(
        "市场 %s 不在支持范围：本脚本只支持 8 个市场——"
        "尼日利亚、加纳、肯尼亚、坦桑尼亚、哥伦比亚、巴西、沙特、阿联酋。"
        "（英文名 nigeria / ghana / kenya / tanzania / colombia / brazil / saudi / uae 也能认）"
        % (market,))


def _check_li(li):
    """载重指数：单值（150）或双值（150/147）都行，范围 100–180，别的直接报错。"""
    if li is None:
        return None
    s = str(li).strip()
    if not re.fullmatch(r"\d{3}(/\d{3})?", s):
        raise ValueError("载重指数 %s 格式不对：写 150 或 150/147 这种，别带字母。" % li)
    for part in s.split("/"):
        if not 100 <= int(part) <= 180:
            raise ValueError("载重指数 %s 超出合理范围（100–180）：是不是把速度级别也写进来了？" % li)
    return s


def _check_speed(speed):
    """速度级别：单个大写字母，TBR 常见 K/L/M；别的字母先警告不拦路。"""
    if speed is None:
        return None
    s = str(speed).strip().upper()
    if not re.fullmatch(r"[A-Z]", s):
        raise ValueError("速度级别 %s 格式不对：写一个字母，如 K、L、M。" % speed)
    return s


# Spec checklist — what a complete spec pack needs, and what is only a
# common-value fallback. Every line is English first, Chinese after.
# 规格核对表：一份完整的规格包需要什么，哪些只是常见值兜底。
# 每行英文在前、中文在后。
_FIELD_LABELS = {
    "size": ("tire size", "轮胎规格"),
    "market": ("target market", "目标市场"),
    "load_index": ("load index", "载重指数"),
    "speed_rating": ("speed rating", "速度级别"),
}


def _gap_line(field, detail_en, detail_zh):
    """One checklist line: 'load index: ... / 载重指数：...'."""
    en, zh = _FIELD_LABELS[field]
    return "%s: %s / %s：%s" % (en, detail_en, zh, detail_zh)


def check_spec(size=None, market=None, li=None, speed=None):
    """Check a spec pack before you build it — and say exactly what is missing.

    Returns a dict with four lists (each item is one plain-language line,
    English first, Chinese after) plus a ready flag:
      missing    — required inputs not given at all (size / market).
      assumed    — optional inputs left blank, so a common value is used
                   instead (load index / speed rating). The pack still
                   builds, but the value is NOT from the manufacturer
                   datasheet — verify it before you quote.
      unverified — optional inputs you filled in yourself. They are used
                   as given, but they are still NOT verified against the
                   manufacturer datasheet.
      errors     — inputs that fail validation (unknown size / market,
                   bad load-index / speed format). Fix these first.
    "ready" is True only when nothing is missing and nothing errors;
    assumed / unverified items do not block the build, they just get
    listed so nobody mistakes a fallback for a verified fact.
    """
    missing, assumed, unverified, errors = [], [], [], []

    size_key = None
    if size is None or not str(size).strip():
        missing.append(_gap_line("size", "not given — give one of 11.00R20 / "
                                  "12.00R20 / 295/80R22.5 / 315/80R22.5",
                                  "没给——从 11.00R20 / 12.00R20 / 295/80R22.5 / "
                                  "315/80R22.5 里给一个"))
    else:
        try:
            size_key = normalize_size(size)
        except ValueError as e:
            errors.append(str(e))

    market_key = None
    if market is None or not str(market).strip():
        missing.append(_gap_line("market", "not given — give one of Nigeria / "
                                  "Ghana / Kenya / Tanzania / Colombia / Brazil / "
                                  "Saudi Arabia / UAE",
                                  "没给——从尼日利亚 / 加纳 / 肯尼亚 / 坦桑尼亚 / "
                                  "哥伦比亚 / 巴西 / 沙特 / 阿联酋里给一个"))
    else:
        try:
            market_key = normalize_market(market)
        except ValueError as e:
            errors.append(str(e))

    # Load index / speed rating: only name the common value when the size
    # itself is valid — otherwise the fallback is unknown, say that instead.
    for field, raw, checker in (("load_index", li, _check_li),
                                ("speed_rating", speed, _check_speed)):
        if raw is None or not str(raw).strip():
            if size_key is not None:
                common = (TIRE_SIZES[size_key]["common_li"] if field == "load_index"
                          else TIRE_SIZES[size_key]["common_speed"])
                assumed.append(_gap_line(
                    field, "not given, using common value %s for %s "
                    "(not verified against the manufacturer datasheet)"
                    % (common, size_key),
                    "没填，用了 %s 的常见值 %s（未按厂家数据表核实）"
                    % (size_key, common)))
            else:
                assumed.append(_gap_line(
                    field, "not given — common value unknown until the tire "
                    "size is fixed", "没填——规格定下来之前不知道常见值是多少"))
        else:
            try:
                checker(raw)
            except ValueError as e:
                errors.append(str(e))
            else:
                unverified.append(_gap_line(
                    field, "%s as given by you — still not verified against "
                    "the manufacturer datasheet" % str(raw).strip(),
                    "按你填的 %s 走，仍未按厂家数据表核实" % str(raw).strip()))

    return {
        "missing": missing,
        "assumed": assumed,
        "unverified": unverified,
        "errors": errors,
        "ready": not missing and not errors,
    }


def build_tire_pack(size, market, li=None, speed=None):
    """核心纯函数：规格 + 市场 → GCC 要点 + 清关单证 + 市场注意事项。

    不联网、不读文件、不写文件；--li/--speed 不填就用该规格的常见值，
    但常见值只是参考，载重指数/速度级别最终以厂家数据表为准。
    """
    key = normalize_size(size)
    mkey = normalize_market(market)
    spec = TIRE_SIZES[key]
    mkt = MARKETS[mkey]

    # Gaps first: which values are common-value fallbacks or your own
    # un-verified input — so the pack itself says what is still missing.
    # 先算缺项：哪些值是常见值兜底、哪些是你填了但还没核实的——包里直接写出来。
    check = check_spec(size, market, li, speed)

    li = _check_li(li) or spec["common_li"]
    speed = _check_speed(speed) or spec["common_speed"]
    speed_note = ""
    if speed == spec["common_speed"]:
        speed_note = "%s（约 %s km/h，常见值）" % (speed, spec["speed_kmh"])
    else:
        speed_note = "%s（你填的值，以厂家数据表为准）" % speed

    gcc_points = list(GCC_POINTS) if mkt["gcc"] else [NON_GCC_POINT]
    docs = list(COMMON_DOCS) + [mkt["cert_doc"]]

    return {
        "size": spec["display"],
        "kind": spec["kind"],
        "rim_in": spec["rim_in"],
        "section": spec["section"],
        "load_index": li,
        "speed_rating": speed_note,
        "typical_use": spec["typical_use"],
        "market": mkt["name"],
        "market_en": mkt["name_en"],
        "port": mkt["port"],
        "gcc_applies": mkt["gcc"],
        "gcc_points": gcc_points,
        "program": mkt["program"],
        "docs": docs,
        "notes": list(mkt["notes"]),
        "gaps": check["assumed"] + check["unverified"],
        "disclaimer": DISCLAIMER,
    }




def render_table(p):
    W = 66
    s = []
    s.append("=" * W)
    s.append("  轮胎行业包：%s → %s（%s）" % (p["size"], p["market"], p["market_en"]))
    s.append("  目的港：%s" % p["port"])
    s.append("=" * W)
    s.append("  规格：%s · %s · 断面 %s · 轮辋 %s 英寸"
             % (p["size"], p["kind"], p["section"], p["rim_in"]))
    s.append("  载重指数：%s · 速度级别：%s" % (p["load_index"], p["speed_rating"]))
    s.append("  常见用途：%s" % p["typical_use"])
    s.append("  （载重指数/速度级别是常见值，最终以厂家数据表为准）")
    if p.get("gaps"):
        s.append("-" * W)
        s.append("  To verify before you quote / 报价前先核实（%d 项）" % len(p["gaps"]))
        for i, gap in enumerate(p["gaps"], 1):
            s.append("   %d. %s" % (i, gap))
    s.append("-" * W)
    s.append("  GCC 认证要点（%s）" % ("适用" if p["gcc_applies"] else "不适用"))
    for i, point in enumerate(p["gcc_points"], 1):
        s.append("   %d. %s" % (i, point))
    s.append("-" * W)
    s.append("  目的港清关单证清单（%d 项，当地符合性程序：%s）"
             % (len(p["docs"]), p["program"]))
    for i, doc in enumerate(p["docs"], 1):
        s.append("   %d. %s" % (i, doc))
    s.append("-" * W)
    s.append("  该市场注意事项")
    for i, note in enumerate(p["notes"], 1):
        s.append("   %d. %s" % (i, note))
    s.append("-" * W)
    s.append("  %s" % p["disclaimer"])
    s.append("=" * W)
    return "\n".join(s)




def render_check(check):
    """Human-readable checklist from check_spec: what is missing, what fell
    back to a common value, what you filled in but have not verified yet,
    and what fails validation. English first, Chinese after."""
    W = 66
    s = []
    s.append("=" * W)
    if check["ready"]:
        s.append("  Spec check / 规格核对：OK — nothing required is missing")
        s.append("  （必填项都齐了；下面列的是还没核实的值，报价前按厂家数据表复核）")
    else:
        s.append("  Spec check / 规格核对：NOT READY — fix the items below first")
        s.append("  （还不能出包：先把下面标出来的缺项 / 报错补上）")
    s.append("=" * W)
    sections = (
        ("missing", "Missing (required, not given) / 缺项（必填没给）"),
        ("assumed", "Assumed common values (not verified) / 用了常见值（未核实）"),
        ("unverified", "Filled in by you (not verified) / 你填的（未核实）"),
        ("errors", "Errors — fix first / 报错，先改"),
    )
    shown = False
    for key, title in sections:
        items = check[key]
        if not items:
            continue
        shown = True
        s.append("  %s（%d 项）:" % (title, len(items)))
        for i, item in enumerate(items, 1):
            s.append("   %d. %s" % (i, item))
    if not shown:
        s.append("  Nothing to flag / 没什么要标的：规格、市场、载重指数、速度级别"
                 "都给了，值仍以厂家数据表为准。")
    s.append("=" * W)
    return "\n".join(s)


def main():
    p = _ZhArgumentParser(
        prog="tire_pack.py",
        description="轮胎行业包：规格 + 市场 → GCC 认证要点 + 清关单证 + 市场注意事项",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例（都亲手跑过，输出见 docs/tire-pack.md）：\n"
               "  python scripts/tire_pack.py --size 11.00R20 --market nigeria\n"
               "    → GCC 不适用；单证 5 项（含 SONCAP 符合性证书）；注意事项 3 条\n"
               "  python scripts/tire_pack.py --size 295/80R22.5 --market saudi --format json\n"
               "    → GCC 适用：GSO 标志 + 检测报告 + GCC 符合性证书；SABER 平台登记\n"
               "  python scripts/tire_pack.py --size 315/80R22.5 --market uae --li 156/150 --speed L\n"
               "    → GCC 适用；ECAS 注册；杰贝阿里转口先确认是当地卖还是转口\n"
               "  只核对、不出包：\n"
               "  python scripts/tire_pack.py --check --size 11.00R20 --market nigeria\n"
               "    → 缺 2 项：载重指数、速度级别用了常见值（未按厂家数据表核实）\n"
               "  python scripts/tire_pack.py --check --market nigeria\n"
               "    → 缺 1 项必填：规格没给（退出码 2）\n"
               "  认证与单证都是一般性提示，不是法规原文：发货前按输出末尾那句\n"
               "  「须以官方最新要求为准、发货前复核」去官方渠道复核一遍。")
    p.add_argument("--size", required=False, default=None,
                   help="轮胎规格：11.00R20 / 12.00R20 / 295/80R22.5 / 315/80R22.5")
    p.add_argument("--market", required=False, default=None,
                   help="目标市场：尼日利亚/加纳/肯尼亚/坦桑尼亚/哥伦比亚/巴西/沙特/阿联酋"
                        "（英文名 nigeria/gh.../saudi/uae 也能认）")
    p.add_argument("--li", default=None, help="载重指数，如 150/147；不填用该规格常见值")
    p.add_argument("--speed", default=None, help="速度级别，如 K；不填用该规格常见值")
    p.add_argument("--check", action="store_true",
                   help="只核对缺什么，不出完整包：列出缺项/用了常见值的项/未核实项")
    p.add_argument("--format", choices=["table", "json"], default="table")
    p.add_argument("--out", default=None, help="把结果写入文件(UTF-8)")
    if len(sys.argv) == 1:
        p.print_usage(sys.stderr)
        print("\n没给参数：不知道怎么填就跑 python scripts/tire_pack.py --help，"
              "里面有能直接复制的例子。", file=sys.stderr)
        raise SystemExit(2)
    args = p.parse_args()

    if args.check:
        check = check_spec(args.size, args.market, args.li, args.speed)
        out = (json.dumps({"check": check}, ensure_ascii=False, indent=2)
               if args.format == "json" else render_check(check))
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(out + "\n")
        print(out)
        raise SystemExit(0 if check["ready"] else 2)

    if not args.size or not str(args.size).strip():
        raise SystemExit("✗ 没给规格：--size 后面要跟一个规格，如 11.00R20。"
                         "不知道怎么填就跑 python scripts/tire_pack.py --help。")
    if not args.market or not str(args.market).strip():
        raise SystemExit("✗ 没给市场：--market 后面要跟一个市场，如 nigeria 或 尼日利亚。"
                         "不知道怎么填就跑 python scripts/tire_pack.py --help。")

    try:
        pack = build_tire_pack(args.size, args.market, args.li, args.speed)
    except ValueError as e:
        raise SystemExit("✗ %s" % e)

    if args.format == "json":
        out = json.dumps({"pack": pack}, ensure_ascii=False, indent=2)
    else:
        out = render_table(pack)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
    print(out)


if __name__ == "__main__":
    main()
