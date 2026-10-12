# D1 — Week 5 / Sprint 1 baseline

Date: 2026-10-03
TARGET_WEEK: 5
BRANCH: course/d1
REVIEWED_MAIN: d849081bfe9a32ce42ed2b98b4abda55976d7dfd

## Engineering artifact

`tests/roles/d1/test_baseline.py` adds 21 executable standard-library unittest cases.
No production source changes are included. Week 1–4 evidence is retained with its
original catch-up labels and real commit dates. No Week 6 or later artifacts are created.

The latest reviewed main changes only `_extract_requirement` in shared main.py,
outside D1's two adapters. Neither D1 adapter nor the sandbox/checker scripts differs
between the personal branch and that main revision.

## Validation actually executed

Environment: Windows, Python 3.11.5, Node.js v22.22.3.

```sh
python -B -m unittest discover -s tests/roles/d1 -p 'test_*.py' -v
```

Observed: `Ran 21 tests`; `OK (expected failures=6)`; process exit code 0.
There were **15 passing tests, 6 expected failures, 0 unexpected failures/errors,
and 0 skipped tests** on this environment.

BASELINE_SUITE: PASS_WITH_6_KNOWN_FAILURES
FULL_SANDBOX_EXECUTION: NOT_RUN
ESLINT_AND_TYPESCRIPT_COMPILER_VALIDATION: NOT_RUN
ASTRBOT_END_TO_END: NOT_RUN

The suite's successful exit means that its baseline expectations held. It does not
mean the six desired contracts passed or the production defects were repaired.

## Coverage and isolation

- Eight passing adapter unit tests import the real main.py with only AstrBot imports
  stubbed, then mock subprocess.run. They check sandbox result preservation,
  nonzero process failure, timeout, malformed JSON, missing script, forwarded
  session/language/filename and outer timeout; checker tests retain nonzero-exit
  JSON diagnostics and reject a nonzero exit without valid JSON.
- Seven passing tests start the real checker with Node.js: JSON schema and missing
  ESLint disclosure, rejection of eval with a correct source line, whitespace input,
  missing file, Unicode code-file input and output paths containing spaces, automatic
  TypeScript detection with missing-compiler disclosure, and quality-threshold failure.
- Each CLI test supplies its own temporary directory and overrides TEMP/TMP/TMPDIR.
  PATH deliberately excludes external lint tools, so the tests exercise the deterministic
  no-tool path and built-in security/quality logic. They do not assert real lint/compiler
  correctness. Node itself is resolved before changing the child environment.
- Checker input is inspected, not executed. The sandbox subprocess only runs --help;
  it never executes submitted code or applies resource limits during this baseline.
- Adapter unit tests do not initialize a live AstrBot plugin. They verify adapter behavior
  with controlled subprocess responses rather than claiming full integration.

## Reproduced known failures

| ID | Desired contract tested | Observed baseline defect | Test boundary |
| --- | --- | --- | --- |
| D1-001 | Sandbox receives original multiline/Unicode code | Adapter sends JSON-encoded code including quotes/escapes | Real adapter, mocked child |
| D1-002 | Sandbox --config is a readable JSON file while the child runs | Adapter passes inline JSON, which cannot be opened as the required file | Real adapter, file-read contract probe |
| D1-003 | Checker receives original multiline/Unicode code | Adapter sends JSON-encoded code | Real adapter, mocked child |
| D1-004 | Missing Node must not report passed=true | Adapter reports passed=true with error | Real adapter, simulated missing executable |
| D1-005 | Checker timeout must not report passed=true | Adapter reports passed=true with error | Real adapter, simulated timeout |
| D1-006 | Sandbox --help can start on Windows | Process exits 1 with ModuleNotFoundError for resource | Real Python subprocess on Windows |

These six cases use unittest.expectedFailure. A future successful result becomes an
unexpected success and fails the suite, requiring removal of the marker after review.
The Windows-specific case is skipped on other platforms, and real checker CLI tests
are skipped when Node is absent; reviewers must inspect counts instead of treating
skipped coverage as executed validation.

## Remaining work and Sprint 1 scope

The unresolved resource-limit effectiveness, filesystem/network isolation, default
workspace_root type, external tool discovery, and concurrent temporary-directory
behavior remain as recorded in Week 3. This baseline does not validate those guarantees.
The next engineering stage should resolve the six tracked contracts with focused
regressions and ownership review for shared main.py changes.

Sprint 1 PR direction: course/d1 -> main. Its intended diff contains only
course_evidence/D1/week01–week05 and tests/roles/d1/test_baseline.py. PR identity,
merge status, final branch synchronization and scope checks are reported in the
delivery response after the actual GitHub operations.
