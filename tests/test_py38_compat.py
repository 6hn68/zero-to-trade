"""Python 3.8 compatibility: what the CI gate really catches, and what it misses.

Why this file exists / 为什么要有这个文件：
  .github/workflows/ci.yml 里「3.8 语法门禁」那一步只做了一件事：
  ast.parse(src, feature_version=(3, 8))。2026-11-26 实测（往副本里塞
  探针语法，见 ROUTE.md）证明它只拦得住语法层的东西——match 语句；
  PEP 585（list[str]、dict[str, int]）和 PEP 604（int | str、dict | list）
  在 3.8 的文法下都能解析，只在 3.8 上跑起来时才炸（TypeError），
  门禁放它们过去。门禁自己的报错文案还写着「写成 dict[str, int]
  而不是 dict | dict」——这两者在 3.8 上都会炸，文案本身就是错的。
  3.8 上正确的写法是 typing.Dict / typing.List / typing.Union /
  typing.Optional。
  这个文件把门禁漏掉的三类补上：PEP 585 内置泛型、PEP 604 联合类型、
  3.9 才有的运行时 API（str.removeprefix / removesuffix）。每条规则
  都有反向探针测试：只会通过、永远拦不住坏代码的检查等于没有检查。

Rules / 规则：
  * No network, no third-party packages: ast + stdlib unittest only.
    不联网、不引第三方包：只用 ast + 标准库 unittest。
  * The checks run on the real files under scripts/*.py, not on copies.
    查的是 scripts/*.py 的真文件，不是复制品。
  * A bare `|` between two sets (set(a) | set(b)) is legal 3.8 and
    must NOT trip the union check; only type-shaped operands count.
    集合求并集的 `|` 是合法 3.8 写法，不许误报；只有类型样子的两边
    才算联合类型。
"""

import ast
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = sorted((REPO_ROOT / "scripts").glob("*.py"))

BUILTIN_GENERICS = {"list", "dict", "set", "frozenset", "tuple", "type"}
# Runtime APIs that only exist from 3.9 on: syntax is fine on 3.8,
# the AttributeError only fires when the line actually runs.
# 3.9 才有的运行时 API：语法上 3.8 能过，跑起来才炸。
PY39_RUNTIME_APIS = {"removeprefix", "removesuffix"}


def _is_type_expr(node):
    """True if this AST node looks like a type expression (a bare
    builtin generic, a Capitalized class name, or a subscript of one).
    判断一个 AST 节点像不像类型表达式。"""
    if isinstance(node, ast.Name):
        return node.id in BUILTIN_GENERICS or node.id[:1].isupper()
    if isinstance(node, ast.Subscript):
        return _is_type_expr(node.value)
    if isinstance(node, ast.Constant):
        return node.value is None
    return False


def check_source(src, filename="<string>"):
    """Return a list of 3.8-incompatible constructs found in src.
    Empty list means the source is clean under these rules.
    返回 src 里所有 3.8 不兼容的写法；空列表表示干净。"""
    problems = []
    try:
        tree = ast.parse(src, feature_version=(3, 8))
    except SyntaxError as e:
        problems.append("%s: 3.8 语法不认：%s" % (filename, e))
        return problems
    for node in ast.walk(tree):
        if (isinstance(node, ast.Subscript)
                and isinstance(node.value, ast.Name)
                and node.value.id in BUILTIN_GENERICS):
            problems.append("%s:%d: PEP 585 内置泛型 %s[...] 在 3.8 上跑起来会炸，"
                            "请写 typing.%s" % (filename, node.lineno,
                                               node.value.id,
                                               node.value.id.capitalize()))
        if isinstance(node, ast.Attribute) and node.attr in PY39_RUNTIME_APIS:
            problems.append("%s:%d: .%s 是 3.9 才有的 API，3.8 上跑起来会炸"
                            % (filename, node.lineno, node.attr))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            if _is_type_expr(node.left) and _is_type_expr(node.right):
                problems.append("%s:%d: PEP 604 联合类型 X | Y 在 3.8 上跑起来会炸，"
                                "请写 typing.Union / typing.Optional"
                                % (filename, node.lineno))
    # Unions inside annotations are type context by definition, whatever
    # the operands look like: Optional[int] | None, "A" | "B", anything.
    # 注解里的 `|` 一律是类型语境，不管两边长什么样都算。
    for node in ast.walk(tree):
        annotations = []
        if isinstance(node, ast.AnnAssign) and node.annotation is not None:
            annotations.append(node.annotation)
        if isinstance(node, ast.arg) and node.annotation is not None:
            annotations.append(node.annotation)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                and node.returns is not None:
            annotations.append(node.returns)
        for ann in annotations:
            for sub in ast.walk(ann):
                if isinstance(sub, ast.BinOp) and isinstance(sub.op, ast.BitOr):
                    problems.append("%s:%d: 注解里的 X | Y 是 PEP 604，"
                                    "3.8 上跑起来会炸，请写 typing.Union / "
                                    "typing.Optional" % (filename, node.lineno))
                    break
    return problems


