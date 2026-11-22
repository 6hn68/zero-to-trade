"""Smoke test: every script must run its smallest example and exit 0.
冒烟测试：十四个脚本，每个至少能跑一次最小示例并成功退出。

Why this file exists / 为什么要有这个文件：
  Dedicated tests cover the tricky logic, but nothing used to check the
  plainest thing: "does each script actually start and finish?" A script
  can pass all its unit tests yet crash on its own --help example because
  nobody ever ran it end to end. This file is that check, one test per
  script, so a red line names the broken script directly.
  单测管的是难逻辑，但没人管最朴素的一件事：“脚本到底能不能跑起来？”
  一个脚本可以单测全绿，却在自己的 --help 例子上直接崩掉——因为从来
  没人端到端跑过一次。这个文件就是补这一关：一个脚本一个测试，红了
  哪行就知道是哪个脚本坏了。

Rules for the examples below / 下面例子的规矩：
  * Every example is copied from the script's own --help text where one
    exists, so the smoke test also proves the documented example works.
    有 --help 例子的，一律照抄 --help 里的例子，顺带证明文档里的例子
    是真的能跑的。
  * All data is fictional. Company names carry the 【示例】 prefix and
    the email uses the reserved sample.example domain, so nothing here
    can be mistaken for a real customer.
    数据全是虚构的。公司名带【示例】前缀，邮箱用保留域名
    sample.example，不会跟真实客户撞上。
  * No test writes into the repo: fast_path state goes to a temp dir.
    不往仓库里写东西：fast_path 的打卡状态文件写进临时目录。
  * No network, no third-party packages: subprocess + stdlib unittest only.
    不联网、不引第三方包：只用 subprocess + 标准库 unittest。
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"

# The smallest working example per script, taken from each script's --help.
# 每个脚本的最小可跑例子，取自各脚本自己的 --help。
EXAMPLES = {
    "anchor_price": ["--comp-low", "30", "--comp-high", "40", "--cost", "28"],
    "check_private_data": [],
    "daily_video_list": [],
    "due_diligence": ["--company", "【示例】海湾轮胎贸易"],
    "fast_path": ["--day", "1"],  # --state is added per-run, see below
    "followup_plan": ["--tier", "T0", "--start", "2026-10-08"],
    "landed_cost": ["--fob", "28"],
    "lead_score": ["examples/leads_example.csv"],
    "market_rules": ["--country", "Turkey"],
    "nudge": ["--day", "D3", "--scenario", "quoted"],
    "outreach_gen": ["examples/leads_example.csv", "--tier", "T0", "--lang", "en"],
    "quote_engine": ["--cost", "28", "--freight", "6"],
    "tire_pack": ["--size", "11.00R20", "--market", "nigeria"],
    "trade_show": ["--add", "【示例】海湾轮胎贸易", "--country", "Saudi Arabia",
                   "--product", "TBR 12.00R20", "--interest", "高",
                   "--email", "demo01@sample.example"],
}

# Keep this list in sync with scripts/*.py. If a script is added or renamed,
# this test must fail loudly instead of silently skipping it.
# 跟 scripts/*.py 保持同步。加了/改名了脚本，这里必须大声报错，
# 不许悄悄跳过。
EXPECTED_SCRIPTS = sorted(EXAMPLES)


def _run(name, args, cwd=REPO_ROOT):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / (name + ".py"))] + args,
        capture_output=True, text=True, cwd=cwd)


class TestSmokeAllScripts(unittest.TestCase):
    def test_no_script_is_missing_from_this_file(self):
        # Test coverage guard / 覆盖守门员：脚本数变了，先在这里拦住。
        on_disk = sorted(p.stem for p in SCRIPTS.glob("*.py"))
        self.assertEqual(on_disk, EXPECTED_SCRIPTS,
                         "scripts/ 里多了/少了脚本，先给它补一条冒烟例子再走："
                         "%s" % [s for s in on_disk if s not in EXPECTED_SCRIPTS])

    def test_help_exits_zero_for_all_scripts(self):
        for name in EXPECTED_SCRIPTS:
            with self.subTest(script=name):
                proc = _run(name, ["--help"])
                self.assertEqual(proc.returncode, 0, name)
                self.assertIn("usage:", proc.stdout.lower(), name)

    def test_anchor_price_minimal_example(self):
        proc = _run("anchor_price", EXAMPLES["anchor_price"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_check_private_data_scans_repo(self):
        proc = _run("check_private_data", EXAMPLES["check_private_data"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_daily_video_list_minimal_example(self):
        proc = _run("daily_video_list", EXAMPLES["daily_video_list"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())
        self.assertIn("5", proc.stdout)

    def test_due_diligence_minimal_example(self):
        proc = _run("due_diligence", EXAMPLES["due_diligence"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_fast_path_day_one(self):
        # fast_path writes its check-in state next to --state; keep it in
        # a temp dir so the repo stays clean.
        # fast_path 的打卡状态写在 --state 指定的文件里，放临时目录，
        # 别脏了仓库。
        with tempfile.TemporaryDirectory() as tmp:
            state = str(Path(tmp) / "fast_path_state.json")
            proc = _run("fast_path",
                        EXAMPLES["fast_path"] + ["--state", state])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue(proc.stdout.strip())

    def test_followup_plan_minimal_example(self):
        proc = _run("followup_plan", EXAMPLES["followup_plan"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_landed_cost_minimal_example(self):
        proc = _run("landed_cost", EXAMPLES["landed_cost"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_lead_score_minimal_example(self):
        proc = _run("lead_score", EXAMPLES["lead_score"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_market_rules_minimal_example(self):
        proc = _run("market_rules", EXAMPLES["market_rules"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())
        self.assertIn("Turkey", proc.stdout)

    def test_nudge_minimal_example(self):
        proc = _run("nudge", EXAMPLES["nudge"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_outreach_gen_minimal_example(self):
        proc = _run("outreach_gen", EXAMPLES["outreach_gen"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_quote_engine_minimal_example(self):
        proc = _run("quote_engine", EXAMPLES["quote_engine"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_tire_pack_minimal_example(self):
        proc = _run("tire_pack", EXAMPLES["tire_pack"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())

    def test_trade_show_minimal_example(self):
        # trade_show refuses a company with no contact info, so the
        # example carries the --email from its own --help text.
        # trade_show 没联系方式的公司不收，所以例子里带上了它自己
        # --help 里那行 --email。
        proc = _run("trade_show", EXAMPLES["trade_show"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(proc.stdout.strip())


if __name__ == "__main__":
    unittest.main()
