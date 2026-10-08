---
title: Remove the worktree of a merged PR with git worktree remove
type: practice
summary: After a PR merges, check its worktree is clean, run git worktree remove on it, and delete the local and remote branch
tags: [procedure, git, worktrees, pull-request]
created: 2026-10-07
updated: 2026-10-07
sources: [wiki/sources/session-2026-10-02-04edad59.md, wiki/sources/session-2026-10-06-180e52eb.md, wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/session-2026-10-07-9e3fae7e.md]
---

## Rule

After a PR merges, check that its worktree has no uncommitted work, then remove it with `git worktree remove <path>`.
Delete the PR's local and remote branch. Do not delete a worktree folder by hand.

## Evidence

- With #84 merged: "Enquanto o revisor roda: limpeza do worktree `../omoikane-79` (já mergeado) e dos rascunhos em `%TEMP%`.", then "#84 e #88 mergeados, worktrees e rascunhos removidos" (source: [[session-2026-10-02-04edad59]], turn 3).
- Asked which `omoikane-*` folders could go, the agent said: "Para remover, use `git worktree remove ../omoikane-74`, e não a lixeira do Windows. Apagar pela lixeira deixa registros órfãos no `.git`, que depois exigem `git worktree prune`." (source: [[session-2026-10-06-180e52eb]], turn 1). After #102 merged it ran `git worktree remove ../omoikane-101 && git branch -d feat/101-wrap-up-skill` and `git push -q origin --delete feat/101-wrap-up-skill` (turn 8).
- The handoff the user pasted: "Depois de cada merge, remova a worktree correspondente com `git worktree remove` (nunca apague a pasta pela lixeira) e apague a branch local e remota." The agent ran `git -C ../omoikane-term status --short && echo "term clean" && git worktree remove ../omoikane-term` before deleting the branches, and removed four worktrees that way (source: [[session-2026-10-06-61eabe29]], turns 2, 6, 7).
- After the merges of the #111 stack, the agent found the worktrees `omoikane-103` to `omoikane-106` still there; the branches of the first three had merged (#107 to #109) after the session that opened them ended (source: [[session-2026-10-07-9e3fae7e]], turn 2).

## Scope

A worktree whose branch has commits not on the remote: push the branch first. "**`omoikane-96`:** apagar agora perde trabalho. Primeiro envie a branch e abra o PR." (source: [[session-2026-10-06-180e52eb]], turn 1); the branch was pushed so `b695a3b` is kept (turn 8).
A worktree a running process uses is not removed: "**`omoikane-wiki-auto`:** não apague. A execução agendada trabalha nela." (same session, turn 1).
A scratch worktree made for one check is removed with `--force` when the check ends: `git worktree remove --force /tmp/tmp.lpNV5dzqIZ/mergecheck && git worktree prune` (source: [[session-2026-10-06-61eabe29]], turn 6).
A PR that merges after its session ended leaves its worktree behind; the next session that sees the merge removes it.
