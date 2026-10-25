# Week 7 — Nested test layout and failure contracts

Date: 2026-10-25
BRANCH: course/c2
REVIEWED_MAIN: 6b0472c36ffd09c6bfe6e647380cd0d0799ea076
WEEK06_BASE: 3c2e8aaf5d7cb282b65b73ef96d7e3892d9f03ee

## Verified behavior and fix

The source-file writer creates parent directories, but the test-file writer previously created only the tests root. Valid nested test names such as unit/test_main.py therefore failed with a missing-directory error instead of producing an archive.

The owned packager now creates each test file's parent directory before writing its content, matching the existing source-file behavior. This is one line in `skills/CodeAgent/scripts/codeagent_packager.py`. Shared main.py, other roles and repository governance are unchanged.

`tests/roles/c2/test_week07_layout.py` adds six executable checks:

1. A test file inside one nested directory is preserved under tests/ in the ZIP.
2. Deep unit and integration trees preserve separate files with the same basename.
3. Unicode file names/content and an empty nested file survive packaging.
4. Flat and nested tests coexist; multiple test files can reuse an existing parent directory.
5. A regular test file cannot subsequently act as another test file's parent directory.
6. A test directory cannot subsequently be overwritten as a regular test file.

Successful cases reopen the real ZIP, check CRC, exact member names and test contents, verify returned byte size and file_count, and check staging cleanup. The two conflict cases assert success=false, a non-empty error, an empty zip_path, zero count/size, staging cleanup and an empty output directory.

## Actual execution

Python 3.12.14 on Windows, from the course repository root:

```text
python -B -m unittest discover -s tests/roles/c2 -p 'test_*.py' -v
```

The available bundled interpreter was used. TEMP and TMP pointed to writable scratch storage outside the repository.

Before the production change, the complete suite ran 22 cases: 18 passed and 4 failed. All four failures were new successful-layout cases failing with a missing parent directory. After adding parent-directory creation, all 22 cases passed, with no skips or expected failures and exit code 0. This includes all 16 Week 5–6 tests and the six new Week 7 cases.

RUNTIME_TEST: PASS (22/22 scoped cases)
NEW_WEEK07_CASES: PASS (6/6)

## Isolation and limits

The new test module reuses the existing packager import from the baseline module. Its fixture redirects only the hard-coded temporary staging path into a test-owned temporary directory. Directory creation, file writes, archive creation, archive reads and cleanup are real operations. No external dependencies are installed and no network is used by these tests. Existing dependency/subprocess mocks in the Week 5–6 suite remain in place.

These checks establish valid relative nested test layout and file/directory collision handling. They do not establish path confinement for absolute paths, parent-directory traversal or symlinks. They do not exercise production staging-path portability/concurrency, nested extra_files, actual CLI subprocess execution, npm installation, AstrBot execution or running the archived test code. Those behaviors remain NOT_RUN here; no end-to-end delivery claim is made.

## Scope and publication

Remote main was unchanged from the Week 6 reviewed baseline; course/c2 was pulled with --ff-only before work. The Week 7 commit contains only the owned packager fix, the new C2 test module and this verification document. Week 6 remains a separate earlier commit.

Commit message: `test(c2): week 07 expand verification`. Publish to course/c2. Sprint 2 PR review/integration remains due at Week 9. No C2 Week 8 or later files are created. Final commit and synchronization checks are recorded in the post-publication execution report.
