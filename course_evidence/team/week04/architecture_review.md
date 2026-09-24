# Week 4 architecture review

`main.py` is now in the course repository, so orchestration, session handling, sandboxing, security review, JavaScript/TypeScript checking, packaging, and debug snapshots can be reviewed together at source level.

## Static component relationships

- `metadata.yaml` names `main:CodeAgentPlugin` as the entry point. `CodeAgentPlugin` stores the AstrBot config, creates a workspace and active-session map, derives the scripts directory, and starts Node.js and checker-dependency preparation during initialization.
- `_get_config` is the central read path used by blacklist checks, sandbox limits, debug-round limits, and quality thresholds. `_conf_schema.json` declares those settings alongside network, knowledge, and model settings; a complete schema-to-runtime mapping remains to be checked.
- The `/agent` command extracts a request and classifies project type and size, creates `process.json`, and enters a debug loop. The loop invokes the sandbox, then selects the security scanner or JavaScript/TypeScript checker, saves a `core_complete` snapshot, and calls the packager.
- `codeagent_sandbox.py` provides execution and resource-control paths. `codeagent_security.py` reports security and quality findings. `codeagent_js_checker.js` handles the JavaScript/TypeScript check path. `codeagent_packager.py` prepares project output and dependencies.
- Snapshot saving and lookup helpers are present. Static call-site review shows the command saves a snapshot; a call to `_rollback_to_snapshot` is not evident in the command flow.

Static review is not evidence that all runtime tests pass. The skill contract's confirmation and interruption-recovery expectations also need comparison with the current orchestration behavior.
