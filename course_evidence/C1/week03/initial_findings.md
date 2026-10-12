WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# C1 initial findings

RUNTIME_TEST: NOT_RUN

Static source observations:

- `_analyze_error` scans stderr for the first line containing `Error` or `Exception`, extracts a matching exception name and a line number on that line, and keeps the first 500 characters as the message. Unrecognized output remains `Unknown` with line `0`.
- `_generate_debug_fix` returns text suggestions for recognized error categories. It does not itself change generated code.
- In the debug loop, a failed sandbox call passes stderr or an error string to those two helpers. The loop appends a `# Fixed: ...` comment to the generated code before retrying. Whether that changes the failed behavior needs Week 5+ runtime verification.
- `_save_snapshot` serializes the step, timestamp, code, and files to a JSON file under the session snapshot directory. The main flow calls it after preparing the core files and before packaging.
- `_rollback_to_snapshot` loads the newest matching snapshot by file modification time and returns its data. No call to this helper appears in the current main flow; rollback wiring and restoration behavior need Week 5+ verification.

No runtime test was executed for this stage, so no runtime result is claimed.
