# B2 Week 7 — Contract / Boundary Verification

## Goal

Add at least one executable verification item for the B2 role. This week adds
**contract tests** that lock down the cross-function contracts between the
B2-owned responsibilities. Verification is actually run (no fabricated PASS).

## What was added

New test class `B2Week7ContractTest` in `tests/roles/b2/test_role_b2.py`
(5 cases):

- `test_process_json_contract_fields` — `process.json` contract: `status=init`,
  `current_step=requirement_analysis`, `completed_steps`/`snapshots` are lists,
  `created_at`/`updated_at` are numeric timestamps.
- `test_distinct_groups_do_not_collide` — different group/user pairs never
  collide on the same session id (key uniqueness).
- `test_exit_path_uses_same_session_id` — the session id used to register, to
  create process.json, and to clean up is one and the same key.
- `test_cleanup_keeps_table_consistent` — after cleanup, a dropped session's
  process file no longer exists (table/dir lifecycle consistency).
- `test_create_is_idempotent_for_same_key` — repeated creation on the same key
  yields a consistent schema.

## Verification result

Command:

```bash
python -m unittest tests.roles.b2.test_role_b2
```

Result:

```text
Ran 29 tests in 0.069s
OK
```

29 tests pass (24 from Weeks 5–6 + 5 new contract tests). No business source
(`main.py`) was modified; only the B2-owned test file and evidence were touched.

## Not executed in this round

Full asynchronous `agent_command` flow under a real AstrBot runtime still
requires the astrbot package and sandbox scripts.

RUNTIME_TEST (full runtime flow): NOT_RUN
