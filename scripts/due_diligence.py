#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
due_diligence.py — 客户背调 Agent：输入一家公司的结构化信息，输出
L1/L2/L3 三级背调报告 + A/B/C 评级 + 红旗清单 + 下一步。

只用标准库，Python 3.8+ 可直接跑。不联网，不替你上网查——你把公开渠道
查到的事实填进来，它帮你按规矩判定、定级、列出下一步。

用法见 --help（里面的例子都能直接复制）。

判定口径（跟 docs/03-due-diligence.md 同一套，不另搞一套）：
  L1 筛查（2 分钟，四个问题，全项目统一口径：本页第五节的 L1 四问）：
      官网活着吗 / 有地址和联系方式吗 / 有批发贸易属性吗 / 有规模迹象吗
      任一答不上来先降为 C；任一明确不过也降为 C，并写清理由。
  L2 标准（六维）：身份 / 规模 / 信誉 / 采购力 / 付款习惯 / 合规。
      每维只给三种结论：通过 / 待核实 / 红旗。查不到写「待核实」，不许编。
      每维再带两样东西：
        ① 证据档（三档，只取其一）：已核实 = 对着具名公开来源直接查到的事实
            （海关数据、注册库、制裁名单、打开过的官网）；有据推断 = 靠间接信号
            或对方自述推出来的结论（没交叉核对过）；待核实 = 没数据、没查到。
            查不到的字段输出「待核实」，不许编一个值来凑数。
        ② 打分（0–100）：通过 100 分 / 待核实 40 分 / 红旗 0 分，按 L2_WEIGHTS
            加权平均出总分。打分只是帮你横向比较、看哪维证据最薄的辅助尺子，
            不改评级：评级仍按上面的 A/B/C 硬规则定，打分再高也不越级。
  L3 深度（仅 A 类）：只列「要查什么、去哪查」，不替你编结果。
  评级：A = L1 全过 + 有进口记录 + 品类匹配 + 找到具体采购人，且零红旗；
      B = L1 全过但证据弱（有待核实项），或命中 1 项降级红旗；
      C = L1 不过/答不上来，或命中 2 项及以上红旗；
      制裁名单 / 货款付给第三方账户 = 立即终止（不接触、不报价、不寄样）。
      每命中 1 项降级红旗降一级。

红线：只用你光明正大能打开的公开来源。脚本本身不联网、不读任何外部数据，
你填什么它就按什么判——填进来的事实要是编的，结论就是编的，别怪脚本。
内部判断（评级、红旗）绝不进 --audience client 视图，更不进给客户的文件。
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# ================================================================ 常量
# 想改判定口径，只改这一块。改完务必跑一次：
#   python3 -m unittest discover -s tests
#   python scripts/due_diligence.py --company "【示例】海湾轮胎贸易" ...（见 --help）

# 免费邮箱域名：唯一联系方式是这些，就不是「域名邮箱」，先降级。
FREE_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "qq.com",
    "163.com", "126.com", "sina.com", "foxmail.com", "live.com", "msn.com",
}
# 这些值都等于「没填」，不能因为格子里有字就算提供了信息
PLACEHOLDERS = {"", "-", "--", "---", "/", "n/a", "na", "n.a.", "none", "null",
                "nil", "unknown", "tbd", "?", "??", "待定", "待补", "暂无",
                "未知", "无", "不知道", "未填写", "没有"}
# 能拍板的角色：对接人是这些，才算「找到具体采购人」（A 级的第四个条件）
DECISION_ROLES = ("purchasing manager", "procurement", "buyer", "sourcing manager",
                  "owner", "采购经理", "采购", "总经理", "负责人", "老板")
# 贸易属性：这些角色算「有批发/贸易属性」（L1 第 3 问）
TRADE_ROLES = ("importer", "distributor", "wholesaler", "trading", "dealer",
               "supply", "import", "wholesale")
# 渠道角色的合法取值（--trade-role 只认这些，别的按 unknown 处理并提示）
TRADE_ROLE_VALUES = ("importer", "distributor", "wholesaler", "retailer",
                     "fleet", "peer", "competitor", "trading", "dealer")
SOURCE_VALUES = ("referral", "trade_show", "customs", "linkedin", "search")

# L3 深度清单：只写「查什么、去哪查」，状态永远是「待查」——脚本不替你编结果。
L3_CHECKLIST = (
    ("海关数据", "UN Comtrade（comtradeplus.un.org）/ 各国官方统计与海关公开查询 / "
     "持牌商业数据平台的公开查询功能", "进口品类、频次、量级是否与官网自述对得上"),
    ("财报与规模", "官网 About / LinkedIn 公司页员工数区间 / 展会参展商名录 / "
     "行业协会会员名录", "规模数字能否交叉验证，别只信官网一家之言"),
    ("诉讼与执行", "目标国法院/司法公开检索 / 企业信用公示类公开平台 / "
     "Google News 搜「公司名 + lawsuit / bankruptcy / fraud」",
     "有无被执行、失信、破产清算记录"),
    ("关联公司", "目标国官方商业登记机关公开查询 / 官网集团介绍 / "
     "LinkedIn 母子公司关系", "母子公司、同一控制人、注册名与自称名是否一致"),
    ("制裁名单", "OFAC / EU / UN 公开制裁名单检索", "命中即立即终止，不接触、不报价、不寄样"),
)

# 红旗的处置（照 docs/03-due-diligence.md 第六节，一字不改口径）
RED_FLAG_ACTIONS = {
    "free_email": ("唯一联系方式是免费邮箱", "降级：先补到域名邮箱再回来"),
    "domain_mismatch": ("邮箱域名与官网域名不一致", "降级：先问清主体关系（子公司 / 品牌名？）"),
    "no_website": ("官网不存在 / 多年未更新 / 只有 Coming soon", "降为 C"),
    "whatsapp_only": ("只有一个 WhatsApp 号，无地址、无官网", "降为 C（不给任何账期）"),
    "name_mismatch": ("公司名与注册名对不上", "暂停：先做身份核对，要求对方书面澄清主体"),
    "adverse_record": ("有被执行 / 失信 / 破产记录", "降为 C，且只做预付或即期信用证"),
    "sanctions": ("出现在制裁名单上", "立即终止：不接触、不报价、不寄样"),
    "no_import_claim": ("零进口记录却自称大分销商", "降为 B/C，按「企业真实但商业证据不足」处理"),
    "peer": ("本身是同行品牌商", "转同行处理流程，不给报价单"),
    "credit_first": ("首次接触就要大额账期 / 只接受 EXW-FCA 且拒绝任何预付",
                     "降级：只做预付或即期信用证"),
    "payee_mismatch": ("要求把货款付到与合同主体不一致的第三方账户",
                       "直接终止：这是最典型的贸易诈骗手法，不是谈判问题"),
}

