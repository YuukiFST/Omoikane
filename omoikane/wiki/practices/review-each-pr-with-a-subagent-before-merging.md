---
title: Review each PR with a subagent before merging
type: practice
summary: Before merging a PR, post a subagent review on it and fix the real findings; merge only when the user authorized it
tags: [procedure, pull-request, code-review, git]
created: 2026-09-30
updated: 2026-10-08
sources: [wiki/sources/session-2026-09-15-e04462b2.md, wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md, wiki/sources/session-2026-10-01-d4302021.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-02-04edad59.md, wiki/sources/session-2026-10-02-a9384e33.md, wiki/sources/session-2026-10-05-1de79b19.md, wiki/sources/session-2026-10-06-180e52eb.md, wiki/sources/session-2026-10-06-61eabe29.md, wiki/sources/session-2026-10-06-973284b2.md, wiki/sources/session-2026-10-07-062e80af.md, wiki/sources/session-2026-10-07-9e3fae7e.md, wiki/sources/session-2026-10-08-0ac17a0f.md]
---

## Rule

Before merging a PR in YuukiFST/Omoikane, have a subagent review it and post the findings on the PR.
Fix the findings judged real and wait for green CI.
Merge only when the user authorized it, then with `gh pr merge <n> --merge --delete-branch`, and close the issue.

## Evidence

- Issue #7: with CI green on PR #10, the agent noted "Code review agent still running in background; will post its findings on the PR, then merge" (source: [[session-2026-09-15-e04462b2]], turn 2). The `/code-review 10 --comment` agent posted 10 findings as inline comments; the agent triaged them, "fixing the real ones", and merged PR #10 with a merge commit (source: [[session-2026-09-15-e04462b2]], turn 3).
- Phase 2: "PR #22 (item 1) aberto ... Lanço revisão do #22 por subagente", then "Review do #22: 1 alto, 3 médios, 3 baixos. Posto no GitHub", fixes pushed before `gh pr merge 22 --merge --delete-branch` (source: [[session-2026-09-30-c14af01e]], turn 2). The final report: "Cada PR teve review de subagente postada como PR review, com os achados corrigidos antes do merge", for PRs #22 and #26 to #30 (source: [[session-2026-09-30-c14af01e]], turn 3).
- Post-Phase 2: every item went through an issue, a branch and a subagent review posted on the PR; PR #36 merged after its review found unsupported claims on the pages (source: [[session-2026-09-30-230a182d]], turn 2).
- PR #40: a fourth review by a subagent, posted on the PR, found 9 more findings, fixed in `5fd7e8d`, and PR #48's review led to `--ignore-scripts` and `satisfies Hooks` (source: [[session-2026-10-01-b5b6fb27]], turn 2).
- PR #56: three more subagent review rounds, each posted on the PR with its resolution, before the merge commit `f2ba8ff`; PR #58, reviewed with CI green, was left for the user to authorise (source: [[session-2026-10-01-d4302021]], turns 3, 4).
- PRs #67 to #73: every PR got a subagent review and its findings fixed; only #58 was merged in the session (source: [[session-2026-10-02-1b324082]], turn 6).
- PR #88: "Revisão do #88 postada, achado low corrigido em `8b7edc2`. Aguardo o CI desse SHA para mergear." The second review of #84 had not been posted, so the agent posted a summary rebuilt from its fixes before the merge (source: [[session-2026-10-02-04edad59]], turns 3, 4). The handoff had authorised the merges ahead.

