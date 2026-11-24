#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Order fulfillment checklist / 订单交付核对清单生成器.

Turns a confirmed order into a stage-by-stage checklist so nothing is
missed between PI and repeat order. Aligned one-to-one with the 10 steps
in docs/07-order-delivery.md (PI -> deposit -> production -> inspection
-> balance -> booking -> customs -> bill of lading -> docs pack ->
after-sales). Money gates are enforced, not just listed: production
cannot start before the deposit is confirmed by your own bank statement,
and the bill of lading is not released before the balance clears.

把确认的订单变成一张按阶段走的核对清单，从 PI 到复购，一步都不能漏。
清单与 docs/07-order-delivery.md 的十步一一对应。钱的关口是硬关口，
不只是列出来：定金没经自家银行流水确认就不排产，尾款没到账就不放单。

Stdlib only, no network, no LLM calls. / 只用标准库，不联网，不调 LLM。

Usage / 用法:
    python3 scripts/fulfillment_checklist.py --demo
    python3 scripts/fulfillment_checklist.py --order order.json
    python3 scripts/fulfillment_checklist.py --order order.json --format json
    python3 scripts/fulfillment_checklist.py --order order.json --out checklist.txt
    python3 scripts/fulfillment_checklist.py --order order.json --done deposit
    python3 scripts/fulfillment_checklist.py --order order.json --status
    python3 scripts/fulfillment_checklist.py --order order.json --deposit-received 4032

