---
title: Specs keep paths that record their own day
type: decision
summary: Repoint a spec's path to a source that moved to raw/sources; keep a path that records where a file sat that day
tags: [specs, documentation, review]
created: 2026-10-09
updated: 2026-10-09
sources: [wiki/sources/session-2026-10-08-21f37812.md]
code: [docs/specs/2026-10-07-software-toolkit.md, docs/specs/2026-10-02-realign-to-objective.md]
---

## Decision

When a source moves from `omoikane/raw/inbox/` to `omoikane/raw/sources/`, fix a spec path that sends the reader to that source.
Keep a spec path that records where a file was on the day the spec ran.

## Context

The user asked for a small PR: `docs/specs/2026-10-07-software-toolkit.md:24` "ainda aponta para o caminho antigo do pstack skills review no inbox" (source: [[session-2026-10-08-21f37812]], turn 2).
Issue #125 and PR #126 made that fix (commit `4de531c`).
The subagent review of #126 found the same kind of old path at line 9 of the same spec; the agent fixed it in the same PR (turn 5; commit `bc4be32`).
The review also flagged `docs/specs/2026-10-02-realign-to-objective.md:41` and `:45`, which name `omoikane/raw/inbox/sessions/` paths.

## Alternative rejected

Rewrite every old inbox path in the specs to today's path.
The agent refused the two findings and said why on the PR: "Aquele spec registra onde a captura `d4302021` estava no dia em que ele rodou. Trocar pelo caminho de hoje tornaria falso o plano daquele dia." (turn 5).
The user merged #126 as `007d983` with that answer in the agent's report (turns 5, 6).
