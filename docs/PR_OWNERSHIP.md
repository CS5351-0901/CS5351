# PR file-ownership guard

Each member uses \`course/<role>\` -> \`main\` and may change only \`course_evidence/<ROLE>/**\`, \`tests/roles/<role>/**\`, and owned production files documented in the nine CS5351 agent manuals. The shared \`main.py\` is checked per method. A change to shared imports, class shape, or another member's method needs leader-coordinated work.

The previous D2 incident, which added D2 notes under \`course_evidence/team/week01–03/\`, is now a failing regression test. \`course_evidence/team/\` and governance files are reserved for the team leader. Branches \`ops/*\` are accepted only from GitHub PR author \`gekamok\`.

Open a PR and wait for GitHub's required \`Check ownership\` status. The workflow uses \`pull_request_target\` but executes only the trusted base revision, and uses Git to inspect the proposed changed file paths and the \`main.py\` AST; it **does not run PR-submitted code**. Renames are checked as delete-plus-add. A failed check means split or correct the out-of-scope change; do not bypass it by renaming or merging directly to main.

Run \`python tools/test_pr_ownership.py\` locally to verify the guard. \`.github/CODEOWNERS\` also requests appropriate reviewers, but CODEOWNERS alone does not enforce authorization. The \`main\` branch protection requires the PR and passing CI.

Caveat: repository administrators can change protection settings. All eight current collaborators have repository-admin permission. Demoting non-leaders to write permission would give the team leader exclusive governance control; that separate permission change needs explicit authorization.