Order JSON fields / 订单 JSON 字段 (all example values are fictional /
以下示例值全部虚构，带【示例】前缀）:
    {
      "buyer": "【示例】中东港口批发商",
      "spec": "295/80R22.5", "qty": 480, "unit_price": 28.0,
      "total": 13440.0, "currency": "USD",
      "incoterm": "FOB Yantian",
      "payment_terms": "T/T 30% deposit + 70% against B/L copy",
      "payment_method": "tt_deposit",
      "deposit_rate": 30, "deposit_received": 4032.0,
      "deposit_confirmed_by_bank": true,
      "pi_confirmed": true, "first_order": true,
      "balance_received": 0.0, "docs_sent": false,
      "bl": {"shipper": "...", "consignee": "...", ...},
      "docs": {"invoice": {...}, "packing_list": {...},
               "bill_of_lading": {...}}
    }

Payment methods / 付款方式 (risk per docs/07, from safest to riskiest /
按 docs/07 的风险分级，从安全到危险）:
    tt_advance (100% in advance), tt_deposit (deposit + balance vs B/L
    copy), lc_sight, dp, oa, western_union, third_party.
    O/A, Western Union / personal accounts and third-party payments are
    refused for a first order: the checklist blocks them outright.
    首单不接 O/A、西联/个人账户、第三方代付：清单直接拦下。

Exit codes / 退出码: 0 ok / 2 bad input or a gate refuses --done.
"""

import argparse
import json
import os
import sys
from datetime import datetime

# PI fields that must be on the proforma invoice / PI 上必须有的字段
# (docs/07-order-delivery.md section 7, PI template).
PI_FIELDS = [
    "buyer", "spec", "qty", "unit_price", "total", "incoterm",
    "payment_terms", "validity_days", "bank_details",
]

# Bill of lading draft fields checked word by word / 提单草稿逐字核对的字段
# (docs/07 step 8: shipper, consignee, notify, description, pieces,
# gross weight, freight terms, ports, shipment date).
BL_FIELDS = [
    "shipper", "consignee", "notify", "description", "pieces",
    "gross_weight", "port_of_loading", "port_of_discharge",
    "freight_terms", "shipment_date",
]

# Fields that must match across invoice / packing list / B/L /
# 发票、装箱单、提单三者必须一致的字段 (docs/07 "three-way consistency").
THREE_WAY_FIELDS = ["description", "pieces", "gross_weight"]

# Payment-method risk rating, safest first / 付款方式风险分级，最安全的在前.
PAYMENT_RISK = {
    "tt_advance": "LOW",
    "tt_deposit": "MEDIUM",
    "lc_sight": "MEDIUM",
    "dp": "MEDIUM-HIGH",
    "oa": "HIGH",
    "western_union": "VERY HIGH",
    "third_party": "VERY HIGH",
}

# Payment methods refused outright on a first order / 首单直接拒绝的方式.
REFUSED_FIRST_ORDER = {"oa", "western_union", "third_party"}

# First-order floor for the deposit, percent / 首单定金底线（百分比）.
MIN_FIRST_ORDER_DEPOSIT_RATE = 30.0

# The 10 fulfillment stages, in order / 订单交付十步，按顺序.
STAGES = [
    ("pi", "PI & contract / PI 与合同"),
    ("deposit", "Deposit / 定金"),
    ("production", "Production / 生产"),
    ("inspection", "Inspection / 验货"),
    ("balance", "Balance payment / 尾款"),
    ("booking", "Booking / 订舱"),
    ("customs", "Customs declaration / 报关"),
    ("bill_of_lading", "Bill of lading / 提单"),
    ("docs", "Docs pack for clearance / 清关单据包"),
    ("aftersales", "After-sales & reorder / 售后与复购"),
]
STAGE_IDS = [s[0] for s in STAGES]
STAGE_TITLES = dict(STAGES)

DEFAULT_STATE_FILE = "fulfillment_state.json"


def demo_order():
    """Built-in fictional example order / 内置虚构示例订单.

    Every value is made up for the demo; nothing here is a real company,
    price or contact. / 所有值均为演示编造，不是真实公司、价格或联系方式。
    """
    return {
        "buyer": "【示例】中东港口批发商",
        "spec": "295/80R22.5",
        "qty": 480,
        "unit_price": 28.0,
        "total": 13440.0,
        "currency": "USD",
        "incoterm": "FOB Yantian",
        "payment_terms": "T/T 30% deposit + 70% against B/L copy",
        "payment_method": "tt_deposit",
        "validity_days": 30,
        "bank_details": "【示例】Beneficiary / SWIFT / A/C No. on PI",
        "deposit_rate": 30,
        "deposit_received": 4032.0,
        "deposit_confirmed_by_bank": True,
        "pi_confirmed": True,
        "first_order": True,
        "balance_received": 0.0,
        "docs_sent": False,
        "bl": {
            "shipper": "【示例】出口商",
            "consignee": "【示例】中东港口批发商",
            "notify": "【示例】中东港口批发商",
            "description": "295/80R22.5 tires",
            "pieces": 480,
            "gross_weight": 28800,
            "port_of_loading": "Yantian",
            "port_of_discharge": "Dammam",
            "freight_terms": "Freight prepaid",
            "shipment_date": "2026-12-20",
        },
        "docs": {
            "invoice": {"description": "295/80R22.5 tires",
                        "pieces": 480, "gross_weight": 28800},
            "packing_list": {"description": "295/80R22.5 tires",
                             "pieces": 480, "gross_weight": 28800},
            "bill_of_lading": {"description": "295/80R22.5 tires",
                               "pieces": 480, "gross_weight": 28800},
        },
    }


def money(value):
    """Round money to 2 decimals / 金额保留两位小数."""
    return round(float(value), 2)


def validate_order(order):
    """Validate order facts; raise ValueError on bad input / 校验订单事实.

    Numbers that do not add up are an error, not a silent fix: a wrong
    total on a PI is exactly how money gets lost.
    数字对不上就报错，不悄悄改：PI 上总价算错，丢的就是真钱。
    """
    if not isinstance(order, dict):
        raise ValueError("order must be a JSON object / 订单必须是 JSON 对象")
    qty = order.get("qty")
    unit_price = order.get("unit_price")
    total = order.get("total")
    if qty is not None and (not isinstance(qty, (int, float)) or qty <= 0):
        raise ValueError("qty must be a positive number / 数量必须是正数")
    if unit_price is not None and (
            not isinstance(unit_price, (int, float)) or unit_price < 0):
        raise ValueError("unit_price must be >= 0 / 单价不能为负")
    if total is not None and (
            not isinstance(total, (int, float)) or total < 0):
        raise ValueError("total must be >= 0 / 总价不能为负")
    if qty is not None and unit_price is not None and total is not None:
        if abs(money(qty * unit_price) - money(total)) > 0.01:
            raise ValueError(
                "qty x unit_price (%.2f) does not match total (%.2f) / "
                "数量 x 单价与总价对不上" % (qty * unit_price, total))
    rate = order.get("deposit_rate", MIN_FIRST_ORDER_DEPOSIT_RATE)
    if not isinstance(rate, (int, float)) or rate < 0 or rate > 100:
        raise ValueError("deposit_rate must be 0-100 / 定金比例须在 0-100 之间")
    received = order.get("deposit_received", 0.0)
    if not isinstance(received, (int, float)) or received < 0:
        raise ValueError("deposit_received must be >= 0 / 已收定金不能为负")
    method = order.get("payment_method", "tt_deposit")
    if method not in PAYMENT_RISK:
        raise ValueError(
            "unknown payment_method %r (expect one of %s) / 未知的付款方式"
            % (method, ", ".join(sorted(PAYMENT_RISK))))
    return order


def deposit_expected(order):
    """Deposit due = total x rate / 应收定金 = 总价 x 比例."""
    total = order.get("total")
    if total is None:
        return None
    return money(total * float(order.get(
        "deposit_rate", MIN_FIRST_ORDER_DEPOSIT_RATE)) / 100.0)


def balance_due(order):
    """Balance due = total - deposit received / 应收尾款 = 总价 - 已收定金."""
    total = order.get("total")
    if total is None:
        return None
    return money(total - float(order.get("deposit_received", 0.0)))


def deposit_check(order):
    """Deposit gate: amount, rate floor, bank confirmation / 定金关口.

    A screenshot of a receipt is not proof: only your own bank statement
    counts (docs/07 step 2). / 水单截图不算数：只认自家银行流水。
    Returns a dict with expected / received / shortfall / ok / notes.
    """
    expected = deposit_expected(order)
    received = money(order.get("deposit_received", 0.0))
    rate = float(order.get("deposit_rate", MIN_FIRST_ORDER_DEPOSIT_RATE))
    first = bool(order.get("first_order", True))
    notes = []
    ok = True
    if expected is None:
        notes.append("total missing: cannot compute deposit due / 缺总价，算不出应收定金")
        return {"expected": None, "received": received, "shortfall": None,
                "ok": False, "notes": notes}
    shortfall = money(max(0.0, expected - received))
    if received < expected:
        ok = False
        notes.append("shortfall %.2f %s / 定金还差 %.2f %s"
                     % (shortfall, order.get("currency", "USD"),
                        shortfall, order.get("currency", "USD")))
    if first and rate < MIN_FIRST_ORDER_DEPOSIT_RATE:
        ok = False
        notes.append("first order deposit rate %.1f%% is below the 30%% floor / "
                     "首单定金比例低于 30%% 底线" % rate)
    if received > 0 and not order.get("deposit_confirmed_by_bank"):
        ok = False
        notes.append("deposit not confirmed by your own bank statement "
                     "(a receipt screenshot does not count) / "
                     "定金未经自家银行流水确认（水单截图不算数）")
    if received > money(order.get("total", 0.0)):
        ok = False
        notes.append("received exceeds total: overpayment, check before moving on / "
                     "已收款超过总价：多付了，先核对再往下走")
    method = order.get("payment_method", "tt_deposit")
    if first and method in REFUSED_FIRST_ORDER:
        ok = False
        notes.append("payment method %s is refused on a first order / "
                     "首单不接 %s 这种付款方式" % (method, method))
    return {"expected": expected, "received": received,
            "shortfall": shortfall, "ok": ok, "notes": notes}


def pi_check(order):
    """Missing PI fields / PI 缺哪些字段."""
    return [f for f in PI_FIELDS if order.get(f) in (None, "", 0)]


def bl_check(order):
    """Missing draft B/L fields / 提单草稿缺哪些字段."""
    bl = order.get("bl") or {}
    if not isinstance(bl, dict):
        raise ValueError("bl must be an object / 提单信息必须是对象")
    return [f for f in BL_FIELDS if bl.get(f) in (None, "")]


def three_way_check(order):
    """Three-way consistency: invoice vs packing list vs B/L / 三单一致性.

    Returns a list of mismatches: (field, {doc: value}).
    只比三处都该一样的字段：品名、件数、毛重。
    """
    docs = order.get("docs") or {}
    mismatches = []
    for field in THREE_WAY_FIELDS:
        values = {}
        for doc_name in ("invoice", "packing_list", "bill_of_lading"):
            doc = docs.get(doc_name) or {}
            if isinstance(doc, dict) and doc.get(field) is not None:
                values[doc_name] = doc.get(field)
        unique = set(values.values())
        if len(unique) > 1:
            mismatches.append((field, values))
    return mismatches


def _item(stage, key, text_en, text_zh, status, detail=""):
    return {"stage": stage, "key": key, "text_en": text_en,
            "text_zh": text_zh, "status": status, "detail": detail}


def build_checklist(order, done=None):
    """Build the full 10-stage checklist / 生成十步核对清单.

    done: {stage_id: timestamp} of stages already signed off.
    Status per item: done / pending / blocked / warning.
    """
    done = done or {}
    dep = deposit_check(order)
    pi_missing = pi_check(order)
    bl_missing = bl_check(order)
    mismatches = three_way_check(order)
    method = order.get("payment_method", "tt_deposit")
    risk = PAYMENT_RISK[method]
    items = []

    def done_or(stage, status):
        return "done" if stage in done else status

    # 1. PI & contract / PI 与合同
    items.append(_item("pi", "pi_fields",
                       "PI fields complete (%d/%d)" % (
                           len(PI_FIELDS) - len(pi_missing), len(PI_FIELDS)),
                       "PI 字段齐全（%d/%d）" % (
                           len(PI_FIELDS) - len(pi_missing), len(PI_FIELDS)),
                       "done" if not pi_missing else "blocked",
                       "" if not pi_missing else
                       "missing: %s / 缺：%s" % (", ".join(pi_missing),
                                                 ", ".join(pi_missing))))
    items.append(_item("pi", "pi_confirmed",
                       "PI confirmed by buyer (signed or emailed 'confirmed')",
                       "PI 已获客户确认（回签或邮件确认）",
                       "done" if order.get("pi_confirmed") else "blocked"))
    items.append(_item("pi", "names_match",
                       "Buyer full name identical on PI, contract and payer",
                       "买方全称在 PI、合同、付款人三处一致",
                       done_or("pi", "pending"),
                       "check by hand against the signed PI / 对照已签 PI 人工核对"))
    items.append(_item("pi", "terms_exact",
                       "Exact qty + tolerance, delivery window, packing/marks, "
                       "inspection period, dispute forum — no 'about' or 'ASAP'",
                       "数量精确+溢短装、交期窗口、包装唛头、异议期、争议解决地"
                       "——不写「约」「尽快」",
                       done_or("pi", "pending")))

    # 2. Deposit / 定金
    items.append(_item("deposit", "method_risk",
                       "Payment method %s, risk %s" % (method, risk),
                       "付款方式 %s，风险 %s" % (method, risk),
                       "blocked" if (order.get("first_order", True)
                                     and method in REFUSED_FIRST_ORDER)
                       else "done"))
    items.append(_item("deposit", "amount",
                       "Deposit %.2f %s received of %.2f %s expected"
                       % (dep["received"], order.get("currency", "USD"),
                          dep["expected"] if dep["expected"] is not None else 0,
                          order.get("currency", "USD")),
                       "定金已收 %.2f %s，应收 %.2f %s"
                       % (dep["received"], order.get("currency", "USD"),
                          dep["expected"] if dep["expected"] is not None else 0,
                          order.get("currency", "USD")),
                       "done" if dep["ok"] else "blocked",
                       "; ".join(dep["notes"])))
    items.append(_item("deposit", "bank_statement",
                       "Confirmed on your own bank statement, not a screenshot",
                       "以自家银行流水确认到账，不是客户发来的截图",
                       "done" if order.get("deposit_confirmed_by_bank")
                       and dep["received"] > 0 else "blocked",
                       "water transfer screenshots can be faked / 水单可以 P 图"))
    items.append(_item("deposit", "payer_match",
                       "Payer name matches contract buyer; any bank-account "
                       "change re-confirmed on a known number",
                       "付款人与合同买方一致；银行账号如有变更须用已知电话二次确认",
                       done_or("deposit", "pending")))

    # 3. Production / 生产
    items.append(_item("production", "schedule",
                       "Production schedule and key nodes confirmed with factory",
                       "排产计划与关键节点已与工厂确认",
                       done_or("production", "pending")))
    items.append(_item("production", "progress_evidence",
                       "Progress photos/video received at 30-50% completion",
                       "生产到 30%-50% 时已收到进度照片/视频",
                       done_or("production", "pending")))
    items.append(_item("production", "batch_record",
                       "Raw-material batch / production line recorded",
                       "原料批次/产线已记录",
                       done_or("production", "pending")))

    # 4. Inspection / 验货
    items.append(_item("inspection", "preloading",
                       "Pre-loading inspection: spec, pattern, appearance, "
                       "packing, labels, weight — all checked",
                       "装柜前验货：型号、花纹、外观、包装、标签、重量逐项核对",
                       done_or("inspection", "pending")))
    items.append(_item("inspection", "loading_photos",
                       "Loading photos + container no. + seal no. kept",
                       "装柜照片、柜号、封条号已留证",
                       done_or("inspection", "pending")))
    items.append(_item("inspection", "certs",
                       "Required certificates obtained BEFORE loading, "
                       "numbers match the contract",
                       "所需证书已在装柜前取得，编号与合同一致",
                       done_or("inspection", "pending")))

    # 5. Balance / 尾款
    due = balance_due(order)
    received_bal = money(order.get("balance_received", 0.0))
    bal_ok = due is not None and received_bal >= due
    items.append(_item("balance", "amount",
                       "Balance due %.2f %s, received %.2f %s"
                       % (due if due is not None else 0,
                          order.get("currency", "USD"), received_bal,
                          order.get("currency", "USD")),
                       "尾款应收 %.2f %s，已收 %.2f %s"
                       % (due if due is not None else 0,
                          order.get("currency", "USD"), received_bal,
                          order.get("currency", "USD")),
                       "done" if bal_ok else "pending",
                       "release B/L only after cleared funds / "
                       "到账后才放单"))
    items.append(_item("balance", "release_control",
                       "Telex release / original B/L held until balance clears",
                       "尾款到账前不电放、不寄正本提单",
                       done_or("balance", "pending")))

    # 6. Booking / 订舱
    items.append(_item("booking", "forwarder_compare",
                       "At least 3 forwarders compared (price, schedule, "
                       "direct vs transshipment)",
                       "至少比了 3 家货代（价格、船期、直航/中转）",
                       done_or("booking", "pending")))
    items.append(_item("booking", "so_cutoff",
                       "Shipping order, vessel/voyage, cut-off times confirmed",
                       "订舱单、船名航次、截关/截单时间已确认",
                       done_or("booking", "pending")))

    # 7. Customs / 报关
    items.append(_item("customs", "hs_code",
                       "HS code and declaration elements confirmed",
                       "HS 编码与申报要素已确认",
                       done_or("customs", "pending")))
    items.append(_item("customs", "release_note",
                       "Declaration / release notice kept on file",
                       "报关单/放行通知已留档",
                       done_or("customs", "pending")))

    # 8. Bill of lading / 提单
    items.append(_item("bill_of_lading", "draft_check",
                       "Draft B/L checked word by word (%d/%d fields)"
                       % (len(BL_FIELDS) - len(bl_missing), len(BL_FIELDS)),
                       "提单草稿已逐字核对（%d/%d 项）"
                       % (len(BL_FIELDS) - len(bl_missing), len(BL_FIELDS)),
                       "done" if not bl_missing else "blocked",
                       "" if not bl_missing else
                       "missing: %s / 缺：%s" % (", ".join(bl_missing),
                                                 ", ".join(bl_missing))))
    items.append(_item("bill_of_lading", "consignee_type",
                       "Consignee type confirmed (straight vs to order) — "
                       "it decides who controls the goods",
                       "收货人类型已确认（记名/凭指示）——它决定货权在谁手里",
                       done_or("bill_of_lading", "pending"),
                       "unsure? ask the forwarder, do not assume / "
                       "不确定就问货代，别默认"))

    # 9. Docs pack / 清关单据包
    items.append(_item("docs", "three_way",
                       "Invoice / packing list / B/L agree on description, "
                       "pieces, gross weight",
                       "发票、装箱单、提单三单一致（品名、件数、毛重）",
                       "done" if not mismatches else "blocked",
                       "" if not mismatches else
                       "; ".join("%s: %s" % (f, v)
                                 for f, v in mismatches)))
    items.append(_item("docs", "sent_24h",
                       "Full docs pack sent within 24h of shipment and "
                       "receipt confirmed by buyer",
                       "全套单据已在装船后 24 小时内发给客户并确认收到",
                       "done" if order.get("docs_sent") else
                       done_or("docs", "pending")))

    # 10. After-sales / 售后与复购
    items.append(_item("aftersales", "checkin",
                       "Check-in 3-7 days after delivery (arrival / packing / "
                       "quantity / labels OK?)",
                       "交付后 3-7 天主动问一次到货与使用情况",
                       done_or("aftersales", "pending")))
    items.append(_item("aftersales", "reorder_reminder",
                       "Customer file updated; reorder reminder set 2-3 weeks "
                       "before the expected reorder window",
                       "客户档案已更新；复购提醒已按补货窗口提前 2-3 周设好",
                       done_or("aftersales", "pending")))
    items.append(_item("aftersales", "referral_case",
                       "Referral asked; anonymized case archived (no real names, "
                       "emails or phones)",
                       "已请客户转介绍；脱敏案例已归档（无真实公司名/人名/联系方式）",
                       done_or("aftersales", "pending")))

    # Money gates / 钱的关口
    gates = {
        "production": {
            "title_en": "Production gate: PI confirmed + deposit confirmed",
            "title_zh": "排产关口：PI 已确认 + 定金已确认",
            "go": bool(order.get("pi_confirmed")) and dep["ok"],
            "detail": "; ".join(dep["notes"]) if not dep["ok"]
                      else ("PI not confirmed / PI 未确认"
                            if not order.get("pi_confirmed") else "clear / 通过"),
        },
        "release": {
            "title_en": "Release gate: balance cleared before telex / original B/L",
            "title_zh": "放单关口：尾款到账后才电放/寄正本提单",
            "go": bal_ok,
            "detail": ("balance shortfall %.2f %s / 尾款还差 %.2f %s"
                       % (money(due - received_bal),
                          order.get("currency", "USD"),
                          money(due - received_bal),
                          order.get("currency", "USD")))
                      if due is not None and not bal_ok
                      else "clear / 通过",
        },
        "ship": {
            "title_en": "Ship gate: inspection done + draft B/L complete + "
                        "three-way consistent",
            "title_zh": "出运关口：验货完成 + 提单草稿齐全 + 三单一致",
            "go": ("inspection" in done and not bl_missing
                   and not mismatches),
            "detail": ("inspection not signed off / 验货未确认"
                       if "inspection" not in done
                       else ("draft B/L incomplete / 提单草稿不全"
                             if bl_missing else
                             "three-way mismatch / 三单不一致")),
        },
    }
    blocked = [i for i in items if i["status"] == "blocked"]
    done_count = sum(1 for i in items if i["status"] == "done")
    # Note: release / ship gates read NO-GO until their stage arrives
    # (balance is not due yet, inspection has not happened yet) — that is
    # normal mid-order, so the verdict only counts blocked items.
    # 注意：放单/出运关口在节点未到时本来就是 NO-GO（尾款还没到收的时候，
    # 验货还没发生），属于正常，所以结论只看被拦的核对项。
    verdict = ("BLOCKED — fix the blocked items before moving on / "
               "已拦下——先处理被拦的项再往下走") if blocked else (
        "ON TRACK — no checklist item is blocked right now / "
        "进行中——当前没有被拦的核对项")
    return {"order": order, "items": items, "gates": gates,
            "summary": {"total": len(items), "done": done_count,
                        "blocked": len(blocked),
                        "pending": len(items) - done_count - len(blocked)},
            "verdict": verdict}


def gate_for_done(stage, order, done):
    """Can this stage be signed off now? / 这个阶段现在能打勾吗？

    Returns (allowed, reason). Money gates refuse, with the reason spelled
    out — a silent sign-off is how a deposit gets skipped.
    关口不通过就拒绝打勾，并写清原因——悄悄打勾等于跳过定金。
    """
    checklist = build_checklist(order, done)
    if stage == "production" and not checklist["gates"]["production"]["go"]:
        return False, "production gate fails: %s / 排产关口未过：%s" % (
            checklist["gates"]["production"]["detail"],
            checklist["gates"]["production"]["detail"])
    if stage == "balance" and not checklist["gates"]["release"]["go"]:
        return False, "release gate fails: %s / 放单关口未过：%s" % (
            checklist["gates"]["release"]["detail"],
            checklist["gates"]["release"]["detail"])
    if stage == "bill_of_lading":
        missing = bl_check(order)
        if missing:
            return False, ("draft B/L incomplete, missing: %s / 提单草稿不全，缺：%s"
                           % (", ".join(missing), ", ".join(missing)))
    if stage == "docs":
        mismatches = three_way_check(order)
        if mismatches:
            return False, ("three-way mismatch: %s / 三单不一致：%s"
                           % ("; ".join("%s: %s" % (f, v)
                                        for f, v in mismatches),
                              "; ".join("%s: %s" % (f, v)
                                        for f, v in mismatches)))
    return True, ""


def load_order(path):
    """Load order JSON / 读订单 JSON."""
    with open(path, "r", encoding="utf-8") as f:
        order = json.load(f)
    return validate_order(order)


def load_state(path):
    """Load done-stages state file; missing file = empty state / 读打卡状态."""
    if not path or not os.path.exists(path):
        return {"done": {}}
    with open(path, "r", encoding="utf-8") as f:
        state = json.load(f)
    if not isinstance(state, dict) or not isinstance(
            state.get("done", {}), dict):
        raise ValueError("bad state file: expect {\"done\": {...}} / 状态文件格式不对")
    return state


def save_state(path, state):
    """Save done-stages state file / 写打卡状态."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def render_table(checklist):
    """Plain-text table / 纯文本表格."""
    order = checklist["order"]
    lines = []
    lines.append("Order fulfillment checklist / 订单交付核对清单")
    lines.append("Buyer / 买方: %s" % order.get("buyer", "—"))
    lines.append("Order / 订单: %s x %s @ %.2f %s = %.2f %s (%s)"
                 % (order.get("spec", "—"), order.get("qty", "—"),
                    order.get("unit_price", 0) or 0,
                    order.get("currency", "USD"),
                    order.get("total", 0) or 0,
                    order.get("currency", "USD"),
                    order.get("incoterm", "—")))
    lines.append("Payment / 付款: %s" % order.get("payment_terms", "—"))
    s = checklist["summary"]
    lines.append("Progress / 进度: %d done / %d blocked / %d pending "
                 "(total %d) / 已完成 %d 项，被拦 %d 项，待办 %d 项（共 %d 项）"
                 % (s["done"], s["blocked"], s["pending"], s["total"],
                    s["done"], s["blocked"], s["pending"], s["total"]))
    lines.append("Verdict / 结论: %s" % checklist["verdict"])
    lines.append("")
    lines.append("Money gates / 钱的关口:")
    for gate_id, gate in checklist["gates"].items():
        mark = "GO" if gate["go"] else "NO-GO"
        lines.append("  [%s] %s — %s" % (mark, gate["title_en"], gate["detail"]))
        lines.append("        %s" % gate["title_zh"])
    lines.append("")
    current_stage = None
    marks = {"done": "[x]", "pending": "[ ]", "blocked": "[!]",
             "warning": "[?]"}
    for item in checklist["items"]:
        if item["stage"] != current_stage:
            current_stage = item["stage"]
            lines.append("%s %s" % (current_stage,
                                    STAGE_TITLES[current_stage]))
        detail = (" — %s" % item["detail"]) if item["detail"] else ""
        lines.append("  %s %s / %s%s" % (marks[item["status"]],
                                         item["text_en"], item["text_zh"],
                                         detail))
    lines.append("")
    lines.append("Notes / 说明: only your own bank statement confirms a payment; "
                 "a receipt screenshot does not count. / "
                 "只认自家银行流水，客户发来的水单截图不算到账。")
    lines.append("This checklist is not legal advice; contract wording and "
                 "dispute resolution need professional review. / "
                 "本清单不是法律意见；合同措辞与争议解决须请专业人士审阅。")
    return "\n".join(lines) + "\n"


def render_json(checklist):
    """JSON output / JSON 输出."""
    out = {"buyer": checklist["order"].get("buyer"),
           "spec": checklist["order"].get("spec"),
           "qty": checklist["order"].get("qty"),
           "total": checklist["order"].get("total"),
           "currency": checklist["order"].get("currency", "USD"),
           "summary": checklist["summary"],
           "verdict": checklist["verdict"],
           "gates": {k: {"go": v["go"], "detail": v["detail"]}
                     for k, v in checklist["gates"].items()},
           "items": checklist["items"]}
    return json.dumps(out, ensure_ascii=False, indent=2) + "\n"


def main(argv=None):
    """CLI entry / 命令行入口."""
    parser = argparse.ArgumentParser(
        description="Order fulfillment checklist (docs/07-order-delivery.md) / "
                    "订单交付核对清单")
    parser.add_argument("--order", help="order JSON file / 订单 JSON 文件")
    parser.add_argument("--demo", action="store_true",
                        help="run with the built-in fictional example order / "
                             "用内置虚构示例订单跑一次")
    parser.add_argument("--state", default=DEFAULT_STATE_FILE,
                        help="done-stages state file (default: %(default)s) / "
                             "打卡状态文件")
    parser.add_argument("--done", choices=STAGE_IDS,
                        help="sign off one stage (gates are enforced) / "
                             "给一个阶段打勾（关口会拦）")
    parser.add_argument("--status", action="store_true",
                        help="show progress summary only / 只看进度汇总")
    parser.add_argument("--deposit-received", type=float, default=None,
                        help="override deposit received in the order / "
                             "覆盖订单里的已收定金")
    parser.add_argument("--balance-received", type=float, default=None,
                        help="override balance received in the order / "
                             "覆盖订单里的已收尾款")
    parser.add_argument("--format", choices=["table", "json"],
                        default="table", help="output format / 输出格式")
    parser.add_argument("--out", help="also write output to file / 同时写到文件")
    args = parser.parse_args(argv)

    if args.demo and args.order:
        parser.error("--demo and --order cannot be used together / "
                     "--demo 与 --order 不能同时用")
    if not args.demo and not args.order:
        parser.error("give --order FILE or --demo / 须给 --order 文件或 --demo")

    try:
        order = demo_order() if args.demo else load_order(args.order)
        if args.deposit_received is not None:
            order["deposit_received"] = args.deposit_received
        if args.balance_received is not None:
            order["balance_received"] = args.balance_received
        validate_order(order)
        state = load_state(args.state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    done = state.get("done", {})
    if args.done:
        if args.done in done:
            print("stage %s is already signed off at %s / 该阶段已于 %s 打勾"
                  % (args.done, done[args.done], done[args.done]))
            return 0
        allowed, reason = gate_for_done(args.done, order, done)
        if not allowed:
            print("refused: %s" % reason, file=sys.stderr)
            return 2
        done[args.done] = datetime.now().isoformat(timespec="seconds")
        state["done"] = done
        try:
            save_state(args.state, state)
        except OSError as exc:
            print("error: cannot write state file: %s" % exc, file=sys.stderr)
            return 2
        print("signed off: %s (%s) / 已打勾：%s（%s)"
              % (args.done, STAGE_TITLES[args.done], args.done,
                 STAGE_TITLES[args.done]))
        return 0

    checklist = build_checklist(order, done)
    if args.status:
        s = checklist["summary"]
        lines = ["Progress / 进度: %d/%d done, %d blocked, %d pending"
                 % (s["done"], s["total"], s["blocked"], s["pending"]),
                 "Verdict / 结论: %s" % checklist["verdict"]]
        for gate_id, gate in checklist["gates"].items():
            lines.append("Gate %s: %s — %s"
                         % (gate_id, "GO" if gate["go"] else "NO-GO",
                            gate["detail"]))
        output = "\n".join(lines) + "\n"
    elif args.format == "json":
        output = render_json(checklist)
    else:
        output = render_table(checklist)
    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(output)
        except OSError as exc:
            print("error: cannot write output file: %s" % exc, file=sys.stderr)
            return 2
    print(output, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
