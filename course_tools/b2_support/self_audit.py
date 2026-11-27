"""Self-audit for the B2 support toolkit only.

Scans the B2 support directory for:
  - required modules and required self-check files,
  - imports of project/business modules or other members' support packages,
  - third-party imports outside the Python standard library.

It never inspects other members' code or the plugin runtime.
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


REQUIRED_MODULES = (
    "case_models",
    "deterministic",
    "string_case_generator",
    "path_case_generator",
    "json_case_generator",
    "corpus_writer",
    "result_models",
    "result_aggregator",
    "summary_stats",
    "report_renderer",
    "cli",
    "artifact_manifest",
    "corpus_diff",
    "self_audit",
)

REQUIRED_CHECKS = (
    "check_deterministic",
    "check_string_case_generator",
    "check_path_case_generator",
    "check_json_case_generator",
    "check_corpus_writer",
    "check_result_aggregator",
    "check_summary_stats",
    "check_report_renderer",
    "check_cli",
    "check_artifact_manifest",
    "check_corpus_diff",
    "check_self_audit",
)

FORBIDDEN_TOPS = (
    "main",
    "skills",
    "tests",
    "tools",
    "course_evidence",
)

STDLIB_NAMES: Set[str] = set(getattr(sys, "stdlib_module_names", ()))


def _imported_modules(tree: ast.AST) -> List[Tuple[str, int]]:
    """Return (module, line) pairs for absolute imports in a parsed file."""
    names: List[Tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append((alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                # Relative import stays inside the support package.
                continue
            if node.module:
                names.append((node.module, node.lineno))
    return names


def audit(root=None) -> Dict[str, object]:
    """Audit the B2 support toolkit rooted at `root` (defaults to this dir)."""
    support_root = Path(root) if root is not None else Path(__file__).resolve().parent
    checks_root = support_root / "checks"

    modules = sorted(path.stem for path in support_root.glob("*.py"))
    checks = (
        sorted(path.stem for path in checks_root.glob("check_*.py"))
        if checks_root.exists()
        else []
    )

    missing_modules = [
        name
        for name in REQUIRED_MODULES
        if not (support_root / f"{name}.py").exists()
    ]
    missing_checks = [
        name
        for name in REQUIRED_CHECKS
        if not (checks_root / f"{name}.py").exists()
    ]

    known_internal = set(modules) | set(checks)
    forbidden: List[Dict[str, object]] = []
    third_party: List[Dict[str, object]] = []
    errors: List[Dict[str, object]] = []

    py_files = sorted(support_root.glob("*.py"))
    if checks_root.exists():
        py_files += sorted(checks_root.glob("*.py"))

    for path in py_files:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as exc:
            errors.append({"file": path.name, "error": str(exc)})
            continue

        for module, lineno in _imported_modules(tree):
            top = module.split(".")[0]
            if top in known_internal:
                continue
            if module == "course_tools.b2_support" or module.startswith(
                "course_tools.b2_support."
            ):
                continue
            if top in FORBIDDEN_TOPS or module.startswith("course_tools."):
                forbidden.append(
                    {"file": path.name, "line": lineno, "module": module}
                )
                continue
            if top in STDLIB_NAMES:
                continue
            third_party.append(
                {"file": path.name, "line": lineno, "module": module}
            )

    ok = not (
        missing_modules or missing_checks or forbidden or third_party or errors
    )

    return {
        "ok": ok,
        "root": str(support_root),
        "modules": modules,
        "checks": checks,
        "missing_modules": missing_modules,
        "missing_checks": missing_checks,
        "forbidden_imports": forbidden,
        "third_party_imports": third_party,
        "errors": errors,
    }
