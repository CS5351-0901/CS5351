WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Week 2 — A2 Owned Source Map

This map is based on static inspection of the current course `main` baseline. Line numbers describe that baseline and may move after later integration.

| Component | Baseline location | Inputs and dependencies | Output and responsibility |
| --- | --- | --- | --- |
| `CodeAgentPlugin(Star)` and `__init__` | `main.py`, lines 25–38 | AstrBot context and config, workspace, script directory, environment helpers | Creates plugin state and invokes Node.js and checker dependency preparation. |
| `/agent` registration and `agent_command` | `main.py`, lines 478–684 | AstrBot event, requirement and session helpers, execution and checking wrappers, snapshot and packaging helpers | Coordinates the workflow and yields text or file replies. |
| `terminate` | `main.py`, lines 686–691 | Active-session map and cleanup helper | Marks active sessions inactive, cleans their directories, and clears the map. |
| `get_star` | `main.py`, lines 694–695 | AstrBot context | Returns a plugin instance; its arguments need comparison with the constructor signature. |

`metadata.yaml` declares `main:CodeAgentPlugin` as the entry point. Metadata, configuration reads, and environment preparation are adjacent A1 responsibilities.

The command calls `_call_sandbox`, `_call_security_scan`, `_call_js_checker`, and `_call_packager` to connect the helper scripts. Requirement, session, debug, and snapshot helpers also supply inputs and state to the command. A2 review focuses on the call order, interface expectations, replies, and lifecycle behavior.

This is a static source map, not runtime verification.
