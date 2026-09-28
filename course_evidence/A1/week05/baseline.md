# A1 Week 5 executable baseline

## Artifact and scope

`tests/roles/a1/test_baseline.py` adds A1's first executable regression baseline using Python's standard-library `unittest`. It imports `main.py` with small AstrBot import stubs and does not run plugin initialization. Production files are unchanged.

The tests check that the schema has defaults for settings read directly by `main.py`, `_get_config` preserves values and fallbacks, blacklist matching accepts string IDs, and configured time/memory/file-size limits reach the sandbox call with the expected subprocess timeout. Controlled subprocess stubs cover Windows Node.js present and missing paths, skipping npm when `node_modules` exists, and reporting an unavailable npm command without raising.

## Validation performed

Interpreter: `C:\ProgramData\miniconda3\python.exe`, observed version `Python 3.13.2`.

Command, run from the repository root:

```text
C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests/roles/a1 -p test_baseline.py -v
```

Final observed result: exit code 0; 8 tests ran; all passed (`OK`). The `-B` option prevents Python bytecode cache writes.

The same command was run twice before changing the path fixtures to in-memory stubs. Both early runs reported 5 passing tests and 3 fixture setup errors: writes were denied first in the system temporary directory and then in temporary subdirectories under the repository. No test assertions failed in those runs. The final run above passed after removing filesystem writes from the fixtures.

The host also reported `node --version` as `v26.2.0` and `npm --version` as `11.13.0`; both commands were available on `PATH`. The suite stubs Node and npm subprocess calls, so these versions were observed on the host and were not exercised by the tests.

## Limitations

This is a structural/helper baseline, not a live AstrBot startup or end-to-end plugin test. Node.js and npm behavior is simulated; the suite does not run `npm install`, contact a package registry, or verify installed checker dependencies. Runtime compatibility with the project's minimum Python 3.10 version was not separately executed; validation used Python 3.13.2.
