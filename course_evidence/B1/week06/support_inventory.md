# Week 6 — B1 Independent Repository Inventory

## Sequence and isolation

The original Week 6 work was validated and committed first as `485ae004296c4d6dbbf54d505d6d630d89db3cf7`. Immediately before support development, `git status --short` and `git diff --name-only HEAD` both returned no entries. The support change set contains only `course_tools/b1_support/**` and this B1 evidence file.

The five required files are `models.py`, `path_rules.py`, `file_inventory.py`, `checks/check_path_rules.py`, and `checks/check_file_inventory.py`. They use Python standard-library modules and imports within B1's own support package. They do not import plugin runtime, another role's code or tests, or any third-party package. No dependency, hook, runtime configuration, or governance file was changed. Modules perform no scanning or writes on import; the tool runs only when explicitly called.

## API and behavior

`scan_directory(directory, include=(), exclude=())` returns an immutable `InventoryResult` containing regular-file entries and structured issues. Each file entry contains a relative path, lowercase final extension, and byte size. `total_files`, `total_size_bytes`, and `extension_counts` summarize the selected entries. Files and issues are sorted by relative path; results contain no machine root path.

- Relative-path rules normalize separator and dot segments, preserve Unicode and filename spaces, and reject absolute paths, parent traversal, and NUL bytes.
- A glob without slashes matches basenames at any depth. A glob with slashes is root-relative; `**` matches zero or more directory segments. Matching is case-sensitive, and exclusions win over inclusions. Excluded directories are pruned.
- An empty directory produces an empty result. Missing roots raise `FileNotFoundError`; file roots raise `NotADirectoryError`; symlink roots are rejected.
- Symlinks and special files are skipped and reported. Nonportable POSIX names that would become path aliases are also skipped and reported. Scan/stat failures have stable relative-path issue records and errno values.
- File size comes from metadata; the scanner does not open file contents or write reports. An inventory is not a transactional snapshot if another process changes the input during scanning.

Explicit use from the course repository:

```python
from course_tools.b1_support.file_inventory import scan_directory

result = scan_directory(
    ".", include=("*.py",), exclude=(".git/**", "**/__pycache__/**")
)
print(result.total_files, result.total_size_bytes, result.extension_counts)
```

## Executed validation

- `python3 -B -m unittest discover -s course_tools/b1_support/checks -p "check_*.py" -v` — PASS, 22 checks; all executed without skips on this environment.
- Compilation of all five support Python files — PASS.
- AST import/module-side-effect audit — PASS; standard-library/own-support imports only, no network imports, no executable module-level scanning, and no default `test_*.py` discovery files.
- Explicit scan of `course_tools/b1_support`, excluding caches — PASS: 5 Python files, 17,697 bytes, zero issues, stable relative ordering. No report file was written.
- Original B1 suite rerun after support development — PASS, 10 tests.
- Read-only fixture checks verify repeated scans return equal results, input bytes and modification times remain unchanged, and file-content reads are unnecessary.

The required post-commit isolation command is `git show --name-only --format="" HEAD`; the support-only commit must contain only the support directory and B1 evidence. Remote push is deferred for user review.

## Current integration-policy mismatch

The ownership guard in the current course `main` does not yet include the new manual's `course_tools/b1_support/**` exception. Calling its `allowed("b1", path)` rule for each of the five support files returned false. Thus the current PR ownership CI would reject the support paths even though they meet the replacement manual's isolation rules.

No governance files were changed or checks bypassed. Before the Sprint 2 PR at Week 9, the team leader needs to reconcile the guard with the revised B1 support ownership. This is a recorded integration limitation; it is not reported as an ownership CI PASS.
