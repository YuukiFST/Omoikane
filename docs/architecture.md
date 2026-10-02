# Architecture

Objective: every new system starts from this template, and its agents feed the wiki on their own with what the user states while building, domain knowledge included (business rules, design system, organisation conventions). A change to this repository is worth making only when it moves the tool towards that; the plan that set it down is [specs/2026-10-02-realign-to-objective.md](specs/2026-10-02-realign-to-objective.md).

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

The template's repository is built with Omoikane too, so its `omoikane/` holds the memory of Omoikane's own development. `omoikane/bin/new-system.py` empties it in a fresh clone (#66): every page, capture and source, the log and review entries, the rules block of `AGENTS.md`. Why a script and not a separate empty template branch: the branch would drift from `main` on every change to the prompts and scripts. Why it refuses uncommitted changes and never commits: `git restore .` then undoes a run, including one started by mistake in the template itself.

## Autonomy loop

```
omoikane/raw/inbox/*           --Task Scheduler (omoikane/bin/install-schedule.ps1)-->  omoikane/bin/wiki-ingest.ps1 -Commit
   review-gate.py prepare        worktree <repo>-wiki-auto on wiki/auto: merge origin/wiki/auto, then origin/main;
                                 move the quiet inbox files into it
   <worktree>/omoikane/bin/wiki-ingest.ps1 -Commit -NoGate
     for each file:  claude -p "/ingest <file>"      plain source   (or opencode run)
                     claude -p "/distill <file>"     captured session, only when idle > 30 min
                     python omoikane/bin/wiki-lint.py      findings handed back to the agent, up to two rounds
                     python omoikane/bin/wiki-index.py     regenerate index.md
                     git commit                            one commit per file, on wiki/auto
   review-gate.py publish        push wiki/auto; open the PR to main, or let the push update the open one
```

Why a gate: the run once committed onto whatever branch the checkout had, usually `main`, with nobody reading the diff first (#45). Now the human's checkout is never committed to or switched, and merging the PR is the human's act. Why a worktree and not a clone: it shares the refs, so `session-capture.py` sees on `wiki/auto` the parts of a session already distilled but not merged, and a session that goes on does not capture them again. Why merges and not a rebase: the branch is pushed and may be under review. `log.md` merges by union (`.gitattributes`): both sides only append. `_review.md` does not: the human deletes and ticks bullets there, and a union merge brought deleted bullets back and duplicated ticked ones, so a conflict in it is resolved as main's file plus the bullets the branch added. A conflict in the generated `index.md` is resolved by regenerating it; any other conflict stops the run for the human. `prepare` also refuses a `wiki/auto` that differs from `main` outside what `-Commit` commits: the scheduler runs the worktree's own scripts, and the branch is not protected the way `main` is. Publishing waits for the run to exit 0: a blocked run publishes nothing, and its marker in the worktree stops every later `prepare`. A source whose operation failed stays in the worktree's inbox and is retried. After a squash or rebase merge, of the tip or of an earlier head, `prepare` finds the landed commits on main by patch id and records them as merged (main up to them by a normal merge, the landed commits with `-s ours`), so a bullet the human deletes afterwards stays deleted, and `publish` finds nothing new. A PR closed unmerged is not opened again while `wiki/auto` still holds its commits.

The agent's semantic pass (`/lint`) runs on demand or weekly and writes to `omoikane/_review.md`.
It changes no page, so an unattended run cannot damage the wiki.
After every `-SynthesizeEvery` distills (5 by default; `omoikane/bin/synthesize-due.py` counts them in `log.md`), the same script runs `/synthesize` once. When that run writes no `synthesize` heading, the script appends one, or every later run would start it again.

`/distill` routes each lesson it keeps to one destination: a guard (a `wiki-lint.py` rule, a test, a hook), a fix to an Omoikane prompt, a wiki page, or a todo.
Why not a page for everything: a page prevents a mistake only when a later agent reads it, and a guard fails every time the mistake is made. A lesson about how distill or ingest runs is a defect in the prompt, not knowledge about the system being built.
Guards and prompt fixes reach `omoikane/_review.md` as diffs and wait for the human: a scheduled run that rewrites its own prompt or checks changes every later run with nobody having read the change.
Deleting a bullet is the whole rejection. At the start of each scheduled run, `omoikane/bin/review-removals.py` appends `- removed (<kind>) <slug>` to `log.md` for every item the log shows routed (or, for `/lint`, `unguarded`) that `_review.md` no longer names, and `/distill`, `/synthesize` and `/lint` do not file a removed slug again. An interactive `/distill` right after a deletion runs before the script and may file it once more. Why not tell applied from rejected: either way the human decided, and an applied guard already stops the lesson. Why a script and not the next distill noticing: the deletion is only visible as an absence, which a prompt reading one session cannot see. Because an absence is permanent, the script errs towards "still open": a bullet counts while any line outside the diff fences names its kind and slug, it records nothing while a fence is left open, and `review-ticks.py` fails a run that deleted or rewrote a bullet, so only the human's deletions are recorded.

## Session capture (build mode)

```
coding session ends a turn  --stop hook of the harness-->  omoikane/bin/session-capture.py --harness <claude|pi|opencode>
   reads the harness transcript, no LLM
   skips: OMOIKANE_NO_CAPTURE set, first prompt runs an operation of omoikane/prompts/, no file edited, subagent session
   replaces every term listed in omoikane/.capture-redact (gitignored) with [redacted]
   writes omoikane/raw/inbox/sessions/<date>-<id8>.md   (rewritten on every turn: idempotent)

new session starts  --start hook of the harness-->  omoikane/bin/session-context.py
   prints pending work (undistilled captures, open _review.md items), then omoikane/index.md
   index filled entry by entry up to a character budget: each section first gets a floor (half the budget,
   shared equally), the rest goes in PAGE_TYPES order; a last line counts what was omitted
```

Why the hook and not the agent: an instruction "save what is valuable" fails silently when the agent forgets or when the session is cut short. The harness fires the hook every time.

Why capture without an LLM: the hook runs on every turn and must return in well under a second. Selection happens once, in `/distill`, on the scheduled run.

Why redact at capture: the scheduled run commits and pushes every capture, and under `raw/sources/` it is immutable, so a name the user does not want published (an organisation, a customer, a private path) has to be gone before the file is written (#62). The list stays out of git because it names what it hides. A term matches in any case, with `\` and `/` interchangeable and any whitespace run between its words, and the start of a term cut by a clip goes too; the frontmatter keys continuation reads (`session`, `turns`, ...) are left alone. Each drive spelling of a path (`C:/x`, `/c/x`) is a separate line. The list is per checkout: a session in a linked worktree reads that worktree's file. A redacted term in the middle of a path or command loses that detail for `/distill`; the alternative was a hand redaction after the fact (`286fbc6`), which reaches the remote only if someone remembers.

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

## Domain knowledge

The objective names it: the business rules, design system and organisation conventions the user states while building. A `domain` page holds one of them, `summary` being the rule itself, since only the summary reaches the brief.

Why a type of its own (#64):

- The existing types were shaped for lessons about code. A practice needs two sessions; a rule the user states once is already true. A decision needs rejected alternatives; "prices are integer cents" has none. A concept page is not imperative, has no source floor and comes after decisions, gotchas and practices in the brief.
- One type, not three: a business rule, a design-system rule and a convention share the lifecycle (stated by an authority, valid from one statement, may contradict the code, needs the statement). Tags tell them apart.
- `wiki-lint.py` fails a domain page that cites no existing source page: a rule nobody stated is the agent's guess, and every later session would obey it. `session-context.py` lists domain pages first, so the brief cuts them last.

Why the `## Domain` section of `AGENTS.md` went away: it waited for the human to describe the domain by hand, which the objective rules out. The domain now arrives the way everything else does, through capture and distill.

## Pruning

The wiki only grows unless something removes pages. `/prune` (on demand) marks stale, redundant and low-value pages with `prune:` in their frontmatter and merges each duplicate into the stronger page, repointing the links.
Why it never deletes: a deleted page takes its history with it, and a wrong deletion by an unattended run is found late. The marks sit in the git diff; the human deletes, and `index.md` shows the mark until then.
Why it stops under three findings: a diff is worth a human's review only when it holds several changes; one or two go to the next run (the gate comes from brainmaxxing's `meditate`).

## Promoted rules and the context budget

A practice page reaches an agent only when the agent opens it. The few practices that govern most tasks can be promoted into the rules block of `AGENTS.md`, which every session loads.
`/synthesize` proposes them as `- [ ] rule` bullets in `_review.md`; the human ticks one and runs `python omoikane/bin/wiki-rules.py`, which moves it into the block with a pointer to its page.

Why a script and not the agent: approval must be a human act. The scheduled run's permissions do not include `wiki-rules.py`, so an agent cannot tick a box and promote in the same run.
Why a cap of 15 and a budget gate: `AGENTS.md` is a shared budget, and adherence drops for every rule as it grows, not only for the new ones. `wiki-rules.py` refuses at the cap, so admitting a rule means retiring one. `context-budget.py` estimates the tokens of `AGENTS.md`, the skill descriptions and the `session-context.py` output at 3.5 characters each and fails CI above the limits in the script. The brief is measured on a generated tree past every bound (an index past its budget in every section, more pending captures than the brief lists; within one index entry of the cap), not only on this repository's wiki: the wiki was empty in CI, so a raised cap would have passed.

## What is deterministic and why

- `index.md` is generated from frontmatter. An LLM-maintained index drifts; a generated one cannot.
- `wiki-lint.py` catches broken links, orphans, missing keys, malformed dates, source pages without `dated`, two pages sharing a slug, and `code:` paths that no longer exist in the repository or are absolute. A `code:` entry is resolved from its git spelling (`/`, no `./`), so a page written on Windows gets the same result on the Linux CI. A `code:` path with a commit dated after the page's `updated` is a warning, not a finding: most code changes leave the page true, so `/lint` reads the warnings and judges. One `git log --first-parent` call, limited to the `code:` paths, serves every page, so a merged change is dated at its merge. A shallow clone or a copy without git skips the check: every file would carry the same date. A gotcha must say which check guards it (`guard: lint | test | hook | none`); one still at `none` `GUARD_GRACE_DAYS` (14) days after it was written is another warning, because a mistake only a page prevents recurs whenever an agent skips the page. It runs after every operation. An interactive agent runs it and fixes its findings itself; in a scheduled run `wiki-ingest.ps1` runs it and hands the findings back to the agent, which has no shell.
- `wiki-ingest.ps1` moves the source file itself: the headless agent may not. A re-run with an empty inbox is a no-op.
- The headless run may read the repository and edit pages (`.md`) under `omoikane/wiki/`, `omoikane/log.md` and `omoikane/_review.md`; nothing else, and no shell at all. Why no shell, not even for index and lint: an allowed script is code the agent can replace or shadow from a directory it writes to (a `.py` under `omoikane/wiki/` ran as `python omoikane/bin/wiki-index.py` from inside `omoikane/wiki/`), and four of five runs had their index and lint calls denied anyway, for an `echo` or a `cd` added to them. `wiki-ingest.ps1` runs `wiki-lint.py` after the agent and hands its findings back, up to two rounds, then commits the operation as it stands. The scope lives in `omoikane/bin/headless-scope.py`, rendered for both harnesses so they cannot drift:
  - Claude Code: `--tools Read,Glob,Grep,Edit,Write`, `--permission-mode dontAsk` with the edit allowlist and reads anchored at the repository (`Read(/**)`, `.env*` denied; a bare `Read` reached `~/.ssh`), project settings only (`--setting-sources project`: a user-level `Bash(git checkout:*)` or a PreToolUse hook answering allow would apply too), `--strict-mcp-config`. `acceptEdits` was dropped because it also auto-approves `rm`, `mv`, `cp` and `sed`.
  - OpenCode: `opencode run --pure --agent omoikane-headless-<random>` with the prompt as the message; the agent is defined in `OPENCODE_CONFIG_CONTENT`, every permission map opening with `"*": "deny"`. Why an agent: OpenCode merges config maps key by key, so a user's `"bash": {"*": "allow", "git *": "allow"}` kept `git *` after a top-level `"*": "deny"`, and the last matching rule wins; agent rules come after the top-level ones. Why a random name: a same-named agent in the user's config merges into it the same way. Why not `--command`: a command's own `agent` overrides `--agent`. No rule restricts `apply_patch`: OpenCode offers it in place of edit and write to a gpt- model, it checks `edit` on the source of a move only, and a deny on it maps onto `edit`. So before each call `wiki-ingest.ps1` reads the tools OpenCode resolves (`opencode debug agent`, no model call) and refuses to run when any tool outside the scope is offered. `--pure` keeps user plugins out; user MCP servers still start, and `read` denies their resources.
- Permission rules belong to the harness and have holes the harness owns, so `wiki-ingest.ps1` also snapshots the tree (HEAD, the staged tree, a hash of every changed or untracked file, size and mtime of every ignored one: a user's global git ignore hides paths such as `.claude/settings.local.json` from `git status`; the git hooks, `info/exclude`, `info/attributes` and the config keys that can run code, which the git commands after the agent run or read; not `branch.*`, `remote.*` or `info/refs`, which routine git work in any worktree of the repository rewrites) before each operation and runs `headless-scope.py verify` after every agent call, from a private copy under `python -I` so nothing the agent wrote is on its path. A change outside the scope writes `omoikane/.wiki-ingest.blocked` (under the review gate, in its worktree), stops the run with nothing committed and makes every later run refuse until the human deletes the file; nothing is restored, the human reads what happened. A check that fails to give a verdict blocks the same way (a crash of `verify` once failed open), and so does a failure of `review-ticks.py`, `wiki-index.py`, `git add` or `git commit`. `-Commit` commits only the paths an operation may change, the moved source by name, and nothing the human had staged. It refuses to start an operation while those paths hold uncommitted changes, and a failed operation that left some blocks the run: the next commit would otherwise take them under its own message. Not seen by the check: paths outside the repository and the inside of a nested repository. Anything else writing ignored files during a run (a coding session's `__pycache__`, an editor's state) blocks it, so a scheduled run needs a tree nobody else works in (the review gate gives it its own worktree). Any `[x]` tick the run adds to `_review.md` is undone by `review-ticks.py`, since ticking is the human's approval.
- `session-capture.py` and `session-context.py` never exit non-zero: a failure there must not stop the harness.

## Where the human stays

- Curating what enters `omoikane/raw/inbox/`.
- `omoikane/_review.md`: contradictions and gaps the agent refuses to resolve alone, and the guards and prompt changes it proposes. Ticking `[x]` is the approval.
- Reading the wiki in Obsidian (open `omoikane/` as the vault). The graph view shows hubs and orphans faster than any script.

## Growing it

- Other harnesses: a reader in `session-capture.py` plus the hook registration the harness supports; the markdown and the rest of the loop stay the same (Pi and OpenCode are the two examples).
- Search: when `index.md` passes a few hundred pages, add qmd or a small BM25 script, and let `session-context.py` inject search hits instead of the whole index.
- Capture: point Obsidian Web Clipper, a synced phone folder, or an RSS fetcher at `omoikane/raw/inbox/`.
