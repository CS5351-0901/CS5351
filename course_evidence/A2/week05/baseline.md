# Week 5 — A2 Executable Baseline

## Engineering change

Added `tests/roles/a2/test_orchestration.py`, a standard-library unittest suite that imports the actual course `main.py` with minimal AstrBot import stubs. It exercises `CodeAgentPlugin` construction, `agent_command`, `terminate`, and the factory entry. No production source was changed.

The command tests cover empty input, denied users, missing requirements, duplicate requests, targeted exit cleanup, stage order and packaging arguments, exhausted execution retries, Python security rejection, JS critical findings, dependency exceptions, and successful file delivery. The lifecycle tests check constructor state and repeatable cleanup of all active sessions. Temporary files are confined to each test's temporary directory.

Process creation, script execution, security checking, snapshots, and packaging are controlled at their call boundaries. Environment preparation is stubbed during construction, and unexpected subprocess calls are guarded. The tests execute the real async command and lifecycle methods without installing dependencies or executing generated code.

## Validation performed

Date: 2026-10-12. Interpreter: Python 3.14.6 on Windows.

Commands run from the course repository root:

```text
python -B -m unittest discover -s tests/roles/a2 -p test_orchestration.py -v
python -m ruff check tests/roles/a2/test_orchestration.py
```

Final observed unittest result: 14 tests ran; 13 passed and 1 was an expected failure; no skips or unexpected failures; exit code 0. Ruff reported `All checks passed!`, exit code 0. An earlier run before adding the delivery case had 12 passes and the same expected failure.

## Known failure and limits

`test_factory_accepts_context_using_declared_constructor` records the existing factory mismatch with `unittest.expectedFailure`: `get_star(context)` calls `CodeAgentPlugin(context)`, while the constructor requires `config`. This remains unresolved. A successful suite exit does not mean this entry works. An unexpected success will fail the suite so the marker must be reviewed after a fix. The intended host factory/configuration contract still needs confirmation with A1.

AstrBot imports and file components are stubs. Direct invocation of the exit branch does not prove that the host routes a standalone `/exitconver` command to it. The delivery test checks when the generator yields and deletes the fixture archive, not when a real adapter reads it. Live loader startup, real sandbox/checker/packager execution, confirmation handling, event-loop responsiveness, and end-to-end delivery were not run. Compatibility with the minimum supported Python version was not separately tested.

## Sprint 1 scope

The branch retains the English Week 1–4 evidence and adds this Week 5 record and the executable A2 test file. Current course main was merged without conflicts before testing, preserving integrated work from other roles. The Sprint 1 PR targets `main` from `course/a2`; its changes are limited to `course_evidence/A2/**` and `tests/roles/a2/**`. No Week 6 or later files are included.
