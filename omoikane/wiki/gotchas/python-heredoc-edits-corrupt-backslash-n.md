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
The agent wrote "Caí na armadilha conhecida do `\n` em heredoc" and hit it at least twice in one session (turn 2).
One corrupted docstring had already reached `main` in an item 1 commit and was fixed while working on item 4 (turn 2).

Cause, added in the review of PR #36 (the session does not state it): the heredoc is quoted (`<<'EOF'`), so the shell passes the text unchanged; Python then reads `\n` inside an ordinary string literal as a newline, and a script that writes source code containing `\n` writes a line break where the file needed the two characters.

## Workaround

Redo the change with the Edit tool (source: [[session-2026-09-30-c14af01e]], turn 2), or build the text with raw strings (`r"..."`) when a script has to write it.
