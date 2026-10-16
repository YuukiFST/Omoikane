"""Score whether a headless /distill kept the literal details of a captured session, with no LLM involved.

Each fixture under tests/fixtures/distill-*.md carries an answer key in its frontmatter: `must_mention` (strings the
distilled pages must carry verbatim) and `must_not_mention` (strings no rule page may carry). `prepare` copies the
fixtures into an inbox without the key, so the model never sees it; `score` checks what distill wrote.
Usage: python omoikane/bin/distill-fidelity.py prepare <omoikane-dir> <fixture>...
       python omoikane/bin/distill-fidelity.py score <omoikane-dir> <fixture>...
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from wikilib import FRONTMATTER, SESSION_PAGE, load_pages, parse_frontmatter

KEYS = ("must_mention", "must_not_mention")
# Page types a later session obeys: a must_not string there turns a task-only or open claim into a rule.
RULE_TYPES = ("domain", "decision", "gotcha", "practice")
WHITESPACE = re.compile(r"\s+")


@dataclass
class Fixture:
    name: str
    id8: str
    date: str
    part: int
    # wikilib splits inline lists on every comma, so a key item cannot carry one: list each clause on its own.
    must_mention: list[str]
    must_not_mention: list[str]
    body: str


@dataclass
class WikiPage:
    rel: str  # relative to the omoikane dir, the form `sources:` lists use: wiki/sources/<slug>.md
    type: str
    sources: list[str]
    text: str  # whole file: the frontmatter `summary` carries a rule as much as the body does


@dataclass
class Score:
    fixture: str
    kept: int
    total: int
    lost: list[str] = field(default_factory=list)
    hits: list[tuple[str, str]] = field(default_factory=list)  # (must_not string, page rel path)
    errors: list[str] = field(default_factory=list)

    @property
    def failed(self) -> bool:
        return bool(self.lost or self.hits or self.errors)


def parse_fixture(name: str, text: str) -> Fixture:
    parsed = parse_frontmatter(text)
    if parsed is None:
        raise ValueError(f"{name}: no frontmatter")
    meta, body = parsed
    session, started = str(meta.get("session", "")), str(meta.get("started", ""))
    part = str(meta.get("part", "1"))
    keys = {k: meta.get(k, []) for k in KEYS}
    if not session or len(started) < 10 or not part.isdigit() or not all(isinstance(v, list) for v in keys.values()):
        raise ValueError(f"{name}: needs `session`, `started`, a numeric `part` when present and inline lists "
                         "`must_mention`, `must_not_mention`")
    return Fixture(name=name, id8=session[-8:], date=started[:10], part=int(part),
                   must_mention=list(keys["must_mention"]), must_not_mention=list(keys["must_not_mention"]), body=body)


def strip_keys(text: str) -> str:
    """The fixture text without its answer-key lines; every other byte unchanged.

    Example: strip_keys("---\\nsession: s\\nmust_mention: [a]\\n---\\nbody") returns "---\\nsession: s\\n---\\nbody".
    """
    m = FRONTMATTER.match(text)
    if not m:
        return text
    lines = [line for line in m.group(1).split("\n") if not line.startswith(tuple(f"{k}:" for k in KEYS))]
    return "---\n" + "\n".join(lines) + "\n---\n" + text[m.end():]


def normalize(text: str) -> str:
    # A line wrap or a re-indented quote is not a paraphrase: compare with every whitespace run as one space.
    return WHITESPACE.sub(" ", text)


def contains(haystack: str, needle: str) -> bool:
    return normalize(needle) in normalize(haystack)


def sections(text: str, id8: str) -> list[str]:
    """The `## [date] distill | session <id8>` sections of log.md or _review.md, each up to the next `## ` heading.

    Example: sections("## [2026-10-02] distill | session abc\\n- x\\n## [2026-10-03] ingest | y\\n", "abc")
    returns ["## [2026-10-02] distill | session abc\\n- x"].
    """
    heading = re.compile(rf"## \[\d{{4}}-\d{{2}}-\d{{2}}\] distill \| session {re.escape(id8)}(?![0-9A-Za-z])")
    found: list[str] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                found.append("\n".join(current))
            current = [line] if heading.match(line) else None
        elif current is not None:
            current.append(line)
    if current is not None:
        found.append("\n".join(current))
    return found


def score_fixture(fx: Fixture, pages: list[WikiPage], log: str, review: str) -> Score:
    sources = {p.rel for p in pages if (m := SESSION_PAGE.search(p.rel)) and m.group(1) == fx.id8}
    citing = [p for p in pages if p.rel not in sources and sources & set(p.sources)]
    log_sections = sections(log, fx.id8)
    written = [p.text for p in pages if p.rel in sources] + [p.text for p in citing]
    written += log_sections + sections(review, fx.id8)

    result = Score(fixture=fx.name, kept=0, total=len(fx.must_mention))
    result.errors = [f'must_mention not in the fixture body: "{s}"' for s in fx.must_mention if not contains(fx.body, s)]
    if not sources and not log_sections:
        result.errors.append(f"not distilled: no source page and no log section for session {fx.id8}")
    for s in fx.must_mention:
        if any(contains(w, s) for w in written):
            result.kept += 1
        else:
            result.lost.append(s)
    rules = [p for p in citing if p.type in RULE_TYPES]
    result.hits = [(s, p.rel) for s in fx.must_not_mention for p in rules if contains(p.text, s)]
    return result


def report(scores: list[Score]) -> str:
    out: list[str] = []
    for sc in scores:
        out.append(f"{sc.fixture}: kept {sc.kept}/{sc.total}")
        out += [f'  lost: "{s}"' for s in sc.lost]
        out += [f'  must_not: "{s}" on {page}' for s, page in sc.hits]
        out += [f"  error: {e}" for e in sc.errors]
    kept, total = sum(sc.kept for sc in scores), sum(sc.total for sc in scores)
    hits, errors = sum(len(sc.hits) for sc in scores), sum(len(sc.errors) for sc in scores)
    out.append(f"total: kept {kept}/{total}, must_not hits {hits}, fixture errors {errors}")
    return "\n".join(out) + "\n"


def read(path: Path) -> str:
    # Bytes, not read_text: newline translation would break the byte-identical copy in prepare.
    return path.read_bytes().decode("utf-8")


def prepare(omoikane: Path, fixtures: list[Path]) -> None:
    inbox = omoikane / "raw" / "inbox" / "sessions"
    inbox.mkdir(parents=True, exist_ok=True)
    for path in fixtures:
        text = read(path)
        fx = parse_fixture(path.name, text)
        # The name session-capture.py gives a later part of one session.
        suffix = "" if fx.part == 1 else f"-part{fx.part}"
        (inbox / f"{fx.date}-{fx.id8}{suffix}.md").write_bytes(strip_keys(text).encode("utf-8"))


def score(omoikane: Path, fixtures: list[Path]) -> list[Score]:
    wiki = omoikane / "wiki"
    pages: list[WikiPage] = []
    for p in load_pages(wiki) if wiki.is_dir() else []:
        cited = p.meta.get("sources", [])
        pages.append(WikiPage(rel=p.path.relative_to(omoikane).as_posix(), type=str(p.meta.get("type", "")),
                              sources=[str(s) for s in cited] if isinstance(cited, list) else [], text=read(p.path)))
    log, review = (read(p) if p.is_file() else "" for p in (omoikane / "log.md", omoikane / "_review.md"))
    return [score_fixture(parse_fixture(p.name, read(p)), pages, log, review) for p in fixtures]


def fixture_paths(args: list[str]) -> list[Path]:
    """Each argument as a path, a glob pattern expanded in sorted order: PowerShell and cmd pass `distill-*.md`
    through unexpanded, and Python on Windows does not expand it.

    Example: fixture_paths(["fixtures/distill-term-*.md"]) returns [Path("fixtures/distill-term-session.md")].
    """
    paths: list[Path] = []
    for arg in args:
        if not any(c in arg for c in "*?["):
            if not Path(arg).is_file():
                raise ValueError(f"{arg}: no such file")
            paths.append(Path(arg))
            continue
        matched = sorted(glob.glob(arg))
        if not matched:
            raise ValueError(f"{arg}: matches no file")
        paths += [Path(m) for m in matched]
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=("prepare", "score"))
    parser.add_argument("omoikane", type=Path, help="the omoikane/ directory distill runs in")
    parser.add_argument("fixtures", nargs="+", help="fixture paths or glob patterns")
    args = parser.parse_args(argv)
    omoikane = args.omoikane.resolve()
    try:
        fixtures = fixture_paths(args.fixtures)
        if args.command == "prepare":
            prepare(omoikane, fixtures)
            return 0
        scores = score(omoikane, fixtures)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    # The keys are mostly Portuguese; a cp1252 console would mangle them past recognition.
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    sys.stdout.write(report(scores))
    return 1 if any(sc.failed for sc in scores) else 0


if __name__ == "__main__":
    sys.exit(main())