TERMINATE_FLAGS = ("sanctions", "payee_mismatch")  # 命中任一，直接终止

# 证据三档 (evidence grades)：每条 L1 检查、每维 L2 结论都标一个，只取其一。
#   已核实 / verified：对着具名公开来源直接查到的事实（海关数据、注册库、
#       制裁名单、打开过的官网）。没核实 = 不能写这档。
#   有据推断 / inferred：靠间接信号或对方自述推出来的结论，没交叉核对过
#       （对方报的年份/人数、公开检索没查到不良记录、对方自述的付款条件）。
#   待核实 / pending：没数据、没查到。查不到的字段就标这档，不许编值凑数。
EVIDENCE_VERIFIED = "已核实"    # verified: checked against a named public source
EVIDENCE_INFERRED = "有据推断"  # inferred: from indirect signals / self-reported claims
EVIDENCE_PENDING = "待核实"     # pending: no data, not checked yet
EVIDENCE_GRADES = (EVIDENCE_VERIFIED, EVIDENCE_INFERRED, EVIDENCE_PENDING)

# L2 六维打分 (six-dimension scoring)：每维 0–100 分，按结论给分——
#   通过 100 / 待核实 40 / 红旗 0。待核实只给 40 分不给满分，是因为
#   「没查到」不等于「没问题」，证据薄的维不能靠缺席拿高分。
# 权重 (weights)：采购力、付款习惯各 2——这份背调核心问的是「钱能不能收回来」，
#   这两维最贴钱；其余四维各 1。总分 = 加权平均，0–100。
# 想改口径只改这一块：改权重、改给分、改分档，都不用动判定逻辑。
L2_WEIGHTS = {"身份": 1.0, "规模": 1.0, "信誉": 1.0,
              "采购力": 2.0, "付款习惯": 2.0, "合规": 1.0}
L2_SCORE_BY_STATUS = {"pass": 100, "unknown": 40, "red_flag": 0}
# 总分分档 (score bands)：分档只看证据扎实程度，不改评级。
L2_SCORE_BANDS = ((80, "证据扎实"), (50, "证据一般"), (0, "证据薄弱"))


# ---------------------------------------------------------------- 小工具
def _clean(value: Any) -> str:
    """输入值 -> 去掉首尾空白的字符串。None 变空串。"""
    if value is None:
        return ""
    return str(value).strip()


def _is_filled(value: str) -> bool:
    """有字不等于真填了：「-」「n/a」「待补」这类占位符一律算没填。"""
    return _clean(value).lower() not in PLACEHOLDERS


def _norm(value: str) -> str:
    """枚举类输入归一化：去空格、转小写。"""
    return _clean(value).lower()


def _yn(value: str) -> Optional[bool]:
    """yes/no/unknown 三态：填了是/否返回 True/False，没填或写「未知」返回 None。
    查不到就返回 None，别把「没说」当成「没有」。"""
    v = _norm(value)
    if v in ("yes", "y", "true", "1", "是", "有", "对", "通过", "clear", "clean"):
        return True
    if v in ("no", "n", "false", "0", "否", "无", "没有", "不通过", "flagged"):
        return False
    return None


def _domain_of(value: str) -> str:
    """从网址或邮箱里抠域名：带 http://、带 www.、带路径的都认；
    传了完整邮箱（xxx@sample.example）就取 @ 后面那段。抠不出来返回空串。"""
    v = _clean(value).lower()
    if "@" in v:
        v = v.rsplit("@", 1)[-1]
    v = re.sub(r"^https?://", "", v)
    v = v.split("/")[0].split("?")[0].split("#")[0]
    v = v[4:] if v.startswith("www.") else v
    return v.strip()


def _is_free_email(domain: str) -> bool:
    """域名是不是免费邮箱（gmail/qq 之类）。保留域名 sample.example 不算免费。"""
    d = domain.lower()
    return d in FREE_EMAIL_DOMAINS or any(
        d.endswith("." + free) for free in FREE_EMAIL_DOMAINS)


def _years_value(raw: str) -> Optional[float]:
    """成立年数：填 '18年' / '18 years' 都能读；填年份（如 2010）自动换算；
    读不懂返回 None（待核实），不猜。"""
    if not _is_filled(raw):
        return None
    match = re.search(r"\d+(?:\.\d+)?", _clean(raw))
    if not match:
        return None
    value = float(match.group())
    if value > 100:  # 填的是成立年份
        value = float(datetime.now().year) - value
    return max(0.0, value)


def _employees_value(raw: str) -> Optional[int]:
    """员工数：只认数字；写「几十人」「50+」取第一个数；读不懂返回 None。"""
    if not _is_filled(raw):
        return None
    match = re.search(r"\d+", _clean(raw).replace(",", ""))
    return int(match.group()) if match else None


def _is_decision_maker(role: str) -> bool:
    """对接人角色是不是能拍板的那种。写了 'buyer' 这类词就算，别写人名来充数。"""
    r = _norm(role)
    return bool(r) and any(k in r for k in DECISION_ROLES)


def clean_inputs(raw: Dict[str, Any]) -> Dict[str, Any]:
    """CLI 传进来的原始参数 -> 归一化后的输入 dict。缺的键补空串，后面统一按缺失处理。"""
    keys = ("company", "country", "product", "source", "website",
            "website_updated", "years", "email_domain", "phone", "address",
            "social", "customs_record", "import_match", "contact_role",
            "employees", "trade_role", "legal_name_match", "sanctions",
            "adverse", "payment", "payee_mismatch", "note")
    return {k: _clean(raw.get(k, "")) for k in keys}


