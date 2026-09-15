"""Shared helpers for the wiki scripts: frontmatter parsing and page discovery."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# omoikane/ holds everything the wiki owns; its parent is the repository (the system being built, in build mode).
OMOIKANE = Path(__file__).resolve().parent.parent
REPO = OMOIKANE.parent
WIKI = OMOIKANE / "wiki"
REQUIRED_KEYS = ("title", "type", "summary", "tags", "created", "updated", "sources")
# Order matters: wiki-index.py and session-context.py emit groups in this order, most useful to a coding agent first.
PAGE_TYPES = ("decision", "gotcha", "concept", "entity", "source", "query")
# Source pages carry `dated`: the date the source itself bears. Not in REQUIRED_KEYS so older pages of other types keep passing.
SOURCE_KEYS = ("dated",)
# Optional on any page: repository paths the page is about. wiki-lint.py fails when one no longer exists.
CODE_KEY = "code"
DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
UNDATED = "unknown"
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class Page:
    path: Path
    slug: str
    meta: dict[str, object] = field(default_factory=dict)
    body: str = ""
    links: set[str] = field(default_factory=set)

    @property
    def rel(self) -> str:
        return self.path.relative_to(REPO).as_posix() if self.path.is_relative_to(REPO) else self.path.as_posix()


def parse_frontmatter(text: str) -> tuple[dict[str, object], str] | None:
    """Parse the YAML subset the page contract uses: scalars and inline lists.

    Example: parse_frontmatter("---\\ntitle: A\\ntags: [x, y]\\n---\\nbody")
    returns ({"title": "A", "tags": ["x", "y"]}, "body").
    """
    m = FRONTMATTER.match(text)
    if not m:
        return None
    meta: dict[str, object] = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith("#"):
            continue
        key, _, raw = line.partition(":")
        raw = raw.split("  #")[0].strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            meta[key.strip()] = [v.strip() for v in inner.split(",") if v.strip()] if inner else []
        else:
            meta[key.strip()] = raw
    return meta, text[m.end():]


def load_pages(wiki: Path = WIKI) -> list[Page]:
    pages: list[Page] = []
    for path in sorted(wiki.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        parsed = parse_frontmatter(text)
        meta, body = parsed if parsed else ({}, text)
        links = {slug.strip() for slug in WIKILINK.findall(body)}
        pages.append(Page(path=path, slug=path.stem, meta=meta, body=body, links=links))
    return pages
