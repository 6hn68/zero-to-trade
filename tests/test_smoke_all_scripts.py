"""Smoke test: every script must run its smallest example and exit 0.
冒烟测试：十五个脚本，每个至少能跑一次最小示例并成功退出。

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

import json
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
    "fulfillment_checklist": ["--demo"],  # --state is added per-run, see below
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

    def test_fulfillment_checklist_minimal_example(self):
        # fulfillment_checklist writes its done-stages state next to
        # --state; keep it in a temp dir so the repo stays clean.
        # fulfillment_checklist 的打卡状态写在 --state 指定的文件里，
        # 放临时目录，别脏了仓库。
        with tempfile.TemporaryDirectory() as tmp:
            state = str(Path(tmp) / "fulfillment_state.json")
            proc = _run("fulfillment_checklist",
                        EXAMPLES["fulfillment_checklist"] + ["--state", state])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue(proc.stdout.strip())
            self.assertIn("4032.00", proc.stdout)

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



class TestSmokeDailyVideoListExamples(unittest.TestCase):
    """daily_video_list beyond the no-arg run: its --help lists five
    usage lines, and the unit tests cover the pure functions, but only
    the smoke layer proves the documented CLI combinations actually
    run end to end. Four checks, no overlap with
    tests/test_daily_video_list.py (which tests the functions and
    single flags, not these CLI-level combinations).

    daily_video_list 光跑无参还不够：--help 里写了 5 行用法，单测管
    的是纯函数，这里只证明文档里写的 CLI 组合端到端真能跑。4 项，
    与 tests/test_daily_video_list.py 不重叠（那边测函数和单个
    flag，不测这些 CLI 组合）。
    """

    def test_daily_video_list_same_date_same_output(self):
        # Same date -> same list, twice in a row, byte for byte.
        # The docstring promises this; the unit test only checks the
        # pure function, this checks the real CLI output.
        # 同一天跑两次，输出要逐字节一样。文档里承诺了这点；单测只
        # 验了纯函数，这里验的是真实 CLI 输出。
        first = _run("daily_video_list", ["--date", "2026-11-22"])
        second = _run("daily_video_list", ["--date", "2026-11-22"])
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(first.stdout, second.stdout)

    def test_daily_video_list_date_plus_market_from_help(self):
        # The --help line: --date 2026-11-22 --market nigeria.
        # All five videos must land in the pinned market.
        # --help 里那行：--date 2026-11-22 --market nigeria。
        # 5 条视频必须全钉在这个市场。
        proc = _run("daily_video_list",
                    ["--date", "2026-11-22", "--market", "nigeria",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(len(data["videos"]), 5)
        self.assertTrue(all(v["market_en"] == "Nigeria"
                            for v in data["videos"]),
                        proc.stdout)

    def test_daily_video_list_bad_date_says_it_in_plain_words(self):
        # Bad date must exit non-zero AND speak plainly: no traceback.
        # Same bar the CI bad-CSV step holds the other scripts to.
        # 坏日期必须非零退出，而且说人话：不许甩 traceback。
        # 跟 CI 里烂 CSV 那步对别的脚本的要求是同一条线。
        proc = _run("daily_video_list", ["--date", "2026-13-40"])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("Bad date", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_daily_video_list_out_file_matches_screen(self):
        # --out writes the same text the screen shows, into a temp
        # dir so the repo stays clean (the unit test writes into
        # tests/ and deletes it afterwards; this one never touches
        # the repo).
        # --out 落盘的内容要跟屏幕上的一样，写进临时目录，别脏仓库
        # （单测是写进 tests/ 再删，这里全程不碰仓库）。
        with tempfile.TemporaryDirectory() as tmp:
            out_file = str(Path(tmp) / "today.txt")
            proc = _run("daily_video_list",
                        ["--date", "2026-11-22", "--out", out_file])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            written = Path(out_file).read_text(encoding="utf-8")
            self.assertEqual(written, proc.stdout)


if __name__ == "__main__":
    unittest.main()
