---
title: Machine-local paths stay out of the public repo
type: domain
summary: A path that only holds on one machine stays out of the repository, which is public; keep it in the user's own memory
tags: [convention, public-repo, privacy]
created: 2026-10-06
updated: 2026-10-08
sources: [wiki/sources/session-2026-10-02-a9384e33.md, wiki/sources/session-2026-10-08-0ac17a0f.md]
---

## Rule

A path that is valid only on the user's machine does not go into the Omoikane repository (source: [[session-2026-10-02-a9384e33]], turn 2).
The user, on where to record the location of the local clones of the reference projects: "Esse caminho não entra no repo, porque o repo é público e o caminho só vale nesta máquina." (turn 2).
The two reasons hold apart: the repository is public, and the path means nothing on another machine.

## Where it applies

Any committed file: docs, prompts, wiki pages, `AGENTS.md`.
The user asked for that path to go to the global memory in `~/.claude` instead (turn 2); the session put it in `~/.claude/CLAUDE.md` (turn 9).
Raw session captures can carry such paths too; `docs/architecture.md` names a private path as one thing the capture redaction list (`omoikane/.capture-redact`) exists for.
On 2026-10-08 the term went into `omoikane/.capture-redact`, which is gitignored, and the agent tested `redact` on both forms of the path (source: [[session-2026-10-08-0ac17a0f]], turn 10).
The raw capture of session a9384e33, already committed, keeps the path: "O path ficou no arquivo público, como você aprovou." (turn 10). The reason for that choice is cut from the capture (turn 9).

Related: [[company-internal-material-stays-out-of-the-public-repo]], the same reason applied to the user's company material.
