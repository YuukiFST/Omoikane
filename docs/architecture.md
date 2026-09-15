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

## Session capture (build mode)

```
coding session ends a turn  --Stop / SessionEnd hook-->  omoikane/bin/session-capture.py
   reads the harness transcript, no LLM
   skips: OMOIKANE_NO_CAPTURE set, first prompt is /ingest /ask /lint /distill, no file edited
   writes omoikane/raw/inbox/sessions/<date>-<id8>.md   (rewritten on every turn: idempotent)

new session starts  --SessionStart hook-->  omoikane/bin/session-context.py
   prints omoikane/index.md, sections in PAGE_TYPES order, cut to a character budget
```

Why the hook and not the agent: an instruction "save what is valuable" fails silently when the agent forgets or when the session is cut short. The harness fires the hook every time.

Why capture without an LLM: the hook runs on every turn and must return in well under a second. Selection happens once, in `/distill`, on the scheduled run.

Why the quiet period: Stop fires per turn, so a session file may still be growing. `wiki-ingest.ps1` waits until the file has been untouched for `-QuietMinutes`. A session that continues after its file was distilled produces a `-part2` file with only the turns not yet covered; `session-capture.py` reads `turns:` from the distilled copy under `raw/sources/sessions/`.

Why `OMOIKANE_NO_CAPTURE`: the headless runs started by `wiki-ingest.ps1` are sessions too. Without the guard, every distill would capture itself and the loop never ends.

The transcript format is internal to the harness and undocumented. `session-capture.py` reads only the fields seen in real sessions and ignores the rest; a format change thins the capture instead of breaking the hook. `tests/test_session_capture.py` pins the fields it depends on.

## What is deterministic and why

- `index.md` is generated from frontmatter. An LLM-maintained index drifts; a generated one cannot.
- `wiki-lint.py` catches broken links, orphans, missing keys, malformed dates, source pages without `dated`, and `code:` paths that no longer exist in the repository. It runs after every ingest, and its non-zero exit makes the agent fix its own mistakes inside the same call.
- `wiki-ingest.ps1` moves the source file itself if the agent forgot. A re-run with an empty inbox is a no-op.
- `session-capture.py` and `session-context.py` never exit non-zero: a failure there must not stop the harness.

## Where the human stays

- Curating what enters `omoikane/raw/inbox/`.
- `omoikane/_review.md`: contradictions and gaps the agent refuses to resolve alone.
- `AGENTS.md` Domain section: what the wiki is about, what to emphasise.
- Reading the wiki in Obsidian (open `omoikane/` as the vault). The graph view shows hubs and orphans faster than any script.

## Growing it

- Other harnesses: Pi Agent and OpenCode adapters call `session-capture.py` and `session-context.py` with their own transcript reader; the markdown they produce and the rest of the loop stay the same.
- Search: when `index.md` passes a few hundred pages, add qmd or a small BM25 script, and let `session-context.py` inject search hits instead of the whole index.
- Review gate: switch `wiki-ingest.ps1` to commit on a `wiki/auto` branch and merge after reading the diff.
- Capture: point Obsidian Web Clipper, a synced phone folder, or an RSS fetcher at `omoikane/raw/inbox/`.