# ---------------------------------------------------------------- L1 筛查
def l1_screen(inp: Dict[str, Any]) -> List[Dict[str, str]]:
    """L1 四问（docs/03 第五节，全项目统一口径）：
    每问只给三种结论：通过 / 不通过 / 待核实。查不到写「待核实」，不写「没有」。
    每问再标证据档（evidence：已核实/有据推断/待核实）+ 证据来源
    （evidence_source：这条结论是拿什么查出来的，没查就写没查）。"""
    checks: List[Dict[str, str]] = []

    # 第 1 问：网站活着吗？
    website = inp["website"]
    updated = _norm(inp["website_updated"])
    if not _is_filled(website):
        checks.append({"item": "官网存在性", "status": "fail",
                       "note": "没给官网 / 官网打不开：先按不存在处理",
                       "evidence": EVIDENCE_PENDING, "evidence_source": "未提供官网"})
    elif updated in ("old", "outdated", "多年未更新", "none"):
        checks.append({"item": "官网存在性", "status": "fail",
                       "note": "官网多年未更新 / 只有 Coming soon：按模板站处理",
                       "evidence": EVIDENCE_VERIFIED,
                       "evidence_source": "官网（已打开，多年未更新）"})
    else:
        note = "官网能打开"
        if updated in ("recent", "recently", "最近更新"):
            note += "，最近有更新痕迹"
            evidence, source = (EVIDENCE_VERIFIED, "官网（已打开，最近有更新）")
        else:
            note += "（更新时间待核实）"
            evidence, source = (EVIDENCE_INFERRED, "官网（已打开，更新时间未确认）")
        checks.append({"item": "官网存在性", "status": "pass", "note": note,
                       "evidence": evidence, "evidence_source": source})

    # 第 2 问：有地址和联系方式吗？
    email_domain = _domain_of(inp["email_domain"])
    if email_domain and not _is_free_email(email_domain):
        checks.append({"item": "联系方式", "status": "pass",
                       "note": "域名邮箱 %s" % email_domain,
                       "evidence": EVIDENCE_INFERRED,
                       "evidence_source": "域名邮箱（域名存在，归属未核对）"})
    elif _is_filled(inp["address"]):
        checks.append({"item": "联系方式", "status": "fail",
                       "note": "有地址但无域名邮箱：先补域名邮箱再回来",
                       "evidence": EVIDENCE_INFERRED,
                       "evidence_source": "对方提供的地址（未实地核对）"})
    elif email_domain and _is_free_email(email_domain):
        checks.append({"item": "联系方式", "status": "fail",
                       "note": "唯一联系方式是免费邮箱（%s）：先补域名邮箱" % email_domain,
                       "evidence": EVIDENCE_VERIFIED,
                       "evidence_source": "免费邮箱域名（可查）"})
    elif _is_filled(inp["phone"]):
        checks.append({"item": "联系方式", "status": "fail",
                       "note": "只有电话/WhatsApp，无地址无域名邮箱：降级，不给账期",
                       "evidence": EVIDENCE_INFERRED,
                       "evidence_source": "对方提供的电话/WhatsApp（未拨通核对）"})
    else:
        checks.append({"item": "联系方式", "status": "fail",
                       "note": "无任何联系方式",
                       "evidence": EVIDENCE_PENDING, "evidence_source": "未提供"})

    # 第 3 问：有批发/贸易属性吗？
    role = _norm(inp["trade_role"])
    if role in ("peer", "competitor", "同行"):
        checks.append({"item": "贸易属性", "status": "fail",
                       "note": "本身是同行品牌商：转同行流程，不给报价单",
                       "evidence": EVIDENCE_INFERRED,
                       "evidence_source": "对方自述的渠道角色"})
    elif role in TRADE_ROLES or role in ("retailer", "fleet", "零售", "车队"):
        note = "渠道角色：%s" % role
        if role in ("retailer", "fleet", "零售", "车队"):
            note += "（零售/车队自用：价格带和起订量要另核，别按进口商的量报）"
        checks.append({"item": "贸易属性", "status": "pass", "note": note,
                       "evidence": EVIDENCE_INFERRED,
                       "evidence_source": "对方自述的渠道角色"})
    elif role:
        checks.append({"item": "贸易属性", "status": "unknown",
                       "note": "渠道角色 %s 不在识别列表里：待核实" % role,
                       "evidence": EVIDENCE_PENDING, "evidence_source": "未核实"})
    else:
        checks.append({"item": "贸易属性", "status": "unknown",
                       "note": "没给渠道角色（进口商/批发/零售/车队）：待核实",
                       "evidence": EVIDENCE_PENDING, "evidence_source": "未提供"})

    # 第 4 问：有规模迹象吗？（成立年份 / 人数 / 社媒活跃，三样有一就行）
    years = _years_value(inp["years"])
    employees = _employees_value(inp["employees"])
    social = _norm(inp["social"])
    signals = []
    if years is not None:
        signals.append("成立约 %s 年" % ("%g" % years))
    if employees is not None:
        signals.append("员工约 %s 人" % employees)
    if social in ("active", "活跃"):
        signals.append("社媒活跃")
    if signals:
        checks.append({"item": "规模迹象", "status": "pass",
                       "note": "；".join(signals),
                       "evidence": EVIDENCE_INFERRED,
                       "evidence_source": "对方提供的年份/人数/社媒（未交叉核对）"})
    elif social in ("inactive", "none", "不活跃", "无"):
        checks.append({"item": "规模迹象", "status": "unknown",
                       "note": "社媒不活跃，且年份、人数都没给：待核实",
                       "evidence": EVIDENCE_PENDING, "evidence_source": "未提供"})
    else:
        checks.append({"item": "规模迹象", "status": "unknown",
                       "note": "成立年份、人数、社媒全没给：待核实",
                       "evidence": EVIDENCE_PENDING, "evidence_source": "未提供"})

    return checks


def l1_status(checks: List[Dict[str, str]]) -> str:
    """L1 总判定：任一不通过 -> fail；任一待核实 -> unknown；全过 -> pass。"""
    if any(c["status"] == "fail" for c in checks):
        return "fail"
    if any(c["status"] == "unknown" for c in checks):
        return "unknown"
    return "pass"


