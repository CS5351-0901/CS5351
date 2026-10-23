# Week 7 — B1 Boundary and Contract Verification

## Expanded verification

Added four executable regression tests to the B1 suite. They verify command-separator whitespace with CRLF requirement preservation, a tab-separated Chinese request, trimmed Unicode character-count boundaries at 29/30/99/100 characters, a project keyword after a line break, and numeric group blacklist normalization without confusing a user ID with a group ID.

All cases pass against the current B1 implementation, so no production source fix is claimed or included this week. The existing multiline, blank-input, trigger-boundary, blacklist, precedence, and size checks remain in the suite.

## Validation performed

- `python3 -B -m unittest discover -s tests/roles/b1 -v` — PASS, 14 tests.
- `python3 -m py_compile tests/roles/b1/test_role_baseline.py` — PASS.
- `git diff --check` — PASS.

Only `tests/roles/b1/test_role_baseline.py` and this B1 evidence file belong to the original Week 7 commit. The independent support extension is developed after this original task passes and is committed separately. Push is deferred for user review.

## Limits

The role suite loads the real helpers with AstrBot import stubs. It does not verify installed-runtime initialization, adapter message serialization, or live event dispatch. Inputs outside the helpers' annotated string contract remain outside this verification.
