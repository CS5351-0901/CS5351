# C1 Week 4 integration review

RUNTIME_TEST: NOT_RUN

Static call-site review of the current course `main`:

- `agent_command` calls `_analyze_error` and `_generate_debug_fix` only after a sandbox result reports failure. It reports the suggested fix and retries until success or the configured limit.
- The retry currently adds the suggestion as a source comment. A failing program may therefore fail again; this needs an executable regression test in Week 5+.
- `agent_command` calls `_save_snapshot` once at `core_complete`, after constructing generated files and before calling the packager.
- `_rollback_to_snapshot` is defined but has no call site in `main.py`. The active command flow does not restore a snapshot when a later step fails. Wiring and expected rollback behavior need Week 5+ review.
- Week 1–4 on this personal branch changes only `course_evidence/C1/**`; business source is reviewed without modification.

These findings come from source inspection, not a runtime or end-to-end test.
