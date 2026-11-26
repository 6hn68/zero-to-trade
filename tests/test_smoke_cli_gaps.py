"""Smoke test, second layer: CLI flags no other test ever invokes.

Why this file exists / 为什么要有这个文件：
  tests/test_smoke_all_scripts.py 只跑每个脚本的最小例子；逐个核对
  15 个脚本的 --help 后发现，下面这 9 个 CLI 组合在全套测试（单测 +
  冒烟 + CI 步骤）里一次都没跑过——有些只在函数层测过，有些连函数
  层都没有。--help 里写了的例子（landed_cost 的 --qty/--sell-price、
  tire_pack 的 --li/--speed、nudge 的 --channel whatsapp）本该能跑，
  却从来没人端到端跑过一次。这里一次补齐，每条都是照抄 --help 里
  的例子或只加一个没盖到的 flag。

Scope / 范围：
  * Only flags that no test file and no CI step invokes as a CLI arg.
    只收全套测试 + CI 里一次都没以 CLI 形式跑过的 flag。
  * Flags already covered elsewhere (fast_path --done/--list/--progress,
    followup_plan --today/--reply, outreach_gen --review/--channel,
    nudge --list, due_diligence 的函数层) 不重复收。
  * All data is fictional: 【示例】 prefix, sample.example domain,
    +000 placeholder phones. No test writes into the repo.
    数据全是虚构的，不往仓库里写东西。
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def _run(name, args, cwd=REPO_ROOT):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / (name + ".py"))] + args,
        capture_output=True, text=True, cwd=cwd)


class TestSmokeCliGaps(unittest.TestCase):
    def test_anchor_price_unit_flag(self):
        # --unit appears nowhere in tests/: the display unit is never
        # exercised end to end. JSON must carry it through.
        # --unit 在全套测试里一次没出现过；JSON 里必须原样带出来。
        proc = _run("anchor_price",
                    ["--comp-low", "30", "--comp-high", "40", "--cost", "28",
                     "--unit", "箱", "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["meta"]["unit"], "箱")

    def test_landed_cost_help_example_qty_sell_price(self):
        # Copied from landed_cost --help: --qty 100 --sell-price 48.
        # The documented numbers must come out exactly.
        # 照抄 --help 里的例子；文档里那两个数必须原样算出来。
        proc = _run("landed_cost",
                    ["--fob", "30", "--freight", "5", "--duty", "10",
                     "--port-charges", "2", "--qty", "100",
                     "--sell-price", "48"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("4056.36", proc.stdout)
        self.assertIn("7.44", proc.stdout)

    def test_quote_engine_unit_flag(self):
        # --unit appears nowhere in tests/ for quote_engine either.
        # quote_engine 的 --unit 同样一次没跑过。
        proc = _run("quote_engine",
                    ["--cost", "28", "--freight", "6",
                     "--unit", "箱", "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["meta"]["unit"], "箱")

    def test_market_rules_note_flag_lifts_turkey_cap(self):
        # --note is only tested at function level; the CLI flag itself
        # never runs. With a re-export note the verdict must change.
        # --note 只在函数层测过，CLI 本身一次没跑。给了转口备注，
        # 裁决必须从「先确认转口」变成「已确认转口」。
        without = _run("market_rules", ["--country", "Turkey"])
        with_note = _run("market_rules",
                         ["--country", "Turkey",
                          "--note", "re-export confirmed"])
        self.assertEqual(without.returncode, 0, without.stdout + without.stderr)
        self.assertEqual(with_note.returncode, 0,
                         with_note.stdout + with_note.stderr)
        self.assertIn("先确认转口", without.stdout)
        self.assertIn("已确认转口", with_note.stdout)

    def test_due_diligence_full_flag_cli(self):
        # The dedicated tests call build_report() directly; the CLI
        # flags --website/--years/--customs-record/--import-match/
        # --sanctions/--adverse/--payment never run end to end.
        # 单测直接调 build_report()；这串 CLI flag 一次没端到端跑过。
        proc = _run("due_diligence",
                    ["--company", "【示例】海湾轮胎贸易",
                     "--country", "Saudi Arabia",
                     "--website", "sample.example",
                     "--years", "18",
                     "--customs-record", "yes",
                     "--import-match", "yes",
                     "--sanctions", "clear",
                     "--adverse", "no",
                     "--payment", "prepaid",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["company"], "【示例】海湾轮胎贸易")
        self.assertIn("rating", data)

    def test_fulfillment_balance_received_flag(self):
        # --balance-received is only tested at function level
        # (base_order(balance_received=...)); the CLI flag itself
        # never runs. 9408 must flip the release gate to go.
        # --balance-received 只在函数层测过；9408 必须把放单关口翻成通过。
        proc = _run("fulfillment_checklist",
                    ["--demo", "--balance-received", "9408",
                     "--format", "json"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertTrue(data["gates"]["release"]["go"])
        self.assertEqual(data["summary"]["done"], 8)

    def test_trade_show_add_with_phone_and_whatsapp(self):
        # --phone / --whatsapp are only exercised via the --csv path;
        # the --add CLI flags themselves never run.
        # --phone/--whatsapp 只在 --csv 路径上测过；--add 的这两个
        # flag 本身一次没跑过。
        proc = _run("trade_show",
                    ["--add", "【示例】海湾轮胎贸易",
                     "--country", "Saudi Arabia",
                     "--product", "TBR 12.00R20",
                     "--interest", "高",
                     "--phone", "+000 00 000 0000",
                     "--whatsapp", "+000 00 000 0000"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("WhatsApp +000 00 000 0000", proc.stdout)

    def test_tire_pack_li_speed_flags(self):
        # Copied from tire_pack --help: --li 156/150 --speed L.
        # --speed is only tested at function level (build_tire_pack).
        # 照抄 --help 里的例子；--speed 只在函数层测过。
        proc = _run("tire_pack",
                    ["--size", "315/80R22.5", "--market", "uae",
                     "--li", "156/150", "--speed", "L"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("156/150", proc.stdout)
        self.assertIn("速度级别：L", proc.stdout)

    def test_nudge_channel_whatsapp_help_example(self):
        # Copied from nudge --help: --day D7 --scenario sampled
        # --channel whatsapp. Only WhatsApp copy must come out.
        # 照抄 --help 里的例子；只要 WhatsApp 短版，不许带邮件长版。
        proc = _run("nudge",
                    ["--day", "D7", "--scenario", "sampled",
                     "--channel", "whatsapp"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("WhatsApp", proc.stdout)
        self.assertNotIn("邮件长版", proc.stdout)


if __name__ == "__main__":
    unittest.main()
