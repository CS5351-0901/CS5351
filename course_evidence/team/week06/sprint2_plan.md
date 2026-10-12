# Week 6 — Sprint 2 team plan

Recorded: 2026-10-12. Target: Week 6 only. This is a team-leader planning and remote-branch review record, not a record of a team meeting or commitments made by other members.

## Sprint boundary and current baseline

- Sprint 1: Weeks 2–5; all eight Sprint 1 PRs were merged, with role Week 1–5 evidence and scoped baseline tests documented in the Week 5 closeout.
- Sprint 2: Weeks 6–9. Each role should contribute at least one non-document engineering artifact in the sprint, complete one real Week 6 role change or executable verification enhancement, and record the command/results before marking PASS.
- Member branches remain `course/a1`, `course/a2`, `course/b1`, `course/b2`, `course/c1`, `course/c2`, `course/d1`, `course/d2`. Week 6 changes stay on each member branch; the handbook schedules Sprint 2 PR review/integration at Week 9.
- At this plan's remote check, **no member branch had a `course_evidence/<ROLE>/week06/` file**. The target items below are proposed ownership-scoped engineering goals, not falsely reported completed work.

## Role-specific Week 6 review and proposed engineering backlog

| Role | Owned scope / suggested Week 6 engineering goal | Evidence and acceptance for that role | Status at team plan |
| --- | --- | --- | --- |
| A1 | Configuration / Node and npm setup: extend executable regression coverage of real preparation/failure paths; avoid altering production code without a demonstrated defect. | `course_evidence/A1/week06/change.md`, owned tests or code, actual test result, role commit/push. | Planned by leader; not yet committed at initial review. |
| A2 | AstrBot lifecycle / command orchestration: exercise a previously untested failure or cancellation path and record observed behavior. | Own Week 6 change, A2-scoped tests/verification, commit/push. | No Week 6 evidence observed. |
| B1 | Requirement extraction / classification: add a meaningful behavior or failure-path test around requirement parsing and classification boundaries. | Own Week 6 change, test command/result, commit/push. | No Week 6 evidence observed. |
| B2 | Session/state handling: verify state cleanup and repeat-request behavior with an executable regression or focused fix. | Own Week 6 change, test command/result, commit/push. | No Week 6 evidence observed. |
| C1 | Debug / snapshots: add an executable regression for a recovery or rollback edge case, or fix a confirmed owned defect. | Own Week 6 change, test command/result, commit/push. | No Week 6 evidence observed. |
| C2 | Packaging/delivery: extend regression coverage for file layout, omitted tests, or packaging failures without claiming a complete end-to-end delivery run. | Own Week 6 change, test command/result, commit/push. | No Week 6 evidence observed. |
| D1 | Sandbox and JS checker: investigate the six documented expected failures and strengthen a scoped check or fix a confirmed problem; the handbook does not demand fixing all six this week. | Own Week 6 change, actual check outcome including remaining expected failures, commit/push. | No Week 6 evidence observed. |
| D2 | Security and quality scan: add one meaningful runnable failure-path/security regression; pytest is optional, but the executed verification type must be named honestly. | Own Week 6 change, explicit test command/outcome, commit/push. | No Week 6 evidence observed. |

## Cross-role constraints and integration plan

1. Each member owns only its source areas, `course_evidence/<ROLE>/**`, and `tests/roles/<role>/**`. Shared `main.py` has method-level ownership; cross-owner edits require leader review. Team evidence and CI policy are leader-owned.
2. The main branch is protected: PRs and a passing `Check ownership` status are required. Do not bypass checks, rewrite other people's commits, or use automatic ours/theirs conflict resolution.
3. Week 5 baseline limitations remain technical debt: D1 has six intentionally expected test failures; D2's pytest run was NOT_RUN; no full live AstrBot end-to-end check was established. Track honestly rather than adding new Week 6 hard requirements absent from the handbooks.
4. Before accepting each role's Week 6 result, check actual changed files, a real non-document change/verification enhancement, relevant test output, and one current-date role commit/push. Merely creating a Week 6 Markdown document is not enough.
5. The team leader will independently review later integration against the live `origin/main` and record conflicts and blockers. Do not merge Sprint 2 member PRs before the manual's Week 9 checkpoint.

## Week 6 team-leader checkpoint

- Team Sprint 2 backlog and eight role goals: RECORDED (plan only).
- Remote status review of eight member branches: DONE; all Week 6 files absent at the time of review.
- Other seven members' Week 6 work: NOT_CLAIMED / NOT_COMPLETED_BY_LEADER.
- A1 Week 6 implementation and validation: tracked separately on `course/a1` and must not be marked PASS by this team plan.
- Week 7–9 integration and final Sprint 2 PRs: NOT_RUN (out of scope for Week 6).
