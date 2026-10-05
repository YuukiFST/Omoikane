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

Outcome of each, recorded 2026-10-02 (#87).

- **Closed** by #74, the user's decision of 2026-10-02: knowledge reached the user's sessions only after a human merged the `wiki/auto` PR (`docs/architecture.md`, "Why a gate"), and the objective asks for no involvement.
  `review-gate.py publish` now asks GitHub to merge the PR by merge commit once the required checks pass (the `enablePullRequestAutoMerge` mutation; `gh pr merge --auto`, the proposal, merges at once a PR already mergeable), keeping the PR as the audit trail and reversing part of #45; the repository needs "Allow auto-merge" and a required status check on `main`.
  The agent's permission classifier had refused this edit once, so it waited for the user.
  Even merged, a session sees the pages after `git pull`: the brief reads the checkout.
- **Reopened and closed** by #96 once the merge became automatic: each capture arms a timer, and the run starts 31 minutes after a session's last turn, with no window; the scheduled task is a daily fallback.
  Recorded on 2026-10-02 as discarded: latency (30-minute quiet period plus the schedule).
  The next session gets the newest undistilled capture in the brief's Pending section and can read it at once, until the scheduled run moves it into `wiki/auto`; the wiki reaches sessions only after the merge above, so distilling sooner reaches no session sooner, and takes the capture out of Pending sooner.
  A run started at `SessionEnd` would also race the scheduled run over the one `wiki/auto` worktree.
  Worth reopening once the merge is automatic.
- **Closed** by #83 (#75): the brief kept sections in strict order, so about 60 domain pages pushed every decision and gotcha out.
  Domain, decision, gotcha and practice sections now get a floor of the budget, and the budget counts the separators.
  A search script (BM25) was not added: the omitted line points at `omoikane/index.md`, which the agent can grep.
- **Closed** by #86 (#76): a domain rule reaches the `AGENTS.md` rules block from one statement; `/synthesize` proposes it within the room the block has, the human's tick still approves it, and `wiki-lint.py` warns when a promoted rule's page is gone, disputed or pruned.
- **Closed** by #85 (#80): `new-system.py --from <another system>` starts the new wiki with that system's `convention` and `design-system` domain pages; design in [2026-10-02-cross-system-knowledge.md](2026-10-02-cross-system-knowledge.md).
- **Closed** by #84 (#79): `bootstrap.py [--from <path>]` seeds the inbox from a project's README, docs, agent rule files and git history, skipping what the template shipped.

Found while closing these:

- **Closed** by #82 (#77): captures redacted only the listed terms; secrets (API keys, tokens, private keys, passwords) now go too.
- **Closed** by #81 (#78): the review gate moved tracked inbox files out of the human's checkout; only files `origin/main` does not hold as they are move now.
