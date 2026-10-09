# Omoikane as a software-development toolkit

Status: written before the code, issue #111.

## Problem

Omoikane is a memory template only.
A system built from it starts with seven memory skills (`/ingest`, `/distill`, `/ask`, `/lint`, `/prune`, `/synthesize`, `/wrap-up`) and nothing for the work itself.
On 2026-10-07 the user set a narrower, more precise objective: Omoikane is for software development, not generic research, and it gives the agent the skills for the work plus a mode that picks the best skill for each task, as pstack's `poteto-mode` does (`omoikane/raw/sources/2026-10-07-omoikane-becomes-a-toolkit.md`).

## The objective, restated

Every new software system starts from the template.
Its agents keep the wiki on their own, from what the user states while building, domain knowledge included; that part does not change.
Every system also starts with a set of development skills and with `omoikane-mode`, which routes each task to a playbook and to the skills and principles it needs.

What follows from it:

- The research use goes. `README.md` "Two uses, one layout" becomes one use; `/ingest` stays, for the documents a system's domain comes from (specs, business rules, design-system docs).
- There is no opt-in: every system gets the skills, so there is one skill budget, not one per profile, and a later merge of `template/main` brings skill updates as it brings prompt updates.
- `omoikane/wiki/domain/omoikane-objective.md`, `omoikane/wiki/decisions/objective-criterion-stays-out-of-agents-md.md`, the opening of `docs/architecture.md` and the opening of `README.md` change. The wiki pages change through `/wrap-up`, from the inbox note above, not by hand.
- `AGENTS.md` has no budget room: with a full rules block it measures 2,796 of 2,800 tokens (`tests/test_wiki_rules.py`). Its opening is reworded at equal or smaller length; the toolkit description lives in `README.md` and `docs/architecture.md`.
- `omoikane/wiki/domain/omoikane-references.md` gets three references, through the same inbox note: pstack, the Cloudflare security-audit-skill, and the Cloudflare post "Build your own vulnerability harness".
- The verdicts in `omoikane/raw/sources/2026-10-06-pstack-skills-review.md` that rejected a skill for "no memory link" are reopened here; the verdicts about memory gaps stand.

## References and sources

| Source | Commit | Licence | Use |
|---|---|---|---|
| pstack, https://github.com/cursor/plugins/tree/main/pstack | `df58112` (2026-10-06) | MIT, Lauren Tan | `poteto-mode` becomes `omoikane-mode`; principles and several skills are vendored |
| agent-dotfiles, https://github.com/YuukiFST/agent-dotfiles/tree/main/skills | `cc99061` (2026-10-06) | none at the repo; each skill's licence comes from its own upstream | The user's skills; most are copies of obra/superpowers, mattpocock, shadcn, humanlayer, openclaw, anthropics or pstack |
| security-audit-skill, https://github.com/cloudflare/security-audit-skill | `c1c8a8c` (2026-09-14) | MIT, Cloudflare | Vendored, with a Windows fallback |
| "Build your own vulnerability harness", https://blog.cloudflare.com/build-your-own-vulnerability-harness/ | Grant Bourzikas, 2026-06-18 | n/a | Reference only: the multi-stage harness (recon, hunt, validate, dedup, trace) the skill is the starting point of |

Where pstack depends on Cursor: per-call `model`, `readonly` and `environment` on the `Task` tool, Custom Modes (`mode: true`, `reminder:`), `/loop`, `AskQuestion`, rules written to `~/.cursor/rules/pstack-models.mdc`, transcripts read from `~/.cursor/projects/`, Cursor cloud agents, Bugbot, and the `cursor-team-kit` skills (`deslop`, `control-cli`, `control-ui`).
Its principles and several skills (`blast-radius`, `correct`, `create-verification-skill`, `maintain-verification-skill`) use none of these.
A skill that fans work out "one reviewer per model" still works with one model when the reviewers differ by lens instead.

Excluded by the user: pstack `tdd` and `unslop`.

## omoikane-mode

The counterpart of `poteto-mode` (pstack `skills/poteto-mode/SKILL.md`, 20.6 KB, 23 playbooks).
The user turns it on with `/omoikane-mode` (Claude Code, OpenCode) or `/skill:omoikane-mode` (Pi); once loaded, its body stays in the session's context, so it holds for the rest of the session.
Cursor's `reminder:` field has no counterpart in the three harnesses; the session brief carries one line instead: "Nontrivial task with a playbook match: load omoikane-mode."
Rejected: always on through `AGENTS.md`; the file has no budget room, and the user turns the mode on, as with `poteto-mode`.

