---
title: wiki-ingest
type: entity
summary: omoikane/bin/wiki-ingest.ps1, the scheduled run: one headless agent call per inbox file, then /synthesize on cadence
tags: [wiki-ingest, module, headless, autonomy-loop]
created: 2026-09-30
updated: 2026-10-01
sources: [wiki/sources/session-2026-09-15-e04462b2.md, wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-01-b5b6fb27.md]
code: [omoikane/bin/wiki-ingest.ps1, omoikane/bin/synthesize-due.py, omoikane/bin/review-ticks.py, tests/test_wiki_ingest.py, tests/test_powershell_scripts.py]
---

`omoikane/bin/wiki-ingest.ps1` runs `/ingest` on plain sources and `/distill` on captured sessions, one headless agent call per file.

## Agents

`-Agent opencode` first ran `opencode run --command distill <file>` (source: [[session-2026-09-15-e04462b2]], turn 3).
Since PR #40 it runs `opencode run --pure --agent <fresh name> <message>`, the prompt passed as the message (source: [[session-2026-09-30-230a182d]], turn 2); see [[opencode]].

## Permissions

The first scope allowed wiki edits and two scripts: [[headless-runs-scoped-to-wiki-edits-and-two-scripts]] (source: [[session-2026-09-30-c14af01e]], turn 2).
It loads project settings only: [[user-settings-apply-to-headless-claude-runs]] (turn 2).
The headless agent may not move files; the script moves the source after the run (turn 3).
Since PR #40 the agent has no shell, both harnesses take their scope from [[headless-scope]], and a change outside it blocks every later run: [[headless-runs-have-no-shell]] (source: [[session-2026-09-30-230a182d]], turns 2, 4).
With `-Agent opencode` the script starts OpenCode once before the first snapshot: [[opencode-writes-its-own-files-on-first-start]] (source: [[session-2026-10-01-b5b6fb27]], turn 2).

## Commit

`-Commit` commits only the operation's paths; an operation that fails and leaves edits under them blocks the run (source: [[session-2026-10-01-b5b6fb27]], turn 2).
The end-to-end tests added for it cover a fake `opencode`, a crashing `verify`, `review-ticks`, synthesize and the explicit stage (turn 2).

## Lint loop

The script runs `wiki-lint.py` after the agent and hands the findings, not the warnings, back for up to 2 rounds (source: [[session-2026-09-30-230a182d]], turn 4).
Its first version had two bugs found by a real eval: [[powershell-function-output-becomes-its-return-value]] and 26 warnings handed back with the 1 finding (turn 4).
`tests/test_wiki_ingest.py` drives the whole script with a fake `claude`; its tests were red against the `main` version and green on the branch (turn 4).

## Cross-session pass

After a number of distills since the last pass, the script runs `/synthesize` once; `synthesize-due.py` decides (source: [[session-2026-09-30-c14af01e]], turn 2).
When the run writes no log entry, the script appends the heading itself so the next run does not trigger again; the agent tested this with a fake `claude` that writes no log, and a second run did not fire (turn 2).

## Scheduling

`install-schedule.ps1` registers the script in the Windows Task Scheduler; at capture it was not registered, and `-Commit` committed on whatever branch the checkout was on, often `main` (source: [[session-2026-09-30-230a182d]], turn 4).
The review gate (issue #45, unmerged at capture) moves the run to a worktree on branch `wiki/auto` that opens a PR; the agent recommended registering the task only after it lands (turn 4).

`tests/test_powershell_scripts.py` parses every tracked `.ps1` with the PowerShell parser in CI (PR #43) (turn 2).