# ---------------------------------------------------------------- L2 标准
def l2_assess(inp: Dict[str, Any]) -> List[Dict[str, str]]:
    """L2 六维：身份 / 规模 / 信誉 / 采购力 / 付款习惯 / 合规。
    每维只给三种结论：通过 / 待核实 / 红旗。
    每维再标证据档（evidence：已核实/有据推断/待核实）+ 证据来源
    （evidence_source）：已核实只给对着具名公开来源直接查到的事实；
    对方自述、没查到不良记录这类间接信号只能算有据推断；没数据就标待核实。"""
    dims: List[Dict[str, str]] = []
    years = _years_value(inp["years"])
    employees = _employees_value(inp["employees"])
    customs = _yn(inp["customs_record"])
    match = _yn(inp["import_match"])
    role = _norm(inp["trade_role"])
    registry = "目标国官方商业登记机关公开查询"

    # 1. 身份：注册名和自称名一致吗？
    legal = _yn(inp["legal_name_match"])
    if legal is True:
        dims.append({"dimension": "身份", "status": "pass",
                     "note": "注册名与自称名一致",
                     "evidence": EVIDENCE_VERIFIED, "evidence_source": registry})
    elif legal is False:
        dims.append({"dimension": "身份", "status": "red_flag",
                     "note": "注册名与自称名对不上：暂停，先做身份核对，要求对方书面澄清主体",
                     "flag": "name_mismatch",
                     "evidence": EVIDENCE_VERIFIED, "evidence_source": registry})
    else:
        dims.append({"dimension": "身份", "status": "unknown",
                     "note": "注册名是否与自称名一致：待核实（目标国官方商业登记机关公开查询）",
                     "evidence": EVIDENCE_PENDING, "evidence_source": registry})

    # 2. 规模：多少人、多少年？
    # 年份/人数都是对方报的数，没交叉核对过，只能算有据推断，不能算已核实。
    size_source = "对方提供的年份/人数（未交叉核对）"
    if years is not None and years >= 3 or employees is not None and employees >= 10:
        bits = []
        if years is not None:
            bits.append("成立约 %s 年" % ("%g" % years))
        if employees is not None:
            bits.append("员工约 %s 人" % employees)
        dims.append({"dimension": "规模", "status": "pass",
                     "note": "；".join(bits),
                     "evidence": EVIDENCE_INFERRED, "evidence_source": size_source})
    elif years is not None or employees is not None:
        bits = []
        if years is not None:
            bits.append("成立约 %s 年" % ("%g" % years))
        if employees is not None:
            bits.append("员工约 %s 人" % employees)
        dims.append({"dimension": "规模", "status": "pass",
                     "note": "小公司，规模有限但正常（%s）" % "；".join(bits),
                     "evidence": EVIDENCE_INFERRED, "evidence_source": size_source})
    else:
        dims.append({"dimension": "规模", "status": "unknown",
                     "note": "成立年份、员工数都没给：待核实",
                     "evidence": EVIDENCE_PENDING, "evidence_source": "未提供"})

    # 3. 信誉：有官司、有执行吗？
    # 「公开渠道没查到」只是没查到，不等于没有，只能算有据推断。
    adverse = _yn(inp["adverse"])
    court = "目标国法院/司法公开检索"
    if adverse is True:
        dims.append({"dimension": "信誉", "status": "red_flag",
                     "note": "有被执行 / 失信 / 破产记录：降为 C，只做预付或即期信用证",
                     "flag": "adverse_record",
                     "evidence": EVIDENCE_VERIFIED, "evidence_source": court})
    elif adverse is False:
        dims.append({"dimension": "信誉", "status": "pass",
                     "note": "公开渠道未见被执行 / 失信 / 破产记录",
                     "evidence": EVIDENCE_INFERRED, "evidence_source": court})
    else:
        dims.append({"dimension": "信誉", "status": "unknown",
                     "note": "被执行 / 失信 / 破产记录：待核实（目标国法院公开检索）",
                     "evidence": EVIDENCE_PENDING, "evidence_source": court})

    # 4. 采购力：真在进口吗？品类对得上吗？
    customs_source = "公开海关数据"
    if customs is True and match is True:
        dims.append({"dimension": "采购力", "status": "pass",
                     "note": "有进口记录，且品类与你的产品匹配",
                     "evidence": EVIDENCE_VERIFIED, "evidence_source": customs_source})
    elif customs is True and match is False:
        dims.append({"dimension": "采购力", "status": "unknown",
                     "note": "有进口记录但品类与你的产品对不上：谨慎",
                     "evidence": EVIDENCE_VERIFIED, "evidence_source": customs_source})
    elif customs is True:
        dims.append({"dimension": "采购力", "status": "unknown",
                     "note": "有进口记录，品类是否匹配：待核实",
                     "evidence": EVIDENCE_INFERRED,
                     "evidence_source": "公开海关数据（品类未核对）"})
    elif customs is False and role in ("importer", "distributor"):
        dims.append({"dimension": "采购力", "status": "red_flag",
                     "note": "零进口记录却自称大分销商/进口商：按「企业真实但商业证据不足」处理",
                     "flag": "no_import_claim",
                     "evidence": EVIDENCE_INFERRED,
                     "evidence_source": "公开海关数据（无记录不等于没进口）"})
    elif customs is False:
        dims.append({"dimension": "采购力", "status": "unknown",
                     "note": "无公开进口记录（小买家也可能没记录，别直接当没有）",
                     "evidence": EVIDENCE_INFERRED,
                     "evidence_source": "公开海关数据（无记录不等于没进口）"})
    else:
        dims.append({"dimension": "采购力", "status": "unknown",
                     "note": "进口记录：待核实（UN Comtrade / 海关公开查询）",
                     "evidence": EVIDENCE_PENDING,
                     "evidence_source": "UN Comtrade / 海关公开查询"})

    # 5. 付款习惯：首触就要账期吗？
    # 付款条件是对方自述的，没经过一笔真实交易验证，只能算有据推断。
    payment = _norm(inp["payment"])
    payment_source = "对方自述（未经交易验证）"
    if payment in ("prepaid", "预付", "lc", "信用证", "即期信用证"):
        dims.append({"dimension": "付款习惯", "status": "pass",
                     "note": "接受预付 / 即期信用证",
                     "evidence": EVIDENCE_INFERRED, "evidence_source": payment_source})
    elif payment in ("credit", "账期", "赊销", "oa"):
        dims.append({"dimension": "付款习惯", "status": "red_flag",
                     "note": "首次接触就要大额账期：降级，只做预付或即期信用证",
                     "flag": "credit_first",
                     "evidence": EVIDENCE_INFERRED, "evidence_source": payment_source})
    else:
        dims.append({"dimension": "付款习惯", "status": "unknown",
                     "note": "付款习惯：待核实（首触就要账期是红旗，先问清再报价）",
                     "evidence": EVIDENCE_PENDING, "evidence_source": "未问清"})

    # 6. 合规：制裁名单 / 收款账户
    sanctions = _norm(inp["sanctions"])
    payee = _yn(inp["payee_mismatch"])
    sanctions_source = "OFAC / EU / UN 公开制裁名单"
    if sanctions in ("flagged", "hit", "命中"):
        dims.append({"dimension": "合规", "status": "red_flag",
                     "note": "出现在制裁名单上：立即终止，不接触、不报价、不寄样",
                     "flag": "sanctions",
                     "evidence": EVIDENCE_VERIFIED, "evidence_source": sanctions_source})
    elif payee is True:
        dims.append({"dimension": "合规", "status": "red_flag",
                     "note": "要求把货款付到与合同主体不一致的第三方账户：直接终止（典型诈骗手法）",
                     "flag": "payee_mismatch",
                     "evidence": EVIDENCE_VERIFIED,
                     "evidence_source": "对方书面要求（原话在沟通记录里）"})
    elif sanctions in ("clear", "clean", "无"):
        dims.append({"dimension": "合规", "status": "pass",
                     "note": "公开制裁名单未命中；收款账户与合同主体一致",
                     "evidence": EVIDENCE_INFERRED,
                     "evidence_source": "公开制裁名单检索未命中（没命中不等于绝对干净）"})
    else:
        dims.append({"dimension": "合规", "status": "unknown",
                     "note": "制裁名单：待核实（OFAC / EU / UN 公开检索）",
                     "evidence": EVIDENCE_PENDING, "evidence_source": sanctions_source})

    return dims


