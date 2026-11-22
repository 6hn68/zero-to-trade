"""trace-*.jsonl 落地（第 8 轮钉死，字段见 docs/trace-format.md）。

每次运行（成功或报错）都在 logs/trace-YYYY-MM-DD.jsonl 追加一行，
字段：trace_id / ts / tool / input / output / duration_s / error。
测试跑完把当天文件截回原样，不留残留行。
"""
import json
import subprocess
import sys
import tempfile
import unittest
import uuid
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
TRACE_FILE = (REPO_ROOT / "logs"
              / ("trace-%s.jsonl" % datetime.now().strftime("%Y-%m-%d")))


def _read_lines():
    if not TRACE_FILE.exists():
        return []
    return TRACE_FILE.read_text(encoding="utf-8").splitlines()


def _run(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args],
                          capture_output=True, text=True, cwd=REPO_ROOT)


class TestTraceLog(unittest.TestCase):
    def setUp(self):
        self._before = TRACE_FILE.read_bytes() if TRACE_FILE.exists() else None

    def tearDown(self):
        # 截回跑之前的样子：测试不留残留行
        if self._before is None:
            if TRACE_FILE.exists():
                TRACE_FILE.unlink()
        else:
            TRACE_FILE.write_bytes(self._before)

    def _new_records(self):
        before = self._before.decode("utf-8").splitlines() if self._before else []
        return [json.loads(line) for line in _read_lines()[len(before):]]

    def _check_shape(self, rec, tool):
        self.assertEqual(rec["tool"], tool)
        uuid.UUID(rec["trace_id"])  # 不是合法 uuid 就抛
        datetime.fromisoformat(rec["ts"])  # 不是 ISO 时间就抛
        self.assertIsInstance(rec["duration_s"], (int, float))
        self.assertGreaterEqual(rec["duration_s"], 0)
        self.assertIn("input", rec)
        self.assertIn("output", rec)
        self.assertIn("error", rec)

    def test_lead_score_success_writes_trace(self):
        proc = _run("lead_score.py", "examples/leads_example.csv")
        self.assertEqual(proc.returncode, 0)
        recs = self._new_records()
        self.assertEqual(len(recs), 1)
        self._check_shape(recs[0], "lead_score.py")
        self.assertEqual(recs[0]["input"], "leads_example.csv")
        self.assertIn("T0:", recs[0]["output"])
        self.assertEqual(recs[0]["error"], "")

    def test_lead_score_error_run_writes_trace_with_error(self):
        with tempfile.NamedTemporaryFile(
                "w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
            tmp.write("")
            path = tmp.name
        try:
            proc = _run("lead_score.py", path)
            self.assertNotEqual(proc.returncode, 0)
            recs = self._new_records()
            self.assertEqual(len(recs), 1)
            self._check_shape(recs[0], "lead_score.py")
            self.assertIn("空的", recs[0]["error"])
        finally:
            Path(path).unlink(missing_ok=True)

    def test_outreach_and_followup_write_trace(self):
        proc = _run("outreach_gen.py", "--company", "Acme Ltd",
                    "--country", "Nigeria", "--product", "tyres", "--tier", "T1")
        self.assertEqual(proc.returncode, 0)
        proc = _run("followup_plan.py", "--tier", "T0",
                    "--start", "2026-10-08", "--market", "gcc")
        self.assertEqual(proc.returncode, 0)
        recs = self._new_records()
        self.assertEqual(len(recs), 2)
        self._check_shape(recs[0], "outreach_gen.py")
        self._check_shape(recs[1], "followup_plan.py")
        self.assertEqual(recs[0]["input"], "单条模式（--company）")
        self.assertIn("份草稿", recs[0]["output"])
        self.assertIn("tier=T0", recs[1]["input"])
        # 公司名不进 trace：单家模式也只记“单家”二字
        self.assertNotIn("Acme", recs[0]["input"] + recs[0]["output"])

    def test_trace_file_is_gitignored(self):
        proc = subprocess.run(["git", "check-ignore", "-q", str(TRACE_FILE)],
                              capture_output=True, cwd=REPO_ROOT)
        self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
