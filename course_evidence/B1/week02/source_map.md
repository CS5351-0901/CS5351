WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Week 2 — B1 Owned Source Map

This source map is based only on static inspection of the current course `main` baseline. Line numbers describe that baseline and may move after later integration.

| Owned method | Baseline location | Inputs and dependencies | Output and responsibility |
| --- | --- | --- | --- |
| `CodeAgentPlugin._extract_requirement` | `main.py`, lines 43–52 | Message text and Python regular expressions | Returns trimmed text captured after an `/agent` trigger, or `None` when neither trigger pattern matches. |
| `CodeAgentPlugin._is_in_blacklist` | `main.py`, lines 60–67 | User ID, group ID, `_get_config`, `admin_blacklist`, and `group_blacklist` | String-normalizes identifiers and returns whether either configured deny list contains the request context. |
| `CodeAgentPlugin._assess_project` | `main.py`, lines 401–428 | Requirement text and ordered string checks | Returns a dictionary containing a project `type` and a character-count-based `size`. |

The three helpers share `main.py` with methods owned by other roles. B1 verification files belong under `tests/roles/b1/**`, while B1 weekly evidence belongs under `course_evidence/B1/**`.

No runtime checks were performed for this reconstructed Week 2 stage.