def score_l2(l2: List[Dict[str, str]],
             weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """L2 六维打分 (score the six dimensions)：每维按结论给分
    （通过 100 / 待核实 40 / 红旗 0），按权重加权平均出总分。
    weights 不传用默认 L2_WEIGHTS；传了只认六维的名字，缺的维按默认补，
    多余的键忽略。返回每维得分 + 总分 + 分档。打分是辅助尺子，不改评级。"""
    w = dict(L2_WEIGHTS)
    if weights:
        for name, value in weights.items():
            if name in w:
                try:
                    w[name] = float(value)
                except (TypeError, ValueError):
                    continue
    total_weight = sum(w.values()) or 1.0
    scored = []
    weighted_sum = 0.0
    for d in l2:
        name = d["dimension"]
        score = L2_SCORE_BY_STATUS.get(d["status"], 0)
        weight = w.get(name, 1.0)
        weighted_sum += score * weight
        scored.append({
            "dimension": name,
            "status": d["status"],
            "score": score,
            "weight": weight,
            "evidence": d.get("evidence", EVIDENCE_PENDING),
            "evidence_source": d.get("evidence_source", ""),
        })
    total = round(weighted_sum / total_weight, 1)
    band = next(label for floor, label in L2_SCORE_BANDS if total >= floor)
    return {"dimensions": scored, "total": total, "band": band,
            "weights": w}


def l3_checklist() -> List[Dict[str, str]]:
    """L3 深度清单：只列「查什么、去哪查」，状态永远是「待查」。
    仅 A 类值得花这 30 分钟；B/C 不做。"""
    return [{"item": item, "where": where, "why": why, "status": "待查"}
            for item, where, why in L3_CHECKLIST]


# ---------------------------------------------------------------- 红旗与评级
def collect_red_flags(l1: List[Dict[str, str]],
                      l2: List[Dict[str, str]],
                      inp: Dict[str, Any]) -> List[Dict[str, str]]:
    """把 L1 不过项和 L2 红旗收成一张清单，每条带处置动作。
    L1 的「不通过」本身就是红旗（处置见 docs/03 第六节）。"""
    flags: List[Dict[str, str]] = []
    seen = set()

    def add(key: str) -> None:
        if key in seen:
            return
        seen.add(key)
        label, action = RED_FLAG_ACTIONS[key]
        flags.append({"flag": label, "action": action,
                      "severity": "terminate" if key in TERMINATE_FLAGS
                      else "downgrade"})

    for c in l1:
        if c["status"] != "fail":
            continue
        if c["item"] == "官网存在性":
            add("no_website")
        elif c["item"] == "联系方式":
            if "免费邮箱" in c["note"]:
                add("free_email")
            elif "WhatsApp" in c["note"]:
                add("whatsapp_only")
            else:
                add("free_email")
        elif c["item"] == "贸易属性":
            add("peer")
    for d in l2:
        if d["status"] == "red_flag" and "flag" in d:
            add(d["flag"])

    # 邮箱域名与官网域名不一致：单拎出来算（L1 联系方式过了也可能撞上）
    email_domain = _domain_of(inp["email_domain"])
    website_domain = _domain_of(inp["website"])
    if (email_domain and website_domain
            and not _is_free_email(email_domain)
            and email_domain != website_domain
            and not (email_domain.endswith("." + website_domain)
                     or website_domain.endswith("." + email_domain))):
        add("domain_mismatch")

    return flags


def rate(l1: List[Dict[str, str]], l2: List[Dict[str, str]],
         flags: List[Dict[str, str]], inp: Dict[str, Any]) -> Dict[str, Any]:
    """定级。A 的四个条件缺一不可（docs/03 评级标准表）；命中 1 项降级红旗
    降一级，命中 2 项及以上直接降为 C；终止项一票否决。"""
    l1s = l1_status(l1)
    terminated = any(f["severity"] == "terminate" for f in flags)
    downgrades = sum(1 for f in flags if f["severity"] == "downgrade")
    customs = _yn(inp["customs_record"])
    match = _yn(inp["import_match"])
    decision_maker = _is_decision_maker(inp["contact_role"])
    l2_unknowns = [d["dimension"] for d in l2 if d["status"] == "unknown"]

    missing: List[str] = []
    if l1s != "pass":
        missing += ["L1：%s（%s）" % (c["item"], c["note"])
                    for c in l1 if c["status"] != "pass"]
    missing += ["L2 %s：待核实" % d for d in l2_unknowns]
    if customs is not True:
        missing.append("进口记录：需要公开海关数据佐证")
    if match is not True:
        missing.append("品类匹配：需要确认进口品类与你的产品对得上")
    if not decision_maker:
        missing.append("具体采购人：需要找到采购/老板一级的对接人")

    if terminated:
        return {"rating": "C", "terminated": True, "t_tier": "T3",
                "next_action": "立即终止：不接触、不报价、不寄样",
                "missing": missing}
    if l1s != "pass":
        return {"rating": "C", "terminated": False, "t_tier": "T3",
                "next_action": "放弃或放冷池：先补 L1 没过/待核实的项，补完再重评；"
                               "补之前不进主动建联序列",
                "missing": missing}
    if downgrades >= 2:
        return {"rating": "C", "terminated": False, "t_tier": "T3",
                "next_action": "放弃或放冷池：命中 %d 项降级红旗，先处理红旗再说" % downgrades,
                "missing": missing}
    a_candidate = (customs is True and match is True and decision_maker)
    if a_candidate and not l2_unknowns and downgrades == 0:
        return {"rating": "A", "terminated": False, "t_tier": "T0",
                "next_action": "48 小时内首触，投人（映射 T0）；首触前先做 L3 深度档案（30 分钟）",
                "missing": []}
    if downgrades == 1:
        return {"rating": "B", "terminated": False, "t_tier": "T1/T2",
                "next_action": "补材料再推进（映射 T1/T2）：先处理命中的 1 项红旗，"
                               "再补下面缺的材料；补之前只用低成本方式试",
                "missing": missing}
    return {"rating": "B", "terminated": False, "t_tier": "T1/T2",
            "next_action": "补材料再推进（映射 T1/T2）：先补下面缺的材料，"
                           "补完重评；补之前只用低成本方式试",
            "missing": missing}


def _note_for_csv(inp: Dict[str, Any], l1: List[Dict[str, str]],
                  l2: List[Dict[str, str]]) -> str:
    """回写线索表 note 列的一句英文证据：只写已核实的事实，能当着对方面念出来。
    没核实出东西就返回空串——空着也别编一句。"""
    bits = []
    years = _years_value(inp["years"])
    if years is not None:
        bits.append("Est. %g years" % years)
    customs = _yn(inp["customs_record"])
    if customs is True:
        bits.append("import record found on public customs data")
    if _yn(inp["import_match"]) is True:
        bits.append("product category matches")
    if _is_decision_maker(inp["contact_role"]):
        bits.append("contact: %s" % _clean(inp["contact_role"]))
    if _norm(inp["trade_role"]) in ("importer", "distributor"):
        bits.append("importer/distributor")
    return "; ".join(bits)


def build_report(raw_inputs: Dict[str, Any],
                 weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """纯函数入口：输入 dict -> 完整报告 dict。不联网，不写文件，不抛错（缺项按待核实算）。
    weights：可选，覆盖 L2 六维打分的默认权重（只认六维的名字）。"""
    inp = clean_inputs(raw_inputs)
    if not _is_filled(inp["company"]):
        raise ValueError("缺公司名：--company 是必填项（公司名是这份报告唯一的主键）")
    l1 = l1_screen(inp)
    l2 = l2_assess(inp)
    flags = collect_red_flags(l1, l2, inp)
    verdict = rate(l1, l2, flags, inp)
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "company": inp["company"],
        "country": inp["country"],
        "product": inp["product"],
        "source": inp["source"],
        "l1": {"status": l1_status(l1), "checks": l1},
        "l2": {"checks": l2},
        "l2_scores": score_l2(l2, weights),
        "l3": {"note": "仅 A 类做（30 分钟，硬上限 45 分钟）",
               "checklist": l3_checklist()},
        "red_flags": flags,
        "rating": verdict["rating"],
        "terminated": verdict["terminated"],
        "t_tier": verdict["t_tier"],
        "next_action": verdict["next_action"],
        "missing_items": verdict["missing"],
        "note_for_csv": _note_for_csv(inp, l1, l2),
        "user_note": inp["note"],
        "inputs": inp,
    }


# ---------------------------------------------------------------- 客户视图
def client_view(report: Dict[str, Any]) -> Dict[str, Any]:
    """客户能看的那一面：只给已核实的公开事实 + 还需要对方补的材料。
    评级、红旗、终止状态、内部判断、原始输入一律不带出门。
    （跟 quote_engine.py 的 client_view 一个路数：内部判断绝不进给客户的文件。）"""
    facts = []
    for c in report["l1"]["checks"]:
        if c["status"] == "pass":
            facts.append("%s：%s" % (c["item"], c["note"]))
    for d in report["l2"]["checks"]:
        if d["status"] == "pass":
            facts.append("%s：%s" % (d["dimension"], d["note"]))
    return {
        "company": report["company"],
        "country": report["country"],
        "verified_facts": facts,
        "needed_materials": report["missing_items"],
        "note": "以下为公开信息核实结果。评级与内部判断不对外提供；"
                "如需推进，请先提供上面列出的材料。",
    }


# ---------------------------------------------------------------- 渲染
def _wide(text: str) -> int:
    """中文占 2 格，英文占 1 格——表格对齐用（跟 lead_score.py 同一个做法）。"""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1
               for ch in text)


