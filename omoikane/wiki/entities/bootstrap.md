---
title: bootstrap
type: entity
summary: omoikane/bin/bootstrap.py seeds the inbox from a project's README, docs, agent rule files and git history
tags: [bootstrap, module, ingest, redaction]
created: 2026-10-02
updated: 2026-10-02
sources: [wiki/sources/session-2026-10-02-a8b45323.md]
code: [omoikane/bin/bootstrap.py, tests/test_bootstrap.py]
---

`omoikane/bin/bootstrap.py` (issue #79, PR #84) writes one inbox file per source of an existing project, its README, docs, agent rule files and git history, for `/ingest` (source: [[session-2026-10-02-a8b45323]], turn 2).
It comes from ai-memory's `bootstrap` and brainmaxxing's `/ruminate` ([[omoikane-references]]): a project's written rules otherwise reach the wiki only when the user restates them (`omoikane/bin/bootstrap.py`).

Content is read from `HEAD`, never the working tree, and goes through the same redaction as a captured session ([[redact-captures-when-they-are-written]], [[secret-redaction-patterns-leak-swallow-and-backtrack]]), because the scheduled run pushes what it ingests (`omoikane/bin/bootstrap.py`).
In a system born from the template, a file the template shipped contributes only the lines the system added since (`omoikane/bin/bootstrap.py`).

Reviews (turn 2):

- The tests were rewritten to cover the first review's findings, and the agent asked for a second pass because the rewrite was large.
- The second review found that template detection still depended on the remote's name, file names leaked listed terms, and a clipped body leaked part of a token; the agent was adding tests for them (the "Use this template" flow with the real `new-system.py`, a redacted name, a clipped body, an attached manual, `node_modules`) when the capture ended.
