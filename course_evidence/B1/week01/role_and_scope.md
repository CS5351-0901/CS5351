WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Week 1 — B1 Role and Scope

This retrospective record defines B1's responsibility from the current Week 4 course baseline. It does not claim that this document or any B1 implementation existed during Week 1.

B1 owns the following helpers in `main.py`:

- `CodeAgentPlugin._extract_requirement`: identify and return the requirement text associated with an `/agent` command.
- `CodeAgentPlugin._is_in_blacklist`: decide whether a user or group identifier appears in the configured deny lists.
- `CodeAgentPlugin._assess_project`: classify a requirement by project type and estimated size.

Through Week 4, the B1 branch is limited to role evidence under `course_evidence/B1/**`. It does not modify business source, tests, configuration, scripts, or another role's evidence. From Week 5 onward, any shared `main.py` edit must remain inside the three named method bodies and follow the ownership and review rules.

No implementation change or runtime validation is asserted for this retrospective stage.