What it holds, adapted from `poteto-mode`:

- Triggers: a table from kind of task to the skill to run (`how` before a nontrivial change, `codebase-design` before code crossing a module boundary, `interrogate` for a contested design, `security-audit` for anything touching auth, input or secrets, `git-workflow` before the first commit, `test-audit` when a test is written).
- Principles: the 24 pstack principles, one file each under `omoikane-mode/references/principles/`, read on demand; the user's 9 adapted versions win where both exist. This is the single principles router the user chose; there is no separate `principles` skill.
- Playbooks: one file each under `omoikane-mode/playbooks/`. The agent copies the matched playbook's steps into its todo list.
- Autonomy: proceed on reversible work; pause before force-push to a shared branch, deploy, data deletion, or a message to a customer.
- Subagents: fresh subagent per unit of work, file pointers instead of pasted context, the parent reviews every subagent's diff. One model; no per-role model lines. In Pi, which has no subagents (Pi README), the steps run one after another in the main thread.
- Memory: before editing an area, open the decision and gotcha pages whose `code:` lists it; never write under `omoikane/wiki/` mid-session; a lesson for the next agent goes in a note under `omoikane/raw/inbox/`.

Playbooks kept: investigation, bug fix, perf issue, hillclimb, runtime forensics, trace forensics, feature, refactoring, prototype, visual parity, authoring a skill, eval, babysit, shipping, autonomous run, multi-phase plan, opening a PR.
Rewritten on Omoikane's memory: session pickup reads the brief's last captured session; pause safely writes an inbox note.
New: security audit, routing to `security-audit`.
Dropped: orchestrate, autopilot-full, autopilot-stack (fleets of Cursor cloud agents), worktree and simulator cleanup (iOS simulators).
Changed: babysit uses `gh pr checks --watch` instead of the Bun `watch-pr` script; Bugbot triage becomes triage of any automated reviewer's comments.
The reply-writing rules of `poteto-mode` cite `unslop`; they keep only the rules that stand alone (evidence or a label on every claim, no invented links).

## Layout

The skills are ordinary folders under `.claude/skills/`, next to the seven memory skills.

- `omoikane/skills.md` is the manifest: one row per vendored skill with its original upstream URL, commit, SPDX licence id, and every change made to the upstream text. Tests read the skill names from it.
- A vendored skill keeps its upstream `LICENSE` in its own folder, taken from the original repository at the recorded commit (the agent-dotfiles copies carry none).
- An Apache-2.0 file that Omoikane changes gets a notice at its top saying it was changed (Apache-2.0 section 4(b)), and any upstream `NOTICE` file is copied.
- `README.md` gets a third-party section pointing at the manifest.
- A skill a system generates for itself (`verify-<app>` from `create-verification-skill`) is the system's, not the template's, and has no manifest row.

Harness discovery and tools, checked 2026-10-07:

| Harness | Reads skills from | Subagents | Change needed |
|---|---|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md`; a personal skill in `~/.claude/skills/` of the same name wins | yes | none |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/`, and `~/.claude/skills/` (opencode.ai/docs/skills); `permission.skill` can deny one | yes | none |
| Pi | `.pi/skills/`, `.agents/skills/`, and paths in `.pi/settings.json` `skills`, resolved from `.pi/` (`docs/skills.md`, `docs/settings.md` of `@earendil-works/pi-coding-agent` 1.0.4); first skill found wins a name clash; descriptions capped at 1,024 characters | no | `.pi/settings.json` with `"skills": ["../.claude/skills"]`; Pi then gets the memory skills too, which is intended |

Rejected: a copy per harness (`.agents/skills/` beside `.claude/skills/`). OpenCode reads both folders and would load every skill twice.

