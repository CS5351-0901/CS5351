# C1 Week 7 contract and boundary verification

## Check added

Snapshot `step` is used to form a filename and a glob pattern. Static review found that path syntax could affect the save location and glob metacharacters could make rollback select a differently named step.

`main.py` now accepts only step identifiers made of letters, digits, underscores, and hyphens. Saving an invalid step raises `ValueError`; rollback with an invalid step returns `None`. Two C1 regression tests cover a wildcard rollback request and a path-like save request.

## Validation performed

```text
python -B -m unittest discover -s tests/roles/c1 -p 'test_*.py' -v
RESULT: PASS (10 tests)
```

The first in-sandbox run could not write Python's system temporary directory. The same command was rerun with the required filesystem permission; all 10 tests passed. The tests use temporary snapshot data and AstrBot import stubs, so they do not claim an end-to-end bot run.
