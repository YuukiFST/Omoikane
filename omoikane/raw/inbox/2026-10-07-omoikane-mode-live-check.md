---
title: omoikane-mode shows in the command list of OpenCode and Pi
date: 2026-10-07
---

On 2026-10-07 the user checked omoikane-mode in both harnesses.
The user first said: "eu ja verifiquei no OpenCode, esta funcionando perfeitamente, no PI tambem".
The user then made the claim precise: "quando eu digo que eles estão funcionando é que eles apareceram quando eu fui digitar omoikane-mode".

- OpenCode: `/omoikane-mode` shows in the command list while typing.
- Pi: the omoikane-mode skill command shows in the command list while typing.
- OpenCode, loading: confirmed. The user ran `/omoikane-mode`, asked for an AI-slop audit of `README.md`, and pasted the reply.
  The reply opens with `throughput checkpoint: n/a, read-only investigation`, the exact line of `.claude/skills/omoikane-mode/playbooks/investigation.md` step 2, so the agent routed the task to the Investigation playbook.
  It ends with "Princípios aplicados: prove-it-works ... minimize-reader-load", two files under `references/principles/`.
  It follows the skill's "Writing the reply" rules: short sentences, one paragraph for the consumer and one for the maintainer, and evidence labelled automatic or manual.
  It also used the user's personal `ai-tells` skill from `~/.claude/skills/`, which Omoikane does not ship; OpenCode loaded both.
- Pi, loading: not checked yet.

The `_review.md` todo `omoikane-mode-live-check` (session 9e3fae7e, turn 2) asks that the skill loads; it now holds only for Pi.
The todos `pi-live-verification` and `pi-skill-capture-live-check` are not covered by this check.
