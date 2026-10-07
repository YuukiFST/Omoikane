---
title: Omoikane objective widens to a work toolkit
dated: 2026-10-07
---

# Omoikane objective widens to a work toolkit

On 2026-10-07 the user widened Omoikane's objective:

> O objetivo do Omoikane vai ser mais amplo, quero pegar como referência o https://github.com/cursor/plugins/tree/main/pstack e trazer para o Omoikane, ele vai ser mais que um sistema de memória, vai ser uma ferramenta de trabalho, um toolkit para iniciar o trabalho encima dele, e caso o usuario for utilizar para desenvolvimento de software e não apenas pesquisas genericas e universais, ele vai ter diversas skills. Veja como podemos adaptar para o nosso uso, acredito que o pstack é para o grok bot ou cursor em especifico. Ignore skills como TDD e UNSLOP. Tambem pegue skills do meu proprio repo caso forem uteis https://github.com/YuukiFST/agent-dotfiles/tree/main/skills e a skill de segurança da cloudflare https://github.com/cloudflare/security-audit-skill

Translation: "Omoikane's objective will be wider. I want to take pstack as a reference and bring it into Omoikane. It will be more than a memory system: a work tool, a toolkit to start work on top of. When the user builds software, and not only generic research, it will have many skills. See how to adapt them for our use; I believe pstack is specific to Grok Bot or Cursor. Ignore skills like TDD and UNSLOP. Also take skills from my own repo if useful, and Cloudflare's security skill."

Later in the same session the user made it narrower:

> Eu quero deixar mais preciso na verdade o objetivo do Omoikane, não vai ser para pesquisas genericas, vai ser para desenvolvimento de software. Então caso não tenha colocado como referencia coloque : https://github.com/cloudflare/security-audit-skill https://blog.cloudflare.com/build-your-own-vulnerability-harness/ e tambem https://github.com/cursor/plugins/tree/main/pstack, eu gosto do pstack, gosto de habilitar poteto-mode e deixar o agente seguir utilizando a melhor skill para tal tarefa, quero que no omoikane tenha isso tambem

Translation: "I want Omoikane's objective more precise: it is not for generic research, it is for software development. So, if not yet listed as references, add [the Cloudflare skill], [the Cloudflare blog post 'Build your own vulnerability harness'] and pstack. I like pstack; I like to enable poteto-mode and let the agent go on using the best skill for each task. I want Omoikane to have that too."

What this changes:

- `omoikane/wiki/domain/omoikane-objective.md` states the objective as memory only ("every change must improve Omoikane at holding domain knowledge"). The objective is now a toolkit for software development: the memory, plus development skills and a mode that routes each task to the best skill. Generic research is no longer a use.
- `omoikane/wiki/decisions/objective-criterion-stays-out-of-agents-md.md`, `docs/architecture.md` (opening) and `README.md` (opening, "Two uses, one layout") describe the memory-only objective and the research use; they need the same update.
- `omoikane/wiki/domain/omoikane-references.md` gets three references: pstack (https://github.com/cursor/plugins/tree/main/pstack), Cloudflare security-audit-skill (https://github.com/cloudflare/security-audit-skill) and the Cloudflare post https://blog.cloudflare.com/build-your-own-vulnerability-harness/ (Grant Bourzikas, 2026-06-18; the multi-stage harness the skill is the starting point of).
- `omoikane/raw/inbox/2026-10-06-pstack-skills-review.md` rejected many pstack skills because they had "no memory link". That criterion no longer holds for a software-development skill set; those verdicts are reopened for it. The verdicts about memory gaps stay as they are.
- Excluded by the user: pstack `tdd` and `unslop`.
- Sources named for the skill set: pstack (https://github.com/cursor/plugins/tree/main/pstack, commit `df58112`), the user's agent-dotfiles (https://github.com/YuukiFST/agent-dotfiles/tree/main/skills, commit `cc99061`), Cloudflare security-audit-skill (https://github.com/cloudflare/security-audit-skill, commit `c1c8a8c`, MIT).
