# Week 11 — B1 Regression and Cleanup

## Role changes

`_assess_project` now uses `isdisjoint` for alias checks to avoid building an intersection result. The token pattern matches lowercase ASCII after normalization, and the size variable now reflects its character-count unit. Classification precedence, input trimming, size thresholds, and return keys are preserved.

Two additional regressions cover blank direct assessments and digits adjoining a language alias. The full suite also exercises malformed command fragments, multiline extraction, blacklist normalization, classification precedence, and Unicode size boundaries.

## Executed checks

- `python3 -B -m unittest discover -s tests/roles/b1` — PASS, 19 tests after cleanup.
- `python3 -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS.
- `git -c core.whitespace=cr-at-eol diff --check` — PASS.
- The existing support suite passed all 72 checks before the Week 11 extension.

## Course Git evidence review

Checked tracked paths and text in the Week 10 branch tip and locally available course main, plus their reachable commit messages for external repository links. The targeted scan found no source-input directory, external repository URL on the hosting domains checked, or source-tracking field. Full hexadecimal ID candidates were compared with locally available Git objects. Three unresolved IDs are documented in existing A1/C2 evidence as a course main baseline and two temporary integration trees. Their objects are unavailable locally, and the surrounding records do not identify them as external source commits. The existing evidence was preserved.

The scan is based on identifiable path names, URL patterns, and fields in tracked text. Role tests use AstrBot stubs and do not exercise a live adapter.
