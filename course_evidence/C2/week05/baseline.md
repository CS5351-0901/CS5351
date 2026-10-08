# Week 5 — C2 Sprint 1 baseline

Date: 2026-10-09
BRANCH: course/c2
REVIEWED_MAIN: 959e3e62004350c3aee7a640e2c77cbb5b8589df

## Engineering artifacts

- `tests/roles/c2/test_baseline.py`: 12 standard-library unittest cases.
- `skills/CodeAgent/scripts/codeagent_packager.py`: create the Python tests directory before writing its package initializer, including when test_files is omitted or empty.

The latest course main changes to main.py concern requirement extraction, outside C2 ownership. The owned packager method and script were unchanged at review time. This week does not edit main.py or another role's files.

## Executed validation

Runtime: Python 3.12.14 on Windows. From the repository root:

```text
python -B -m unittest discover -s tests/roles/c2 -p test_baseline.py -v
```

The actual invocation used the available bundled Python interpreter. The initial sandbox temporary directory rejected file operations, so TEMP and TMP were pointed to a writable scratch directory outside the repository. Tests normalize platform text line endings when checking archived content. Neither adjustment changes production behavior.

After these test-environment adjustments, the unmodified packager ran 12 cases: 10 passed and 2 failed. Both failures were real missing-directory errors when writing tests/__init__.py with omitted or empty test_files. After the one-line production fix, all 12 cases passed, with no skips or expected failures (exit code 0).

RUNTIME_TEST: PASS (12/12 scoped baseline cases)

Coverage:
- Real ZIP generation, exact archive member set, source/test content, CRC check and reported byte size.
- Python projects with supplied tests, omitted tests and an empty test list.
- Injected write failure: structured failure, no archive, staging cleanup.
- Python import aliases/dotted modules; dependency deduplication, sorting and non-Python exclusion; requirements rendering.
- Node package.json runtime/development dependency separation.
- Actual `_call_packager` method: serialized arguments, optional test argument, JSON response, missing script, invalid stdout and timeout.

## Isolation and limits

The fixture redirects the packager's fixed temporary staging path into a test-owned temporary directory; filesystem writes, cleanup and ZIP operations remain real. It does not validate the production temporary-path portability or concurrent invocation behavior. Dependency classification is mocked for deterministic results independent of installed packages. The real owned wrapper method is compiled from main.py's AST to avoid loading AstrBot; subprocess.run is mocked. The test suite does not install dependencies or contact the network.

Full AstrBot execution, CLI subprocess integration, npm installation, generated-test execution, extracted-project installation/startup and production path confinement: NOT_RUN. These scoped tests do not establish end-to-end delivery readiness.

Remaining Week 3 findings include Node import-string stripping, dependency detection tied to installed modules, entry-point layout, nested test paths, file-count semantics and subprocess timeout/exit-code handling. They are not fixed or reported as passing here.

## Sprint 1 delivery

The intended PR is course/c2 into main, containing only C2 Week 1–5 evidence, the C2 baseline tests and the owned packager fix. Final PR status and commit identifiers are recorded after publication in the execution report. No Week 6 or later files are created.
