"""Turn a coding-session transcript into a source file under raw/inbox/sessions/, with no LLM call.

Runs from the harness Stop and SessionEnd hooks (see .claude/settings.json). Idempotent: every run rewrites
the file for the session, so firing on every turn is safe. Never blocks the harness: any failure prints one
line and exits 0.

Usage:
    python omoikane/bin/session-capture.py                      # hook: reads the harness JSON payload on stdin
    python omoikane/bin/session-capture.py --transcript X.jsonl # manual or test run

The Claude Code transcript format is internal and undocumented; the parser reads only the fields observed
in real sessions and ignores anything it does not recognise, so a format change degrades to a thinner
capture rather than a crash.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

from wikilib import OMOIKANE, parse_frontmatter

INBOX = OMOIKANE / "raw" / "inbox" / "sessions"
INGESTED = OMOIKANE / "raw" / "sources" / "sessions"
NO_CAPTURE_ENV = "OMOIKANE_NO_CAPTURE"
# Headless runs of these commands are Omoikane maintaining itself; capturing them would loop forever.
OMOIKANE_COMMANDS = {"/ingest", "/ask", "/lint", "/distill"}
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "PowerShell"}
COMMAND_TAG = re.compile(r"<command-name>(/[\w:-]+)</command-name>")
NOTE_CHARS = 1500
PROMPT_CHARS = 2000
ERROR_CHARS = 400
COMMAND_CHARS = 200
NOTES_BUDGET = 40_000


@dataclass
class Turn:
    prompt: str
    notes: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class Session:
    session_id: str
    harness: str
    cwd: str = ""
    branch: str = ""
    started: str = ""
    ended: str = ""
    first_command: str = ""
    turns: list[Turn] = field(default_factory=list)

    @property
    def day(self) -> str:
        return self.started[:10] if len(self.started) >= 10 else date.today().isoformat()

    @property
    def files(self) -> list[str]:
        return sorted({f for t in self.turns for f in t.files})


def clip(text: str, limit: int) -> str:
    text = text.strip()
    return text if len(text) <= limit else text[:limit].rstrip() + f" [... {len(text) - limit} chars cut]"


def relative_to(path: str, cwd: str) -> str:
    try:
        return Path(path).resolve().relative_to(Path(cwd).resolve()).as_posix() if cwd else path
    except (ValueError, OSError):
        return path


def read_claude_transcript(path: Path, session_id: str = "") -> Session:
    """Parse a Claude Code JSONL transcript into turns: one per user prompt, with what the agent did in reply.

    Example: read_claude_transcript(Path("~/.claude/projects/<proj>/<id>.jsonl")).turns[0].files
    returns the files the first prompt led the agent to edit.
    """
    session = Session(session_id=session_id, harness="claude")
    current: Turn | None = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(entry, dict) or entry.get("isSidechain"):
            continue
        kind = entry.get("type")
        message = entry.get("message")
        if kind not in ("user", "assistant") or not isinstance(message, dict):
            continue
        stamp = str(entry.get("timestamp", ""))
        if stamp:
            session.started = session.started or stamp
            session.ended = stamp
        session.session_id = session.session_id or str(entry.get("sessionId", ""))
        session.cwd = session.cwd or str(entry.get("cwd", ""))
        session.branch = session.branch or str(entry.get("gitBranch", ""))
        content = message.get("content")
        if kind == "user" and isinstance(content, str):
            if entry.get("isMeta") or content.lstrip().startswith("<local-command-"):
                continue
            command = COMMAND_TAG.search(content)
            if command and not session.first_command:
                session.first_command = command.group(1)
            current = Turn(prompt=clip(command.group(1) if command else content, PROMPT_CHARS))
            session.turns.append(current)
            continue
        if current is None:
            continue
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if kind == "user" and block_type == "tool_result" and block.get("is_error"):
                current.errors.append(clip(result_text(block.get("content")), ERROR_CHARS))
            elif kind == "assistant" and block_type == "text" and str(block.get("text", "")).strip():
                current.notes.append(clip(str(block["text"]), NOTE_CHARS))
            elif kind == "assistant" and block_type == "tool_use":
                record_tool_use(current, str(block.get("name", "")), block.get("input") or {}, session.cwd)
    return session


def result_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(str(b.get("text", "")) for b in content if isinstance(b, dict))
    return ""


def record_tool_use(turn: Turn, name: str, tool_input: object, cwd: str) -> None:
    if not isinstance(tool_input, dict):
        return
    if name in EDIT_TOOLS:
        path = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
        if path and relative_to(path, cwd) not in turn.files:
            turn.files.append(relative_to(path, cwd))
    elif name in SHELL_TOOLS:
        command = str(tool_input.get("command", "")).strip().splitlines()
        if command:
            turn.commands.append(clip(command[0], COMMAND_CHARS))


def skip_reason(session: Session, worktree: list[str]) -> str | None:
    """Return why the session is not worth a source file, or None when it is.

    Example: skip_reason(Session(first_command="/ingest", ...), []) returns "omoikane operation /ingest".
    """
    if session.first_command in OMOIKANE_COMMANDS:
        return f"omoikane operation {session.first_command}"
    if not session.turns:
        return "no prompts"
    if not session.files and not worktree:
        return "no files edited"
    return None


def git_status(cwd: str) -> list[str]:
    """Changed paths in the working tree at capture time; catches edits made through shell commands, not edit tools."""
    if not cwd or not Path(cwd).is_dir():
        return []
    try:
        out = subprocess.run(
            ["git", "status", "--short"], cwd=cwd, capture_output=True, text=True, timeout=5, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return [line for line in out.stdout.splitlines() if line.strip()][:50] if out.returncode == 0 else []


def keep_ends(lengths: list[int], budget: int) -> tuple[int, int]:
    """How many notes to keep from the start and from the end within a character budget: the plan and the outcome.

    Example: keep_ends([10, 10, 10, 10], 25) returns (1, 1).
    """
    if sum(lengths) <= budget:
        return len(lengths), 0
    head = used = 0
    while head < len(lengths) and used + lengths[head] <= budget // 2:
        used += lengths[head]
        head += 1
    tail = 0
    while head + tail < len(lengths) and used + lengths[-1 - tail] <= budget:
        used += lengths[-1 - tail]
        tail += 1
    return head, tail


def render(session: Session, turns: list[Turn], part: int, worktree: list[str]) -> str:
    """Markdown the distill prompt reads. Frontmatter carries the ids the continuation logic needs."""
    out = [
        "---",
        f"harness: {session.harness}",
        f"session: {session.session_id}",
        f"part: {part}",
        f"turns: {len(session.turns)}",
        f"started: {session.started}",
        f"ended: {session.ended}",
        f"cwd: {session.cwd}",
        f"branch: {session.branch}",
        "---",
        "",
        f"# Coding session {session.day} ({session.session_id[:8]}, part {part})",
        "",
        "Captured by `omoikane/bin/session-capture.py`, no LLM involved. Agent notes are clipped, not summarised.",
        "",
    ]
    if worktree:
        out += ["## Working tree at capture", "", "```", *worktree, "```", ""]
    files = sorted({f for t in turns for f in t.files})
    if files:
        out += ["## Files edited", "", *[f"- `{f}`" for f in files], ""]
    flat = [(ti, ni) for ti, t in enumerate(turns) for ni in range(len(t.notes))]
    head, tail = keep_ends([len(turns[ti].notes[ni]) for ti, ni in flat], NOTES_BUDGET)
    kept = set(flat[:head] + (flat[len(flat) - tail:] if tail else []))
    cut = len(flat) - len(kept)
    for i, t in enumerate(turns):
        out += [f"## Turn {i + 1}", "", "### Prompt", "", t.prompt, ""]
        if t.files:
            out += ["### Edited", "", *[f"- `{f}`" for f in t.files], ""]
        if t.commands:
            out += ["### Commands", "", "```", *t.commands, "```", ""]
        if t.errors:
            out += ["### Errors", "", *[f"- {e}" for e in t.errors], ""]
        notes = [n for ni, n in enumerate(t.notes) if (i, ni) in kept]
        if notes:
            out += ["### Agent notes", "", *[n + "\n" for n in notes]]
    if cut:
        out += [f"[... {cut} agent notes cut to fit {NOTES_BUDGET} chars]", ""]
    return "\n".join(out).rstrip() + "\n"


def ingested_turns(session: Session) -> int:
    """How many turns of this session already sit in raw/sources/sessions/, so a later capture appends only the rest."""
    covered = 0
    for path in INGESTED.glob(f"{session.day}-{session.session_id[:8]}*.md"):
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
        if parsed and str(parsed[0].get("session")) == session.session_id:
            covered = max(covered, int(str(parsed[0].get("turns", 0)) or 0))
    return covered


def capture(transcript: Path, session_id: str = "") -> str:
    session = read_claude_transcript(transcript, session_id)
    worktree = git_status(session.cwd)
    reason = skip_reason(session, worktree)
    if reason:
        return f"skip: {reason}"
    covered = ingested_turns(session)
    if covered >= len(session.turns):
        return "skip: already ingested"
    part = 1 if covered == 0 else 1 + len(list(INGESTED.glob(f"{session.day}-{session.session_id[:8]}*.md")))
    suffix = "" if part == 1 else f"-part{part}"
    target = INBOX / f"{session.day}-{session.session_id[:8]}{suffix}.md"
    INBOX.mkdir(parents=True, exist_ok=True)
    target.write_text(render(session, session.turns[covered:], part, worktree), encoding="utf-8")
    return f"captured {target.relative_to(OMOIKANE.parent).as_posix()} ({len(session.turns) - covered} turns)"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--transcript", type=Path, help="JSONL transcript; default: transcript_path from the hook payload on stdin")
    parser.add_argument("--session-id", default="")
    args = parser.parse_args(argv)
    if os.environ.get(NO_CAPTURE_ENV):
        return 0
    transcript, session_id = args.transcript, args.session_id
    if transcript is None:
        payload = json.loads(sys.stdin.read() or "{}")
        transcript = Path(str(payload.get("transcript_path", "")))
        session_id = session_id or str(payload.get("session_id", ""))
    if not transcript or not transcript.is_file():
        print(f"session-capture: no transcript at {transcript}")
        return 0
    print(f"session-capture: {capture(transcript, session_id)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - a capture failure must never block the harness from stopping
        print(f"session-capture: error {type(exc).__name__}: {exc}")
        sys.exit(0)
