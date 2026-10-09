#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提交前自查：扫一遍你要提交的东西里有没有真实客户数据。

为什么需要这个：
    `.gitignore` 只对「还没被 git 记住」的文件有效。
    `examples/leads_example.csv` 是仓库自带的，早就被 git 记住了——
    你往里面填真客户，再一个 `git add -A + git commit`，它就上去了，
    .gitignore 一声不吭。这个脚本就是补那个洞。

用法（在你打算提交之前）：
    python scripts/check_private_data.py

有真数据就打印文件名和第几行，并退出码1（挡住提交）。
干净就打印一行「没查到真实客户数据」，退出码 0。

零依赖，跟仓库里其他脚本一个规矩。
"""
from __future__ import print_function

import os
import re
import sys

# 允许出现的邮箱域名：RFC 2606 保留域名 + 本项目约定的示例域名
OK_DOMAINS = {
    "sample.example", "example.com", "example.org", "example.net",
    "localhost", "test", "invalid",
}

# 允许出现的电话：占位符形态（+000 00 000 0000 之类）
PLACEHOLDER_PHONE = re.compile(r"[+\d][\d\s()+-]*\b0{3,}\b")

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")

# 中国/中东常见手机号形态：11 位手机、或带国家码的 +966 51xxxxxxx
PHONE = re.compile(r"(?<!\d)(?:\+?\d{1,3}[\s-]?)?(?:\d[\s-]?){8,13}\d(?!\d)")

SCAN_EXT = (
    ".md", ".csv", ".txt", ".json", ".html", ".py", ".yml", ".yaml",
    ".tsv", ".xlsx", ".xls",
)
SKIP_DIR = {".git", "__pycache__", "node_modules", ".venv", "venv"}

# 明显的占位/示例/脱敏标记——出现在同一行就放过
SAFE_HINT = (
    "sample.example", "example.com", "【示例】", "[示例]", "占位", "placeholder",
    "yourcompany", "your-email", "yourname", "test@", "fake", "dummy",
)


def looks_like_real_phone(line):
    """这行里的号码是不是看着像真电话（不是 +000 00 000 0000 这种占位）。"""
    if PLACEHOLDER_PHONE.search(line):
        return False
    for m in PHONE.finditer(line):
        digits = re.sub(r"\D", "", m.group())
        if len(digits) < 9:
            continue
        # 全是 0 / 全是同一个数字 → 占位
        if len(set(digits)) <= 1:
            continue
        return True
    return False


def scan_file(path):
    """返回 [(行号, 为什么中招)]，干净就返回空列表。"""
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except (OSError, IOError):
        return []

    hits = []
    for no, line in enumerate(lines, 1):
        low = line.lower()
        if any(h in line for h in ("【示例】", "[示例]")) or \
           any(h in low for h in SAFE_HINT):
            continue

        for domain in EMAIL.findall(line):
            if domain.lower() not in OK_DOMAINS:
                hits.append((no, "邮箱域名 %s（不是保留域名，像是真人邮箱）" % domain))
                break

        if looks_like_real_phone(line):
            hits.append((no, "手机号/座机号（看着像真号码）"))

    return hits


def main():
    # 只扫要提交的目录，别把 node_modules、.venv 这些翻一遍
    roots = ["scripts", "docs", "examples", "prompts", ".github"]
    # 仓库根目录下的单文件（README / LICENSE 之类）
    root_files = []

    seen = set()
    files = []
    for fn in sorted(os.listdir(".")):
        if fn.endswith(SCAN_EXT) and os.path.isfile(fn):
            root_files.append(fn)

    for root in roots:
        if not os.path.isdir(root):
            continue
        for fn in sorted(os.listdir(root)):
            p = os.path.join(root, fn)
            if os.path.isfile(p) and fn.endswith(SCAN_EXT):
                files.append(p)

    files = sorted(set(files) | set(root_files))
    files = [f.replace("\\", "/") for f in files]

    total_hits = 0
    report = []
    for path in files:
        if path in seen:
            continue
        seen.add(path)
        hits = scan_file(path)
        if hits:
            total_hits += len(hits)
            report.append((path, hits))

    print("扫了 %d 个文件" % len(files))
    if not report:
        print("没查到真实客户数据，这一关过了。")
        return 0

    print("")
    print("下面这些地方看着像真客户数据，提交前先处理掉：")
    for path, hits in report:
        print("")
        print("  %s" % path)
        for no, why in hits[:8]:
            print("    第 %d 行 — %s" % (no, why))
        if len(hits) > 8:
            print("    ……还有 %d 处" % (len(hits) - 8))
    print("")
    print("怎么改（挑一个）：")
    print("  · 真客户挪到 my_leads.csv，别留在要提交的文件里")
    print("  · 邮箱换成 sample.example（保留域名，不会真的寄出去）")
    print("  · 电话换成 +000 00 000 0000（明显的假号）")
    print("  · 确实只是示例，就把公司名带上【示例】前缀")
    return 1


if __name__ == "__main__":
    sys.exit(main())