WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Non-functional requirements and architecture notes

These notes describe source-level mechanisms present in the Week 3 scripts and package metadata. They are not runtime test results.

## Security

- The sandbox configuration defaults network access off and enables restricted Python execution when the optional RestrictedPython support is available.
- The execution configuration includes wall-time, memory, per-file size, total output size, and file-count limits.
- The security module collects static-analysis and dangerous-pattern findings for supported languages; the shell path can use ShellCheck.
- These controls need execution, bypass, and missing-tool validation before their effective protection can be established.

## Reliability

- The sandbox runs work in per-session directories and returns execution results, output, and errors through structured result data.
- Subprocess execution has a configured wall-time bound, and the sandbox records elapsed time and reports timeout outcomes.
- The packager generates project metadata and installation or usage instructions from project information.
- Error handling, cleanup, interrupted execution, and package-install failure paths need runtime coverage.

## Performance / Resource Control

- `SandboxConfig` defines defaults of 120 seconds wall time, 512 MB memory, 10 MB per file, 50 MB total output, and at most 50 files.
- The execution result checks file sizes and total output after execution; generated dependency installation also invokes package-manager subprocesses.
- Limit enforcement and dependency-install duration should be measured on supported platforms and with boundary-size inputs.
