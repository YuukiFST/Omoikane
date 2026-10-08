---
title: wiki-lint
type: entity
summary: omoikane/bin/wiki-lint.py, the deterministic check on the page contract that every wiki operation ends with
tags: [wiki-lint, module, page-contract]
created: 2026-09-30
updated: 2026-10-07
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-02-a8b45323.md, wiki/sources/2026-10-06-pstack-skills-review-round-2.md, wiki/sources/session-2026-10-06-973284b2.md]
code: [omoikane/bin/wiki-lint.py, omoikane/bin/wikilib.py, tests/test_wiki_lint.py]
---

`omoikane/bin/wiki-lint.py` checks the page contract; shared parsing lives in `omoikane/bin/wikilib.py`.

Phase 2 added three checks (source: [[session-2026-09-30-c14af01e]]):

- `guard:` on gotchas: missing or invalid fails, `guard: none` older than 14 days warns, and `guard:` outside gotchas fails (turns 2, 3). See [[gotcha-guard-field-records-the-existing-check]].
- The `practice` type with a two-session floor; after review only session pages that exist count toward it (turn 2).
- The `prune:` mark in the page contract (turn 2).

`code:` paths are judged the same on Windows and Linux and an absolute one is a finding, since PR #33: [[windows-path-lookup-ignores-case-and-trailing-dots]] (source: [[session-2026-09-30-230a182d]], turn 2).
In the scheduled run the agent no longer runs lint; `wiki-ingest.ps1` runs it and hands the findings back: [[headless-runs-have-no-shell]] (turn 4).

The `domain` page type (issue #64, PR #71) fails a domain page that cites no existing source page (source: [[session-2026-10-02-1b324082]], turn 3).
The first version accepted any existing page as the statement behind the rule, the page itself or a concept included; the subagent review rated it high, and the fix, red test first, accepts only a source page (turn 3).

`rule_pointers` (PR #86) warns about a promoted rule in `AGENTS.md` whose page is gone, `Disputed:` or marked `prune:`. It began as a finding and failed CI, because the scheduled agent cannot edit `AGENTS.md`: [[lint-findings-the-scheduled-agent-cannot-fix-are-warnings]] (source: [[session-2026-10-02-a8b45323]], turn 2).

No code checked that a proposal diff in `_review.md` applies: a headless distill could not run `git apply --check` (commit `43423c4`), and a later diff went stale once its target changed (source: [[2026-10-06-pstack-skills-review-round-2]], proposal 3).
Since issue #106 (PR #110, `4000448`) `wiki-lint.py` checks that every diff in `_review.md` applies.
A diff under a bullet that HEAD's `_review.md` lacks is a finding, which the run that wrote it can fix; an older one is a warning, since its target changed and only the human decides (commit `4000448`).
The diff goes to `git apply --check` as bytes: [[python-text-mode-stdin-writes-crlf-on-windows]] (source: [[session-2026-10-06-973284b2]], turn 2).
The subagent review of #110 led to six fixes (turn 2; commit `1572515`): a fence never closed is reported, the `error:` line is shown instead of git's whitespace warning, a diff under a new heading is no longer credited to the previous bullet, `_review.md` is split on `\n` only, so a form feed in a diff no longer splits it, lint skips the check when git is missing, and HEAD's copy is read from the repo argument (`HEAD:./`).
Proposed, with no issue yet: flag a quote a page cites to a session turn when the capture lacks it; 31 of 32 such quotes were verbatim on 2026-10-06 (proposal 4).
