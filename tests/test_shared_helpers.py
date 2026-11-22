"""共用函数只留一份（第 9 轮钉死）。

_ZhArgumentParser / setup_log / _width / _pad / money / fmt /
_clean / _is_filled 的唯一一份在 lead_score.py，各脚本从那里 import；
due_diligence.py 的 parser 是特制的（报错里带本脚本例子），故意不抽。
"""
import importlib
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS))
import lead_score as ls  # noqa: E402

SHARED_PARSER = ["anchor_price", "fast_path", "followup_plan", "landed_cost",
                 "nudge", "outreach_gen", "quote_engine", "tire_pack",
                 "trade_show"]


def _mod(name):
    return importlib.import_module(name)


class TestSharedHelpers(unittest.TestCase):
    def test_parser_is_shared(self):
        for name in SHARED_PARSER:
            self.assertIs(_mod(name)._ZhArgumentParser, ls._ZhArgumentParser,
                          f"{name} 还在用自己的 _ZhArgumentParser")

    def test_due_diligence_parser_stays_custom(self):
        self.assertIsNot(_mod("due_diligence")._ZhArgumentParser,
                         ls._ZhArgumentParser)

    def test_setup_log_is_shared(self):
        self.assertIs(_mod("outreach_gen").setup_log, ls.setup_log)
        self.assertIs(_mod("followup_plan").setup_log, ls.setup_log)

    def test_money_helpers_are_shared(self):
        # anchor_price 的 _width/_pad 是死代码，第 9 轮直接删了，不 import
        for name in ["landed_cost", "quote_engine"]:
            mod = _mod(name)
            self.assertIs(mod.money, ls.money, name)
            self.assertIs(mod.fmt, ls.fmt, name)
            self.assertIs(mod._width, ls._width, name)
            self.assertIs(mod._pad, ls._pad, name)
        mod = _mod("anchor_price")
        self.assertIs(mod.money, ls.money)
        self.assertIs(mod.fmt, ls.fmt)
        self.assertFalse(hasattr(mod, "_width"))
        self.assertFalse(hasattr(mod, "_pad"))

    def test_clean_helpers_are_shared(self):
        mod = _mod("trade_show")
        self.assertIs(mod._clean, ls._clean)
        self.assertIs(mod._is_filled, ls._is_filled)

    def test_bad_flag_hint_is_uniform(self):
        for name in SHARED_PARSER + ["lead_score"]:
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / (name + ".py")), "--nope"],
                capture_output=True, text=True, cwd=REPO_ROOT)
            out = proc.stdout + proc.stderr
            # error() 抛的是 SystemExit("…")，退出码一直是 1（字符串即 1）；
            # 无参那条路才是显式 SystemExit(2)，两者别混。
            self.assertEqual(proc.returncode, 1, name)
            self.assertIn("参数没写对", out, name)
            self.assertIn("python scripts/%s.py --help" % name, out, name)

    def test_due_diligence_bad_flag_keeps_own_hint(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "due_diligence.py"), "--nope"],
            capture_output=True, text=True, cwd=REPO_ROOT)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("due_diligence.py --help", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
