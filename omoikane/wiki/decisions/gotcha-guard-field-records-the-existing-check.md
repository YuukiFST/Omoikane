---
title: Gotcha guard field records the existing check
type: decision
summary: A gotcha's guard names the check that catches the mistake today, never a proposed one; none until it lands
tags: [gotcha, guard, page-contract, lint]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-30-c14af01e.md]
code: [omoikane/bin/wiki-lint.py, omoikane/prompts/distill.md]
---

The `guard:` field on a gotcha page records the guard that exists today, not the one proposed in `_review.md` (source: [[session-2026-09-30-c14af01e]], turn 3).

Reason, in the agent's words: "Assim ele não afirma uma checagem que ninguém aplicou." (turn 3).

Rejected: recording the proposed guard, which would claim a check nobody approved or applied.

Consequences:

- A guard proposed during distill leaves the page at `guard: none` until it lands (see `omoikane/prompts/distill.md`, step 4).
- [[wiki-lint]] fails a gotcha without `guard:` or with an invalid value, and warns on `guard: none` older than 14 days; `/lint` files that warning in `_review.md` and logs `- unguarded <slug>` so it is not filed twice (turn 3).
- After review, `wiki-lint.py` also rejects `guard:` on pages that are not gotchas (turn 2).
