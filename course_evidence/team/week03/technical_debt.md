WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Static observations and later validation items

This list records source observations only. It does not mark unrun tests as passed.

- Sandbox controls are represented in code, but enforcement and isolation strength need runtime checks for each supported operating system and execution mode.
- Resource limits have boundary behavior that needs tests at, below, and above the configured wall-time, memory, file-size, total-size, and file-count limits.
- Security and quality results depend in part on external tools being available. Verify missing-tool behavior and result reporting for Ruff, Mypy, Bandit, ShellCheck, ESLint, and TypeScript.
- Packager dependency discovery is static and heuristic. Validate Python and Node dependency detection against standard-library imports, project-local modules, scoped packages, and malformed inputs.
- `package.json` declares ESLint and TypeScript as development dependencies. Verify installation behavior, version compatibility, and checker startup when dependencies are absent or installation fails.
- At this repository stage `main.py` is not present, so plugin-to-script wiring, configuration propagation, and end-to-end orchestration remain to be reviewed after integration.

Later validation items are open; none of the runtime items above is reported as passed.
