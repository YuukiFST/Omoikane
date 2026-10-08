---
title: Python heredoc edits corrupt backslash-n
type: gotcha
summary: Editing files through python heredoc scripts mangles \n in the text; one corrupted docstring reached main; use Edit
tags: [agent-tooling, editing, heredoc]
created: 2026-09-30
updated: 2026-10-07
sources: [wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-02-a9384e33.md, wiki/sources/session-2026-10-05-1de79b19.md, wiki/sources/commits-2026-09-29-to-2026-10-06.md, wiki/sources/session-2026-10-06-180e52eb.md, wiki/sources/session-2026-10-06-973284b2.md]
code: [.claude/hooks/escape-edit-guard.py, tests/test_escape_edit_guard.py]
guard: hook
---

## Behaviour

The session edited files with `python - <<'EOF'` scripts; when the text carried `\n`, the written file came out corrupted (source: [[session-2026-09-30-c14af01e]], turn 2).
The agent wrote "Caí na armadilha conhecida do `\n` em heredoc" and hit it at least twice in one session (turn 2).
One corrupted docstring had already reached `main` in an item 1 commit and was fixed while working on item 4 (turn 2).

Cause, added in the review of PR #36 (the session does not state it): the heredoc is quoted (`<<'EOF'`), so the shell passes the text unchanged; Python then reads `\n` inside an ordinary string literal as a newline, and a script that writes source code containing `\n` writes a line break where the file needed the two characters.

## Recurrence

The next session hit the same class with `sed`: "Armadilha do escape de novo (sed transformou `\n` em quebra de linha). Corrigindo com Edit." (source: [[session-2026-09-30-230a182d]], turn 2).

## Guard

Issue #47, PR #49 (open at capture, merged since): a Claude Code `PreToolUse` hook on Bash, `.claude/hooks/escape-edit-guard.py`, with `tests/test_escape_edit_guard.py` (source: [[session-2026-10-01-b5b6fb27]], turn 2).
It blocks `sed -i` and a heredoc fed to Python whose body holds `\n`, `\t` or `\\`, and points to the Edit tool.
Its review found false positives; the fix tokenises the command with `shlex`, matches `sed` only at the start of a command and judges a Python heredoc by its body (turn 2).
The second review found a PR title naming python blocked, and a `.py` in a comment or a redirection letting a Python heredoc through; the hook now splits the opening line into simple commands, catches `sed` inside `for`, `if` and `{ }`, and its message says how to run a script instead (source: [[commits-2026-09-29-to-2026-10-06]], `d30e434`).
A later session met the hook twice, on a Python heredoc and on a `sed -i`, and redid both through Edit: "Hook do projeto bloqueou (gotcha conhecido). Vou pelo Edit" (source: [[session-2026-10-02-a9384e33]], turns 4, 9).
The next session met it on a `sed -i` that rewrote the `/ask` descriptions in the `omoikane-ask` worktree ("Blocked: sed -i rewrites escapes in its replacement. Use the Edit tool") and made the change with Edit (source: [[session-2026-10-05-1de79b19]], turn 1).
The `/wrap-up` session met it on a `sed -i` that rewrote a line of the scheduled-run docs in the `omoikane-101` worktree (source: [[session-2026-10-06-180e52eb]], turn 4).
The session of issues #103 to #106 met it twice, on a Python heredoc ("Blocked: a Python heredoc with \n, \t or \\ in its text rewrites them on the way to the file") and on a `sed -i` in the `omoikane-105` worktree (source: [[session-2026-10-06-973284b2]], turn 2).

## Workaround

Redo the change with the Edit tool (source: [[session-2026-09-30-c14af01e]], turn 2), or build the text with raw strings (`r"..."`) when a script has to write it.
