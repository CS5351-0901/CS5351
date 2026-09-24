WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# A1 source map for the current course main branch

- `metadata.yaml`: plugin identity, AstrBot compatibility declaration, entry point, supported platforms, and tags.
- `_conf_schema.json`: plugin settings for network access and whitelist, knowledge use, user and group blacklists, debug rounds, model selection, execution time, quality threshold, memory, and file size.
- `pyproject.toml`: package identity, Python requirement, runtime dependencies, and optional development dependencies.
- `main.py` configuration reads: `_get_config` delegates to the AstrBot config object. Current call sites read `admin_blacklist`, `group_blacklist`, `code_running_time`, `memory_limit`, `max_file_size`, `max_debug_rounds`, and `quality_threshold`.
- `main.py` Node.js preparation: `_ensure_nodejs` checks `node -v`, then dispatches to Linux or macOS installation helpers; other systems reach the unsupported-system path.
- `main.py` checker dependency preparation: `_ensure_js_dependencies` locates the checker and package manifest, checks Node.js, and runs npm installation when `node_modules` is absent.

This map covers the current course main branch source relevant to A1. It is a static map, not runtime verification.
