# Week 11 — Archive failure cleanup and regression review

Date: 2026-11-22
BRANCH: course/c2
REVIEWED_MAIN: 60743b0485bc7404f8573cd54bdb1bab99ef2700
WEEK10_COMMIT: 8afa9855a3514dd8a669f1328336860ecce164e5

## Failure-path findings and cleanup

Week 10 made staging/output allocation independent. This week verified failures after output reservation: ZIP open, the second archive member write, and final size lookup could leave a reserved or partially written archive even though the result reported failure.

The packager now tracks only the archive path reserved by the current call and removes it on failure. It does not remove previously completed or unrelated files. If the operating system refuses archive deletion, the returned error retains the original failure and adds the cleanup failure rather than claiming complete cleanup. Staging cleanup remains in the existing finally block.

Six new cases in tests/roles/c2/test_week11_failures.py verify:
- Partial-write failure removes the partial archive while preserving an unrelated sentinel file.
- ZIP open failure removes the reserved empty file.
- Size lookup failure removes the unreported archive.
- Output reservation failure preserves existing files and cleans staging.
- Cleanup permission denial reports both errors; the test explicitly observes the remaining file.
- A successful retry after a failed write leaves only the successful delivery.

## Executed validation

Python 3.12.14 on Windows, bundled interpreter, writable TEMP/TMP:

```text
python -B -m unittest discover -s tests/roles/c2 -p 'test_*.py' -v
python -B tools/test_pr_ownership.py
```

Before the cleanup change: 33 cases, 28 passed and 5 failed. The failures demonstrated leftover archives or missing cleanup-error reporting. After the change: **33/33 C2 tests passed**, no skips/expected failures, exit 0. The **16/16 current ownership-policy tests** also passed; these are not additional C2 runtime cases.

RUNTIME_TEST: PASS (33/33 scoped cases)

All prior Week 5–10 tests were rerun, including the same-name overlapping-thread test. New failures are injected at the ZIP/filesystem API boundaries; allocation, surviving files, writes, archive reads and cleanup are real. Temp allocation is now real under a configured test-owned temp root. Existing wrapper/dependency/npm mocks remain.

## Course Git metadata audit

Read-only screening covered the current tracked text tree plus newly added Week 11 files, not arbitrary external repositories or the entire historical object database. Methods: enumerate git ls-files; inspect URL, local-source-path and provenance-field candidates; extract full 40-hex identifiers and resolve them against course Git objects; inspect candidates in context.

Findings:
- No external source-repository URL or source-provenance assignment was found. Course repository/PR URLs are legitimate evidence.
- Other URL candidates were the existing GitHub API sample, official Node binary download template and license link; these are not external source-repository provenance.
- The broad absolute-path screen produced 15 existing occurrences: 13 interpreter-command references in A1/team evidence and two synthetic B2 path-generator cases. They are not source input-directory disclosures. This is not a claim that the repository contains no absolute paths at all.
- One full hash in course_evidence/A1/week04/git_evidence.md was absent from the local object store. It was verified through the course repository's Git commit API as its Week 4 orchestration commit. It is not an external-source hash. Other full identifiers resolved to local course commit/tree objects.
- No existing evidence or other member's files were removed or rewritten to make the scan pass. The final execution report records the final scan counts and classifications.

SOURCE_METADATA_REVIEW: NO_CONFIRMED_FORBIDDEN_SOURCE_HITS (screened current text scope; not an exhaustive secret/history scan)

## Remaining limits and next checkpoint

This change does not guarantee deletion when the OS denies it, when the process is terminated, or when the existing staging removal silently fails. Arbitrary project/file path confinement, symlinks, adversarial filesystem access, multi-process stress, dependency parsing and generated-project usability remain unresolved. Real AstrBot, CLI subprocess, npm install, extracted-project startup and archived-test execution remain NOT_RUN.

Only the owned packager, C2 tests and C2 evidence change. No Week 12/13 files or early final PR are created. Commit: test(c2): week 11 run role regression. The post-publication execution report supplies exact commit IDs and remote/scope/cleanliness results.
