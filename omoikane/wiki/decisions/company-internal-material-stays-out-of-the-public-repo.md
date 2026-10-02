---
title: Company-internal material stays out of the public repo
type: decision
summary: Omoikane is public; material from the user's company, its name included, is kept outside every repository
tags: [privacy, public-repo]
created: 2026-10-01
updated: 2026-10-02
sources: [wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md]
---

For the third front, a subagent mapped how a company-internal kit governs knowledge, read only through `git show origin/main` (source: [[session-2026-09-30-230a182d]], turn 4).
The agent's note: "Omoikane é **público**: o mapa do [redacted] (interno da empresa) não pode ir para o repo. Salvo fora dos repositórios." (turn 4).
The map was written to a private note outside every repository, next to the handoff prompt (turn 4).

The rejected alternative is the repository itself, which is public (turn 4).

The next session kept to it for the organisation knowledge design: the generic spec and `org-candidates.py` went to the Omoikane branch `feat/52-org-candidates`, while the changes for the kit went into a private note as proposed diffs, not applied (source: [[session-2026-10-01-b5b6fb27]], turn 2).
The agent read the kit's files "só via `git show` (sem tocar no checkout)" (turn 2).
