# Omoikane

Each coding agent session starts blank: the business rules, design system and conventions the user explained, and what the last session learned, are gone.

Omoikane is a template every new system starts from.
Its agents keep a wiki of that knowledge on their own, from what the user states while building, without asking the user to write anything down.

Named after 思金神 (Omoikane), the kami who gathers the thoughts of the other gods and returns a synthesis.
Built on Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern, with [brainmaxxing](https://github.com/poteto/brainmaxxing) and [ai-memory](https://github.com/akitaonrails/ai-memory) as references. Omoikane's addition: coding sessions are a source too.

## Two uses, one layout

- **Research.** Drop sources into the inbox; the agent ingests them into entity, concept and source pages.
- **Build.** Clone this repository as the root of a new system and run `python omoikane/bin/new-system.py` (Setup, below). Code lives at the root; `omoikane/` is its memory. Every coding session that edits files is captured on stop and distilled into decision and gotcha pages, and every new session starts with the wiki index in context.

## How it works

1. A source arrives in `omoikane/raw/inbox/`: a clipped article, a synced file, or a coding session written there by the `Stop` hook (`omoikane/bin/session-capture.py`, no LLM).
2. `omoikane/bin/wiki-ingest.ps1` runs on a schedule, calls the agent once per file (`/ingest` for sources, `/distill` for sessions), moves the file to `omoikane/raw/sources/`.
3. The agent writes and updates pages under `omoikane/wiki/`, appends to `omoikane/log.md`, and leaves anything it could not decide in `omoikane/_review.md`.
4. `wiki-index.py` regenerates `omoikane/index.md` from page frontmatter. `wiki-lint.py` checks links, orphans, frontmatter and `code:` paths without an LLM.
5. The `SessionStart` hook (`omoikane/bin/session-context.py`) injects the index into every new session, domain rules, decisions and gotchas first, plus any captured session not yet distilled. You read the wiki in Obsidian (vault: `omoikane/`), answer `_review.md`, and ask questions with `/ask`.

## Commands

| Task | Claude Code | OpenCode |
|---|---|---|
| Ingest one source | `/ingest omoikane/raw/inbox/<file>` | same |
| Distill one captured session | `/distill omoikane/raw/inbox/sessions/<file>` | same |
| Ask the wiki | `/ask <question>` | same |
| Semantic health check | `/lint` | same |
| Mark stale, redundant, low-value pages; merge duplicates | `/prune` | same |
| Practices across sessions (also every 5 distills, headless) | `/synthesize [n sessions]` | same |
| Process everything in inbox (headless) | `omoikane/bin/wiki-ingest.ps1` | `omoikane/bin/wiki-ingest.ps1 -Agent opencode` |
| Structural checks (no LLM) | `python omoikane/bin/wiki-lint.py` | same |
| Promote rules ticked in `_review.md` into `AGENTS.md` | `python omoikane/bin/wiki-rules.py` | same |
| Measure what every session loads | `python omoikane/bin/context-budget.py` | same |
| Rebuild index | `python omoikane/bin/wiki-index.py` | same |
| Start a new system from a fresh clone | `python omoikane/bin/new-system.py` | same |
| Tests | `python -m unittest discover -s tests` | same |

Both agents run the same prompt files in `omoikane/prompts/`; the skill and command folders are thin wrappers.

## Session hooks

The two scripts are harness-independent; each harness registers them its own way, and the registration is committed in the repository.

| Harness | Registration | Index at start | Capture on stop |
|---|---|---|---|
| Claude Code | `.claude/settings.json` | `SessionStart` | `Stop`, `SessionEnd` |
| Pi | `.pi/extensions/omoikane.ts` | `before_agent_start` (system prompt) | `agent_end`, `session_shutdown` |
| OpenCode | `.opencode/plugins/omoikane.ts` | `experimental.chat.system.transform` | `session.idle`, plugin `dispose` |

Pi loads a project extension only after you trust the project (`pi` asks once; headless runs need `--approve` or `defaultProjectTrust`).
OpenCode installs `@opencode-ai/plugin` into `.opencode/` on first start and ignores those files itself.
Manual capture from a saved session: `python omoikane/bin/session-capture.py --harness pi --transcript <file>.jsonl`, or `opencode export <id> > s.json` then `--harness opencode --transcript s.json`.

## Setup

```powershell
git clone <repo> my-project
cd my-project
python -m unittest discover -s tests       # sanity check
python omoikane/bin/new-system.py          # empty the template's own memory; then commit
git remote add origin <new-system-url>     # the script renamed the template's remote to `template`
omoikane/bin/install-schedule.ps1          # optional: Task Scheduler job every 30 min
```

`new-system.py` removes the wiki, log entries, review items and captures the template carries about its own development, which the brief would otherwise inject into every session of the new system. It refuses a tree with uncommitted changes and commits nothing, so `git restore .` undoes it. It also renames `origin` to `template`: the scheduled run publishes to `origin`, and the new system's pages must not reach the template. `docs/specs/` holds the template's own plans; delete it or keep it as history.

Requirements: Python 3.11+, `claude` or `opencode` on PATH (they run the wiki operations; `pi` sessions are captured but Pi has no `/ingest`, `/distill`, `/ask`, `/lint` yet), git.

Architecture, conventions and the reasoning behind them: `docs/architecture.md`. The agent's own operating manual: `AGENTS.md`.
