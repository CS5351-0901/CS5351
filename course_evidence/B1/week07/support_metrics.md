# Week 7 — B1 Independent Text and Source Metrics

## Sequence and isolation

Original Week 7 verification was completed first in commit `ddd7e3814e8bf1c3f7d595957411f9e195aa0648`; the original ownership check passed for its two files. Before support development, `git status --short` and `git diff --name-only HEAD` were both empty. This support-only change adds the four required Python files and this B1 evidence document. Existing inventory modules and role/runtime files are unchanged by the support task.

## Modules and contracts

- `text_metrics.py` provides `analyze_text_bytes` and `analyze_text_file`. Results include original-byte SHA-256 and size, total/blank/nonblank lines, maximum line length, and mean line length. Line splitting recognizes LF, CRLF, CR, and Python's other text separators without adding a phantom final line. Blank means whitespace-only. Length is measured in Unicode codepoints, includes blank lines, and excludes separators; empty input has zero counts and lengths.
- `source_stats.py` provides `analyze_source_bytes(data, kind="python" or "json")` and `analyze_source_file`. Python AST counts include nested classes, synchronous functions, and async functions separately. JSON reports parse status and the top-level value type; object key counts count unique parsed keys and exclude nested objects. Non-object JSON has no applicable key count. Nonstandard NaN/Infinity constants are rejected.
- Both modules accept strict UTF-8 with an optional BOM. BOM bytes remain part of the raw-byte hash but not text length. The binary-control heuristic, invalid UTF-8, syntax errors, unreadable files, and nonregular files have explicit statuses. Unavailable counts are `None`, rather than zero. Error records contain errno/parse positions where available and omit exception text, source excerpts, and machine paths.
- Only regular files are read. The source file API supports `.py` and `.json` case-insensitively and does not open unsupported file types. Source is parsed, never imported, evaluated, or executed. Inputs are read wholly into memory; metrics are not designed as a bounded-memory streaming or hostile-code sandbox service.

Explicit use from the repository:

```python
from course_tools.b1_support.text_metrics import analyze_text_file
from course_tools.b1_support.source_stats import analyze_source_bytes

text = analyze_text_file("course_tools/b1_support/text_metrics.py")
source = analyze_source_bytes(b'{"example": 1}', kind="json")
print(text.total_lines, text.sha256, source.top_level_key_count)
```

## Executed validation

- `python3 -B -m unittest discover -s course_tools/b1_support/checks -p "check_*.py" -v` — PASS, 44 checks: 22 existing inventory/path checks plus 22 new text/source checks. No skips.
- Compilation of the four new Python files — PASS.
- AST import/module-side-effect audit across B1 support — PASS: only standard-library and own-support imports, no network imports, no executable module-level scanning, no default `test_*.py` check filenames.
- Explicit metrics smoke check on the new text module — PASS: 77 total lines, 13 blank, 64 nonblank; Python AST reported 1 class, 4 synchronous functions, and 0 async functions. A generic JSON byte fixture reported 2 top-level keys. No output file was created.
- Original B1 helper regression rerun after support development — PASS, 14 tests.
- Fixtures cover empty/whitespace/multiline/Unicode text, raw-byte hashes, BOM, binary controls, invalid UTF-8, nested Python definitions, parsing without execution, Python/JSON syntax errors, JSON value types, duplicate keys, missing files, and read-only behavior.

The support-only staged paths and resulting commit must be audited against the allowed prefixes `course_tools/b1_support/**` and `course_evidence/B1/**`; the post-commit command is `git show --name-only --format="" HEAD`. Push is deferred for user review. No Week 8 files, CLI, report writer, hook, dependency, or project-runtime integration is introduced.

## Integration limitation carried forward

Remote `main` remains at the Week 6 baseline inspected previously. Its ownership guard still lacks the replacement manual's support-directory exception, as documented in Week 6. This task does not modify leader-owned governance files or claim the future PR CI will pass. The team leader must reconcile the support directory rule before the Week 9 Sprint 2 PR.
