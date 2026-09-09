# Omoikane

An LLM-maintained personal wiki that ingests sources on its own, so knowledge compounds instead of being re-derived on every question.

Named after 思金神 (Omoikane), the kami who gathers the thoughts of the other gods and returns a synthesis.

## How it works

1. Drop a file into `raw/inbox/` (Obsidian Web Clipper, a synced folder, by hand).
2. `bin/wiki-ingest.ps1` runs on a schedule, calls the agent once per file, moves the file to `raw/sources/`.
3. The agent writes and updates pages under `wiki/`, appends to `log.md`, and leaves anything it could not decide in `_review.md`.
4. `bin/wiki-index.py` regenerates `index.md` from page frontmatter. `bin/wiki-lint.py` checks links, orphans and frontmatter without an LLM.
5. You read the wiki in Obsidian, answer `_review.md`, and ask questions with `/ask`. Answers are filed under `wiki/queries/`.

## Commands

| Task | Claude Code | OpenCode |
|---|---|---|
| Ingest one source | `/ingest raw/inbox/<file>` | `/ingest raw/inbox/<file>` |
| Ask the wiki | `/ask <question>` | `/ask <question>` |
| Semantic health check | `/lint` | `/lint` |
| Ingest everything in inbox (headless) | `bin/wiki-ingest.ps1` | `bin/wiki-ingest.ps1 -Agent opencode` |
| Structural checks (no LLM) | `python bin/wiki-lint.py` | same |
| Rebuild index | `python bin/wiki-index.py` | same |

Both agents run the same prompt files in `prompts/`; the skill and command folders are thin wrappers.

## Setup

```powershell
git clone <repo> omoikane
cd omoikane
python bin/wiki-lint.py          # sanity check
bin/install-schedule.ps1         # optional: Task Scheduler job every 30 min
```

Requirements: Python 3.11+, `claude` or `opencode` on PATH, git.

Architecture, conventions and the reasoning behind them: `docs/architecture.md`. The agent's own operating manual: `AGENTS.md`.
