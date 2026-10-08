---
title: Git Bash rewrites a leading slash argument into a path
type: gotcha
summary: From Git Bash, an issue title starting with /ask became C:/Program Files/Git/ask; read such titles back
tags: [windows, git-bash, msys, github, slash-commands]
created: 2026-10-06
updated: 2026-10-06
sources: [wiki/sources/session-2026-10-05-1de79b19.md]
code: []
guard: none
---

## Behaviour

The agent created issue #97 from Git Bash with a title that started with the slash command `/ask` (source: [[session-2026-10-05-1de79b19]], turn 1).
GitHub stored the title as "C:/Program Files/Git/ask should read git history before asking the human for a source" (the issue's `renamed` timeline event, read 2026-10-06).
The agent's note: "MSYS reescreveu `/ask` no título da issue #97. Corrigindo." (turn 1).

Omoikane's operations are slash commands (`/ask`, `/distill`, `/ingest`, `/wrap-up`), so issue and PR titles often start with one.
PR #100's title, "feat(prompts): let /ask read git history before asking for a source", kept its slash: there the slash is not at the start of the argument.

## Workaround

The agent renamed the issue: `gh-axi issue edit 97 --title "/ask should read git history before asking the human for a source"` (turn 1); the title on GitHub is now correct.
The capture does not show why the edit kept the slash when the create did not. After creating an issue or PR whose title starts with `/`, read the title back.
