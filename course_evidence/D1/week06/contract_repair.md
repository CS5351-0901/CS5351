WEEK6_CATCH_UP

This Week 6 artifact was completed during Week 7. It uses the real current date
and does not claim that the work or file existed during the historical Week 6.

# D1 — Week 6 adapter contract repair

Date: 2026-10-25
TARGET_WEEK: 6
BRANCH: course/d1

## Completed contracts

- D1-001: `_call_sandbox` now passes the original code string to `--code`.
  Multiline and Unicode source is no longer serialized a second time with
  `json.dumps`.
- D1-002: `_call_sandbox` writes the configured wall-time, memory, and file-size
  limits to a temporary UTF-8 JSON file, passes its path through `--config`, and
  removes the file after the child process returns.
- D1-003: `_call_js_checker` now passes the original JavaScript or TypeScript
  source to `--code`.
- D1-004: a missing checker script or unavailable Node.js returns
  `passed=false` instead of a permissive success-shaped result.
- D1-005: checker timeout and unexpected checker failure return `passed=false`
  with an error.

The five former `unittest.expectedFailure` markers were removed after their
contracts passed. The A1 baseline assertion that described the old inline-JSON
configuration contract was updated to read the temporary configuration file while
the mocked child is running. No A1 production logic was changed.

## Engineering files

- `main.py`
- `tests/roles/d1/test_baseline.py`
- `tests/roles/a1/test_baseline.py`

## Validation

Final D1 suite:

```text
python -B -m unittest discover -s tests/roles/d1 -p test_*.py -v
```

Observed: 24 tests ran; all passed; exit code 0. There are no expected failures.

The final integration checks recorded with the Week 7 evidence also show A1 at
8 passing tests and B1 at 7 passing tests.

## Boundary

This stage fixes the adapter parameter and failure contracts. It does not claim
full AstrBot event integration, complete sandbox isolation, or effective
resource-limit enforcement.