Pi sends `/skill:<name>` as a `<skill name=...>` block (`formatSkillInvocation` in Pi's dist), which `session-capture.py`'s `COMMAND_TEMPLATE` and `SLASH_COMMAND` do not match, so a Pi `/skill:distill` or `/skill:wrap-up` session would be captured and later distilled into itself.
`command_of` learns that block, with a Pi fixture, before `.pi/settings.json` lands.
Not yet checked against a real Pi session file.

### Personal skills of the same name

`~/.claude/skills/` on the user's machine holds 12 of the names below (brainstorming, writing-plans, executing-plans, grilling, prototype, codebase-design, improve, code-simplifier, test-audit, git-workflow, writing-for-agents, show-me).
Claude Code runs the personal copy over the project copy, OpenCode asks for unique names, and Pi keeps the first it finds.
So the template's own sessions on that machine would run the unadapted copies.
Checks run under a clean `HOME`, and the README says that a personal skill shadows the template's.
Open question for the user: drop those 12 from the agent-dotfiles global set once the template carries them, or keep them and accept the shadowing.

## Context budget

Every skill description loads at session start in Claude Code and Pi; OpenCode can hide one only by permission.
The user chose every skill model-invocable (no `disable-model-invocation`).

- `context-budget.py` keeps one `skill frontmatter` part; its limit is set from the ported descriptions, first estimate 2,600 tokens (600 today plus about 2,000). `total` rises by the same amount.
- A test fails any `.claude/skills/*/SKILL.md` description over 1,024 characters (Pi's cap; Claude Code truncates its listing at 1,536).
- Descriptions are rewritten to state the trigger in one or two sentences where the upstream text is longer; the upstream text stays in the body.

## The skills, first cut

"dotfiles" is agent-dotfiles; the original upstream follows in brackets. "Fan-out" marks a skill that spawns subagents and runs in sequence in Pi.

Mode:
- `omoikane-mode` (pstack `poteto-mode`, MIT), above. Fan-out.

Design and planning:
- `brainstorming` (dotfiles [obra/superpowers]). Drop the visual-companion server: it carries Superpowers branding, an external logo URL and a telemetry toggle.
- `writing-plans`, `executing-plans` (dotfiles [obra/superpowers]). Fan-out.
- `grilling`, `prototype`, `codebase-design` (dotfiles [mattpocock/skills]).
- `figure-it-out` (pstack), with `arena` replaced by two sketches from one model.

Reading and changing code:
- `how` (pstack), one explorer per area instead of per model. Fan-out.
- `blast-radius` (pstack).
- `improve` (dotfiles [shadcn/improve, MIT]). Fan-out.
- `code-simplifier` (dotfiles [anthropics/claude-plugins-official, Apache-2.0]); changed, so it gets the change notice.
- `test-audit` (dotfiles [openclaw/openclaw]).
- `correct` (pstack).
- `create-verification-skill`, `maintain-verification-skill` (pstack), output path `.claude/skills/verify-<app>/` instead of `.cursor/skills/`. Fan-out.

Review:
- `interrogate` (pstack), reviewers by lens instead of by model. Fan-out.

Security:
- `security-audit` (Cloudflare), with the Windows fallback below. Fan-out; its full audit mode needs parallel subagents, so in Pi only its guidance mode runs.

Shipping:
- `git-workflow` (dotfiles, the user's own), with `gh` instead of `gh-axi`, and no references to `~/.claude/rules`, the harness-config repository or agent-dotfiles issue numbers.

Writing for agents:
- `writing-for-agents` (dotfiles [mattpocock/skills]), `show-me` (dotfiles [humanlayer/skills]; licence to confirm at the path it came from).

Each upstream URL, commit and SPDX id is confirmed when the skill's pull request adds its manifest row; a skill whose licence cannot be confirmed is not vendored.

## Rejected, with the reason

- `tdd`, `unslop`: excluded by the user. `ai-tells` (dotfiles) is built partly from `unslop`.
- `poteto-agent`, `poteto-help`, `setup-pstack`, `arena`, `swarm`: per-role model routing and Cursor modes; nothing left once one model runs everything. `omoikane-mode` replaces `poteto-mode`.
- `make-bot-ui`, the benny pack: Grok Bot webhooks, Slack triage, Cursor automations.
- `recall`, `reflect`, `automate-me`, `research`, `handoff`, `backpass`: the memory does this already (`/ask`, `/distill`, `/synthesize`, notes in `omoikane/raw/inbox/`).
- `why`: `/ask` reads `origin/main` history (PR #100); the rest of `why` is MCP playbooks for Slack, Linear, Notion, Datadog, Sentry, Databricks.
- `architect`: built on `arena`; `codebase-design` holds "design it twice" without it.
- `improve-codebase-architecture` (dotfiles [mattpocock]): `improve` and `codebase-design` cover it; it writes its report to the OS temp folder.
- `security-review`, `security-bounty-hunter` (dotfiles): `security-audit` covers both; `security-review` leans on Supabase, Next.js and Solana.
- `thermo-nuclear-code-quality-review`, `storm-research` (dotfiles): no stated provenance or licence; `storm-research` is generic research, which is no longer a use.
- `ai-copywriter` (dotfiles): marketing copy, not software development.
- `optimizing-startup` (dotfiles): desktop-only, needs ffmpeg, numpy and Pillow.
- `find-skills`, `setup-matt-pocock-skills`, `chrome-devtools-axi` (dotfiles): need tools installed on one machine.
- `no-comments` and its `comment-sicko` agent: delete an agent's comments, against the user's rule to keep them.
- `teach` (both), `bro`, `technical-writing`, `benchmark-checklist`, `show-me-your-work`: `technical-writing` overlaps the page contract and `writing-for-agents`; `benchmark-checklist` is folded into `principle-explain-the-number`; the rest are out of scope.

Later, each with its blocker:
- `ui-polish` (dotfiles): reads `~/.claude/ui-refs` and drives `chrome-devtools-axi`; its references must be vendored first.
- `helmsman`, `helmsman-explain` (dotfiles): need an issue-tracker setup doc.
- `domain-modeling` (dotfiles): writes `CONTEXT.md` and `docs/adr/`, which compete with `omoikane/wiki/domain/` and `decisions/`; adapted, it would leave the writing to `/distill`.
- `typescript-best-practices` (pstack): one language; its `paths:` field is not in the Agent Skills fields Pi and OpenCode list.

## Cloudflare validators on Windows

`readFileWithinLimit` in `validate-findings.cjs` (lines 604-613), and its copy in `validate-coverage-ledger.cjs`, open the input with `O_NOFOLLOW | O_NONBLOCK` and refuse to run when Node does not define them.
Node on Windows defines neither, so both validators exit with `OS no-follow and nonblocking input protection is unavailable`.
Linux, macOS and WSL are not affected.

Fallback, on `win32` only:

1. `lstat` with `bigint: true`; refuse a symbolic link or junction, require a regular file.
2. `open` with `O_RDONLY`.
3. `fstat` with `bigint: true` on the descriptor; refuse when `dev` or `ino` differ from step 1, which closes the swap between check and open.

`O_NONBLOCK` has no counterpart to add: Windows named pipes live under `\\.\pipe\`, not on the file system.
The POSIX path stays as it is.

The upstream suites prove nothing on Windows today: they skip every CLI test when `O_NOFOLLOW` is missing (`validate-findings.test.cjs` lines 18-19, `validate-coverage-ledger.test.cjs` lines 20-21) and skip the symlink and FIFO tests on `win32`.
So the change adds `win32` tests for a regular file, a symbolic link, a junction and a swap between check and open, and lifts the skip for the fallback path.
Omoikane's CI (`.github/workflows/ci.yml`) runs on Ubuntu only; a Windows job runs both suites.
The patched copy is listed in `omoikane/skills.md`.
The same change went upstream as cloudflare/security-audit-skill#69; the owner closed it unmerged on 2026-10-07 and deleted the fork, so the patched copy is a permanent divergence (#138).

`SKILL.md` also describes the parent's artifact promotion in POSIX terms (no-follow descriptors, link count of 1). Check whether it needs a Windows step before the skill ships.

## Sequence

One pull request each, in this order:

1. This spec.
2. Objective: `README.md`, `docs/architecture.md`, `AGENTS.md` opening at equal length; the research use removed.
3. Mechanism: `omoikane/skills.md`, the budget limits, the description-length test, the manifest-to-folder test, the Pi capture fix, `.pi/settings.json`, the brief's mode line.
4. `omoikane-mode` with its principles and playbooks.
5. Design and planning skills.
6. Code and review skills.
7. `security-audit` with the Windows fallback and the Windows CI job; the upstream pull request.
8. `git-workflow`.

## Checks

- `python -m unittest discover -s tests` passes after each pull request.
- `python omoikane/bin/context-budget.py` passes.
- Every manifest row names an existing folder under `.claude/skills/`, and every vendored folder has a row and a `LICENSE`.
- No Markdown file sits directly in `.claude/skills/`: Pi loads one there as a skill. (A nested `SKILL.md` inside a skill folder is not loaded: Pi 1.0.4 stops at a folder that holds one.)
- Under a clean `HOME`: Claude Code and OpenCode list each skill once; Pi with the new `.pi/settings.json` lists them at startup; a Pi `/skill:wrap-up` session is not captured.
- `node --test` on both Cloudflare suites passes on the Windows and Ubuntu CI jobs, with the `win32` tests running, not skipped.