class TestPy38Compat(unittest.TestCase):
    def test_gate_parse_all_scripts_feature_version_38(self):
        # Same check as the CI gate step, pinned in the suite so a
        # future edit to ci.yml cannot silently drop it.
        # 跟 CI 门禁同一条检查，钉进测试套件，免得以后改 ci.yml 时
        # 悄悄把它弄丢。
        bad = []
        for path in SCRIPTS:
            src = path.read_text(encoding="utf-8")
            try:
                ast.parse(src, feature_version=(3, 8))
            except SyntaxError as e:
                bad.append("%s -> %s" % (path.name, e))
        self.assertEqual(bad, [])

    def test_no_pep585_builtin_generics(self):
        bad = []
        for path in SCRIPTS:
            bad.extend(p for p in check_source(path.read_text(encoding="utf-8"),
                                               path.name)
                       if "PEP 585" in p)
        self.assertEqual(bad, [])

    def test_no_pep604_unions(self):
        bad = []
        for path in SCRIPTS:
            bad.extend(p for p in check_source(path.read_text(encoding="utf-8"),
                                               path.name)
                       if "PEP 604" in p)
        self.assertEqual(bad, [])

    def test_no_py39_runtime_apis(self):
        bad = []
        for path in SCRIPTS:
            bad.extend(p for p in check_source(path.read_text(encoding="utf-8"),
                                               path.name)
                       if "3.9 才有" in p)
        self.assertEqual(bad, [])

    def test_all_scripts_clean_under_all_rules(self):
        bad = []
        for path in SCRIPTS:
            bad.extend(check_source(path.read_text(encoding="utf-8"),
                                    path.name))
        self.assertEqual(bad, [])


class TestPy38DetectorTripsOnProbes(unittest.TestCase):
    """Negative controls: each rule must actually fire on a bad snippet.
    A check that never fires is no check at all.
    反向探针：每条规则必须真能拦住坏代码，否则等于没有检查。"""

    def test_detector_catches_pep585_annotation(self):
        bad = check_source("x_probe: list[str] = []\n")
        self.assertTrue(any("PEP 585" in p for p in bad), bad)

    def test_detector_catches_pep585_function_annotation(self):
        bad = check_source("def f(a: dict[str, int]):\n    return a\n")
        self.assertTrue(any("PEP 585" in p for p in bad), bad)

    def test_detector_catches_match_statement(self):
        bad = check_source("match 1:\n    case 1:\n        pass\n")
        self.assertTrue(bad, "match 语句必须被 3.8 解析器拦住")

    def test_detector_catches_pep604_annotation(self):
        bad = check_source("y_probe: int | str = 1\n")
        self.assertTrue(any("PEP 604" in p for p in bad), bad)

    def test_detector_catches_pep604_expression(self):
        bad = check_source("z_probe = dict | list\n")
        self.assertTrue(any("PEP 604" in p for p in bad), bad)

    def test_detector_catches_py39_runtime_api(self):
        bad = check_source('v_probe = "abc".removeprefix("a")\n')
        self.assertTrue(any("3.9 才有" in p for p in bad), bad)

    def test_detector_leaves_legal_38_alone(self):
        # walrus (3.8) and f-string = (3.8) must NOT trip anything.
        # 3.8 合法的海象运算符和 f-string = 不许误报。
        self.assertEqual(check_source("if (n := 3) > 2:\n    pass\n"), [])
        self.assertEqual(check_source('u = f"{1 + 1=}"\n'), [])

    def test_detector_leaves_set_union_alone(self):
        # set(a) | set(b) is a plain 3.8 set union, not a type union.
        # 集合求并集是正经 3.8 写法，不许误报（check_private_data.py
        # 第 415 行就是这种写法）。
        self.assertEqual(check_source("files = sorted(set(a) | set(b))\n"), [])


if __name__ == "__main__":
    unittest.main()
