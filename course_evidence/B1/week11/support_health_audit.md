# Week 11 — B1 Support Health Report and Self-Audit

The original role regression was validated and committed first as `7b67f14`. The working tree and `git diff --name-only HEAD` were empty immediately after that commit. This separate support change adds two modules, their opt-in checks and this evidence.

- `build_health_report(directory, include=(), exclude=())` returns read-only file counts, byte totals, per-extension counts and bytes, and inventory issue counts. It reuses the Week 6 inventory, skips Git metadata and Python bytecode caches, and reads file metadata. It produces no grades or role-specific findings.
- `audit_support()` reads Python files from B1 support only. It checks required modules, syntax, static imports, common network and dynamic import entry points, absolute path literals, and common filesystem or environment mutations. Results contain relative paths and line numbers. Explicit check fixtures can use synthetic paths and writes. The existing report writer's two output operations are recognized and separately tested against its destination policy.

```python
from course_tools.b1_support.health_report import build_health_report
from course_tools.b1_support.self_audit import audit_support

summary = build_health_report("course_tools/b1_support")
audit = audit_support()
```

## Executed checks

- `python3 -B -m unittest discover -s course_tools/b1_support/checks -p "check_*.py"` — PASS, 77 checks (72 existing and five new), no skips.
- Direct invocation on the B1 support tree — PASS. The report counted 22 Python files and no inventory issues. The audit checked 22 Python files and returned no violations.
- `python3 -B -m unittest discover -s tests/roles/b1` — PASS, 19 tests after support development.
- CLI help and compilation of the two support modules and their check file — PASS.

The audit is a static check for recognizable patterns and does not execute inspected code or prove the absence of all runtime behavior. The support commit is scoped to B1 support and B1 evidence. It creates no Week 12 artifacts.
