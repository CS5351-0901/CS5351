# D1 — Week 6 engineering evidence index

Recorded: 2026-11-02. TARGET_WEEK: 9. BRANCH: course/d1.

This handbook-named entry is added during Week 9; it does not backdate work.
The original Week 6 catch-up implementation and verification are recorded in
[contract_repair.md](contract_repair.md), dated 2026-10-25.

Engineering commits: `e74446e` and follow-up `7de2841`. The owned adapters pass
raw multiline source, send sandbox configuration through a temporary JSON file,
clean up that file, and fail closed on unavailable or failed JS checking.
The executable artifact is `tests/roles/d1/test_baseline.py`, alongside changes
to owned production functions/scripts. This was not a documentation-only sprint.

Current revalidation on 2026-11-02 after merging current main: D1 unittest
discovery ran 25 tests, all OK, exit 0. See Week 8 for commands and integration
limitations. The original implementation date and evidence are preserved.
