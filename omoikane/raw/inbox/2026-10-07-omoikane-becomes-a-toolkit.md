---
title: Omoikane objective widens to a work toolkit
dated: 2026-10-07
---

# Omoikane objective widens to a work toolkit

On 2026-10-07 the user widened Omoikane's objective:

> O objetivo do Omoikane vai ser mais amplo, quero pegar como referência o https://github.com/cursor/plugins/tree/main/pstack e trazer para o Omoikane, ele vai ser mais que um sistema de memória, vai ser uma ferramenta de trabalho, um toolkit para iniciar o trabalho encima dele, e caso o usuario for utilizar para desenvolvimento de software e não apenas pesquisas genericas e universais, ele vai ter diversas skills. Veja como podemos adaptar para o nosso uso, acredito que o pstack é para o grok bot ou cursor em especifico. Ignore skills como TDD e UNSLOP. Tambem pegue skills do meu proprio repo caso forem uteis https://github.com/YuukiFST/agent-dotfiles/tree/main/skills e a skill de segurança da cloudflare https://github.com/cloudflare/security-audit-skill

Translation: "Omoikane's objective will be wider. I want to take pstack as a reference and bring it into Omoikane. It will be more than a memory system: a work tool, a toolkit to start work on top of. When the user builds software, and not only generic research, it will have many skills. See how to adapt them for our use; I believe pstack is specific to Grok Bot or Cursor. Ignore skills like TDD and UNSLOP. Also take skills from my own repo if useful, and Cloudflare's security skill."

What this changes:

- `omoikane/wiki/domain/omoikane-objective.md` states the objective as memory only ("every change must improve Omoikane at holding domain knowledge"). The memory stays; the objective now also covers a toolkit of working skills, with a software-development set for systems that build software.
- `omoikane/wiki/decisions/objective-criterion-stays-out-of-agents-md.md`, `docs/architecture.md` (opening) and `README.md` (opening) describe the memory-only objective and need the same update.
- `omoikane/raw/inbox/2026-10-06-pstack-skills-review.md` rejected many pstack skills because they had "no memory link". That criterion no longer holds for a software-development skill set; those verdicts are reopened for it. The verdicts about memory gaps stay as they are.
- Excluded by the user: pstack `tdd` and `unslop`.
- Sources named for the skill set: pstack (https://github.com/cursor/plugins/tree/main/pstack, commit `df58112`), the user's agent-dotfiles (https://github.com/YuukiFST/agent-dotfiles/tree/main/skills, commit `cc99061`), Cloudflare security-audit-skill (https://github.com/cloudflare/security-audit-skill, commit `c1c8a8c`, MIT).
