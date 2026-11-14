# Week 10 — B1 Project Classification Boundaries

Sprint 2 PR #23 was confirmed merged at `a12ca9f`. Before editing, `course/b1` was fast-forwarded to `origin/main` at `37f3055`, which also contains the remote B1 branch head.

The second improvement round fixes substring false positives in `_assess_project`. For example, `unit tests` no longer selects TypeScript and `capital costs` no longer selects API. English aliases now match whole ASCII identifier tokens. Punctuation and Chinese text may border an alias, so `Node.js`, `TS-node`, `实现JavaScript解析器`, and `REST APIs` remain recognized. Chinese keyword rules, classification precedence, trimming, size thresholds, and return keys remain unchanged.

Three regression methods cover false matches, supported aliases and precedence. Before the fix, five subcases failed in the 17-test suite. After the fix:

- `python3 -B -m unittest discover -s tests/roles/b1 -v` — PASS, 17 tests.
- `python3 -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS.
- `git -c core.whitespace=cr-at-eol diff --check` — PASS.

Only the B1-owned assessment method, its role tests and this evidence belong to the original commit. This is heuristic classification, not intent inference; conflicting keyword categories still follow the existing precedence. Tests use AstrBot import stubs and do not establish live adapter behavior. The independent support extension follows after this commit.
