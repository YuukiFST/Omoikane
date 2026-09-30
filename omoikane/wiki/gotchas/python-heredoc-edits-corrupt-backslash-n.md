---
title: Python heredoc edits corrupt backslash-n
type: gotcha
summary: Editing files through python heredoc scripts mangles \n in the text; one corrupted docstring reached main; use Edit
tags: [agent-tooling, editing, heredoc]
created: 2026-09-30
updated: 2026-09-30
sources: [wiki/sources/session-2026-09-30-c14af01e.md]
guard: none
---

## Behaviour

The session edited files with `python - <<'EOF'` scripts; when the text carried `\n`, the written file came out corrupted (source: [[session-2026-09-30-c14af01e]], turn 2).
The agent called it "a armadilha conhecida do `\n` em heredoc" and hit it at least twice in one session (turn 2).
One corrupted docstring had already reached `main` in the item 1 commit and was fixed later (turn 2); the agent looked for it with `grep -n '\\n' omoikane/bin/wiki-index.py` (turn 2).

## Workaround

Redo the change with the Edit tool (source: [[session-2026-09-30-c14af01e]], turn 2).
