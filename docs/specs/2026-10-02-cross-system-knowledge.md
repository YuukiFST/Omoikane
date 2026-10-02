# Carry organisation conventions into a new system

Status: written before the code, issue #80.

## Problem

Every new system starts from Omoikane, and `new-system.py` empties the clone's memory (#66).
The organisation's conventions and design-system rules, already learned in an earlier system, are gone with it: the user has to restate them, session by session, in every system.
The objective asks the agent to hold what the user stated without the user's involvement, so stating the same convention again in each system is the failure.

## What crosses from one system to the next

| Page | Crosses | Why |
|---|---|---|
| `domain`, tag `convention` | yes | An organisation convention ("commit messages in English", "every service logs JSON") holds in every system of that organisation. |
| `domain`, tag `design-system` | yes | An organisation usually shares one design system across its products. |
| `domain`, tag `business-rule` | no | A business rule belongs to one system's domain: "prices are integer cents" in a shop says nothing about a payroll system. |
| `decision`, `gotcha`, `entity` | no | They are about code; their `code:` paths do not exist in the new system, and `wiki-lint.py` fails on them. |
| `practice` | no | A practice cites the sessions that showed it, and those session pages stay behind; `wiki-lint.py` fails a practice citing fewer than two. A preference that holds everywhere is better stated once as a convention. |

## Design

`python omoikane/bin/new-system.py --from <checkout of another system>` empties the memory as today, then copies the other system's domain pages tagged `convention` or `design-system` into `omoikane/wiki/domain/`.

- Provenance. One source page, `wiki/sources/inherited-from-<system>.md` (`type: source`, `dated` the date of the other system's last commit), lists every page copied and the commit it was copied at. Each copied page cites it in `sources:`, so `wiki-lint.py`'s rule that a domain page cites a source page holds, and its body keeps the user's words and gains one line naming where it came from.
- Links. A wikilink to a page that did not come along becomes plain text: the copy must pass `wiki-lint.py` on its own, and `code:` goes for the same reason.
- No sync. A convention that changes later in the other system does not follow; the next session that states it in this system updates the page through `/distill`, which records the old rule under `## History` or the disagreement under `## Contradictions`. Why no sync: a live link makes one system's memory depend on another checkout being present and current, and an unattended run in one system would rewrite the other's rules.
- Where the knowledge lives. Inside each system's own wiki. Not a shared organisation repository and not an external base: that reading of the objective was the one reverted in #68.

## Alternatives rejected

- A shared organisation wiki, mounted or synced into every system: a second home for the same rules, which the objective does not ask for, and the reverted #55 design.
- Copying every page: decisions and gotchas name code that does not exist in the new system, and the brief would open each session with another system's lessons.
- A `scope: global` key on pages, as ai-memory does: Omoikane has no store outside the repository for a global scope to live in; the tag already says which rules are the organisation's.

## Test cases

1. A `convention` and a `design-system` domain page cross, cite the new source page, and the new wiki passes `wiki-lint.py`.
2. A `business-rule` domain page, a decision and a practice stay behind.
3. A link to a page that stayed behind becomes plain text; `code:` is dropped.
4. `--from` a path with no `omoikane/wiki/` refuses before the reset, so nothing changes.
