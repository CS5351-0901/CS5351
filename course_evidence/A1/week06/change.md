# A1 Week 6 — Node/npm preparation regression enhancement

Date: 2026-10-12. Sprint 2, Week 6. Scope: A1-owned environment/setup verification only.

## What changed and why

Added an executable, standard-library-only test suite in tests/roles/a1/test_week06_environment.py (12 tests), building on the 8 Week 5 A1 baseline tests.

The Week 4 team technical-debt review identified OS-specific Node.js preparation, package-manager fallback, and npm failure/timeout handling as areas requiring real checks. Week 5 tested Windows Node.js detection and two npm scenarios. This week extends coverage without modifying production behavior or claiming a live installer test.

The new tests exercise actual A1-owned methods _ensure_nodejs, _install_nodejs_linux, _install_nodejs_mac, and _ensure_js_dependencies, including:

- Existing Node.js is detected and does not call installers.
- Linux missing/broken Node probe dispatches to Linux installation; absent package managers use official fallback; a failing package manager is skipped for the next one.
- macOS probe timeout leads to the macOS setup branch; failing Homebrew uses official fallback.
- Missing JS checker, missing package.json and missing node prevent unnecessary npm execution.
- npm nonzero exit reports a bounded error without falsely logging success; npm timeout reports a warning; successful npm reports completion.

All process launches, package installation commands and downloads in these tests are mocked; the plugin methods themselves execute. No packages were installed, no network calls or system writes were performed, and no behavior from another role or shared production function was changed.

## Actual validation

Host: Windows, C:\ProgramData\miniconda3\python.exe (Python 3.13.2), from course repository root.

    C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests/roles/a1 -p test_week06_environment.py -v
    Ran 12 tests ... OK (12 passed)

    C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests/roles/a1 -p test_*.py -v
    Ran 20 tests ... OK (20 passed; 8 Week 5 + 12 Week 6)

Both commands actually ran with exit code 0, no skips and no expected failures. The new suite is a non-document executable verification enhancement, satisfying the handbook's Week 6 engineering requirement without a speculative production fix.

## Limits and known follow-up

- No actual OS package manager, official Node.js download, or npm install was executed; Linux/macOS branches were simulated on Windows. This does not prove a real installation works or that Windows can install Node automatically.
- JavaScript dependency setup still runs synchronously when the real plugin is initialized; startup responsiveness and partially created node_modules are not established here.
- A1 Week 6 changes are restricted to tests/roles/a1/ and course_evidence/A1/week06/. Other roles' code and tests remain untouched.
- Sprint 2 A1 PR is due at Week 9 per the role manual, not Week 6. Week 7+ tasks were not performed.

WEEK06_A1_EXECUTABLE_TESTS: PASS (12/12)

A1_BASELINE_INTEGRATED_TESTS: PASS (20/20)

ASTRBOT_LIVE_RUNTIME: NOT_RUN
