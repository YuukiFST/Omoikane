---
title: Company-internal material stays out of the public repo
type: decision
summary: Omoikane is public; the sb360-kit knowledge map is company-internal and is kept outside every repository
tags: [sb360-kit, privacy, public-repo]
created: 2026-10-01
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md]
---

For the third front, a subagent mapped how sb360-kit governs knowledge, read only through `git show origin/main` (source: [[session-2026-09-30-230a182d]], turn 4).
The agent's note: "Omoikane é **público**: o mapa do sb360-kit (interno da empresa) não pode ir para o repo. Salvo fora dos repositórios." (turn 4).
The map was written to `C:\Users\Desenvolvimento\.omoikane-handoff\2026-10-01\sb360-kit-map.md`, next to the handoff prompt (turn 4).

The rejected alternative is the repository itself: anything committed here, the wiki and the inbox included, is published (turn 4).

The next session kept to it for the organisation knowledge design: the generic spec and `org-candidates.py` went to the Omoikane branch `feat/52-org-candidates`, while the sb360-kit changes went into a private note, `C:\Users\Desenvolvimento\.omoikane-handoff\2026-10-01\sb360-kit-org-knowledge.md`, as proposed diffs, not applied (source: [[session-2026-10-01-b5b6fb27]], turn 2).
The agent read sb360-kit files "só via `git show` (sem tocar no checkout)", and drafted against a separate clone at commit `b0f8b46` (turn 2).
