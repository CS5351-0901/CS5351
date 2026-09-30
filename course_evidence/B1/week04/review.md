# Week 4 — B1 Integration Review

This review covers the current staged integration baseline and is limited to static source inspection. It is not a runtime validation report.

## Call sites and dependencies

`CodeAgentPlugin.agent_command` obtains the message, user ID, and group ID from the AstrBot event. It first calls `_is_in_blacklist`; a denied request returns without entering the remaining workflow. After exit-command handling, it calls `_extract_requirement`. A missing or empty result prevents session creation and may produce the request-description prompt. Once a request is accepted and a session is registered, the command calls `_assess_project`.

The assessment result supplies the `project_type` and `project_size` values used by status output, process metadata, scaffold behavior, language selection, checking paths, and packaging. Consequently, later B1 changes must preserve the helper signatures and the assessment dictionary keys expected by the orchestration code.

`_is_in_blacklist` depends on `_get_config`, which is outside B1 ownership. `_extract_requirement` and `_assess_project` depend on Python string and regular-expression behavior. Adjacent session, cleanup, process, snapshot, sandbox, security, checker, and packaging methods remain outside B1 ownership.

## Week 1–4 scope check

The prepared B1 change set contains only `course_evidence/B1/week01` through `course_evidence/B1/week04`. No business source, test, script, configuration, or another role's evidence has been changed. Week 5 is the first stage that should add executable B1 tests and make any evidence-backed behavior correction.

RUNTIME_TEST: NOT_RUN
