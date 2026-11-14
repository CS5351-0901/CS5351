# Week 10 — B1 Snapshot Comparison and Duplicate Reports

Original B1 improvement passed its tests and was committed first as `408c7e2`. The working tree and `git diff --name-only HEAD` were empty before starting the support extension.

- `snapshot_compare.py` compares two generic mappings with a `files` list, including Week 8 manifest output. It reports added, removed, and changed paths, old/new hashes and sizes, per-entry byte deltas, and total byte delta. It normalizes relative paths, rejects malformed entries and duplicate normalized paths, and ignores unrelated metadata. A missing hash becoming known or vice versa changes the recorded hash, but does not prove a change in bytes.
- `duplicate_finder.py` groups two or more paths with the same recorded SHA-256 and byte size. It supports case-insensitive extension selection and inclusive minimum/maximum sizes before grouping. Unknown hashes are excluded. Results are deterministic and describe the snapshots supplied by the caller; they do not revalidate live files.

Example with previously generated manifests:

```python
from course_tools.b1_support.snapshot_compare import compare_snapshots
from course_tools.b1_support.duplicate_finder import find_duplicates

delta = compare_snapshots(previous_manifest, current_manifest)
groups = find_duplicates(current_manifest, extensions=(".py",), min_size=1)
```

Neither module reads, deletes, repairs, or rewrites source files. Both return reports in memory and use only the standard library and B1's own support modules. No dependency, CLI hook, plugin runtime, or other role is changed.

Executed validation:

- `python3 -B -m unittest discover -s course_tools/b1_support/checks -p "check_*.py"` — PASS, 72 checks (62 existing and 10 new). Covers path/hash/size changes, invalid manifests, ordering, duplicate filters, and read-only behavior against Week 8 manifests.
- `python3 -B -m unittest discover -s tests/roles/b1` — PASS, 17 tests after support development.
- Python compilation of the two new modules and their two checks — PASS.

The support commit contains only the four support Python files and this B1 evidence file. The final commit paths are checked with `git show --name-only --format="" HEAD`; no Week 11 work is included.