def _pad(text: str, width: int) -> str:
    """左对齐补空格，中文按 2 格算。"""
    return text + " " * max(0, width - _wide(text))


def _fit(text: str, width: int) -> str:
    """超长截断，末尾留 …"""
    if _wide(text) <= width:
        return text
    cut = ""
    for ch in text:
        if _wide(cut + ch) > width - 1:
            break
        cut += ch
    return cut + "…"


def _mark(status: str) -> str:
    return {"pass": "通过", "fail": "不通过", "unknown": "待核实",
            "red_flag": "红旗"}.get(status, status)


def render_table(report: Dict[str, Any], audience: str = "internal") -> str:
    """内部报告：L1/L2/红旗/L3/评级/下一步，一行不多一行不少。"""
    if audience == "client":
        return render_client_table(client_view(report))
    lines = []
    title = "客户背调报告：%s" % report["company"]
    lines.append("=" * 60)
    lines.append(title)
    lines.append("=" * 60)
    meta = []
    if report["country"]:
        meta.append("国家：%s" % report["country"])
    if report["product"]:
        meta.append("产品：%s" % report["product"])
    if report["source"]:
        meta.append("来源：%s" % report["source"])
    meta.append("生成时间：%s" % report["generated_at"])
    lines.append("  " + "  |  ".join(meta))
    lines.append("")

    lines.append("【L1 筛查】  %s" % {
        "pass": "全过", "fail": "有不通过项", "unknown": "有待核实项"
    }[report["l1"]["status"]])
    for c in report["l1"]["checks"]:
        lines.append("  [%s] %s：%s（证据：%s，%s）" % (
            _mark(c["status"]), c["item"], c["note"],
            c.get("evidence", EVIDENCE_PENDING),
            c.get("evidence_source", "")))
    lines.append("")

    lines.append("【L2 标准六维】")
    for d in report["l2"]["checks"]:
        lines.append("  [%s] %s：%s（证据：%s，%s）" % (
            _mark(d["status"]), d["dimension"], d["note"],
            d.get("evidence", EVIDENCE_PENDING),
            d.get("evidence_source", "")))
    lines.append("")

    scores = report.get("l2_scores") or score_l2(report["l2"]["checks"])
    lines.append("【L2 六维打分】总分 %.1f / 100（%s）——只看证据扎实程度，不改评级" % (
        scores["total"], scores["band"]))
    for s in scores["dimensions"]:
        lines.append("  %s：%d 分（权重 %s，证据：%s）" % (
            s["dimension"], s["score"], "%g" % s["weight"], s["evidence"]))
    lines.append("")

    if report["red_flags"]:
        lines.append("【红旗清单】共 %d 项" % len(report["red_flags"]))
        for f in report["red_flags"]:
            tag = "终止" if f["severity"] == "terminate" else "降级"
            lines.append("  [%s] %s —— %s" % (tag, f["flag"], f["action"]))
        lines.append("")
    else:
        lines.append("【红旗清单】无")
        lines.append("")

    lines.append("【L3 深度清单】%s" % report["l3"]["note"])
    for item in report["l3"]["checklist"]:
        lines.append("  - %s：去哪查：%s" % (item["item"], item["where"]))
        lines.append("      验什么：%s（状态：%s）" % (item["why"], item["status"]))
    lines.append("")

    lines.append("【评级】%s 级（映射 %s）" % (report["rating"], report["t_tier"]))
    if report["terminated"]:
        lines.append("  状态：已终止")
    lines.append("【下一步】%s" % report["next_action"])
    if report["missing_items"]:
        lines.append("【还缺的材料】")
        for m in report["missing_items"]:
            lines.append("  - %s" % m)
    if report["note_for_csv"]:
        lines.append("【线索表 note 列（可对外说的一句证据）】")
        lines.append("  %s" % report["note_for_csv"])
    if report["user_note"]:
        lines.append("【用户补充（未核实）】%s" % report["user_note"])
    lines.append("")
    lines.append("口径：L1 四问 / L2 六维打分（通过 100 / 待核实 40 / 红旗 0，"
                 "采购力、付款习惯权重 2）/ L3 仅 A 类，见 docs/03-due-diligence.md。")
    return "\n".join(lines)


