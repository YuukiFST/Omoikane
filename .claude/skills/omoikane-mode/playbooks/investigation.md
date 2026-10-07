### Investigation

**You own the answer. Plan, route, write.**

Investigation requests are read-only. They produce a cited explanation or a recommendation, not a code change.

1. Route through the **how** skill. For motivation questions ("why was this built so"), also run `/ask`, which answers from the wiki and `origin/main` history, and read `git log` / `git blame` on the code in question.
2. Throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only investigation`.
3. Produce the `how`-shaped output (Overview / Key Concepts / How It Works / Where Things Live / Gotchas), or a recommendation with a tradeoffs table if the request is a decision between alternatives.
4. Write the reply per **Writing the reply** in `../SKILL.md`.

No PR, no babysit, no `codebase-design` unless the investigation precedes a code change. If it does, hand back to the user and re-route to Bug fix or Feature.

**Reply:** the investigation output. For "are we sure?" answers, include your real judgment with reasons. Push back if the premise is wrong (see Autonomy).

Adapted from pstack `skills/poteto-mode/playbooks/investigation.md` at df58112. MIT, see `../LICENSE`.
