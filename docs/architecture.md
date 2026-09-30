# Architecture

Three layers, as in Karpathy's LLM Wiki pattern, plus one rule that makes it run unattended: bookkeeping is code, only meaning goes through the LLM.

## Layers

| Layer | Path | Owner |
|---|---|---|
| Raw sources | `omoikane/raw/` | Human, plus the session hook. Immutable once in `raw/sources/`. |
| Wiki | `omoikane/wiki/` | Agent. Every page, every cross-reference. |
| Schema | `AGENTS.md`, `omoikane/prompts/` | Human and agent together. |
| System under construction | repository root | Whoever builds it. Omoikane only reads it. |

`CLAUDE.md` contains only `@AGENTS.md`, so Claude Code and OpenCode read one manual.
Everything Omoikane owns sits under `omoikane/` so the same clone serves as a research wiki or as the root of a software project.

## Autonomy loop

```
omoikane/raw/inbox/*           --Task Scheduler (omoikane/bin/install-schedule.ps1)-->  omoikane/bin/wiki-ingest.ps1
   for each file:  claude -p "/ingest <file>"      plain source   (or opencode run)
                   claude -p "/distill <file>"     captured session, only when idle > 30 min
                   python omoikane/bin/wiki-index.py     regenerate index.md
                   python omoikane/bin/wiki-lint.py      structure check, non-zero on findings
                   git commit                            one commit per file
```

The agent's semantic pass (`/lint`) runs on demand or weekly and writes to `omoikane/_review.md`.
It changes no page, so an unattended run cannot damage the wiki.
After every `-SynthesizeEvery` distills (5 by default; `omoikane/bin/synthesize-due.py` counts them in `log.md`), the same script runs `/synthesize` once. When that run writes no `synthesize` heading, the script appends one, or every later run would start it again.

`/distill` routes each lesson it keeps to one destination: a guard (a `wiki-lint.py` rule, a test, a hook), a fix to an Omoikane prompt, a wiki page, or a todo.
Why not a page for everything: a page prevents a mistake only when a later agent reads it, and a guard fails every time the mistake is made. A lesson about how distill or ingest runs is a defect in the prompt, not knowledge about the system being built.
Guards and prompt fixes reach `omoikane/_review.md` as diffs and wait for the human: a scheduled run that rewrites its own prompt or checks changes every later run with nobody having read the change.

## Session capture (build mode)

```
coding session ends a turn  --stop hook of the harness-->  omoikane/bin/session-capture.py --harness <claude|pi|opencode>
   reads the harness transcript, no LLM
   skips: OMOIKANE_NO_CAPTURE set, first prompt runs an operation of omoikane/prompts/, no file edited, subagent session
   writes omoikane/raw/inbox/sessions/<date>-<id8>.md   (rewritten on every turn: idempotent)

new session starts  --start hook of the harness-->  omoikane/bin/session-context.py
   prints pending work (undistilled captures, open _review.md items), then omoikane/index.md
   index filled entry by entry in PAGE_TYPES order up to a character budget; a last line counts what was omitted
```

Why the hook and not the agent: an instruction "save what is valuable" fails silently when the agent forgets or when the session is cut short. The harness fires the hook every time.

Why capture without an LLM: the hook runs on every turn and must return in well under a second. Selection happens once, in `/distill`, on the scheduled run.

Why the quiet period: Stop fires per turn, so a session file may still be growing. `wiki-ingest.ps1` waits until the file has been untouched for `-QuietMinutes`. A session that continues after its file was distilled produces a `-part2` file with only the turns not yet covered; `session-capture.py` reads `turns:` from the distilled copy under `raw/sources/sessions/`.

Why `OMOIKANE_NO_CAPTURE`: the headless runs started by `wiki-ingest.ps1` are sessions too. Without the guard, every distill would capture itself and the loop never ends.

