# Week 6 — Accurate delivery file counts

Date: 2026-10-25
BRANCH: course/c2
REVIEWED_MAIN: 6b0472c36ffd09c6bfe6e647380cd0d0799ea076

## Change and reason

The packager reported `len(source files) + len(test files) + 2`, rather than the number of files actually delivered. A Python project with one source file and no tests reported 3, but its ZIP contained 5 files, including generated package initializers. The mismatch also affected generated requirements, extra files, overwritten paths and Node install artifacts. The main workflow displays this field in its delivery report.

`skills/CodeAgent/scripts/codeagent_packager.py` now records the number of entries in the ZIP after all file writes, and returns that count on success. The archive loop writes only files, so generated files are included, cleaned cache files are excluded, and overwritten input paths are counted once. Error handling and the failure result's initial zero count remain unchanged.

`tests/roles/c2/test_baseline.py` adds four regression cases and extends the three existing successful Python archive tests to compare the reported count with the reopened ZIP. The new cases verify:

- Generated requirements are present and counted.
- Extra NOTICE content is counted while coverage.json and pyc files removed by cleanup are absent.
- Duplicate source paths and an overwritten README are counted once, retaining the final content.
- Simulated Node installation adds a lockfile and dependency file; both are included in the actual ZIP count.

## Actual validation

Runtime: Python 3.12.14 on Windows. Command from the repository root:

```text
python -B -m unittest discover -s tests/roles/c2 -p 'test_*.py' -v
```

The available bundled interpreter was used, with TEMP and TMP pointing to writable scratch storage outside the repository.

Before the production fix: **16 tests, 9 passed and 7 failed**, all seven failures due to mismatched file counts. After the fix: **16 tests passed, exit 0**, no skips or expected failures. Existing wrapper argument/error tests, dependency checks and staging cleanup tests also passed.

RUNTIME_TEST: PASS (16/16 scoped tests)

ZIP generation, reopening, CRC checking, member-set checks, file content checks and cleanup use real filesystem/archive operations. The existing fixture redirects the hard-coded staging path to a test-owned temporary directory. Dependency detection for the requirements case and Node installation are mocked; no packages are downloaded. The Node test verifies accounting for simulated install outputs, not that npm succeeds. Wrapper subprocess execution remains mocked.

Full AstrBot execution, real CLI subprocess integration, npm installation, extracted-project startup and generated-test execution: NOT_RUN. Existing concerns about Node dependency parsing, staging concurrency/path confinement, entry-point layout, nested test paths and subprocess exit-code handling are outside this change.

## Scope and delivery

The branch was fast-forwarded from the merged Week 5 checkpoint to the reviewed course main. Changes on main affected other members' methods and governance; the owned `_call_packager` method and packager script were unchanged before this work. This week changes only the owned packager script, C2 tests and this evidence file. No shared main.py or governance files are edited.

Commit: `test(c2): week 06 verify owned behavior`. Publish to `course/c2`; Sprint 2 PR review/integration remains scheduled for Week 9. No C2 Week 7 or later files are created. The post-publication execution report records the final commit, remote synchronization and scope checks.
