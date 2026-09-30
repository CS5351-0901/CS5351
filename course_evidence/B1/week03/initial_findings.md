WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Week 3 — B1 Initial Findings

This is a static review of the current Week 4 baseline. The observations below identify candidate tests; they do not claim that a defect has been reproduced at runtime.

## Requirement extraction

- Input: message text. Output: trimmed requirement text or `None`.
- The baseline tries a plain `/agent` regular expression and an `@.../agent` expression in order.
- Candidate Week 5+ cases include plain and mentioned commands, missing requirement text, leading and trailing whitespace, multi-line input, CRLF input, and command-like text embedded in paths or other tokens.
- The current `.` capture is not configured to span line breaks, so multi-line requirements require explicit regression coverage.

## Blacklist decision

- Inputs: user ID and group ID. Output: a Boolean deny decision.
- Both incoming IDs and configured list entries are converted to strings before comparison.
- Candidate cases include numeric and string identifiers, one-list-only matches, empty lists, absent settings, and allowed requests.

## Project assessment

- Input: requirement text. Output: `type` and `size` labels.
- Type selection uses ordered substring checks, so precedence and partial-word matches require regression coverage.
- Size is based on the unmodified character count: below 30 is `S`, 30–99 is `M`, and 100 or more is `L`.
- Candidate cases include each supported keyword, overlapping or embedded keywords, outer whitespace, Unicode text, and the 29/30/99/100 boundaries.

RUNTIME_TEST: NOT_RUN

No B1 test suite or runtime command was executed for this retrospective stage.
