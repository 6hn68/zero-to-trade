"""提示词与脚本实际行为对齐（第 7 轮钉死）。

钉死两处过期说法：
- P04-4 的跟进命令须带 --avoid-weekend：周五主麻日避让是可选项，
  不加这个开关，触达照样落在周末（只给一句“建议顺延”）。
- P10-2 的跟进窗口统一 48 小时：标题写 48，正文原写 24，两处打架。
"""
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS = REPO_ROOT / "prompts" / "AI_PROMPTS.md"


def _section(text, start_marker, end_marker):
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[start:end]


class TestPromptsAlignment(unittest.TestCase):
    def setUp(self):
        self.text = PROMPTS.read_text(encoding="utf-8")

    def test_p04_4_followup_command_avoids_weekend(self):
        section = _section(self.text, "### P04-4", "## 05 ")
        self.assertIn("--avoid-weekend", section)

    def test_p10_2_window_is_48_hours_everywhere(self):
        section = _section(self.text, "### P10-2", "## 11 ")
        self.assertIn("48 小时", section)
        self.assertIn("within 48 hours", section)
        self.assertNotIn("24 小时", section)
        self.assertNotIn("within 24 hours", section)


if __name__ == "__main__":
    unittest.main()
