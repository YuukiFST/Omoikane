# Realign Omoikane to its objective

Status: plan approved by the user on 2026-10-02.

## Objective (the user's words, source of truth)

Omoikane is a template built on three references: Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), [brainmaxxing](https://github.com/poteto/brainmaxxing) and [ai-memory](https://github.com/akitaonrails/ai-memory).
Every new system starts from Omoikane.
The agent feeds the knowledge base on its own, without the user's involvement, with the important information the user gives while building the system.
That includes domain knowledge: business rules, design system, organisation conventions.

Criterion for any work in this repository: does it improve the tool towards this objective? If not, it is not done.

## What went wrong

An example of the kind of knowledge to remember (a company's internal starter kit that holds its business rules and design system) was read as "integrate Omoikane with that kit".
Result: PR #55 (`docs/specs/2026-10-01-org-knowledge.md`, `omoikane/bin/org-candidates.py`), whose central decision (`018e1eb:docs/specs/2026-10-01-org-knowledge.md`, line 35; the file is removed by #68) keeps organisation knowledge out of Omoikane, the opposite of the objective, plus references to the kit's name in the public wiki.

## 1. Where the objective is recorded

| Place | Loaded by | Content |
|---|---|---|
| `AGENTS.md`, opening paragraph | every session, every harness (`CLAUDE.md` imports it) | The objective, phrased so it stays true in a system cloned from the template. Paid for by replacing the "Two ways" block; `context-budget.py` must stay green with a full rules block. |
| `omoikane/raw/inbox/<date>-omoikane-objective.md` | `/ingest`, which writes a source page (and a concept page if it judges one central); the summaries reach this repository's sessions through the brief's index | The objective in the user's words, the criterion for work in this repository, the misreading rejected. Repository-specific, so it stays out of `AGENTS.md`, which every cloned system inherits. Left untracked, like a capture: `review-gate.py` moves every inbox file out of the checkout into `wiki/auto`. |
| `README.md`, first line | humans and GitHub visitors, not sessions | The problem the template solves. |
| `docs/architecture.md`, opening | agents changing the architecture | One line pointing at the objective. |

Why not the README alone: no session loads it.
Why not `AGENTS.md` alone: the criterion "work here must improve the tool" is about this repository, and a system cloned from the template would inherit it as a wrong instruction.

## 2. PR #55: revert

Recommendation: revert the merge `018e1eb` with `git revert -m 1`, on a branch, through a PR.

- The spec's core decision rejects what the objective asks for; rewriting it means a new spec, not an edit.
- `org-candidates.py` exists only to feed an external base the objective excludes. Kept as an "optional feature" it is code nobody runs, and the "Across systems" section of `docs/architecture.md` would keep telling every agent that organisation knowledge belongs elsewhere.
- The real need behind it (a system born later starts with the conventions learned in earlier ones; ai-memory's `scope: "global"`) is listed below as an open gap, to be designed from the objective once domain pages exist. Git history keeps the code.

## 3. Cleanup of the kit's name

Already done: the scheduled task `OmoikaneIngest` is disabled. Its 07:34 run would have distilled `omoikane/raw/inbox/sessions/2026-10-01-d4302021.md` (15 occurrences) into `wiki/auto` and pushed it to the public remote.

| Where | Action |
|---|---|
| `omoikane/raw/inbox/sessions/` (d4302021 and this session's capture, which quotes the search term) | Redact before distill, as `286fbc6` did: not yet raw sources, so no immutability rule applies. |
| `omoikane/wiki/decisions/company-internal-material-stays-out-of-the-public-repo.md` | Rewrite without the name and the private path; the principle (organisation material stays out of a public repository) stays. |
| Three session source pages (c14af01e, 230a182d, b5b6fb27) | Replace the name with "a company-internal starter kit". |
| `omoikane/_review.md` | The bullet goes away with PR #58. |
| `omoikane/index.md` | Regenerated. |
| `omoikane/log.md:32` and three captures under `omoikane/raw/sources/sessions/` | DECIDE: redact in place with a `[redacted]` marker, breaking append-only and immutability once, with the reason in the commit; or leave them. Recommended: redact, the precedent `286fbc6` did the same. `session-capture.py` reads only `turns:` from a distilled capture, so redacting the body breaks nothing. |
| Git history of `main` | Stays public either way; removing it needs a force-push of `main`, not recommended. |

Guard so it does not recur: `session-capture.py` replaces every term listed in a gitignored `omoikane/.capture-redact` file with `[redacted]` at capture time (ai-memory sanitizes at a typed privacy boundary before storing). The term list never enters the repository.
Re-enable the scheduler after the guard and the cleanup are merged.

## 4. Tool changes for domain knowledge

### Page type `domain`

One new type, `omoikane/wiki/domain/`: a business rule, design-system rule or organisation convention, stated by the user in a session or by an ingested document. Tags tell them apart (`business-rule`, `design-system`, `convention`).

Why a type and not an existing one:

- `practice` needs two sessions (`wiki-lint.py` enforces it); a business rule the user states once is already true.
- `concept` is not imperative, has no source floor and comes after decisions, gotchas and practices in the brief.
- `decision` records a choice with rejected alternatives; "prices are integer cents" is not one.
- One type, not three: the three share the lifecycle (stated by an authority, valid from one statement, may contradict the code, needs the quote).

Contract: `summary` is the rule or fact itself in one line, since only the summary reaches the brief. `wiki-lint.py` fails a domain page with an empty `sources:`. `session-context.py` ranks domain pages first: they govern the code being written. The `## Domain` placeholder in `AGENTS.md` goes away; nothing waits for the human to fill it.

### Distill and ingest

- `omoikane/prompts/distill.md:9` skips "restatements of the prompt". Narrow it: the task restated is skipped; a rule, fact or convention the user states about the domain becomes a domain page, quoted with the turn.
- New reject rule `task-only`, after brainmaxxing's durability test ("would I include this in a prompt for a different task?"): an instruction scoped to the current change ("make this button blue") is not a domain rule.
- A statement that contradicts a domain page or the code records both sides under `## Contradictions` and files `_review.md`, as for sources today.
- `omoikane/prompts/ingest.md` step 4 adds domain pages for documents that state rules (a design-system document dropped into the inbox).
- Evaluation: one fixture session where the user states a business rule and a design token inside a coding prompt, run through headless `/distill` in a throwaway clone; it must produce two domain pages and no page for the task-only instruction.

## 5. Issues, in order

1. #60 Objective recorded (`AGENTS.md`, README, architecture, inbox note).
2. #61 Revert #55.
3. #62 Capture redaction guard (`session-capture.py`, test red first).
4. #63 Cleanup of the kit's name; re-enable the scheduler.
5. #64 Page type `domain` (`wikilib.py`, `wiki-lint.py`, `session-context.py`, `AGENTS.md` contract, architecture).
6. #65 Distill and ingest route domain knowledge, with the evaluation.
7. #66 A new system starts clean: a clone today inherits this repository's own wiki, log and review queue (31 pages about Omoikane), and its brief injects them into the new system's sessions. A script that resets `omoikane/` in a fresh clone.

## Open gaps, not planned here

- Knowledge reaches the user's sessions only after a human merges the `wiki/auto` PR (`docs/architecture.md`, "Why a gate"): the objective asks for no involvement. Options: auto-merge when CI is green, or a brief that also reads `wiki/auto`. DECIDE later; it reverses part of #45.
- Latency: a statement reaches the wiki after the 30-minute quiet period plus the schedule. brainmaxxing's `/reflect` writes during the session.
- No search: the brief stops at a 12,000-character index budget and drops the rest; a design system can outgrow it. Karpathy suggests qmd; ai-memory fuses FTS, entities and graph.
- A domain rule that governs every task reaches `AGENTS.md` only through `/synthesize`, which needs two sessions; ai-memory's lint suggests a rule from one.
- Cross-system knowledge: conventions learned in one system do not reach the next one born from the template.
- No bootstrap from an existing project's history and docs (ai-memory `bootstrap`, brainmaxxing `/ruminate`).
