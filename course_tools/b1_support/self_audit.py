"""Static policy checks for B1 support without importing inspected modules."""

import ast
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath


REQUIRED_MODULES = (
    "models", "path_rules", "file_inventory", "text_metrics", "source_stats",
    "manifest_builder", "report_writer", "cli", "snapshot_compare",
    "duplicate_finder", "health_report", "self_audit",
)
OWN_PACKAGE = "course_tools.b1_support"
NETWORK_MODULES = frozenset({
    "socket", "_socket", "ssl", "_ssl", "http", "urllib", "urllib2", "ftplib",
    "smtplib", "imaplib", "poplib", "telnetlib", "xmlrpc", "nntplib",
})
MUTATING_CALLS = frozenset({
    "write_text", "write_bytes", "touch", "mkdir", "makedirs", "unlink",
    "remove", "rmdir", "rmtree", "rename", "replace", "chmod", "chown",
    "symlink_to", "hardlink_to", "symlink", "link", "putenv", "unsetenv",
    "chdir", "truncate",
})


def _imports(node, package: str):
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom):
        if node.level == 0:
            return [node.module or ""]
        if node.level != 1:
            return [""]
        if node.module:
            return [f"{package}.{node.module}"]
        return [f"{package}.{alias.name}" for alias in node.names]
    return []


def _absolute_literal(value) -> bool:
    if not isinstance(value, str) or value in ("/", "\\"):
        return False  # Separator tokens are used by path normalization.
    return PurePosixPath(value).is_absolute() or PureWindowsPath(value).is_absolute()


def _may_write(call: ast.Call) -> bool:
    target = call.func
    if isinstance(target, ast.Name):
        name = target.id
    elif isinstance(target, ast.Attribute):
        name = target.attr
    else:
        return False
    if name in MUTATING_CALLS:
        # str.replace also occurs in report escaping and path normalization.
        if name == "replace" and len(call.args) == 2 and all(
            isinstance(arg, ast.Constant) and isinstance(arg.value, str)
            for arg in call.args
        ):
            return not isinstance(target, ast.Attribute) or ast.unparse(target.value) == "os"
        return True
    if name != "open":
        return False
    if isinstance(target, ast.Attribute) and ast.unparse(target.value) == "os":
        return True  # Low-level open accepts flags rather than a mode string.
    mode_index = 1 if isinstance(target, ast.Name) or ast.unparse(target.value) in {
        "io", "builtins",
    } else 0
    mode = next((kw.value for kw in call.keywords if kw.arg == "mode"),
                call.args[mode_index] if len(call.args) > mode_index else None)
    return mode is not None and not (
        isinstance(mode, ast.Constant) and mode.value in ("r", "rb", "rt")
    )


def _changes_environment(node: ast.AST) -> bool:
    if isinstance(node, (ast.Subscript, ast.Attribute)) and isinstance(
        node.ctx, (ast.Store, ast.Del)
    ):
        return ast.unparse(node).startswith(("os.environ", "environ"))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        return ast.unparse(node.func.value) in ("os.environ", "environ") and (
            node.func.attr in {"clear", "pop", "popitem", "setdefault", "update"}
        )
    return False


def _inspect(source: str, path: str, own_modules: set[str]) -> list[dict]:
    def issue(code, line):
        return {"path": path, "line": line, "code": code}

    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as exc:
        return [issue("syntax_error", exc.lineno)]

    checks_fixture = path.startswith("checks/")
    package = OWN_PACKAGE + (".checks" if checks_fixture else "")
    allowed_writes = set()
    if path == "report_writer.py":
        # The existing report writer validates its destination before these
        # two operations. Its explicit output behavior has separate checks.
        for function in tree.body:
            if isinstance(function, ast.FunctionDef) and function.name == "write_report":
                for node in ast.walk(function):
                    if isinstance(node, ast.Call) and ast.unparse(node.func) in {
                        "target.parent.mkdir", "target.open",
                    }:
                        allowed_writes.add(node)
    violations = []
    for node in ast.walk(tree):
        for name in _imports(node, package):
            root = name.partition(".")[0]
            if root in NETWORK_MODULES:
                violations.append(issue("network_import", node.lineno))
            elif name not in own_modules and root not in sys.stdlib_module_names:
                violations.append(issue("outside_support_import", node.lineno))
            elif root == "subprocess" and not checks_fixture:
                violations.append(issue("external_process_import", node.lineno))
        if isinstance(node, ast.Call) and ast.unparse(node.func) in {
            "__import__", "builtins.__import__", "importlib.import_module", "import_module",
        }:
            violations.append(issue("dynamic_import", node.lineno))
        # Explicit checks contain synthetic absolute paths and fixture writes.
        if checks_fixture:
            continue
        if isinstance(node, ast.Constant) and _absolute_literal(node.value):
            violations.append(issue("absolute_path_literal", node.lineno))
        if _changes_environment(node) or (
            isinstance(node, ast.Call) and _may_write(node) and node not in allowed_writes
        ):
            violations.append(issue("runtime_mutation", node.lineno))
    return violations


def _audit_tree(root: Path) -> dict:
    issues = []
    sources = {}
    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root).as_posix()
        if any(part.is_symlink() for part in (path, *path.parents) if part.is_relative_to(root)):
            issues.append({"path": relative, "line": None, "code": "symlink_source"})
        elif path.is_file():
            sources[relative] = path
    for module in REQUIRED_MODULES:
        relative = f"{module}.py"
        if relative not in sources:
            issues.append({"path": relative, "line": None, "code": "missing_module"})
    own_modules = {OWN_PACKAGE} | {
        f"{OWN_PACKAGE}.{path[:-3].replace('/', '.')}" for path in sources
    }
    for relative, path in sources.items():
        try:
            source = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            issues.append({"path": relative, "line": None, "code": "unreadable_source"})
            continue
        issues.extend(_inspect(source, relative, own_modules))
    issues.sort(key=lambda issue: (issue["path"], issue["line"] or 0, issue["code"]))
    return {"passed": not issues, "files_checked": len(sources), "issues": issues}


def audit_support() -> dict:
    """Audit the installed B1 support tree for concrete static policy signals."""
    return _audit_tree(Path(__file__).resolve().parent)
