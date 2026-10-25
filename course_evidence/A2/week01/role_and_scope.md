WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Week 1 — A2 Role and Scope

A2 owns AstrBot integration and main orchestration in `main.py`:

- `CodeAgentPlugin`: connect the plugin lifecycle to the AstrBot context and configuration.
- `/agent` and `agent_command`: coordinate request handling, execution, checking, snapshots, packaging, and replies.
- `terminate`: handle plugin shutdown and active-session cleanup.
- `get_star`: provide the plugin factory entry.

Week 1–4 personal branch commits provide role evidence only under `course_evidence/A2/**`. They do not change business source, tests, configuration, or another role's evidence.

The shared `main.py` also contains helpers owned by other roles. Configuration and environment preparation remain with A1; requirement handling with B1; session state with B2; debug and snapshots with C1; packaging with C2; sandbox and JS checking with D1; and security and quality with D2. Later A2 changes must respect these function boundaries and the review rules.
