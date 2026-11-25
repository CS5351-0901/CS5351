# Week 6 — B1 Requirement Boundary Improvement

## Baseline and engineering change

The B1 branch was fast-forwarded to the integrated course baseline `fc2e7052d2676a3a0cea65c318563bb75d6bb90c` before this work. Sprint 1 PR #3 is merged. Upstream changes to `main.py` were outside B1's owned methods.

`_extract_requirement` now requires a command token boundary and accepts either `/agent` or a nonempty direct `@mention/agent` form. It rejects command-like path fragments, embedded email fragments, and an empty mention while retaining prose-prefixed commands, case-insensitive triggers, and multiline bodies. `_assess_project` trims outer whitespace before classification and character-count sizing, so padding does not move a 29-character request into the medium size band. Signatures, output keys, classification precedence, and blacklist behavior are unchanged.

Three new regression tests extend the existing seven-test suite. They cover invalid command fragments, valid command boundaries with multiline text, and outer-whitespace normalization. Before the source fix, the suite reported four failures across the invalid-fragment and size-normalization cases; after the fix, all ten tests passed.

## Validation performed

- `python3 -B -m unittest discover -s tests/roles/b1 -v` — PASS, 10 tests.
- `python3 -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS.
- `git -c core.whitespace=cr-at-eol diff --check` — PASS; the rule accommodates the existing CRLF source format.
- The repository ownership checker was run against the original Week 6 change set — PASS; only `_extract_requirement` and `_assess_project` changed in shared source.

## Scope and limitations

The original task changes only B1-owned method bodies, B1 tests, and this evidence file. Tests load the actual plugin helper code with minimal AstrBot import stubs; live initialization and event dispatch remain unverified. Keyword substring classification is unchanged and remains a later regression area.

The independent Week 6 support extension follows in its own local commit after this task passes validation. Remote push is deferred for user review.
