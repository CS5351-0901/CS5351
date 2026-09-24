# Week 4 static technical debt update

This update records source observations and later validation items. It does not mark unrun tests as passed.

- The schema declares network access, a network whitelist, knowledge use, and model-selection settings that are not read by the current `main.py` configuration call sites found in static review. Verify intended behavior and configuration-to-runtime mapping.
- `_ensure_nodejs` handles Linux and macOS installation paths but reports unsupported systems for other platforms, including Windows. The Windows Node.js setup and dependency-preparation path needs real testing and a supported behavior decision.
- Plugin initialization calls Node.js setup and JavaScript checker dependency installation synchronously. The npm path has a timeout, but startup duration, permissions, network failure, and pre-existing incomplete `node_modules` need validation.
- The skill contract requires confirmation after requirement analysis and scaffold generation. The current command sends a confirmation prompt, sleeps briefly, then continues without an observed confirmation wait. Check and align the interaction before treating the contract as implemented.
- The skill contract describes resuming from `process.json`, while the current orchestration creates process state but has no evident load-and-resume path. `_rollback_to_snapshot` is defined but has no evident call in the command flow.
- `_call_security_scan` and `_call_js_checker` return permissive success-shaped results for some missing-tool, exception, or timeout cases. Failure-path behavior needs tests and a review of whether fail-open results are acceptable.
- The orchestration uses `python3` for helper scripts. Verify interpreter discovery on Windows and other target environments.

All items above are static findings or proposed later validation; no runtime tests are reported as passed.
