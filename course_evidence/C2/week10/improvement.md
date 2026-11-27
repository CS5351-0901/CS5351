# Week 10 — Independent packaging attempts

Date: 2026-11-22
BRANCH: course/c2
REVIEWED_MAIN: 60743b0485bc7404f8573cd54bdb1bab99ef2700

## Engineering change

The branch was fast-forwarded to current main after the other Sprint 2 role merges. The C2 packager and owned wrapper were unchanged upstream; changes to orchestration, sandbox, snapshots and checks belong to other roles and are preserved.

The packager previously reused a hard-coded staging directory and output filename derived only from second-resolution time. Same-name requests within a second could overwrite a previous ZIP and concurrent attempts could mix source content or remove another attempt's staging directory.

The owned packager now allocates staging with tempfile.mkdtemp and reserves each output filename with NamedTemporaryFile in the configured output directory. The reservation handle is closed before ZipFile opens it, supporting Windows access rules. Names retain the project/time prefix plus a unique suffix; consumers must use returned zip_path rather than construct a filename. Result field names and successful archive layout/count semantics remain unchanged.

Existing baseline/layout fixtures now configure tempfile.tempdir inside test-owned storage, using real directory allocation instead of intercepting pathlib.Path. Cleanup assertions verify that the scratch directory is empty.

## Executed validation

Python 3.12.14 on Windows, with the bundled interpreter and writable TEMP/TMP scratch storage:

```text
python -B -m unittest discover -s tests/roles/c2 -p 'test_*.py' -v
```

Added five real-filesystem tests in tests/roles/c2/test_week10_lifecycle.py:
- Same-second sequential same-name attempts preserve both archives and their original bytes.
- A pre-existing timestamp-named output is not overwritten.
- Two threads with the same name and frozen clock retain separate source contents; a barrier forces overlap.
- Staging directories use the configured temp root, are unique and are removed after successful packaging.
- Temp allocation failure returns a structured failure without an archive.

Before production changes: 27 cases, 22 passed and 5 failed. The red run redirected only the legacy hard-coded path into test storage to avoid writes outside the fixture. After changes that legacy adapter was removed: 27/27 passed, no skips/expected failures, exit 0. Allocation, writes, archive reads and cleanup are real. Time is frozen and one allocator failure is injected; prior wrapper/dependency/npm mocks remain.

RUNTIME_TEST: PASS (27/27 scoped cases)

## Limits and remaining work

This addresses independent temporary/output names in ordinary same-process concurrent packaging; it is not a multi-process stress test or protection from malicious filesystem actors. Project/file names remain unvalidated for absolute/traversal/symlink confinement. ZIP creation failures may still leave a partial reserved archive; failure cleanup is the next regression/cleanup task, not claimed fixed here. Process termination and OS cleanup denial are also not proven safe.

Real AstrBot, CLI subprocess, npm install, extracted-project startup and generated-test execution remain NOT_RUN. No shared main.py changes or other-role edits are made. This week has production and test artifacts; no Week 12/13 artifacts or early Sprint 3 PR are created.
