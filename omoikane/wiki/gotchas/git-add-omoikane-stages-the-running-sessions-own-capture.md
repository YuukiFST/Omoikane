---
title: git add omoikane/ stages the running session's own capture
type: gotcha
summary: The Stop hook writes the running session's capture into the inbox; `git add omoikane/` stages it with the wiki work
tags: [session-capture, git, hooks, wrap-up]
created: 2026-10-09
updated: 2026-10-09
sources: [wiki/sources/session-2026-10-08-21f37812.md]
code: [.claude/settings.json, omoikane/bin/session-capture.py]
guard: none
---

## What happened

The agent committed the result of the 2026-10-08 `/wrap-up` on the branch `docs/123-wrap-up-2026-10-08` after `git add omoikane/` (source: [[session-2026-10-08-21f37812]], turn 3).
The commit also held the capture of the session that made it: "O commit pegou a captura desta sessão (`inbox/sessions/2026-10-08-21f37812.md`), que o Stop hook escreveu depois do último turno. Removo antes do push." (turn 3).

## Cause

`.claude/settings.json` runs `omoikane/bin/session-capture.py` on the `Stop` and `SessionEnd` hooks.
So from the first turn on, the running session's capture sits in `omoikane/raw/inbox/sessions/`, not yet distilled.
A broad `git add omoikane/` stages it with the wiki work.

## Workaround

Before the commit, run `git diff --cached --name-only` and unstage each file under `omoikane/raw/inbox/sessions/`.
The session did it with `git rm -q --cached omoikane/raw/inbox/sessions/2026-10-08-21f37812.md`, then `git commit --amend --no-edit`, before the push (turn 3).
The capture stays in the inbox for the next `/wrap-up`.
The earlier wrap-up commit of [[session-2026-10-08-0ac17a0f]] also kept the captures not yet distilled out of git.

A guard is proposed in `omoikane/_review.md`: `git-add-omoikane-stages-the-running-sessions-own-capture`.
See [[session-capture]] and [[wrap-up]].
