---
title: session-capture
type: entity
summary: omoikane/bin/session-capture.py, turns a Claude Code, Pi or OpenCode transcript into an inbox session file
tags: [session-capture, module, build-mode]
created: 2026-09-30
updated: 2026-10-07
sources: [wiki/sources/session-2026-09-15-e04462b2.md, wiki/sources/session-2026-09-30-c14af01e.md, wiki/sources/session-2026-09-30-230a182d.md, wiki/sources/session-2026-10-02-1b324082.md, wiki/sources/session-2026-10-02-a8b45323.md, wiki/sources/2026-10-06-pstack-skills-review-round-2.md, wiki/sources/session-2026-10-06-fd3ff955.md, wiki/sources/session-2026-10-06-973284b2.md, wiki/sources/session-2026-10-07-062e80af.md]
code: [omoikane/bin/session-capture.py, tests/test_session_capture.py]
---

`omoikane/bin/session-capture.py` writes a coding session into `omoikane/raw/inbox/sessions/` for distill.

## Harnesses

`--harness claude|pi|opencode` selects one transcript reader; all produce the same Session/Turn objects (source: [[session-2026-09-15-e04462b2]], turn 3).

- Claude Code: the JSONL transcript, called from `.claude/settings.json` hooks (turn 2).
- [[pi-coding-agent]]: the session JSONL, a tree; the reader walks from the last entry to the root and drops dead `/tree` branches (turn 3).
- [[opencode]]: the `opencode export` document `{info, messages}`; sessions with a `parentID` (subagents) are skipped (turn 3).

## Skipped operations

Sessions that run an Omoikane operation are not captured; the operation names are read from the files in `omoikane/prompts/`, so a new prompt such as `/synthesize` is skipped without a code change (source: [[session-2026-09-30-c14af01e]], turn 2).

Only the first prompt marks a session as an operation (PR #35, issue #34): before, the Claude reader dropped a coding session that ran a command in a later turn (source: [[session-2026-09-30-230a182d]], turn 2).
The review of #35 found two more cases, fixed with tests first: harness command entries before the first real prompt are looked past, and the command tag is anchored, `COMMAND_TAG.match` instead of `.search` (turn 2).
Tests: `OperationOnlyFromTheFirstPrompt` in `tests/test_session_capture.py`.
Since issue #111 (PR #114) a Pi `/skill:<name>` prompt, typed or expanded, also marks an operation: [[pi-expands-a-skill-command-into-a-skill-block]] (source: [[session-2026-10-07-062e80af]], turn 6).

## Naming and continuation

Files are named by the tail of the session id and continuation matches the full id: [[session-file-name-uses-id-tail]].

## Paths

Paths are normalised to `/` before being made relative to the session cwd: [[opencode-mixes-path-separators-on-windows]].

## Redaction

Terms listed in the gitignored `omoikane/.capture-redact` are replaced with `[redacted]` before the capture is written (issue #62, PR #69): [[redact-captures-when-they-are-written]] (source: [[session-2026-10-02-1b324082]], turn 3).
The frontmatter ids, clipped terms and the term list's encoding each broke the first version: [[capture-redaction-breaks-on-frontmatter-clips-and-encodings]].

Since issue #77 (PR #82) `redact_secrets` also replaces API keys, tokens, private keys and passwords, with or without a term list, before the listed terms (source: [[session-2026-10-02-a8b45323]], turn 2; `redact_capture`). Three review rounds found leaks, an unterminated PEM erasing turns and 85 s of backtracking: [[secret-redaction-patterns-leak-swallow-and-backtrack]].
[[bootstrap]] runs the same redaction on what it seeds.

## Prompt length

The capture clipped each prompt at 2000 characters (`session-capture.py:130` at the time); the agent counted four cases where a rule the user stated past the cut never became a page (source: [[session-2026-10-06-fd3ff955]], turn 3).
Issue #104 (PR #109, commit `1a946fe`) raised the limit to `PROMPT_CHARS = 20_000`; the commit gives 10,306 characters as the longest prompt captured so far.
Captures written before `1a946fe` still hold cut prompts, marked `[... N chars cut]`.
The agent measured before the change: 10 prompts cut in 10 of 15 captures, 50,696 characters cut, and whole prompts add about 11% to the captures (source: [[session-2026-10-06-973284b2]], turn 2).
It timed redaction on texts of 20,000 characters before raising the limit (turn 2).
The review of #109 found two more gaps, fixed in `b76c817`: [[opencode-read-tool-cuts-lines-at-2000-characters]], so lines are wrapped after redaction ([[reshaping-capture-text-before-redaction-leaks-secrets]]); and the `curl` and `mysql` scans took over 1 s a turn on a long line ([[secret-redaction-patterns-leak-swallow-and-backtrack]]) (turn 3).

## Failures

The capture swallowed every exception and exited 0, so a capture that crashed on every turn lost sessions with no signal (source: [[2026-10-06-pstack-skills-review-round-2]], proposal 2).
A redaction defect once crashed every later turn; a PR review caught it before merge (proposal 2).
Since issue #103 (PR #107, `872319e`) the capture still exits 0, but appends the failure to the gitignored `omoikane/.capture-errors`, and [[session-context]] names it in the next brief (`session-capture.py` docstring, line 6).
The line holds the UTC time, the harness, the tail of the session id and the error, redacted as a capture is (source: [[session-2026-10-06-973284b2]], turn 2; `record_error`).
A scheduled run sets `OMOIKANE_NO_CAPTURE` (`wiki-ingest.ps1:32`) and `main()` returns before it reads anything, so a headless run never writes the file (turn 2).
The review of #107 found two defects (turn 2), fixed in `fff42de`: a redact list in the ANSI code page also broke the failure record ([[capture-redaction-breaks-on-frontmatter-clips-and-encodings]]), and joining the message's lines before redaction leaked a private key ([[reshaping-capture-text-before-redaction-leaks-secrets]]).