- The user stated it in a handoff prompt: "Cada mudança de código ou de documentação segue o fluxo da skill `git-workflow`: issue, branch, PR, review por subagente, correção dos achados reais. O merge é sempre meu; nunca faça merge sem eu autorizar." (source: [[session-2026-10-02-a9384e33]], turn 2). The session posted subagent reviews on PRs #92 to #95, fixed the real findings, re-reviewed #92 after its fix, and merged none (turns 4, 9).
- The next session followed it unprompted: "PRs #99 e #100 abertos. Regra do repo: review por subagente antes de merge. Lançando dois em paralelo." It fixed two of the three findings on #100, judged the third not real and said why on the PR, posted the #99 review, and merged neither: "nenhum foi mergeado (a regra do repo exige sua autorização)" (source: [[session-2026-10-05-1de79b19]], turns 1 to 3).
- PR #102 (`/wrap-up`): the subagent review was posted on the PR and found 8 problems; the agent checked each against the code and fixed all of them, then said "O merge depende de você." It merged with a merge commit (`887725a`) only after the user's "prossiga de acordo com a sua recomendação" (source: [[session-2026-10-06-180e52eb]], turns 6 to 8).
- PRs #99, #94, #95 and #59: the user's handoff asked to confirm green CI and a posted subagent review, run one where missing, and "Me peça autorização antes de cada merge." The agent had a subagent review the #95 fix and the #59 branch, posted both on the PRs, and merged them only after the user's authorisation, which the agent's note acknowledges with "Autorizado." (source: [[session-2026-10-06-61eabe29]], turns 2, 6, 7). It also merged each PR onto the current `main` first: [[green-pr-ci-can-be-stale-against-the-current-main]].
- PRs #107 to #110: the handoff asked for the `git-workflow` flow. Each PR got a subagent review posted with `gh pr review --comment`, and the agent fixed the real findings with a test or a commit of their own. It merged none: "Nenhum merge feito; cada um espera sua autorização" (source: [[session-2026-10-06-973284b2]], turns 2, 3).
- PRs #112 to #118 (issue #111): after the user's "prossiga com a sua recomendação", the agent tried to merge #112, and the Claude Code auto mode classifier denied it as "[Merge Without Review]". The agent left the merge to the user: "Merge bloqueado pelo classificador de permissões. O merge fica com você." (source: [[session-2026-10-07-062e80af]], turn 6). Each of the seven PRs then got a subagent review posted on GitHub and its real findings fixed (turns 9 to 11). After the session they merged with merge commits, in the order the agent gave (turn 11; `git log`).
- The merge of that stack: the handoff said "Mergeie SÓ quando eu autorizar nesta sessão". The agent checked CI, then stopped: "Ainda não fiz nenhum merge: preciso da sua autorização para começar." It merged the seven PRs only after the user's "prossiga de acordo com a sua recomendação" (source: [[session-2026-10-07-9e3fae7e]], turns 2, 3).
- PRs #120 and #122: a subagent review was posted on each, and the agent fixed the three medium findings on #120 after it checked each in the file. It stopped at "Nenhum foi mergeado: os dois esperam sua autorização" and merged both with merge commits after the user's "autorizo, prossiga" (source: [[session-2026-10-08-0ac17a0f]], turns 8 to 10).

## Scope

Every session merged into `main` with a merge commit, never a squash.
The #111 handoff stated it: "`gh pr merge <n> --merge --delete-branch` (merge commit, nunca squash)", and for a `main` that moved: "integre com merge commit (sem rebase, sem force-push)" (source: [[session-2026-10-07-9e3fae7e]], turn 2).
Before the merge, retest the PR on the current `main`: [[retest-a-pr-on-the-current-main-before-merging-it]]. After it, remove its worktree: [[remove-the-worktree-of-a-merged-pr-with-git-worktree-remove]].
In a stack of PRs, move each upper PR's base to `main` before `--delete-branch` removes it: [[gh-pr-merge-delete-branch-closes-prs-stacked-on-it]].
Authorisation can be given ahead in a handoff prompt: the turn-7 handoff of [[session-2026-10-02-1b324082]] let the next session merge PRs with review and green CI.
In the Phase 2 session the merge of #22 happened after "Merge do #22 autorizado" (source: [[session-2026-09-30-c14af01e]], turn 2); the push and merge confirmation rules of the user's git rules still apply.
