---
title: Omoikane references
type: domain
summary: Before changing how Omoikane captures, distills, stores or loads knowledge, consult the matching reference project
tags: [references, objective]
created: 2026-10-02
updated: 2026-10-07
sources: [wiki/sources/2026-10-02-omoikane-references.md, wiki/sources/session-2026-10-02-680ff986.md, wiki/sources/2026-10-06-pstack-is-an-omoikane-reference.md, wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/2026-10-06-pstack-skills-review-round-2.md, wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/2026-10-07-omoikane-objective-widens-to-a-work-toolkit.md]
code: [README.md, docs/architecture.md, omoikane/bin/bootstrap.py]
---

## The rule

Before changing how Omoikane captures, distills, stores or loads knowledge (`omoikane/prompts/`, `omoikane/bin/`, the page contract, the hooks), read the reference that covers the same problem and say what it does there; adopt, adapt or reject it with a reason (source: [[2026-10-02-omoikane-references]], "The rule").
The user: "deve estar gravado para o agente sempre os analisar quando necessario" (source: [[session-2026-10-02-680ff986]], turn 3).

- Karpathy's LLM Wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- brainmaxxing: https://github.com/poteto/brainmaxxing
- ai-memory: https://github.com/akitaonrails/ai-memory
- pstack: https://github.com/cursor/plugins/tree/main/pstack
- Cloudflare security-audit-skill: https://github.com/cloudflare/security-audit-skill
- Cloudflare, "Build your own vulnerability harness": https://blog.cloudflare.com/build-your-own-vulnerability-harness/

The first three are the references Omoikane is built on ([[omoikane-objective]]).
On 2026-10-06 the user added pstack as a fourth: "Sim, pstack deve ser utilizado como referência https://github.com/cursor/plugins/tree/main/pstack existe muita conteudo valioso nessas skills" (source: [[2026-10-06-pstack-is-an-omoikane-reference]]; said in [[session-2026-10-06-61eabe29]], turn 9).
The user said it after the agent reported that this list named three projects, while pstack and the STE posts ([[2026-10-02-ste-and-oversight-posts]]) had also fed changes (turn 8).
So the rule covers pstack's skills too, those not read yet included ([[pstack]]).
On 2026-10-07, when the user made Omoikane a toolkit for software development ([[omoikane-objective]]), the user added the two Cloudflare items and restated pstack: "caso não tenha colocado como referencia coloque : https://github.com/cloudflare/security-audit-skill https://blog.cloudflare.com/build-your-own-vulnerability-harness/ e tambem https://github.com/cursor/plugins/tree/main/pstack" (source: [[session-2026-10-07-062e80af]], turn 5).
The skill is vendored as [[cloudflare-security-audit-skill]]; the post describes the multi-stage harness the skill is the starting point of (`docs/specs/2026-10-07-software-toolkit.md`, "References and sources").
Grant Bourzikas wrote the post, dated 2026-06-18 (source: [[2026-10-07-omoikane-objective-widens-to-a-work-toolkit]]).

## Who it is for

Only people and agents improving Omoikane in this repository; not users or agents of a system built from the template (source: [[2026-10-02-omoikane-references]]).
The user: "Essas referencias não serão utilizadas por quem vai utilizar o sistema em si, a ferramenta Omoikane, e sim para nós que estamos aprimorando o Omoikane" (source: [[session-2026-10-02-680ff986]], turn 4).
So the rule is kept out of the fixed part of `AGENTS.md`: a `## References` section there was proposed and rejected on that ground, since every cloned system inherits the file (source: [[session-2026-10-02-680ff986]], turns 3, 4).
This page also carries neither the `convention` nor the `design-system` tag, which `new-system.py --from` copies into another system ([[new-system-starts-with-an-empty-memory]]).

## What Omoikane took from each, so far

LLM Wiki, brainmaxxing and ai-memory from [[2026-10-02-omoikane-references]], "What Omoikane took from each, so far"; pstack from [[2026-10-06-pstack-is-an-omoikane-reference]].

- LLM Wiki: the three layers (raw sources, wiki, schema), the ingest, query and lint operations, `index.md` and the append-only `log.md` (`docs/architecture.md`, opening).
- brainmaxxing: routing what a session learned to the right kind of page (`reflect`); pruning with an early exit under three findings (`meditate`, `docs/architecture.md`); the durability test behind distill's `task-only` reject; seeding from an existing project (`/ruminate`, `omoikane/bin/bootstrap.py`).
- ai-memory: a practice needs evidence from two or more sessions; a managed rules block with a cap ([[wiki-rules]]); memory of rejected proposals; sanitising before storing ([[redact-captures-when-they-are-written]]); bootstrap from a project's docs and history (`omoikane/bin/bootstrap.py`). Its `scope: global` was considered and not adopted (`docs/specs/2026-10-02-cross-system-knowledge.md`).
- pstack: `/correct` gave the guard whose error names the fix ([[proposed-guards-name-the-fix-and-prefer-lint-or-test]], issue #98, PR #99, merged 2026-10-06); `/why` and `/recall` gave `/ask` reading `origin/main` history ([[ask-searches-origin-main-history-before-asking-for-a-source]], issue #97, PR #100). The round-2 review of its other skills gave template updates without the template's memory, recorded capture failures and a check that every `_review.md` diff applies (PRs #108, #107, #110; source: [[2026-10-06-pstack-skills-review-round-2]]). Details on [[pstack]].
  Issue #111 then vendored its principles and several skills, and turned `poteto-mode` into [[omoikane-mode-routes-each-task-to-a-playbook]] (source: [[session-2026-10-07-062e80af]]).
- Cloudflare security-audit-skill: vendored as `.claude/skills/security-audit/` with a Windows fallback, PR #115 ([[cloudflare-security-audit-skill]]; source: [[session-2026-10-07-062e80af]], turns 8, 10).
