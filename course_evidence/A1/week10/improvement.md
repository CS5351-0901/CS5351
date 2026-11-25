# A1 Week 10 — Sprint 3 improvement

Recorded: 2026-11-20 (Asia/Singapore). Owner: A1.

## Observed problem and owned change

The existing `_ensure_js_dependencies` helper in `main.py` treated any existing `node_modules` directory as proof that npm dependencies were installed. An empty or interrupted installation could therefore suppress `npm install` on subsequent plugin startup. This risk was already noted in the Week 9 Sprint 2 closeout.

This Week 10 change stays inside A1's owned JavaScript dependency setup function. When `node_modules` exists, the helper reads the local `package.json` dependency and development-dependency names and checks that their package directories exist. A missing required package triggers the original npm installation route. A malformed/unreadable manifest produces a warning and lets npm report the installation error rather than claiming success. The previous npm process arguments, timeout and result reporting are unchanged.

Updated the old A1 baseline test to construct real temporary package directories and added `tests/roles/a1/test_week10_js_dependencies.py` with five new executable cases: empty existing directory, partial dependencies, complete dependencies, manifest-defined names, and invalid manifest/failure reporting. All subprocess calls remain mocked; no real npm install was performed.

## Actual validation

Windows / Python 3.13.2:

```text
C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests/roles/a1 -p test_*.py -v
Ran 33 tests
OK
```

33/33 PASS (28 baseline/Weeks 5–7 plus 5 Week 10). Source diff and whitespace validation also passed. These are controlled A1 regression tests, not a live AstrBot startup or actual npm network installation.

## Remaining limits

Checking for package directories does not verify installed package versions, module integrity or package-lock consistency. Real installer activity, startup time and interactions with the integrated D1 checker require later environment-specific validation. No changes were made to other roles.

WEEK10_A1_ENGINEERING: COMPLETED
WEEK10_A1_ROLE_TESTS: 33/33 PASS
WEEK10_A1_REAL_NPM_INSTALL: NOT_RUN
WEEK10_A1_REAL_ASTRBOT: NOT_RUN
