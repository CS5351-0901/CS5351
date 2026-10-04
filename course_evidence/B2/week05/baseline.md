# B2 Week 5 — Sprint 1 Closeout / Baseline

## Goal

- Establish the first executable baseline / regression test set for the B2 role.
- Produce at least one non-document engineering artifact.
- Actually run the role validation; do not fabricate PASS.

## Engineering artifact (non-document)

- New test suite: `tests/roles/b2/test_role_b2.py`
- Covers all 5 responsibilities owned by B2 in `main.py`:
  - `main.py::_is_exit_command`
  - `main.py::_sanitize_session_id`
  - `main.py::_cleanup_session`
  - `active_sessions` (session state table)
  - `main.py::_create_process_json`

## Design and isolation notes

- The course repo does not ship the `astrbot` runtime, so `main.py`'s top-level
  `import astrbot` fails on import. The test injects a fake `astrbot` module tree
  (stdlib only) into `sys.modules` before loading `main.py`, purely to satisfy
  the import; the objects under test are pure functions.
- Instances are created via `object.__new__(CodeAgentPlugin)` to bypass
  `__init__` and avoid side effects such as the automatic Node.js install.
- Stdlib `unittest` only; no third-party dependency; runs standalone.

## Actual run result

Command:

```bash
python -m unittest tests.roles.b2.test_role_b2 -v
```

Result:

```text
Ran 18 tests in 0.036s
OK
```

All 18 cases pass, covering:

- `_is_exit_command`: exact match / case-insensitive / embedded in long text /
  rejects normal text / rejects empty (5)
- `_sanitize_session_id`: basic / colon / slash / mixed separators (4)
- `_cleanup_session`: removes existing session dir / missing session no-op /
  does not touch other sessions (3)
- `_create_process_json`: file matches return value / fields complete /
  parent dir auto-created (3)
- `active_sessions` consistency contract: one key across table and process.json /
  deterministic / exit path removes state (3)

## Consistency contract conclusion

`agent_command` uses the same `session_id` for a session across the whole flow:
`active_sessions` key == `_sanitize_session_id` result == `process.json.session_id`.
The suite locks this in as a regression contract.

## To be verified in Week 5+ (not executed in this round)

- Full asynchronous `agent_command` flow under a real AstrBot runtime
  (requires astrbot and the sandbox scripts installed).
- Concurrency / residue boundaries (silent semantics of
  `shutil.rmtree(ignore_errors=True)`).

RUNTIME_TEST (full runtime flow): NOT_RUN
