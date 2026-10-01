# Organisation knowledge: from the wikis of several systems to the organisation's shared knowledge

Issue: #52. Status: design written on 2026-10-01; the Omoikane side (`omoikane/bin/org-candidates.py`) implemented in the same branch.

## Problem

An organisation that builds several systems with Omoikane gets one wiki per system.
Each wiki learns from its own sessions: a database rule the ORM breaks, a deploy step that must come first, a practice the team keeps restating.
When the same lesson shows up in two or three systems, nothing notices it, and the organisation's shared knowledge never hears of it.

Most organisations of that kind already keep shared knowledge somewhere: a starter kit that new systems are cloned from, a standards repository, a ledger of rules with the check that enforces each.
That base is curated, versioned and synced into the systems; it has its own intake process, its own budget for what agents load, its own ladder of guards and its own language.
A second, organisation-wide Omoikane wiki next to it would be a duplicate the organisation must keep in step by hand.

## Goals

- A lesson learned in two or more systems reaches the organisation's intake as a proposal, with its evidence.
- Only distilled knowledge crosses the system boundary: no raw session capture, no page body.
- The organisation's knowledge base stays the single home of organisation rules; Omoikane feeds it and does not route around its review.
- A system keeps its own wiki, its own rules block and its own budget; organisation rules reach it the way the organisation already distributes them.
- A system that departs from an organisation rule says so in its wiki, and the departure flows back as evidence.

## Non-goals

- Semantic matching of lessons phrased differently in two systems. Matching is by key; the key is the slug or an explicit `org:` value. A cross-system `/synthesize` pass is a later step.
- Writing into the organisation's knowledge base. Its intake process does that, under its own rules.
- Approval semantics. Some organisations approve every rule by hand, some approve none; a ticked `[x]` in a system's `_review.md` travels as evidence that a human in that system agreed, not as permission at the organisation level.

## Decisions

### Where organisation knowledge lives

| Chosen | Rejected | Why |
|---|---|---|
| In the organisation's existing knowledge base (kit, standards repository, rule ledger). Omoikane produces candidates for it. | A shared Omoikane wiki for the organisation, fed by every system. | Two homes for one rule drift apart; the organisation already reviews, versions and syncs its base, and a second wiki would bypass all three. |
| | Each system's wiki, cross-linked to the others. | A rule needs one canonical text and one owner; links across repositories break on every rename and give no place to decide. |

### How a page becomes an organisation rule

| Chosen | Rejected | Why |
|---|---|---|
| `org-candidates.py` reads the wikis of the systems and lists every decision, gotcha or practice whose key appears in two or more distinct systems. The organisation's intake takes the list as proposals. | Promote any practice page of one system. | One system's habit is not the organisation's rule; the floor is the same as a practice's two sessions, one level up. |
| The key is the page's `org:` value, or its slug. | An LLM matching summaries across systems. | Deterministic output is diffable and reviewable; a wrong semantic match would put a false consensus in front of the intake. The semantic pass can come later as an operation whose output a human reads. |
| Frontmatter only: title, type, summary, guard, path, date. | Page bodies, or the raw captures behind them. | Captures quote whatever the session saw, customer data included; summaries are written to stand alone and are short enough to audit. The organisation's own leak check still runs on what it accepts. |

### How each system receives the rules without outgrowing its budget

| Chosen | Rejected | Why |
|---|---|---|
| Organisation rules reach a system through the organisation's own always-loaded file, synced the way the organisation already syncs. The system's `AGENTS.md` rules block stays for rules local to that system. | Copying organisation rules into each system's managed rules block. | The block is capped at 15 for adherence; organisation rules would crowd out local ones, and every copy drifts from the original. |
| The organisation's budget gate measures everything a session loads, Omoikane's `AGENTS.md` and skill descriptions included. | Omoikane's `context-budget.py` measuring the organisation's file too. | The organisation owns the total; one gate with the whole picture beats two gates each seeing half. A gate that reads only `CLAUDE.md` lets `AGENTS.md` grow unseen, so that gate must learn to count it. |
| Rules that apply to one area load on demand (a page or skill the agent opens when it touches that area), not always. | Injecting every organisation rule into the session brief. | The brief is bounded; a rule about database migrations costs every session that never touches the schema. |

### How the rule becomes a guard in the systems

| Chosen | Rejected | Why |
|---|---|---|
| Each candidate carries the strongest guard any system already has (`lint` > `test` > `hook` > `none`, Omoikane's `guard:`), mapped onto the organisation's guard ladder. The guard is built once in the shared base and synced. | Each system writing its own check for the same rule. | Several copies of one check diverge; a check in the shared base is fixed once. |
| A rule accepted with no guard goes to the organisation's list of known gaps, the counterpart of `guard: none`. | Refusing rules without a guard. | The lesson is still true; recording the gap keeps the pressure to build the check visible. |

### When a system contradicts an organisation rule

| Chosen | Rejected | Why |
|---|---|---|
| The synced organisation rule is a source the system's wiki can cite. A system page that departs from it records both claims under `## Contradictions` and files `_review.md`, as for any two sources that disagree; no winner is picked. | The organisation rule overriding the system page automatically. | The departure may be right for that system (a legacy schema, a regulator); deciding needs a human who knows it. |
| A page that departs carries the rule's key in `org:`, so `org-candidates.py` shows it next to the systems that follow the rule; the intake reads it as evidence against, or for an exception. | The system deleting its page to stay in line. | A deleted page loses why the system departed; the next agent repeats the departure without the reason. |

## Components

- `omoikane/bin/org-candidates.py`: `--system NAME=PATH` per system (a repository root with `omoikane/wiki/`), `--format markdown|json`. Reads decision, gotcha and practice pages, skips pages marked `prune:`, groups by `org:` or slug, keeps keys found in `MIN_SYSTEMS` (2) or more distinct systems, reports per candidate the type and summary of the best-guarded page, the strongest guard, and one evidence line per system. Read-only; exits 2 when a path has no wiki.
- Page contract: optional `org: <key>` on a decision, gotcha or practice page, set by a human or by the organisation's intake when a lesson's slug differs between systems or the page follows or departs from an organisation rule.

## Data flow

1. Systems distill their sessions as today; each wiki grows on its own.
2. The organisation runs `org-candidates.py` over the systems it builds (locally, or in a job that checks them out) and hands the Markdown to its intake process.
3. The intake decides, writes the rule into the shared base with its guard (or into known gaps), and releases it.
4. Each system syncs the release; the rule arrives in the always-loaded file or as an on-demand page.
5. A system whose wiki departs from the rule records the contradiction; the next run of `org-candidates.py` shows it beside the systems that follow the rule.

## Error handling

- A path without `omoikane/wiki/` fails the run (exit 2) and names the path: a silent skip would make one system's lessons look absent.
- The same path given twice counts once, so a typo cannot fake a second system.
- A page without frontmatter or of another type is ignored; the script never writes.

## Testing

`tests/test_org_candidates.py` builds three throwaway systems and runs the script as the organisation would: a lesson in two systems with both evidence lines, `org:` joining pages of different names, the strongest guard reported, a system named twice counting once, no page body or raw capture text in either output format, and a missing wiki failing with its path.
