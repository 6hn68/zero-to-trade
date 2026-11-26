"""运行状态文件进 .gitignore（第 3 轮第 6 路）。

fulfillment_state.json / fast_path_state.json 是两个脚本 --state 的默认
落点（当前目录），跑一遍就变，属于私人进度，不进仓库。*_state.json 兜底，
以后再有脚本加 --state，默认文件名照这个规矩起就不用再改 .gitignore。

本文件不依赖仓库本身带 .git（副本里跑测试时没有 .git），所以验证在
一个临时 git 仓库里做：把仓库真正的 .gitignore 拷进去，再 git check-ignore。
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
GITIGNORE = REPO_ROOT / ".gitignore"

STATE_FILES = ["fulfillment_state.json", "fast_path_state.json"]
# 兜底规则 *_state.json 应该挡住的名字（任意目录层级、任意前缀）
GENERIC_STATE_FILES = ["my_tool_state.json", "sub/dir/other_state.json"]
# 绝不能被误伤的普通文件
KEEP_FILES = ["keep.json", "state_notes.md", "fulfillment_report.json"]


def _git(*args, cwd):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          cwd=cwd)


class TestGitignoreStateFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if shutil.which("git") is None:
            raise unittest.SkipTest("git 不可用，跳过")
        cls._tmp = tempfile.TemporaryDirectory()
        cls.repo = Path(cls._tmp.name)
        proc = _git("init", "-q", cwd=cls.repo)
        assert proc.returncode == 0, proc.stderr
        shutil.copyfile(GITIGNORE, cls.repo / ".gitignore")

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def _is_ignored(self, relpath):
        proc = _git("check-ignore", "-q", relpath, cwd=self.repo)
        self.assertIn(proc.returncode, (0, 1), proc.stderr)
        return proc.returncode == 0

    def test_known_state_files_are_ignored(self):
        for name in STATE_FILES:
            self.assertTrue(self._is_ignored(name),
                            "%s 应该被 .gitignore 挡住" % name)

    def test_generic_state_pattern_covers_future_names(self):
        for name in GENERIC_STATE_FILES:
            self.assertTrue(self._is_ignored(name),
                            "%s 应该被 *_state.json 兜底挡住" % name)

    def test_pattern_does_not_swallow_ordinary_files(self):
        for name in KEEP_FILES:
            self.assertFalse(self._is_ignored(name),
                             "%s 不该被挡住" % name)

    def test_scripts_actually_write_the_default_state_names(self):
        # 端到端：真跑两个脚本，落出来的默认名文件必须被挡住。
        # 状态文件写在临时仓库里，不脏正本仓库。
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "fulfillment_checklist.py"),
             "--demo", "--done", "pi", "--state", "fulfillment_state.json"],
            capture_output=True, text=True, cwd=self.repo)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "fast_path.py"),
             "--done", "3", "--state", "fast_path_state.json"],
            capture_output=True, text=True, cwd=self.repo)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        for name in STATE_FILES:
            self.assertTrue((self.repo / name).is_file(), "%s 没写出来" % name)
            self.assertTrue(self._is_ignored(name),
                            "%s 写出来了却没被挡住" % name)


if __name__ == "__main__":
    unittest.main()
