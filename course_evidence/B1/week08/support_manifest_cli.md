# Week 8 — B1 Manifest, Reports and CLI

## Sequence and scope

Original integration review was committed first as `28410435a32abcfd5b5fb38cf806e75cae03d6a0`. Before starting support work, `git status --short` and `git diff --name-only HEAD` were empty. This support-only commit adds three modules, their three explicit check files, and this B1 evidence document. No runtime, role test, dependency, hook, or governance file is changed by the support commit.

## Features and usage

`manifest_builder.py` produces schema-versioned, sorted relative-path records without timestamps or machine root paths. Scan detail uses metadata only; manifest detail adds raw-byte SHA-256; stats detail adds the existing text and Python/JSON analysis. Summary totals describe selected entries. Input mutation during a scan is not a transactional snapshot guarantee.

`report_writer.py` renders stable JSON, CSV, and Markdown summaries. CSV escapes filename formulas and Markdown escapes table separators, line breaks, and HTML. File writes require an explicit output. Resolved destinations must be system temporary storage, `course_evidence/B1/**`, or `course_tools/b1_support/.tmp/**`; runtime, other-role, and generic repository destinations are rejected. Existing outputs and output symlinks are refused rather than overwritten. Parent directories are created only after validating the destination and rendering the report.

`cli.py` supports direct-script invocation from any working directory and module invocation. It performs no scan or write on import. Each subcommand requires `--output`; `--help` requires none. It supports repeatable `--include`/`--exclude` globs and `--format json|csv|markdown`. The selected output path is omitted from its own inventory when it lies inside the input tree. Successful stdout and filesystem error messages omit machine paths. Other existing reports inside an input directory should be explicitly excluded if they are not intended as input.

Examples from the course repository (choose a new output filename):

```bash
python3 -B course_tools/b1_support/cli.py --help
python3 -B course_tools/b1_support/cli.py scan course_tools/b1_support --exclude '**/__pycache__/**' --output course_evidence/B1/week08/scan.json
python3 -B course_tools/b1_support/cli.py manifest course_tools/b1_support --exclude '**/__pycache__/**' --output course_evidence/B1/week08/manifest.json
python3 -B course_tools/b1_support/cli.py stats course_tools/b1_support --exclude '**/__pycache__/**' --format markdown --output course_evidence/B1/week08/stats.md
```

## Executed validation

- `python3 -B -m unittest discover -s course_tools/b1_support/checks -p "check_*.py" -v` — PASS, 62 checks: 44 existing plus 18 new. An initial check had an incorrect fixture repository-parent index; the fixture was corrected and the complete suite passed.
- `python3 -B course_tools/b1_support/cli.py --help` — PASS.
- Compilation of all six new Python files — PASS.
- Standard-library/own-package import and module-side-effect AST audit — PASS across support code. No plugin runtime, other-role, third-party, or network imports.
- Direct CLI scan/manifest/stats smoke runs against B1's production support modules, excluding check/cache directories — PASS: each selected 8 Python files, 22,874 bytes, zero inventory issues; stats reported 545 lines. Reports were written only inside a temporary fixture and were not committed.
- B1 helper regression rerun after support work — PASS, 14 tests.

Checks cover content-independent scan mode, stable manifests across different machine roots, hashes, source statistics, filters, omission, structured failures, all report formats, path escaping, destination restrictions, symlink escape rejection, existing-file preservation, help, required output, invalid input, and subprocess execution outside the repository working directory.

The post-commit isolation gate is `git show --name-only --format="" HEAD`; only B1 support and B1 evidence paths are permitted. No Week 9 artifacts or PR are created. The updated main policy now authorizes the support directory; actual remote PR CI remains a Week 9 gate, not a claimed result here.
