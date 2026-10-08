---
title: Ask searches origin/main history before asking for a source
type: decision
summary: When the wiki lacks the answer, /ask searches origin/main commits and PRs, ingests a note, then answers; PR #100 merged
tags: [ask, prompts, git-history, pstack]
created: 2026-10-06
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-05-1de79b19.md, wiki/sources/2026-10-06-pstack-is-an-omoikane-reference.md]
code: [omoikane/prompts/ask.md, docs/architecture.md, .claude/skills/ask/SKILL.md, .opencode/command/ask.md]
---

## Decision

When the wiki lacks what a question needs, `/ask` searches the history the remote holds before it gives up: `git log origin/main --grep`, `git log origin/main -S`, `git log origin/main --follow`, `git blame ... origin/main`, and `gh pr view` for a PR those commits name (source: [[session-2026-10-05-1de79b19]], turns 1, 2; issue #97, PR #100).
It writes what answers the question to `omoikane/raw/inbox/<YYYY-MM-DD>-history-<slug>.md` with no author name, email, `*-by:` trailer or secret, ingests it, and answers from the pages the ingest wrote (turn 1).
A reason no commit or PR states in words is marked as the agent's inference (turn 1).
A scheduled run has no shell and skips the search (turn 1).
The idea comes from pstack's `/why` and `/recall`: [[pstack]] (turn 1).

## Rejected alternatives and reasons

- Stop and ask the human for a source, as `ask.md` step 2 does on `main`. The eval showed the cost: with an empty wiki the agent found commit `d263fcf`, which answers the question, and still told the human to write a note, run `/ingest` and ask again (turn 1). The `docs/architecture.md` paragraph on the branch: "the objective rules out asking the human for what the agent can fetch".
- Answer straight from the history, without the inbox note. Rejected so that the next question finds a source page instead of searching again (`docs/architecture.md` on the branch).
- Search local commits too. The review of #100 found that `git log` reads commits not yet pushed, so the pushed wiki could carry them; the fix `a83888d` runs every search on `origin/main` (turn 2).
- Redact the note with the capture's script, as `bootstrap.py` does. Rejected because the note quotes only commits on `origin/main` and this repository's PRs, which the remote already holds; the prompt still leaves out names, emails and trailers (`docs/architecture.md` on the branch, turn 2).

A third review finding said step 6 runs `wiki-index.py` and `wiki-lint.py` again after the ingest; the agent judged it not real, because both scripts are idempotent and the second run is the one that checks the query page (turn 2).

## Status

At capture PR #100 was open, CI green, reviewed with the real findings fixed, not merged (turn 3).
On `main` at `887725a`, `omoikane/prompts/ask.md` step 2 still stops and suggests a source.
PR #100 merged on 2026-10-06 at 09:23 -0400 (merge commit `0118646`); the note [[2026-10-06-pstack-is-an-omoikane-reference]] still calls it open, written before the merge.
