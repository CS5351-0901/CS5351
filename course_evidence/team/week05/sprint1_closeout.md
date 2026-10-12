# Week 5 Sprint 1 closeout

Date: 2026-09-28

## Integrated work

A1 completed the Week 5 executable baseline on `course/a1` and opened Sprint 1 PR #1 into `main`.

The A1 Week 5 engineering artifact is `tests/roles/a1/test_baseline.py`. It contains eight Python standard-library regression tests covering A1-owned configuration and Node.js/dependency-preparation helper behavior. The recorded validation command was:

```text
C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests/roles/a1 -p test_baseline.py -v
```

Observed result: 8 tests ran and all passed (`OK`).

PR #1 was independently checked before merge. Its base was `main`, its head was `course/a1`, GitHub reported it mergeable with a clean merge state, and its diff contained only A1 Week 1-5 evidence plus `tests/roles/a1/test_baseline.py`. It was merged with merge commit `6797cc3b3ae740c491282091877cf06c3f733e55`.

## Pending member work

The following member branches were checked after the A1 merge:

| Role | Remote head | Week 5 engineering artifact or evidence | Sprint 1 PR |
| --- | --- | --- | --- |
| A2 | `eff40df3e515a55e474388c3d442a9ee29b2b2ea` | Not present | Not present |
| B1 | `2ab79cab1f2dd9ab9c11c73a13e48cc95aa3eab8` | Not present | Not present |
| B2 | `418119c6d295d58325cc91136d8fdb82ba7049cc` | Not present | Not present |
| C1 | `b5c18751804ee9b06a188621dc17b87f1a24902a` | Not present | Not present |
| C2 | `2f296e2d0d1dfa0bb6cc691ae8949bcf8ae27291` | Not present | Not present |
| D1 | `dc5817c09c140f547740459705ca62ea07a02494` | Not present | Not present |
| D2 | `9074f0b1a02622eee734e9f9855c78f886b3e2d5` | Not present | Not present |

Each of these seven branches still ended at its Week 4 role-evidence commit when checked. No Week 5 artifact and no open Sprint 1 PR for those roles was present. Their work was not created or modified by the team leader.

## Closeout status

A1 Week 5 integration: PASS.

Whole-team Sprint 1 closeout: BLOCKED / INCOMPLETE.

The team-level closeout cannot be marked PASS until A2, B1, B2, C1, C2, D1, and D2 independently complete their Week 5 engineering work, run their required validation, and submit reviewable Sprint 1 PRs without unresolved conflicts.

No Week 6 or later work was created as part of this closeout.
