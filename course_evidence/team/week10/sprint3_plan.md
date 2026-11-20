# Team Week 10 — Sprint 3 engineering plan

Recorded: 2026-11-20 (Asia/Singapore). Prepared during the leader's Week 10–11 catch-up. This is not a claim that a meeting or earlier Week 10 review happened.

## Baseline, scope and integration boundary

Sprint 2 was closed on protected `main` via team [PR #26](https://github.com/CS5351-0901/CS5351/pull/26), with 8/8 role PRs merged. Sprint 3 spans Weeks 10–13. Team-owned planning stays under `course_evidence/team/**`; members implement and test only their own owned methods, scripts and role support directories. Do not make Week 13 Final PRs before the completed final evidence and integration checks.

Week 10 work is a genuine second engineering increment, not solely Markdown. Each role should independently submit at least one source/test/checker/script/config artifact, together with evidence of actually executed validation. Week 11 focuses on regression, failure paths, cleanup and source metadata leakage; Week 12 gathers presentation/report evidence; Week 13 reviews and merges final role PRs one at a time after tests and required ownership checks.

## Role ownership and focus

| Role | Sprint 3 engineering focus | Interface / validation concern |
| --- | --- | --- |
| A1 | Node/npm startup readiness, configuration and dependency setup | Incomplete `node_modules` must not be treated as complete; preserve D1 sandbox config-file contract |
| A2 | `agent_command` orchestration, cancellation and session lifecycle | Multi-user and exceptional teardown must not leak state |
| B1 | Requirement extraction / project assessment and isolated V3 `b1_support` tools | Input boundaries, inventory/dedup reporting, UTF-8 test environment |
| B2 | Input cases and isolated V3 `b2_support` fixtures, corpus and manifest tools | Deterministic outputs and zero cross-role/runtime imports |
| C1 | Snapshot / rollback and output fault recovery | Different sessions/steps cannot overwrite each other's recovery points |
| C2 | Output, packaging and regression checks | Archive contents, counts and end-to-end handoff to orchestration |
| D1 | Sandbox and JavaScript checker adapters | Temporary config files, CLI exit behavior, Windows Unicode and timeout paths |
| D2 | Security scanner and fail-closed checks | Syntax failures, temporary files, external checker cleanup and risk schema |

The existing protected `main` interface contracts should remain stable across role branches. If multiple members propose the same `main.py` method edit, stop and review rather than silently resolve merge conflicts.

## Actual remote progress observed during this catch-up

At the 2026-11-20 audit, role evidence was: A1 Week 11; B1 and B2 Week 10; D2 Week 11; A2, C1, C2 and D1 Week 9. Therefore, 4/8 branches have submitted Week 10 engineering/evidence, and 4/8 still lack Week 10 submissions. This is a current observation, not a backdated Week 10 acceptance.

- A1 Week 10: concrete fix and five new tests for incomplete JS dependencies (`b59ef6f`), followed by Week 11 tests (`e3ecb44`).
- B1 Week 10: inventory snapshot and duplicate report checks in its own support directory.
- B2 Week 10: artifact manifest and corpus difference checks in its own support directory.
- D2 Week 10: security scanner and syntax-checking improvements with new tests.

The leader will preserve all members' Week 10 work in their own branches until the Week 13 final PR checkpoint; no early member Sprint 3 PR integration is implied.

## Remaining risks

Live AstrBot end-to-end behavior, real Linux/macOS Node installers, concurrent operational sessions and genuine npm installation are not proven by the current mock-heavy role suites. D2's new pytest fixture-based cases need a suitable pytest environment to be independently rerun. B1's platform skips must remain labeled skips, not passes. Report unrun checks as NOT_RUN.

TEAM_WEEK10_SPRINT3_PLAN: DOCUMENTED
TEAM_WEEK10_ENGINEERING_MEMBERS_WITH_EVIDENCE: 4/8
TEAM_WEEK10_ALL_MEMBERS_COMPLETE: NO
WEEK12_WEEK13_ARTIFACTS: NOT_CREATED
