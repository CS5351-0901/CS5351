WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# C1 source map

This map reflects the current course `main` source.

| Owned area | Location and role |
| --- | --- |
| Error analysis | `main.py::_analyze_error` extracts an exception type, line number, and abbreviated error message from stderr. |
| Debug fix suggestion | `main.py::_generate_debug_fix` maps recognized error types and messages to a textual repair suggestion. |
| Snapshot save | `main.py::_save_snapshot` writes code and file metadata to a session snapshot JSON file. |
| Snapshot rollback | `main.py::_rollback_to_snapshot` loads the newest JSON snapshot matching a step, or returns `None`. |
| Debug loop | `main.py::agent_command` calls the sandbox, analyzes failures, emits a suggested fix, and retries up to the configured round limit. |
