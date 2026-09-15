# Build mode: capture coding sessions into the wiki

Issue: #5. Status: approved in chat on 2026-09-15, implemented in the same branch.

## Problem

Omoikane ingests only what a human drops into the inbox.
When the template is the root of a software project, the knowledge worth keeping is produced inside coding sessions: a decision between two designs, a library that behaves unlike its docs, a bug whose cause took an hour to find.
None of that becomes a file, so it is lost, and the next agent starts from zero.

## Goals

- One layout serves both uses: research wiki and project template.
- Capture is guaranteed by the harness, not by the agent remembering.
- Capture costs no LLM call; selection happens once, in a scheduled run.
- Every new session starts knowing what the wiki holds.
- Stale knowledge about code is detectable without an LLM.

## Non-goals

- Pi Agent and OpenCode hook adapters (follow-up issue; the scripts are harness-independent).
- Search or relevance ranking at session start (the whole index is injected until it outgrows a budget).
- Any change to the research-mode ingest flow beyond paths.

## Decisions

| Decision | Chosen | Rejected | Why |
|---|---|---|---|
| Capture trigger | `Stop` and `SessionEnd` hooks run a script | Agent instructed to write notes; git post-commit hook | Instructions fail silently; commits miss dead ends and reasoning. Hooks fire every time. |
| Capture cost | No LLM in the hook; `/distill` on the scheduled run | `claude -p /distill` inline on Stop | Stop fires per turn; an LLM call there is slow and paid on every trivial turn. |
| Layout | Everything under `omoikane/`; root free for the system | Template as root with `src/` beside `wiki/`; separate repo | One layout for both uses; root stays clean; Obsidian vault is `omoikane/`. Visible folder because Obsidian ignores dot-folders. |
| Retrieval | `SessionStart` hook injects `index.md` under a character budget | AGENTS.md instruction only; per-prompt search | Guaranteed by the harness; search comes when the index outgrows the budget. |
| Page types | `decision` and `gotcha` added, with optional `code:` paths | Tags on `concept` | A later agent filters by folder, not by tag; lint can check `code:` paths. |
| Recursion guard | `OMOIKANE_NO_CAPTURE=1` set by `wiki-ingest.ps1`, plus first-prompt check for `/ingest` `/ask` `/lint` `/distill` | Hook checks the process tree | Two cheap checks; either alone has a gap (manual `/ask` in a terminal has no env var; headless runs have the env var). |
| Growing session after distill | `-partN` file with only uncovered turns, from `turns:` in the distilled copy | Re-capture whole session; skip continued sessions | No duplicate distill, no lost turns. |

## Components

- `omoikane/bin/session-capture.py`: hook payload on stdin, or `--transcript` for tests. Parses the Claude Code JSONL, builds one turn per user prompt (prompt, agent text, files edited, shell commands, tool errors), adds `git status --short`, writes Markdown with frontmatter (`session`, `part`, `turns`, `started`, `ended`, `cwd`, `branch`). Skips when guarded, when the first prompt is an Omoikane command, or when nothing was edited. Always exits 0.
- `omoikane/bin/session-context.py`: prints `index.md` without its header, whole sections in `PAGE_TYPES` order, cut at a budget (default 12 000 chars). Prints nothing when guarded or when the wiki is empty. Always exits 0.
- `omoikane/prompts/distill.md`: what counts as a decision or a gotcha, what to skip, where pages go, how a reversal is recorded (`## History`, older page stays), what to do with a session that yields nothing (log entry only).
- `omoikane/bin/wiki-lint.py`: `lint_pages(pages, repo)` pure function; new finding for a `code:` path that does not exist.
- `omoikane/bin/wiki-index.py`: groups in `PAGE_TYPES` order (decision, gotcha, concept, entity, source, query), empty groups omitted, `code:` paths shown inline.
- `omoikane/bin/wiki-ingest.ps1`: recurses the inbox, routes `sessions/` files to `/distill`, waits `-QuietMinutes` (30) after the last write, sets the guard, moves distilled files to `raw/sources/sessions/`.
- `.claude/settings.json`: `SessionStart` (matcher `startup|resume|clear|compact`), `Stop`, `SessionEnd`, all via `${CLAUDE_PROJECT_DIR}` so the cwd does not matter.

## Data flow

1. Coding session edits files; every turn end fires `Stop`; the capture file is rewritten in place.
2. Scheduler runs `wiki-ingest.ps1`; the file has been idle 30 min; `/distill` runs headless with the guard set.
3. Distill writes the session source page, decision and gotcha pages with `code:` paths, entity pages; moves the file; index and lint run.
4. Next session: `SessionStart` injects the index; the agent opens the pages whose `code:` lists the area it is about to touch.
5. Later refactor deletes a file listed in a `code:` list; `wiki-lint.py` fails; the agent updates the page.

## Error handling

- Hook scripts catch every exception, print one line, exit 0. A broken hook must never stop a session.
- Transcript lines that are not JSON, not `user`/`assistant`, or sidechain are ignored.
- `git status` failures (no repo, timeout) yield an empty working-tree section.

## Testing

`python -m unittest discover -s tests`, no LLM, no network.

- `tests/test_session_capture.py`: fixture transcript with meta lines, thinking blocks, sidechain entries, edit and shell tool uses, an error result; asserts turns, files, commands, errors, notes, skip rules, rendered sections, budget trimming.
- `tests/test_wiki_lint.py`: missing `code:` path is a finding; `decision` and `gotcha` pass; index compaction drops the header and cuts on section boundaries.
- Manual: `python omoikane/bin/session-capture.py --transcript <real jsonl>` produced a 31 KB, 5-turn file from a real session on this machine.

## Follow-ups

- Pi Agent and OpenCode adapters: a transcript reader per harness in `session-capture.py`, and the hook registration each harness uses. Done in #7; see `docs/architecture.md`, "Session capture".
- Search-based context injection once `index.md` exceeds the budget.