One reader per harness in `session-capture.py` (`--harness claude|pi|opencode`) produces the same turns; the Markdown, the skip rules and the continuation logic are shared. Claude Code's transcript is internal and undocumented, so its reader keeps only the fields seen in real sessions. Pi's session file is documented ([session-format.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/session-format.md): JSONL tree, the reader follows the active branch from the last entry to the root). OpenCode keeps sessions in SQLite, so the reader takes the `opencode export` document (`{info, messages: [{info, parts}]}`), which the plugin rebuilds from the SDK (`client.session.get`, `client.session.messages`). Every reader ignores what it does not recognise; a format change thins the capture instead of breaking the hook. Whether the first prompt runs an operation is decided once, by `Session.first_command`, not by each reader: the Claude reader once latched a command from any turn and dropped a coding session that ran `/ask` later (#34). Harness commands nobody answered, such as a `/clear` at the head of a Claude transcript, do not count as the first prompt. `tests/test_session_capture.py` pins the fields each reader depends on, with a fixture per harness under `tests/fixtures/`.

Where each harness registers the hooks, and why that shape:

- Claude Code: `.claude/settings.json`, `SessionStart` / `Stop` / `SessionEnd`, with the transcript path in the hook payload.
- Pi: `.pi/extensions/omoikane.ts`. `before_agent_start` appends the index to the system prompt (computed once per session; Pi has no persisted session-start injection). `agent_end` fires once per prompt and `session_shutdown` on exit, both with the session file path from `ctx.sessionManager.getSessionFile()`.
- OpenCode: `.opencode/plugins/omoikane.ts`. `experimental.chat.system.transform` adds the index to the system prompt (once per session). `session.idle` fires once per prompt; event handlers are not awaited by OpenCode, so `dispose` also captures every session not yet captured, which is what makes `opencode run` capture before it exits. A command is stored as its expanded template, which `Session.first_command` recognises. Sessions with a `parentID` are subagents and are skipped.

File names end in the last eight characters of the session id: Pi ids are UUIDv7 and OpenCode ids are time-ordered, so the head is shared by sessions started close together.

## Cross-session pass

`/distill` reads one session, so it cannot see a workflow four sessions repeated, a preference the user keeps restating, or a candidate it skipped as a one-off that keeps coming back.
`/synthesize` reads the last N session pages side by side, plus the `routed` and `skipped` lines of `log.md` grouped by slug, and writes what two or more sessions show.

Why a new page type, `practice`, and one rather than two (`procedure` and `principle`):

- A procedure (steps in an order that matters) and a preference (the user's own words) share everything the loop cares about: evidence from two or more sessions, an imperative rule you can catch an agent breaking, and candidacy for the managed block of `AGENTS.md`. Two types would split one lifecycle.
- The existing types do not fit. A decision records alternatives rejected once; a practice recurs. A concept page is not imperative, and filing practices there hides them among themes.
- A type of its own lets code enforce the floor: `wiki-lint.py` fails a practice citing fewer than two distinct sessions (two parts of one session count once), and `session-context.py` ranks practices right after decisions and gotchas.

Why every N distills and not on each one: a pattern needs sessions to cross, and one LLM call per batch costs less than one per session.
Why the log is the counter: it is already the append-only chronology, so no state file can drift from it.

## Pruning

The wiki only grows unless something removes pages. `/prune` (on demand) marks stale, redundant and low-value pages with `prune:` in their frontmatter and merges each duplicate into the stronger page, repointing the links.
Why it never deletes: a deleted page takes its history with it, and a wrong deletion by an unattended run is found late. The marks sit in the git diff; the human deletes, and `index.md` shows the mark until then.
Why it stops under three findings: a diff is worth a human's review only when it holds several changes; one or two go to the next run (the gate comes from brainmaxxing's `meditate`).

## Promoted rules and the context budget

A practice page reaches an agent only when the agent opens it. The few practices that govern most tasks can be promoted into the rules block of `AGENTS.md`, which every session loads.
`/synthesize` proposes them as `- [ ] rule` bullets in `_review.md`; the human ticks one and runs `python omoikane/bin/wiki-rules.py`, which moves it into the block with a pointer to its page.

Why a script and not the agent: approval must be a human act. The scheduled run's permissions do not include `wiki-rules.py`, so an agent cannot tick a box and promote in the same run.
Why a cap of 15 and a budget gate: `AGENTS.md` is a shared budget, and adherence drops for every rule as it grows, not only for the new ones. `wiki-rules.py` refuses at the cap, so admitting a rule means retiring one. `context-budget.py` estimates the tokens of `AGENTS.md`, the skill descriptions and the `session-context.py` output at 3.5 characters each and fails CI above the limits in the script.

## What is deterministic and why

- `index.md` is generated from frontmatter. An LLM-maintained index drifts; a generated one cannot.
- `wiki-lint.py` catches broken links, orphans, missing keys, malformed dates, source pages without `dated`, two pages sharing a slug, and `code:` paths that no longer exist in the repository or are absolute. A `code:` entry is resolved from its git spelling (`/`, no `./`), so a page written on Windows gets the same result on the Linux CI. A `code:` path with a commit dated after the page's `updated` is a warning, not a finding: most code changes leave the page true, so `/lint` reads the warnings and judges. One `git log --first-parent` call, limited to the `code:` paths, serves every page, so a merged change is dated at its merge. A shallow clone or a copy without git skips the check: every file would carry the same date. A gotcha must say which check guards it (`guard: lint | test | hook | none`); one still at `none` `GUARD_GRACE_DAYS` (14) days after it was written is another warning, because a mistake only a page prevents recurs whenever an agent skips the page. It runs after every ingest, and its non-zero exit makes the agent fix its own mistakes inside the same call.
- `wiki-ingest.ps1` moves the source file itself: the headless agent may not. A re-run with an empty inbox is a no-op.
- The headless Claude Code run loads project settings only (`--setting-sources project`, `--strict-mcp-config`, built-in tools only), runs in `--permission-mode dontAsk` with an allowlist, and has every `git` command denied: edits only under `omoikane/wiki/`, `omoikane/log.md` and `omoikane/_review.md`, and only `wiki-index.py` and `wiki-lint.py`, named exactly. It cannot write a script and run it, reach `AGENTS.md` or the prompts, or delete, move or check out a file. `acceptEdits` was dropped because it also auto-approves `rm`, `mv`, `cp` and `sed` inside the repository; user settings were dropped because their allow rules and hooks (a user-level `Bash(git checkout:*)`, a PreToolUse hook answering allow) would apply too. Any `[x]` tick the run adds to `_review.md` is undone by `review-ticks.py`, since ticking is the human's approval. The OpenCode path (`-Agent opencode`) is not scoped: OpenCode reads permissions from its own config, which this repository does not ship.
- `session-capture.py` and `session-context.py` never exit non-zero: a failure there must not stop the harness.

## Where the human stays

- Curating what enters `omoikane/raw/inbox/`.
- `omoikane/_review.md`: contradictions and gaps the agent refuses to resolve alone, and the guards and prompt changes it proposes. Ticking `[x]` is the approval.
- `AGENTS.md` Domain section: what the wiki is about, what to emphasise.
- Reading the wiki in Obsidian (open `omoikane/` as the vault). The graph view shows hubs and orphans faster than any script.

## Growing it

- Other harnesses: a reader in `session-capture.py` plus the hook registration the harness supports; the markdown and the rest of the loop stay the same (Pi and OpenCode are the two examples).
- Search: when `index.md` passes a few hundred pages, add qmd or a small BM25 script, and let `session-context.py` inject search hits instead of the whole index.
- Review gate: switch `wiki-ingest.ps1` to commit on a `wiki/auto` branch and merge after reading the diff.
- Capture: point Obsidian Web Clipper, a synced phone folder, or an RSS fetcher at `omoikane/raw/inbox/`.
