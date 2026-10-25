# PR file-ownership guard

Each member uses \`course/<role>\` -> \`main\` and may change only \`course_evidence/<ROLE>/**\`, \`tests/roles/<role>/**\`, and owned production files documented in the nine CS5351 agent manuals. The shared \`main.py\` is checked per method. A change to shared imports, class shape, or another member's method needs leader-coordinated work.

The previous D2 incident, which added D2 notes under \`course_evidence/team/week01–03/\`, is now a failing regression test. \`course_evidence/team/\` and governance files are reserved for the team leader. Branches \`ops/*\` are accepted only from GitHub PR author \`gekamok\`.

Open a PR and wait for GitHub's required \`Check ownership\` status. The workflow uses \`pull_request_target\` but executes only the trusted base revision, and uses Git to inspect the proposed changed file paths and the \`main.py\` AST; it **does not run PR-submitted code**. Renames are checked as delete-plus-add. A failed check means split or correct the out-of-scope change; do not bypass it by renaming or merging directly to main.

Run \`python tools/test_pr_ownership.py\` locally to verify the guard. \`.github/CODEOWNERS\` also requests appropriate reviewers, but CODEOWNERS alone does not enforce authorization. The \`main\` branch protection requires the PR and passing CI.

Caveat: repository administrators can change protection settings. All eight current collaborators have repository-admin permission. Demoting non-leaders to write permission would give the team leader exclusive governance control; that separate permission change needs explicit authorization.

## B1/B2 zero-coupling support extension (V3, from Week 6)

B1 alone owns course_tools/b1_support/** and B2 alone owns
course_tools/b2_support/**, as the only new course_tools exceptions.
This does not authorize A/C/D or the other B role to edit these directories.

Original weekly business tasks must be completed and validated first.
Support-only commits may touch only their own support directory and their
own course_evidence/B1/** or course_evidence/B2/** respectively. They may
not contain main.py, production settings, other role tests or CI changes.
The required ownership workflow now checks these commit boundaries.

Support code must use standard-library or its own package imports.
The workflow statically checks this rule on support Python files; dynamic
import/side-effect behavior still needs the member's own verification.
Support checks are named checks/check_*.py to avoid default pytest collection
and must be run explicitly as specified by the V3 manuals.

The new exceptions do not weaken team evidence protection, cross-role
ownership, method-level main.py checks, or required PR review.
