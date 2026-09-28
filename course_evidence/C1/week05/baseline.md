# C1 Week 5 executable baseline

Engineering artifacts:

- `tests/roles/c1/test_baseline.py` adds six standard-library `unittest` cases for error parsing, repair suggestions, and snapshot save/rollback behavior. It imports the real `main.py` with minimal AstrBot import stubs and does not initialize the plugin.
- `main.py::_generate_debug_fix` now recognizes `ModuleNotFoundError` when suggesting a missing dependency. The first test run exposed that the previous `Import` substring check missed this common exception name.

Validation performed:

```text
python -m unittest discover -s tests/roles/c1 -p 'test_*.py' -v
RESULT: PASS (6 tests)
```

Scope and limits:

- The tests exercise the owned helpers directly. They do not claim an AstrBot or end-to-end sandbox run.
- The debug loop still appends repair suggestions as comments, and the main flow still has no rollback call site. Those integration behaviors remain for later engineering work.
