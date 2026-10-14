"""Seed the inbox from an existing project: its README, docs, agent rule files and git history, for /ingest.

A project that adopts Omoikane, or a system that replaces one, already states many of its rules in writing; without
this they reach the wiki only when the user restates them in a session (#79; after ai-memory's `bootstrap` and
brainmaxxing's `/ruminate`). Each source becomes one inbox file, headed with where it came from and when it last
changed, so /ingest can date it. Content is read from the commit HEAD points at, never from the working tree, and
goes through the same redaction as a captured session (secrets, omoikane/.capture-redact): the scheduled run pushes
what it ingests.

In a system born from the template (remote `template`, which new-system.py names), what the template shipped
describes Omoikane, not the system: a file the template shipped contributes only the lines the system added since
it branched off, and the history starts there too. Elsewhere, a file holding Omoikane's managed rules block is
Omoikane's manual and is skipped. A second run writes nothing already in the inbox, in raw/sources/, or on the
review gate's branch, except a source whose file changed since its last copy: that version becomes a new inbox file
named after its commit (raw/sources/ is immutable), and it names the earlier copies it follows (#150).

Usage: python omoikane/bin/bootstrap.py [--from PATH]     # default: this repository
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import importlib
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

from wikilib import OMOIKANE, REPO, RULES_END, RULES_START

capture = importlib.import_module("session-capture")

# What a project writes down for people and agents, not code. Names compare case-insensitively.
ROOT_FILES = {"readme", "readme.md", "readme.mdx", "readme.rst", "readme.txt", "contributing.md", ".cursorrules",
              ".windsurfrules", ".clinerules"}
AGENT_FILES = {"agents.md", "claude.md", "gemini.md"}  # at any depth: a monorepo keeps one per package
# Folders of other people's code, whose agent files are not this system's rules.
VENDORED = {"node_modules", "vendor", "third_party", "third-party", ".venv", "venv", "site-packages"}
DOC_SUFFIXES = {".md", ".mdx", ".rst", ".txt"}
TEMPLATE_REMOTE = "template"
# The log entry new-system.py writes: the commit that adds it is where the system's own history starts, whatever
# its remotes are called (a "Use this template" repository starts from an unrelated commit).
RESET_MARKER = "init | Memory reset from the Omoikane template"
MANUAL_HEADING = "# Omoikane — agent operating manual"
HISTORY_COMMITS = 300  # newest first; a long history past this adds little a rule needs
BODY_CHARS = 1000
TRAILER = re.compile(r"(?im)^[a-z][\w-]*-by:.*$\n?")  # Signed-off-by, Co-authored-by: names and emails
PREFIX = "bootstrap-"
MAX_SLUG = 150  # file names stay well under the 255 bytes Windows and Linux allow
# Where the review gate keeps what it ingested until the human's checkout pulls it (review-gate.py).
GATE_REFS = ("wiki/auto", "origin/wiki/auto", "origin/main")
# A later version of a source is named after its commit; the slug's own collision suffix is 6 characters, not 7.
VERSION = re.compile(r"-[0-9a-f]{7}\.md$")
LAST_CHANGED = re.compile(r"last changed (\d{4}-\d{2}-\d{2}) in commit ([0-9a-f]{4,40})\.")
TITLE = re.compile(r"# .+ \(bootstrap\)\n")
BODY_START = "\n\n---\n\n"


class BootstrapError(Exception):
    """The project cannot be read: not a git repository, no commit yet, git missing, or the template not fetched."""


def git(repo: Path, *args: str, ok: bool = False) -> str:
    try:
        run = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8",
                             errors="replace")
    except FileNotFoundError as exc:
        raise BootstrapError("git is not on PATH") from exc
    if run.returncode != 0:
        if ok:
            return ""
        raise BootstrapError(run.stderr.strip() or f"git {' '.join(args)} failed")
    return run.stdout


def is_source(path: str) -> bool:
    """Example: is_source("docs/adr/0001.md") and is_source("pkg/CLAUDE.md") are True; "src/a.py" is False."""
    p = PurePosixPath(path.lower())
    if p.parts[0] == "omoikane" or VENDORED & set(p.parts[:-1]):
        return False
    if len(p.parts) == 1 and p.name in ROOT_FILES or p.name in AGENT_FILES:
        return True
    if p.parts[0] == "docs" and p.suffix in DOC_SUFFIXES:
        return True
    return path.lower() == ".github/copilot-instructions.md" or (p.parts[:2] == (".cursor", "rules")
                                                                  and p.suffix in {".md", ".mdc"})


def tree(project: Path, rev: str) -> dict[str, str]:
    """Path to blob id of every regular file at `rev`; links and submodules are not text a project wrote."""
    blobs = {}
    for line in git(project, "ls-tree", "-r", "-z", rev).split("\0"):
        if line:
            meta, path = line.split("\t", 1)
            mode, kind, sha = meta.split()
            if kind == "blob" and mode in ("100644", "100755"):
                blobs[path] = sha
    return blobs


def is_ancestor(project: Path, older: str, newer: str) -> bool:
    return subprocess.run(["git", "-C", str(project), "merge-base", "--is-ancestor", older, newer],
                          capture_output=True).returncode == 0


def template_versions(project: Path) -> tuple[str | None, list[str]]:
    """Where the template ends in this history, and the template's other fetched tips.

    The base is the commit new-system.py's reset entry entered omoikane/log.md in, found by content, so neither a
    renamed remote nor a "Use this template" repository hides it (#84 second review); else the newest commit HEAD
    shares with a `template/*` branch. Template tips that hold the base are this system's own branches (a "Use
    this template" repository named its own remote `template`) and do not count. (None, []) outside a system born
    from the template.
    """
    refs = (git(project, "for-each-ref", "--format=%(refname)", f"refs/remotes/{TEMPLATE_REMOTE}/").split()
            if TEMPLATE_REMOTE in git(project, "remote").split() else [])
    reset = git(project, "log", "--format=%H", "-S", RESET_MARKER, "HEAD", "--", "omoikane/log.md").split()
    if reset:
        base = reset[-1]  # the oldest: the entry was added there
        return base, [r for r in refs if not is_ancestor(project, base, r)]
    if TEMPLATE_REMOTE not in git(project, "remote").split():
        return None, []
    bases = [b for b in (git(project, "merge-base", "HEAD", ref, ok=True).strip() for ref in refs) if b]
    if not bases:
        raise BootstrapError(f"remote `{TEMPLATE_REMOTE}` has no branch fetched that HEAD shares history with; "
                             f"run `git fetch {TEMPLATE_REMOTE}` first")
    # The common commit every other one is an ancestor of: the template's history ends there.
    newest = [b for b in bases if all(is_ancestor(project, other, b) for other in bases)]
    return (newest or bases)[0], refs


def without_rules(text: str) -> str:
    """Drop the managed rules block: wiki-rules.py and new-system.py rewrite it, and it points at wiki pages."""
    start, end = text.find(RULES_START), text.find(RULES_END)
    return text if start < 0 or end < start else text[:start] + text[end + len(RULES_END):]


def added_lines(old: str, new: str) -> str:
    """Example: added_lines("a\\nb\\n", "a\\nx\\nb\\n") returns "x\\n"."""
    a, b = old.splitlines(keepends=True), new.splitlines(keepends=True)
    return "".join("".join(b[j1:j2]) for tag, _, _, j1, j2 in
                   difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if tag in ("insert", "replace"))


def without_manual(text: str) -> str | None:
    """A project's own text with Omoikane's manual taken out, or None when nothing else is left.

    Example: without_manual("# Shop rules\\n...\\n" + manual) returns "# Shop rules\\n...\\n".
    """
    start, end = text.find(MANUAL_HEADING), text.find(RULES_END)
    if start < 0 or end < start:
        return None  # the rules block without the heading: cannot tell the manual from the rest
    rest = text[:start] + text[end + len(RULES_END):]
    return rest if rest.strip() else None


def content(project: Path, path: str, sha: str, template: list[dict[str, str]] | None) -> str | None:
    """The text to ingest for one source, or None when it holds nothing of the system's own. `template` holds the
    trees of the template's versions, the base first; a file any of them holds as it is is the template's, and of
    a file they shipped only the lines none of them has are the system's."""
    text = git(project, "cat-file", "blob", sha)
    if "\0" in text:
        return None  # binary
    if template is None:
        return without_manual(text) if RULES_START in text else text  # a project that adopted Omoikane
    shipped = [version[path] for version in template if path in version]
    if not shipped:
        return text
    if sha in shipped:
        return None
    old = [without_rules(git(project, "cat-file", "blob", blob)) for blob in shipped]
    theirs = {line.strip() for version in old for line in version.splitlines() if line.strip()}
    added = [line for line in added_lines(old[0], without_rules(text)).splitlines(keepends=True)
             if line.strip() not in theirs]
    return "".join(added) if "".join(added).strip() else None


def slugs(paths: list[str], terms: list[str]) -> dict[str, str]:
    """Inbox name per path, from the path with the listed terms redacted (the name is pushed too). Unicode letters
    stay; a name is cut at MAX_SLUG, and a cut name or two paths that would share one get a hash of the path.

    Example: slugs(["docs/a-b.md", "docs/a/b.md"], []) gives two different names.
    """
    base = {p: re.sub(r"[^\w]+", "-", capture.redact(p, terms).lower()).strip("-_") for p in paths}
    counts: dict[str, int] = {}
    for name in base.values():
        counts[name] = counts.get(name, 0) + 1

    def name_of(p: str, name: str) -> str:
        unique = counts[name] == 1 and len(name) <= MAX_SLUG
        return f"{PREFIX}{name[:MAX_SLUG]}{'' if unique else '-' + hashlib.sha1(p.encode()).hexdigest()[:6]}.md"
    return {p: name_of(p, name) for p, name in base.items()}


def last_commit(project: Path, path: str) -> tuple[str, str] | None:
    """Date and full id of the newest commit of HEAD that touched `path`."""
    changed = git(project, "log", "-1", "--format=%cs %H", "HEAD", "--", path).split()
    return (changed[0], changed[1]) if changed else None


def source_note(project: Path, path: str, text: str, partial: bool, local: bool, follows: list[str]) -> str:
    """The inbox file for one source. `local`: the project is the wiki's own repository, so the source page can list
    `path` in `code:`. `follows`: the earlier copies of the same file that this version replaces."""
    changed = last_commit(project, path)
    when = f"last changed {changed[0]} in commit {changed[1][:7]}" if changed else "date unknown"
    scope = " Only the lines this system added to the template's copy follow." if partial else ""
    code = f" `{path}` is a file of this repository: list it in the source page's `code:`." if local else ""
    newer = (f" This is a newer version of the file than the earlier copies {', '.join(f'`{n}`' for n in follows)}: "
             "their source pages no longer match it." if follows else "")
    return (f"# {path} of {project.name} (bootstrap)\n\nCopied by `omoikane/bin/bootstrap.py` from `{path}` in "
            f"`{project.name}`, {when}.{scope}{code}{newer}{BODY_START}{text}")


def history_note(project: Path, exclude: list[str]) -> str | None:
    """The commits of HEAD after the template's, newest first, subject and body. Merge commits are left out: in a
    pull-request workflow the reasons sit in the branch commits, not in "Merge pull request #n". Trailers go (they
    carry names and emails), and a long body is cut with the capture's own marker, so a secret cut short still
    matches the redaction's rule for clipped tokens."""
    log = git(project, "log", "--no-merges", f"-{HISTORY_COMMITS}", "--format=%x00%cs %h %s%n%b", "HEAD",
              *(f"^{rev}" for rev in exclude))
    entries = []
    for entry in filter(None, (e.strip() for e in log.split("\0"))):
        head, _, body = entry.partition("\n")
        body = capture.clip(TRAILER.sub("", body), BODY_CHARS)
        entries.append(f"## {head}\n\n{body}" if body else f"## {head}")
    if not entries:
        return None
    return (f"# Git history of {project.name} (bootstrap)\n\nCopied by `omoikane/bin/bootstrap.py`: the commits "
            f"of `{project.name}` without merges, newest first, at most {HISTORY_COMMITS}, as date, commit and "
            "subject, then the body. A body often holds the reason for a change.\n\n" + "\n\n".join(entries) + "\n")


def copies(omoikane: Path) -> dict[str, str]:
    """Every bootstrap file already written, name to text: this checkout's inbox and sources first, then the review
    gate's branches before the human pulled them. One `git cat-file --batch` reads every file on those branches."""
    found: dict[str, str] = {}
    for folder in ("inbox", "sources"):
        for file in sorted((omoikane / "raw" / folder).glob(f"{PREFIX}*.md")):
            found.setdefault(file.name, file.read_text(encoding="utf-8", errors="replace"))
    wanted: list[str] = []
    for ref in GATE_REFS:
        listing = subprocess.run(["git", "-C", str(omoikane.parent), "-c", "core.quotePath=false", "ls-tree", "-r",
                                  "--name-only", ref, "--", "omoikane/raw/sources", "omoikane/raw/inbox"],
                                 capture_output=True, text=True, encoding="utf-8", errors="replace")
        if listing.returncode == 0:
            wanted += [f"{ref}:{line}" for line in listing.stdout.splitlines()
                       if PurePosixPath(line).name.startswith(PREFIX) and PurePosixPath(line).name not in found]
    if not wanted:
        return found
    out = subprocess.run(["git", "-C", str(omoikane.parent), "cat-file", "--batch"], capture_output=True,
                         input="".join(f"{spec}\n" for spec in wanted).encode("utf-8")).stdout
    at = 0
    for spec in wanted:
        end = out.index(b"\n", at)
        header, at = out[at:end].split(), end + 1
        if len(header) != 3:
            continue  # "<spec> missing"
        size = int(header[2])
        found.setdefault(PurePosixPath(spec).name, out[at:at + size].decode("utf-8", "replace"))
        at += size + 1
    return found


def earlier_copies(name: str, found: dict[str, str]) -> dict[str, str]:
    """The copies under `name`: that one and the versions named after a commit.

    Example: earlier_copies("bootstrap-readme-md.md", found) holds "bootstrap-readme-md-1a2b3c4.md" too.
    """
    version = re.compile(re.escape(name[:-3]) + r"(-[0-9a-f]{7})?\.md")
    return {n: text for n, text in found.items() if version.fullmatch(n)}


def place(names: tuple[str, str], title: str, found: dict[str, str]) -> tuple[str, dict[str, str]] | None:
    """The name this source's first copy takes and its earlier copies, the ones whose first line is `title`.

    Copies under the first name with another source's title hold another repository's file with the same slug
    (`--from`), so the source takes the second name, which carries its project. None when a copy under the name
    has no bootstrap title: the human rewrote it, and whose it is cannot be told.
    """
    for name in names:
        group = earlier_copies(name, found)
        mine = {n: text for n, text in group.items() if text.partition("\n")[0] == title}
        if mine or not group:
            return name, mine
        if not all(TITLE.match(text) for text in group.values()):
            return None
    return None


def holds(copy: str, note: str, commit: str) -> bool:
    """True when `copy` holds the version `note` is: the same commit, or the same text under another commit (a
    rebase, or a template update that left this system's own lines alone)."""
    head, _, body = copy.partition(BODY_START)
    copied = LAST_CHANGED.search(head)
    return body == note.partition(BODY_START)[2] or bool(copied and commit.startswith(copied.group(2)))


def newest(copies_of: dict[str, str], order: list[str]) -> str:
    """The copy of the newest version: latest date, then latest in `order`, the file's commits newest first. Only
    this one is compared, so a file put back to an older text is copied again. A commit no longer in `order` was
    rewritten (an amend, a rebase), so it ranks first on its date."""
    def age(text: str) -> tuple[str, int]:
        copied = LAST_CHANGED.search(text.partition(BODY_START)[0])
        if not copied:
            return "", 0
        position = next((i for i, c in enumerate(order) if c.startswith(copied.group(2))), -1)
        return copied.group(1), -position
    return max(copies_of.values(), key=age)


def bootstrap(project: Path, omoikane: Path = OMOIKANE, redact_file: Path = capture.REDACT_FILE) -> list[str]:
    """Write one inbox file per source of `project` and one for its history; return the names written.

    Example: bootstrap(Path("../shop")) returns ["bootstrap-readme-md.md", ..., "bootstrap-git-history.md"].
    """
    if not git(project, "rev-parse", "--verify", "--quiet", "HEAD", ok=True):
        raise BootstrapError("it has no commit yet; bootstrap reads committed files")
    head = tree(project, "HEAD")
    base, tips = template_versions(project)
    template = [tree(project, rev) for rev in (base, *tips)] if base else None
    terms = capture.redaction_terms(redact_file)
    paths = sorted(p for p in head if is_source(p))
    names = slugs(paths, terms)
    local = project.resolve() == omoikane.parent.resolve()
    found = copies(omoikane)

    def redacted(text: str) -> str:
        return capture.redact(capture.redact_secrets(text), terms)
    project_slug = re.sub(r"[^\w]+", "-", capture.redact(project.name, terms).lower()).strip("-_")
    notes: dict[str, str] = {}
    for path in paths:
        text = content(project, path, head[path], template)
        if text is None:
            continue
        partial = template is not None and any(path in version for version in template)
        placed = place((names[path], f"{names[path][:-3]}-{project_slug}.md"),
                       redacted(f"# {path} of {project.name} (bootstrap)"), found)
        if placed is None:
            continue
        first, earlier = placed
        note = redacted(source_note(project, path, text, partial, local, sorted(earlier)))
        if not earlier:
            notes[first] = note
            continue
        order = git(project, "log", "--format=%H", "HEAD", "--", path).split()
        commit = order[0] if order else ""
        if not holds(newest(earlier, order), note, commit):
            notes[f"{first[:-3]}-{commit[:7]}.md"] = note
    history = history_note(project, [base, *tips] if base else [])
    if history and f"{PREFIX}git-history.md" not in found:
        notes[f"{PREFIX}git-history.md"] = redacted(history)
    inbox = omoikane / "raw" / "inbox"
    written = []
    for name, text in notes.items():
        inbox.mkdir(parents=True, exist_ok=True)
        (inbox / name).write_text(text, encoding="utf-8", newline="\n")
        written.append(name)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--from", dest="project", type=Path, default=REPO, help="the project to read")
    args = parser.parse_args(argv)
    project = args.project.resolve()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")  # a legacy code page cannot print every file name
    try:
        git(project, "rev-parse", "--git-dir")
    except BootstrapError as exc:
        print(f"bootstrap: {project} is not a git repository: {exc}", file=sys.stderr)
        return 2
    try:
        written = bootstrap(project)
    except BootstrapError as exc:
        print(f"bootstrap: {project}: {exc}", file=sys.stderr)
        return 2
    if written and project != REPO.resolve():
        print(f"bootstrap: these come from {project.name}, another repository; the scheduled run commits and pushes "
              "what it ingests, so read them first and delete what must stay private")
    for name in written:
        print(f"bootstrap: wrote omoikane/raw/inbox/{name}" + ("; its file changed since the last copy, and /ingest "
                                                               "marks the earlier source page outdated"
                                                               if VERSION.search(name) else ""))
    print(f"bootstrap: {len(written)} files for /ingest, one agent run each")
    return 0


if __name__ == "__main__":
    sys.exit(main())
