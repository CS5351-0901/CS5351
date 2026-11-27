# Week 12 — B1 Presentation and Report Notes

## Role and engineering contributions

B1 owns requirement extraction, user/group blacklist checks, and project assessment in `main.py`. The role suite in `tests/roles/b1/test_role_baseline.py` exercises all three helpers.

- Weeks 5–6 fixed multiline truncation, blank requests, and false command matches inside paths or email-like text. Project assessment now trims outer whitespace before classification and size calculation.
- Weeks 7–9 added regressions for CRLF, Unicode size thresholds, multiline keywords, and numeric group IDs. The Sprint 2 changes were integrated in PR #23.
- Weeks 10–11 switched English classification aliases to whole ASCII tokens and simplified the matching logic. `unit tests` and `capital costs` now fall back to Python, while `TypeScript 5` and `实现JavaScript解析器` still select their language categories. The tests also cover blank direct assessments and aliases adjoining digits. Blacklist behavior was verified through regressions.
- The independent B1 support toolkit grew from file inventory and text/source metrics into deterministic manifests, a report CLI, snapshot comparison, and duplicate grouping. Week 11 added a read-only inventory summary and a static self-audit. These utilities run independently of the AstrBot plugin.

## Demonstration outline

1. Show the requirement extraction test for a multiline `/agent` request and the test that rejects command-like fragments. Explain how the tokenizer preserves valid commands, including direct mentions.
2. Show the classifier regression for `unit tests` and compare it with the positive case `TypeScript 5`. Explain that the classifier matches complete tokens and retains category precedence and the 30/100-character size thresholds.
3. Run the support CLI's `stats` subcommand on a small fixture with one Python function and one JSON top-level key. Use an explicit new output file in a temporary directory. The JSON report shows both counts and relative paths. Then show that `audit_support()` reviews the support source without importing the audited modules.

## Week 12 validation

Validation ran on the Week 11 branch tip `8836521` while preparing these notes.

- `python3 -B -m unittest discover -s tests/roles/b1 -v` passed all 19 tests.
- `python3 -B -m unittest discover -s course_tools/b1_support/checks -p 'check_*.py'` passed all 77 checks.
- `python3 -B course_tools/b1_support/cli.py --help` completed successfully. The direct `stats` smoke test returned two fixture entries with the expected Python function count and JSON top-level key count. The temporary report was cleaned up with the fixture.
- `audit_support()` passed on 22 Python files. `build_health_report("course_tools/b1_support")` counted the same 22 files and reported zero inventory issues.

## Remaining limits

The role tests use AstrBot import stubs. Live adapter startup, event dispatch, and end-to-end request delivery remain unverified. Classification follows fixed keywords and category precedence, which can miss intent in ambiguous or multilingual requests. Duplicate groups rely on the recorded hash and size, so a changed file requires a fresh manifest. The support self-audit detects recognizable static patterns and cannot establish all runtime behavior.

## Contributions for slides and the final report

**Slide takeaway.** B1 made command parsing and project classification more predictable through boundary fixes and 19 role regressions. An independent repository toolkit adds reproducible inventory and comparison reports, backed by 77 support checks.

**Final report wording.** B1 improved requirement extraction by preserving multiline requests and rejecting invalid command fragments. Whole-token matching reduced false project classifications while preserving category precedence and size thresholds. The team can inspect file metadata, source metrics, snapshots, and duplicate groups with the independent B1 toolkit. Week 12 validation passed all 19 role tests and 77 support checks in the local test environment.
