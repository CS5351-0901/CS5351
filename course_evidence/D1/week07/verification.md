# D1 — Week 7 verification evidence index

Recorded: 2026-11-02. TARGET_WEEK: 9. BRANCH: course/d1.

This handbook-named entry is added during Week 9. Original Week 7 engineering
and executed checks remain in [platform_integration.md](platform_integration.md).

Commit `7de2841` added a real adapter-to-sandbox subprocess regression with
multiline Unicode source on Windows. The suite also exercises readable config
files, cleanup, process failures, timeouts, unavailable Node, checker output,
independent checker temporary directories and paths containing spaces.
Commit `e74446e` contains the Windows and checker hardening described there.

Revalidation: 2026-11-02, Python 3.11.5 / Node v22.22.3 on Windows. Command:
`python -B -m unittest discover -s tests/roles/d1 -p 'test_*.py' -v`.
Observed: 25 tests, OK, no skips or expected failures, exit 0.
`node --check skills/CodeAgent/scripts/codeagent_js_checker.js` also exited 0.

This is role verification, not a claim of live AstrBot end-to-end validation
or enforced Windows resource/network isolation.
