---
title: Company-internal material stays out of the public repo
type: decision
summary: Omoikane is public; material from the user's company, its name included, is kept outside every repository
tags: [privacy, public-repo]
created: 2026-10-01
updated: 2026-10-02
sources: [wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/2026-10-02-omoikane-objective.md, wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-1b324082.md]
---

For the third front, a subagent mapped how a company-internal kit governs knowledge, read only through `git show origin/main` (source: [[session-2026-09-30-230a182d]], turn 4).
The agent's note: "Omoikane é **público**: o mapa do [redacted] (interno da empresa) não pode ir para o repo. Salvo fora dos repositórios." (turn 4).
The map was written to a private note outside every repository, next to the handoff prompt (turn 4).

The rejected alternative is the repository itself, which is public (turn 4).

The next session kept to it for the organisation knowledge design: the generic spec and `org-candidates.py` went to the Omoikane branch `feat/52-org-candidates`, while the changes for the kit went into a private note as proposed diffs, not applied (source: [[session-2026-10-01-b5b6fb27]], turn 2).
The agent read the kit's files "só via `git show` (sem tocar no checkout)" (turn 2).

The user later said the kit was only an example and that Omoikane "não tem nenhuma relação com esse toolkit: não integra, não alimenta, não lê"; the kit's name must not appear in this public repository (source: [[2026-10-02-omoikane-objective]]).
The organisation knowledge design above was reversed: [[omoikane-holds-its-systems-domain-knowledge-itself]].
That correction came in [[session-2026-10-01-d4302021]]: the user said the kit "não tem NADA haver com o Omoikane" (turn 6).

The same session applied the decision to the scheduled run: since a run publishes the inbox captures in a public PR, the agent scanned them for the kit's identifiers before the first run, and deleted a clean local clone of the kit (turns 3, 4).
It also left the kit's name out of the handoff prompt it wrote, because "a próxima sessão também será capturada e publicada no repo público" (turn 8).

[[session-2026-10-02-1b324082]] found the scheduled run about to publish a capture naming the kit 15 times and disabled the `OmoikaneIngest` task before its next run, telling the user afterwards; re-enable with `schtasks /Change /TN OmoikaneIngest /ENABLE` (turn 3).
It then removed the name from the wiki, `log.md` and the published raw captures (PR #70), and made capture redact listed terms from then on: [[redact-captures-when-they-are-written]] (turn 3).
