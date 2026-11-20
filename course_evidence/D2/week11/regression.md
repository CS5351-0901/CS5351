# D2 Week 11 regression and cleanup

## Regression scope

Re-ran the complete D2 security and quality scanner suite, including dangerous-pattern handling, ShellCheck success/failure contracts, JSON/CLI integration, Python syntax validation, and temporary-file lifecycle checks.

## Technical-debt cleanup

The Ruff, Mypy, Bandit, and ShellCheck adapters previously removed their temporary source files only after a successful subprocess call. A subprocess or parsing exception could leave those files behind.

Added a shared `temporary_source_file` context manager that writes UTF-8 source and removes it in a `finally` block. All four adapters now use this lifecycle. Added success- and failure-path regression tests proving the temporary file is removed in both cases.

## Repository metadata check

Checked Git-tracked course content for source-input directory fields, external source repository URLs, external source commit metadata, and provenance/source-tracking fields. Existing commit hashes and URLs are retained course evidence, course PR references, the course repository URL, license documentation, or runtime dependency/API configuration; they are not external source provenance and were not deleted.

Candidate review retained two evidence sentences that explicitly report the absence of forbidden provenance and one B2 path-generator fixture (`/home/user/project/scripts/main.py`). The fixture is synthetic test data, not a real source-input directory. URL hosts were limited to course/runtime/license uses (`github.com`, `nodejs.org`, and `unlicense.org`).

`FORBIDDEN_SOURCE_METADATA_HITS: 0`

## Validation

`RUNTIME_TEST: PASS`

Executed `python.exe -m pytest -p no:cacheprovider tests/roles/d2 -q` with Python 3.14.6 and pytest 9.1.1: **18 passed in 3.10s**. This includes the 15 existing D2 tests plus three Week 11 cleanup tests, including an adapter-level subprocess failure path.
