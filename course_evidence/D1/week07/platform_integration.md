# D1 — Week 7 platform and integration hardening

Date: 2026-10-25
TARGET_WEEK: 7
BRANCH: course/d1

## Completed work

- D1-006: Unix-only `resource` and `SIGALRM` usage is now conditional. The
  sandbox imports and displays `--help` on Windows instead of failing during
  module import.
- On platforms without `SIGALRM`, Python execution does not use the in-process
  RestrictedPython path whose timeout depends on that signal. It uses the
  subprocess executor, whose child process is stopped by
  `subprocess.communicate(timeout=...)`.
- The sandbox invokes Python with `sys.executable` instead of the unavailable
  Windows command name `python3`.
- `workspace_root` is normalized to a resolved `Path` before subprocess
  environment construction. Its temporary directory is created before use.
- The sandbox preserves the Windows process `PATH`; the restricted Unix-style
  PATH remains in effect only on non-Windows platforms.
- Each JavaScript checker invocation creates a unique temporary directory with
  `fs.mkdtempSync` and cleans up only that directory.
- Checker tool discovery prefers the project-local `node_modules/.bin` entries
  and falls back to an available global ESLint or TypeScript command. ESLint and
  TypeScript arguments are passed without interpolating a file path into a shell
  command string.
- The `Function` constructor security rule now uses a word boundary, so camel-case
  identifiers such as `safeFunction` are not reported as dynamic code execution.

## Executable evidence

The D1 suite now covers the previously known failure paths plus:

- a real Windows sandbox command with multiline Unicode input and a configuration
  path containing spaces;
- a real adapter-to-sandbox subprocess integration test, including raw multiline
  Unicode source and Windows execution;
- a workspace path containing spaces;
- the current Python interpreter being used by both adapter and sandbox;
- two checker instances owning independent temporary directories;
- temporary sandbox configuration cleanup after the child returns.

Validation commands and observed results:

```text
python -B -m unittest discover -s tests/roles/d1 -p test_*.py -v
25 tests, OK

python -B -m unittest discover -s tests/roles/b1 -p test_*.py -v
7 tests, OK

node --check skills/CodeAgent/scripts/codeagent_js_checker.js
exit code 0

git -c core.whitespace=cr-at-eol diff --check
no whitespace errors; CRLF notice only
```

Python files were parsed with `ast.parse` without writing bytecode cache files.

## Limits

- A live AstrBot startup, event dispatch, and complete `/agent` session were not
  run.
- The Windows resource-limit implementation is a no-op because the Python
  `resource` module is unavailable. The sandbox therefore does not claim enforced
  CPU, memory, or process limits on Windows.
- Network isolation and whitelist enforcement remain unverified.
- A1's Week 5 sandbox configuration assertion still expects inline JSON and must
  be migrated by its owner to the new readable-file contract.
- ESLint and TypeScript correctness were not exercised because their local
  `node_modules` dependencies are not installed in this checkout. Missing-tool
  reporting and project-local discovery behavior are covered structurally.
- Commit `e74446e0f2f816df18f3536330607a4f846a5029` was pushed to
  `origin/course/d1`. The follow-up commit containing this automated adapter
  integration test and evidence correction is reported in the delivery response.
- Sprint 2 PR #15 is open at
  `https://github.com/CS5351-0901/CS5351/pull/15`. Its final ownership result and
  D2 review are not claimed here; Sprint 2 integration is scheduled for Week 9.
