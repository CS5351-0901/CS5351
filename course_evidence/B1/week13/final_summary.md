# Week 13 — B1 Final Summary

## Role and engineering artifacts

B1 owns requirement extraction, user/group blacklist checks, and project assessment in `main.py`. Week 5–6 changes preserved multiline requests, rejected blank input and command-like fragments, and normalized surrounding whitespace before assessment. Week 10 replaced substring matching with whole-token matching for English aliases. Ordinary words such as `tests` and `capital` no longer trigger TypeScript or API classification. Week 11 simplified those checks and added coverage for blank assessments and digits adjoining aliases. The 19 role tests also cover blacklist normalization, mentions, CRLF, Unicode size thresholds, and category precedence.

The independent, standard-library support toolkit provides inventory, text and source statistics, deterministic manifests, report generation, snapshot diffs, duplicate groups, a health report, and a static self-audit. The 12 implementation modules and 10 opt-in check modules live under `course_tools/b1_support/`. The tools run independently of AstrBot. The [Week 12 notes](../week12/presentation_notes.md) describe the demo and include contributions suitable for the final report.

## Course evidence and integration

Week 01–13 each has B1 evidence. Early evidence documents the role, source map and initial findings. Later evidence records validation, engineering changes, integration reviews, and presentation preparation.

- Sprint 1 PR [#3](https://github.com/CS5351-0901/CS5351/pull/3) was confirmed merged.
- Sprint 2 PR [#23](https://github.com/CS5351-0901/CS5351/pull/23) was confirmed merged.
- The Week 13 commit is included in the [Sprint 3 comparison](https://github.com/CS5351-0901/CS5351/compare/main...course/b1) after push. PR and review status are tracked on GitHub.

`git fetch origin --prune` succeeded, and `git status --short` returned no entries before the summary was added. Reviewed main was `60743b0`. Its changes since the Sprint 3 branch point were limited to team evidence.

## Executed final validation

- `python3 -B -m unittest discover -s tests/roles/b1 -v` passed all 19 tests.
- `python3 -B -m unittest discover -s course_tools/b1_support/checks -p 'check_*.py'` passed all 77 checks.
- Python compilation passed for all 24 files checked, covering `main.py`, the B1 regression module, and the 22 support Python files. CLI help and rendering a real support manifest to JSON, CSV, and Markdown passed.
- The support self-audit passed on 22 files. The health report counted 22 Python files and zero inventory issues.

## Git source metadata review

A targeted scan of tracked paths and text across the Week 12 B1 tip and fetched main, plus reachable commit messages, found no source-input directory, machine source-input path, external source repository URL on the hosting domains checked, or source-tracking field. Three full object IDs in A1/C2 course evidence remain unresolved locally. The surrounding records identify a course baseline and two temporary integration trees, with no indication of an external source commit. The original evidence is preserved. This check is limited to tracked content and identifiable source metadata patterns.

## Remaining limits

The role tests use AstrBot import stubs. Live adapter initialization, event dispatch, and end-to-end delivery remain unverified by B1. Classification follows fixed keywords and precedence. Duplicate reports depend on manifest freshness, and a static self-audit cannot establish all runtime behavior.
