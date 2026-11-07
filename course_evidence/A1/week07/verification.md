# A1 Week 7 — contract, boundary and failure-path verification

Date: 2026-10-25. Target: Week 7, Sprint 2. Owner: A1 (configuration and Node/npm preparation).

## Engineering verification increment

Added `tests/roles/a1/test_week07_contracts.py`, eight executable regression/boundary cases against the actual A1-owned helpers `_get_config`, `_ensure_nodejs`, `_install_nodejs_linux`, `_install_nodejs_mac`, `_install_nodejs_from_official`, and `_ensure_js_dependencies`. This extends the Week 5–6 A1 regression baseline; no production source was modified because these scoped checks did not demonstrate a new defect needing an A1 fix.

New contracts and failure paths:
- Explicit falsey config values (`False`, `0`, empty string/list, `None`) are preserved instead of being replaced by fallback defaults; an actually absent key uses the supplied fallback.
- Failed Linux Node setup returns failure without a misleading installed/success log; two failing package managers lead to the official fallback.
- macOS without Homebrew uses the official installer fallback without attempting an unrelated shell install.
- Official Node download network error and corrupt archive are caught, return failure, and do not proceed to extraction/copy where unsafe.
- Checked `node -v` failure prevents npm invocation; an npm permission error emits a warning, not a success log.

All subprocess, download, filesystem-creation and installer boundaries used by these tests are mocked. Actual methods execute; no real Node installation, npm installation, network transfer or archive extraction was performed.

## Commands actually run

Environment: Windows, `C:\ProgramData\miniconda3\python.exe` (Python 3.13.2).

```text
C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests/roles/a1 -p test_week07_contracts.py -v
Ran 8 tests ... OK; exit 0

C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests/roles/a1 -p test_*.py -v
Ran 28 tests ... OK; exit 0
```

The full A1 suite comprises Week 5 baseline (8), Week 6 environment regressions (12) and Week 7 contracts (8), with no unexpected failures or skips.

## Remaining limits

The new contract tests do not prove real Linux/macOS installer operation or a live AstrBot initialization. Synchronous startup/partial `node_modules` behavior remain separate documented integration concerns. No B/C/D code or team-leader evidence was changed in the A1 commit. Under the role handbook, the Sprint 2 role PR belongs at Week 9, not Week 7; Week 8+ deliverables were not created.

A1_WEEK07_VERIFICATION: PASS (8/8)
A1_CUMULATIVE_REGRESSION: PASS (28/28)
LIVE_ASTRBOT_END_TO_END: NOT_RUN