def render_client_table(view: Dict[str, Any]) -> str:
    """客户视图的表格：只有已核实事实 + 还需要对方补的材料。"""
    lines = []
    lines.append("=" * 60)
    lines.append("公开信息核实：%s" % view["company"])
    lines.append("=" * 60)
    if view["country"]:
        lines.append("  国家：%s" % view["country"])
    lines.append("")
    lines.append("【已核实的公开事实】")
    if view["verified_facts"]:
        for f in view["verified_facts"]:
            lines.append("  - %s" % f)
    else:
        lines.append("  （暂无可对外说的已核实事实）")
    lines.append("")
    lines.append("【请提供以下材料以便推进】")
    if view["needed_materials"]:
        for m in view["needed_materials"]:
            lines.append("  - %s" % m)
    else:
        lines.append("  （材料已齐全）")
    lines.append("")
    lines.append(view["note"])
    return "\n".join(lines)


def render_json(report: Dict[str, Any], audience: str = "internal") -> str:
    """JSON 输出：跟 lead_score.py 一个信封口径（generated_at 打头，
    内部版带 inputs，客户版只剩公开事实）。"""
    if audience == "client":
        payload = client_view(report)
        payload = {"generated_at": report["generated_at"], **payload}
        return json.dumps(payload, ensure_ascii=False, indent=2)
    payload = {k: v for k, v in report.items()}
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- CLI
class _ZhArgumentParser(argparse.ArgumentParser):
    """argparse 的中文错误提示（跟 lead_score.py 同一个做法）。

    注意：这个是特制的——报错里带本脚本的例子和常见报错，别抽成共用的。
    """

    def error(self, message):
        message = message.replace(
            "the following arguments are required: ", "缺了必填参数：")
        message = message.replace(
            "unrecognized arguments: ", "不认识的参数：")
        name = os.path.basename(sys.argv[0])
        examples = (
            "\n先看一眼用法再跑：\n"
            "  python3 scripts/due_diligence.py --help\n"
            "最简例子：\n"
            '  python3 scripts/due_diligence.py --company "【示例】海湾轮胎贸易" '
            '--country "Saudi Arabia" --website sample.example --years 18 '
            '--email-domain sample.example --source customs --social active '
            '--customs-record yes --import-match yes '
            '--contact-role "purchasing manager"\n'
            "常见报错：\n"
            "  缺 --company：公司名是必填项，没它报告不知道给谁\n"
            "  参数值拼错（如 --customs-record 写了 maybe）：只认 yes/no/unknown\n"
        )
        self.print_usage(sys.stderr)
        sys.stderr.write("错了：%s\n%s" % (message, examples))
        sys.exit(2)


