# Week 12 — Presentation and report evidence

Date: 2026-11-26
MEMBER: C2
BRANCH: course/c2
REVIEWED_MAIN: 76e6fc1781c7e4a50e127fb78e97f8b550c89939
VALIDATION_BASE: 3ea238234701d8569d569d7e1b772462fc7b03cc

## Contribution summary for slides / final report

C2 made CodeAgent project packaging more reliable across empty or nested tests, accurate archive reporting, overlapping requests and recoverable archive failures. Five focused production fixes are supported by 33 automated role tests. Packaging now preserves separate same-name deliveries and removes a failed call's partial archive when the filesystem permits it. Integration and security limits remain explicit.

Suggested 60-second narrative: I owned project packaging and its calling contract. I first reproduced failures with missing test directories, then corrected archive counts and nested test layout. Sprint 3 isolated staging and output names so overlapping calls cannot accidentally share those resources. Failure-path regression tests exposed leftover ZIPs; cleanup now targets the current attempt and reports deletion denial. Real filesystem and ZIP assertions support these claims, while full application and dependency installation checks remain outside the executed evidence.

## Owned modules and actual engineering work

Owned scope: main.py::_call_packager; skills/CodeAgent/scripts/codeagent_packager.py, including ProjectPackager and DependencyGenerator. Production changes are confined to the packager script; the calling wrapper was exercised through isolated tests.

| Week | Reproduced problem and delivered change | Role suite after change |
| --- | --- | --- |
| 5 | Missing/empty tests caused directory initialization failure; create the tests directory before writing its initializer. | 12 passed |
| 6 | file_count omitted generated/extra files or double-counted overwritten paths; derive it from actual ZIP members. | 16 passed |
| 7 | Nested test paths failed when parents were absent; create parent directories before writing each test. | 22 passed |
| 10 | Second-resolution names could overwrite outputs or share staging; allocate independent OS temporary directories and reserve unique ZIP paths. | 27 passed |
| 11 | ZIP open/write/size failures left reserved or partial archives; remove only this call's output, preserving the original error and reporting cleanup failure. | 33 passed |

Tests live in tests/roles/c2/test_baseline.py, test_week07_layout.py, test_week10_lifecycle.py and test_week11_failures.py. Week 8 and Week 9 record integration review and Sprint 2 closeout. Week 1–4 evidence remains a historical catch-up record; its runtime NOT_RUN labels have not been rewritten as contemporaneous execution.

Sprint 1: https://github.com/CS5351-0901/CS5351/pull/6 (merged).
Sprint 2: https://github.com/CS5351-0901/CS5351/pull/18 (merged).
Sprint 3 contains Week 10/11 engineering and Week 12/13 delivery evidence; the final execution report records its PR and merge result.

## Week 12 executed verification

The branch incorporated the reviewed main through a clean merge before this run. Upstream main changes did not alter the C2 packager or calling wrapper.

Environment: Windows, Python 3.12.14, bundled interpreter, writable TEMP/TMP.

```text
python -B -m unittest discover -s tests/roles/c2 -p 'test_*.py' -v
Ran 33 tests — OK, exit 0, no skips or expected failures.
```

RUNTIME_TEST: PASS (33/33 scoped cases, rerun on 2026-11-26).

Assertions cover archive member names/content/CRC/count/size, actual temporary storage, cleanup, repeated same-name outputs and overlapping threads. The overlap case freezes time and synchronizes two calls. Failure cases inject errors at filesystem/ZIP boundaries. Wrapper subprocess behavior, selected dependency classification and npm artifacts are mocked; these are not live integration runs.

## Remaining limits

- Real AstrBot, CLI subprocess, npm install, extracted-project startup and archived-test execution: NOT_RUN.
- Absolute/traversal paths and symlink confinement, hostile filesystem access and multi-process stress are unresolved.
- Process termination or OS deletion denial can leave artifacts. Archive deletion denial is reported; existing staging removal still ignores errors.
- Dependency parsing/environment dependence, generated entrypoint layout and wrapper exit-code/schema validation need further work.

This week adds presentation evidence only. It does not claim a slide deck, full application certification or fixes for the listed limits.
