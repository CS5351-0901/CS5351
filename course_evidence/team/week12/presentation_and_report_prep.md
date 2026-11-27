# Team Week 12 — Presentation and final report preparation

Recorded: 2026-11-27. Prepared from the eight members' committed Week 12/13 evidence and course PRs after refreshing the remote. This is presentation preparation, not a claim that the final presentation or system demonstration has occurred.

## Contributions for slides and report

| Role | Owned module/interface | Concrete engineering and solved problem | Member-reported final validation (independent leader rerun in Week 13) | Remaining limitation |
| --- | --- | --- | --- | --- |
| A1 | Metadata, configuration and Node/npm preparation | Configuration/installer regression coverage; incomplete node_modules no longer suppresses dependency installation, recovery and manifest cases added. | 38 role tests | Real installs, versions/integrity and live startup unverified. |
| A2 | AstrBot factory and agent orchestration | Factory config forwarding and identity-aware session cleanup; new state-write, packaging exception and cancellation tests. | 29 role tests | Real event delivery, subprocess cancellation and live bot unverified. |
| B1 | Requirement extraction, blacklist and project assessment; independent V3 support | Preserve multiline input, reject blank/command-like fragments, normalize input, use whole-token aliases rather than substrings; independent inventory/metrics/manifest/diff/duplicate/health tools. | 19 role tests; 77 support checks | Fixed classification rules, manifest freshness, static audit limitations. |
| B2 | Session/state helpers; independent V3 support | Baseline and boundary/failure-path tests for session handling and process JSON; deterministic case generation, result aggregation, artifact manifests, corpus diff and self-audit. | 34 role tests; 81 support checks | Business source unchanged by B2; cleanup and exit-command behavior limitations retained. |
| C1 | Debug/snapshot/rollback | Collision-resistant snapshot names, step-boundary tests and deterministic same-time snapshot regression. | 11 role tests | Rollback helper has no call site in the main debug flow; end-to-end restoration unverified. |
| C2 | Packaging and delivery | Correct empty/nested test layout and ZIP counts; isolate staging/output per attempt, remove partial ZIPs on failure and report cleanup denial. | 33 role tests | Live subprocess/npm/extracted startup, hostile paths and multiprocess behavior unverified. |
| D1 | Sandbox and JS checker | Raw code and temporary JSON config contract, Windows compatibility, checker temp isolation, returned artifact-count cap, CLI/failure regressions. | 34 role tests | Real OS isolation/resource limits and installed external JS analysis tools unverified. |
| D2 | Security, quality and scanner tests | Built-in shell dangerous-pattern checks, lowercase risk serialization, dependency-independent Python syntax rejection and temporary checker source cleanup. | 18 pytest tests in member environment | Optional external checker availability, heuristic detection and live integration limits. |

Evidence: each role's course_evidence/<ROLE>/week12/presentation_notes.md and week13/final_summary.md. V3 B1/B2 tooling is independent of plugin runtime; its checks are intentionally executed separately from role suites. Counts above are member-recorded outcomes, not newly executed team results.

## Presentation structure

1. Problem and project scope: CodeAgent is an AstrBot coding-workflow plugin; explain the requirements-to-delivery flow and the course's three incremental sprints.
2. Architecture: A2 entry/orchestration calls B1 assessment and B2 session/state; D2 scans generated code; D1 executes/checks it; C1 snapshots/debugs; C2 packages; A1 supplies config and environment preparation.
3. Engineering before/after examples: A1 incomplete npm installation, A2 cancellation cleanup, B1 token classification, C1 same-time snapshots, C2 overlapping ZIP attempts, D1 artifact caps, D2 invalid Python and checker temp cleanup. B2's deterministic corpus/aggregation tools and session tests supply independent evidence.
4. Validation: show actual role test commands and results, separate B1/B2 support suites, protected ownership checks and merged PRs. Use the final Week 13 independent results when available.
5. Limitations and future work: live AstrBot event-to-delivery, actual Node/npm installation, end-to-end rollback, OS-level isolation, optional tool integration and packaging path confinement remain distinct from scoped regression success.

## Sprint / PR evidence

| Role | Sprint 1 | Sprint 2 | Sprint 3 final PR at preparation |
| --- | --- | --- | --- |
| A1 | #1 merged | #20 merged; #25 integration test correction | #30 merged |
| A2 | #7 merged | #19 merged | #29 open |
| B1 | #3 merged | #23 merged | #28 open |
| B2 | #5 merged | #22 merged | #33 merged |
| C1 | #2 merged | #21 merged | #31 merged |
| C2 | #6 merged | #18 merged | #34 merged |
| D1 | #4 merged | #15 merged | #32 open |
| D2 | #8 merged | #24 merged | #35 open, submitted by team leader on behalf of D2 using D2's existing branch |

All eight roles have committed Week 1–13 evidence. Final integration and independent acceptance belong to Week 13. No meeting, presentation delivery or real runtime result is fabricated.

TEAM_WEEK12_PRESENTATION_AND_REPORT_PREP: COMPLETE