def build_parser() -> argparse.ArgumentParser:
    p = _ZhArgumentParser(
        prog="due_diligence.py",
        description="客户背调 Agent：输入一家公司的公开信息，输出 L1/L2/L3 三级背调报告 "
                    "+ A/B/C 评级 + 红旗清单 + 下一步。只用标准库，不联网，"
                    "不替你上网查——你把查到的事实填进来，它帮你按规矩判定。",
        epilog=(
            "例子（都能直接复制跑，示例公司全是虚构的）：\n"
            "\n"
            "  A 级（海关数据来的老进口商）：\n"
            '    python3 scripts/due_diligence.py --company "【示例】海湾轮胎贸易" \\\n'
            '      --country "Saudi Arabia" --product "TBR 12.00R20" \\\n'
            '      --website sample.example --website-updated recent --years 18 \\\n'
            '      --email-domain sample.example --phone "+000 00 000 0000" \\\n'
            '      --address "Riyadh, Saudi Arabia" --source customs --social active \\\n'
            '      --customs-record yes --import-match yes \\\n'
            '      --contact-role "purchasing manager" --employees 45 \\\n'
            '      --trade-role importer --legal-name-match yes --sanctions clear \\\n'
            '      --adverse no --payment prepaid\n'
            "\n"
            "  B 级（LinkedIn 来的新客户，证据还不够）：\n"
            '    python3 scripts/due_diligence.py --company "【示例】半岛汽车" \\\n'
            '      --country "Saudi Arabia" --product "TBR 12.00R20" \\\n'
            '      --website sample.example --years 4 --email-domain sample.example \\\n'
            '      --source linkedin --social active --customs-record unknown \\\n'
            '      --import-match unknown --contact-role "sourcing manager" \\\n'
            '      --employees 6 --trade-role distributor --legal-name-match unknown \\\n'
            '      --sanctions clear --payment unknown\n'
            "\n"
            "  C 级（官网没有、只剩免费邮箱、首触就要账期）：\n"
            '    python3 scripts/due_diligence.py --company "【示例】黎凡特供配" \\\n'
            '      --country Lebanon --product "TBR 12.00R20" --website none \\\n'
            '      --email-domain gmail.com --source search --social inactive \\\n'
            '      --customs-record no --contact-role "sales" \\\n'
            '      --payment credit\n'
            "\n"
            "  输出 JSON、只给客户看的那一面：\n"
            '    python3 scripts/due_diligence.py --company "【示例】海湾轮胎贸易" \\\n'
            '      --country "Saudi Arabia" --website sample.example --years 18 \\\n'
            '      --email-domain sample.example --source customs --social active \\\n'
            '      --customs-record yes --import-match yes \\\n'
            '      --contact-role "purchasing manager" --format json --audience client\n'
            "\n"
            "  写进文件（默认只打印到屏幕）：\n"
            '    python3 scripts/due_diligence.py --company "【示例】海湾轮胎贸易" \\\n'
            '      --country "Saudi Arabia" --website sample.example --years 18 \\\n'
            '      --email-domain sample.example --source customs --social active \\\n'
            '      --customs-record yes --import-match yes \\\n'
            '      --contact-role "purchasing manager" --out report.txt\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--company", required=True,
                   help="公司名（必填；示例公司请加【示例】前缀）")
    p.add_argument("--country", default="",
                   help="国家/地区（如 Saudi Arabia / Nigeria）")
    p.add_argument("--product", default="",
                   help="对方询的产品（如 TBR 12.00R20）")
    p.add_argument("--website", default="",
                   help="官网域名或网址；没有写 none")
    p.add_argument("--website-updated", default="",
                   choices=["", "recent", "old"], metavar="{recent,old}",
                   help="官网更新情况：recent 最近有更新 / old 多年未更新")
    p.add_argument("--years", default="",
                   help="成立年数（填数字，如 18；填年份如 2010 也认，自动换算）")
    p.add_argument("--email-domain", default="",
                   help="邮箱域名（如 sample.example）；只写域名，别贴完整邮箱")
    p.add_argument("--phone", default="",
                   help="电话/WhatsApp（示例请用 +000 占位号）")
    p.add_argument("--address", default="",
                   help="物理地址（城市+国家就够了）")
    p.add_argument("--source", default="", choices=[""] + list(SOURCE_VALUES),
                   metavar="{referral,trade_show,customs,linkedin,search}",
                   help="线索来源")
    p.add_argument("--social", default="",
                   choices=["", "active", "inactive", "none"],
                   metavar="{active,inactive,none}",
                   help="社媒是否活跃：active 活跃 / inactive 不活跃 / none 没有")
    p.add_argument("--customs-record", default="",
                   choices=["", "yes", "no", "unknown"],
                   metavar="{yes,no,unknown}",
                   help="公开海关数据里有没有它的进口记录")
    p.add_argument("--import-match", default="",
                   choices=["", "yes", "no", "unknown"],
                   metavar="{yes,no,unknown}",
                   help="进口品类与你的产品是否匹配")
    p.add_argument("--contact-role", default="",
                   help="对接人角色（如 purchasing manager；写角色别写人名）")
    p.add_argument("--employees", default="",
                   help="员工数（填数字，如 45；读不懂按待核实算）")
    p.add_argument("--trade-role", default="",
                   choices=[""] + list(TRADE_ROLE_VALUES),
                   metavar="{importer,distributor,wholesaler,retailer,fleet,peer,competitor,trading,dealer}",
                   help="渠道角色")
    p.add_argument("--legal-name-match", default="",
                   choices=["", "yes", "no", "unknown"],
                   metavar="{yes,no,unknown}",
                   help="注册名与自称名是否一致")
    p.add_argument("--sanctions", default="",
                   choices=["", "clear", "flagged", "unknown"],
                   metavar="{clear,flagged,unknown}",
                   help="公开制裁名单是否命中：clear 没命中 / flagged 命中")
    p.add_argument("--adverse", default="",
                   choices=["", "yes", "no", "unknown"],
                   metavar="{yes,no,unknown}",
                   help="有无被执行/失信/破产记录")
    p.add_argument("--payment", default="",
                   choices=["", "prepaid", "lc", "credit", "unknown"],
                   metavar="{prepaid,lc,credit,unknown}",
                   help="付款习惯：prepaid 预付 / lc 信用证 / credit 账期")
    p.add_argument("--payee-mismatch", default="",
                   choices=["", "yes", "no", "unknown"],
                   metavar="{yes,no,unknown}",
                   help="是否要求把货款付到与合同主体不一致的第三方账户")
    p.add_argument("--note", default="",
                   help="你补充的一句信息（未核实，只原样展示，不进判定）")
    p.add_argument("--weights", default="",
                   help="覆盖 L2 六维打分权重：传 JSON，如 '{\"采购力\": 3, \"合规\": 2}'；"
                        "不传用默认权重（采购力、付款习惯各 2，其余各 1）")
    p.add_argument("--format", default="table", choices=["table", "json"],
                   help="输出格式：table 表格（默认）/ json")
    p.add_argument("--audience", default="internal", choices=["internal", "client"],
                   help="受众：internal 内部完整报告（默认）/ client 只给客户看的那一面")
    p.add_argument("--out", default="",
                   help="把报告写进这个文件（不填只打印到屏幕）")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    given = argv if argv is not None else sys.argv[1:]
    if not given:
        parser.print_usage(sys.stderr)
        print("\n没给参数：不知道怎么填就跑 python scripts/due_diligence.py --help，"
              "里面有能直接复制的例子。", file=sys.stderr)
        raise SystemExit(2)
    args = parser.parse_args(argv)
    weights = None
    if args.weights:
        try:
            weights = json.loads(args.weights)
            if not isinstance(weights, dict):
                raise ValueError("权重必须是 JSON 对象")
        except (ValueError, json.JSONDecodeError) as exc:
            print("错了：--weights 不是合法的 JSON 对象：%s" % exc,
                  file=sys.stderr)
            print('例子：--weights \'{"采购力": 3, "合规": 2}\'',
                  file=sys.stderr)
            return 2
    try:
        report = build_report(vars(args), weights)
    except ValueError as exc:
        print("错了：%s" % exc, file=sys.stderr)
        print("先跑 --help 看例子：python3 scripts/due_diligence.py --help",
              file=sys.stderr)
        return 2
    if args.format == "json":
        text = render_json(report, args.audience)
    else:
        text = render_table(report, args.audience)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print("已写入 %s" % args.out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
