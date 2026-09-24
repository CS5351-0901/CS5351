WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# A1 initial static findings

## Metadata and package boundaries

- `metadata.yaml` declares the plugin identity, entry point, compatible AstrBot version, and supported platforms.
- `_conf_schema.json` declares typed settings and defaults for access, optional network and knowledge features, model selection, and execution/resource thresholds.
- `pyproject.toml` declares Python 3.10 or newer and the package's runtime and development dependencies.

## Configuration versus implementation points for later validation

- Static call-site review shows `main.py` reads blacklist, execution time, memory, file size, debug-round, and quality-threshold values through `_get_config`.
- Network, whitelist, knowledge-use, and model-selection values are declared in the schema but do not appear among the current direct configuration reads found in `main.py`. Confirm whether these settings are intended to affect orchestration.
- Verify types, defaults, units, and boundary behavior across the schema, plugin config object, serialized sandbox configuration, and sandbox settings.

## Later Windows Node.js and dependency-preparation items

- Test the Node.js-present path and the Node.js-missing path on Windows. The current installer dispatch has Linux and macOS branches and an unsupported-system path for Windows.
- Test checker dependency preparation with npm available and unavailable, dependencies missing, npm failure, timeout, and an existing `node_modules` directory.
- Confirm that plugin startup behavior remains understandable when Node.js or checker dependencies are unavailable.

These are static source observations and proposed validation items only.

RUNTIME_TEST: NOT_RUN
