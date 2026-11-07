# B2 Week 9 — Support Toolkit Sprint 2 Check

This record documents the additive, isolated `course_tools/b2_support` toolkit
built during Sprint 2 (Weeks 6–8). It does not alter the original Sprint 2
business conclusions.

## Support module list

```text
course_tools/b2_support/
├── __init__.py
├── case_models.py
├── deterministic.py
├── string_case_generator.py
├── path_case_generator.py
├── json_case_generator.py
├── corpus_writer.py
├── result_models.py
├── result_aggregator.py
├── summary_stats.py
├── report_renderer.py
└── cli.py
```
Self-checks under `course_tools/b2_support/checks/` (all `check_*.py`):
`check_deterministic`, `check_string_case_generator`,
`check_path_case_generator`, `check_json_case_generator`, `check_corpus_writer`,
`check_result_aggregator`, `check_summary_stats`, `check_report_renderer`,
`check_cli`.

## Generator types

- string case generator (empty/whitespace/Unicode/emoji/long/newline/tab)
- path case generator (POSIX/Windows/relative/Unicode path strings only)
- JSON case generator (dict/list/nested/empty/numeric/boolean/null/Unicode +
  controllable malformed JSON raw text)
- corpus writer (JSON / JSONL / text)

## Generic result schema (B2-owned)

`ResultRecord(case_id, status, category, duration_ms, message, metadata)`,
where `status ∈ {pass, fail, error, skip}`. B2 does not read or import any other
member's result format.

## Support checks count

```text
python -m unittest discover -s course_tools/b2_support/checks -p "check_*.py"
→ Ran 51 tests ... OK
```

`python course_tools/b2_support/cli.py --help` → exit 0.

## Isolation results

```text
PROJECT_LOCAL_IMPORTS=NONE
THIRD_PARTY_DEPENDENCIES_ADDED=NONE
```

Verification basis: every import inside `course_tools/b2_support` is either a
Python standard-library module or another `b2_support` module. No import of
`main`, `skills.*`, `course_tools.b1_support`, or any A/C/D/other-member module.
`pyproject.toml` is unchanged in the Sprint 2 diff.

## Support commit changed paths

All support commits in Sprint 2 touched only `course_tools/b2_support/**`:

- Week 6 support commit: `course_tools/b2_support/` (case_models, deterministic,
  string/path generators, checks) — 9 files.
- Week 7 support commit: `course_tools/b2_support/{json_case_generator,
  corpus_writer}.py` + 2 checks — 4 files.
- Week 8 support commit: `course_tools/b2_support/{result_models,
  result_aggregator, summary_stats, report_renderer, cli}.py` + 4 checks —
  9 files.

Each was verified with `git show --name-only --format="" HEAD`; no path outside
`course_tools/b2_support/**` or `course_evidence/B2/**` appeared.
