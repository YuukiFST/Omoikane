"""Turn a coding-session transcript into a source file under raw/inbox/sessions/, with no LLM call.

Runs from the harness stop hooks: Claude Code Stop/SessionEnd (.claude/settings.json), Pi agent_end/session_shutdown
(.pi/extensions/omoikane.ts), OpenCode session idle (.opencode/plugins/omoikane.ts). Idempotent: every run rewrites
the file for the session, so firing on every turn is safe. Never blocks the harness: any failure prints one line
and exits 0.

Usage:
    python omoikane/bin/session-capture.py                                    # Claude hook: JSON payload on stdin
    python omoikane/bin/session-capture.py --transcript X.jsonl               # Claude transcript, manual or test run
    python omoikane/bin/session-capture.py --harness pi --transcript X.jsonl  # Pi session file
    python omoikane/bin/session-capture.py --harness opencode --transcript X.json  # `opencode export <id>` output

Each harness has its own reader producing the same Session/Turn objects; the Markdown and the skip rules are shared.
Claude Code's transcript is internal and undocumented; Pi's and OpenCode's are documented (links in docs/architecture.md).
Every reader ignores what it does not recognise, so a format change degrades to a thinner capture, not a crash.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable

from wikilib import OMOIKANE, parse_frontmatter

INBOX = OMOIKANE / "raw" / "inbox" / "sessions"
INGESTED = OMOIKANE / "raw" / "sources" / "sessions"
NO_CAPTURE_ENV = "OMOIKANE_NO_CAPTURE"
# Headless runs of these commands are Omoikane maintaining itself; capturing them would loop forever.
OMOIKANE_COMMANDS = {"/ingest", "/ask", "/lint", "/distill"}
# Lower-cased tool names: Claude Code capitalises (Edit, Bash), Pi and OpenCode do not (edit, bash).
EDIT_TOOLS = {"edit", "write", "multiedit", "notebookedit"}
SHELL_TOOLS = {"bash", "powershell"}
# Path argument per harness: Claude Code file_path/notebook_path, OpenCode filePath, Pi path.
PATH_KEYS = ("file_path", "notebook_path", "filePath", "path")
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
    parent: str = ""  # id of the session that spawned this one (OpenCode subagent); such sessions are skipped
    turns: list[Turn] = field(default_factory=list)

    @property
    def short_id(self) -> str:
        """Tail of the id, used in file names. Pi ids are UUIDv7 and OpenCode ids are time-ordered, so their heads
        collide for sessions started close together; the tail is random in all three harnesses."""
        return self.session_id[-8:]

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
    """Path relative to the session cwd, posix-style; a path outside the cwd is returned as given.

    Separators are normalised first: OpenCode on Windows mixes `C:/x` and `C:\\x` between session and tool input,
    and a transcript captured on Windows must read the same on a Linux CI runner.
    """
    if not cwd:
        return path
    try:
        return Path(path.replace("\\", "/")).resolve().relative_to(Path(cwd.replace("\\", "/")).resolve()).as_posix()
    except (ValueError, OSError):
        return path


def iso_from_ms(stamp: object) -> str:
    """Unix milliseconds (Pi message and OpenCode timestamps) to the ISO-8601 UTC form Claude Code writes."""
    if not isinstance(stamp, (int, float)) or stamp <= 0:
        return ""
    moment = datetime.fromtimestamp(stamp / 1000, tz=timezone.utc)
    return moment.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def text_blocks(content: object) -> str:
    """Join the text of a content string or list of `{type: text}` blocks; other block types contribute nothing."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(str(b.get("text", "")) for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def first_line(command: object) -> str:
    lines = str(command or "").strip().splitlines()
    return clip(lines[0], COMMAND_CHARS) if lines else ""


def jsonl_entries(path: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict):
            entries.append(entry)
    return entries


def read_claude_transcript(path: Path, session_id: str = "") -> Session:
    """Parse a Claude Code JSONL transcript into turns: one per user prompt, with what the agent did in reply.

    Example: read_claude_transcript(Path("~/.claude/projects/<proj>/<id>.jsonl")).turns[0].files
    returns the files the first prompt led the agent to edit.
    """
    session = Session(session_id=session_id, harness="claude")
    current: Turn | None = None
    for entry in jsonl_entries(path):
        if entry.get("isSidechain"):
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
                current.errors.append(clip(text_blocks(block.get("content")), ERROR_CHARS))
            elif kind == "assistant" and block_type == "text" and str(block.get("text", "")).strip():
                current.notes.append(clip(str(block["text"]), NOTE_CHARS))
            elif kind == "assistant" and block_type == "tool_use":
                record_tool_use(current, str(block.get("name", "")), block.get("input") or {}, session.cwd)
    return session


def pi_active_branch(entries: list[dict[str, object]]) -> list[dict[str, object]]:
    """Entries on the path from the current leaf to the root, oldest first; abandoned `/tree` branches are left out.

    Pi's leaf is the last entry appended (docs/session-format.md, "Tree Structure"). Legacy v1 files have no ids
    and are returned as they are.

    Example: pi_active_branch([a, b(parent a), c(parent a)]) returns [a, c].
    """
    tree = [e for e in entries if e.get("type") != "session"]
    if not tree or not all(e.get("id") for e in tree):
        return tree
    by_id = {str(e["id"]): e for e in tree}
    path: list[dict[str, object]] = []
    current: dict[str, object] | None = tree[-1]
    while current is not None and len(path) <= len(tree):
        path.append(current)
        current = by_id.get(str(current.get("parentId") or ""))
    path.reverse()
    return path


def read_pi_transcript(path: Path, session_id: str = "") -> Session:
    """Parse a Pi coding agent session file (~/.pi/agent/sessions/**/*.jsonl) into turns.

    Example: read_pi_transcript(Path("2026-09-15T10-00-00-000Z_<uuid>.jsonl")).turns[0].commands
    returns the shell commands the agent ran for the first prompt.
    """
    session = Session(session_id=session_id, harness="pi")
    entries = jsonl_entries(path)
    header = next((e for e in entries if e.get("type") == "session"), {})
    session.session_id = session.session_id or str(header.get("id", ""))
    session.cwd = str(header.get("cwd", ""))
    session.started = str(header.get("timestamp", ""))
    current: Turn | None = None
    for entry in pi_active_branch(entries):
        message = entry.get("message")
        if entry.get("type") != "message" or not isinstance(message, dict):
            continue
        stamp = str(entry.get("timestamp", "")) or iso_from_ms(message.get("timestamp"))
        if stamp:
            session.started = session.started or stamp
            session.ended = stamp
        role = message.get("role")
        if role == "user":
            current = Turn(prompt=clip(text_blocks(message.get("content")), PROMPT_CHARS))
            session.turns.append(current)
        elif current is None:
            continue
        elif role == "bashExecution" and message.get("command"):
            current.commands.append(first_line(message.get("command")))
        elif role == "toolResult" and message.get("isError"):
            current.errors.append(clip(text_blocks(message.get("content")), ERROR_CHARS))
        elif role == "assistant":
            content = message.get("content")
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and str(block.get("text", "")).strip():
                    current.notes.append(clip(str(block["text"]), NOTE_CHARS))
                elif block.get("type") == "toolCall":
                    record_tool_use(current, str(block.get("name", "")), block.get("arguments") or {}, session.cwd)
    return session


def read_opencode_export(path: Path, session_id: str = "") -> Session:
    """Parse an OpenCode session document `{info, messages: [{info, parts}]}`: the output of `opencode export <id>`,
    and what the plugin writes from the SDK's `client.session.get` and `client.session.messages`.

    Example: read_opencode_export(Path("ses_x.json")).turns[0].files
    returns the files the first prompt led the agent to edit.
    """
    doc = json.loads(path.read_text(encoding="utf-8"))
    info = doc.get("info") if isinstance(doc, dict) and isinstance(doc.get("info"), dict) else {}
    messages = doc.get("messages") if isinstance(doc, dict) and isinstance(doc.get("messages"), list) else []
    session = Session(session_id=session_id or str(info.get("id", "")), harness="opencode")
    session.cwd = str(info.get("directory", ""))
    session.parent = str(info.get("parentID") or "")
    times = info.get("time") if isinstance(info.get("time"), dict) else {}
    session.started = iso_from_ms(times.get("created"))
    session.ended = iso_from_ms(times.get("updated"))
    current: Turn | None = None
    for message in messages:
        if not isinstance(message, dict):
            continue
        meta = message.get("info") if isinstance(message.get("info"), dict) else {}
        raw_parts = message.get("parts") if isinstance(message.get("parts"), list) else []
        parts = [p for p in raw_parts if isinstance(p, dict)]
        role = meta.get("role")
        if role == "user":
            # synthetic parts are written by the harness (tool replays, compaction), not typed by the human
            prompt = "\n".join(str(p.get("text", "")) for p in parts if p.get("type") == "text" and not p.get("synthetic"))
            if not prompt.strip():
                continue
            current = Turn(prompt=clip(prompt, PROMPT_CHARS))
            session.turns.append(current)
            continue
        if role != "assistant" or current is None:
            continue
        for part in parts:
            if part.get("type") == "text" and str(part.get("text", "")).strip():
                current.notes.append(clip(str(part["text"]), NOTE_CHARS))
            elif part.get("type") == "tool":
                state = part.get("state") if isinstance(part.get("state"), dict) else {}
                record_tool_use(current, str(part.get("tool", "")), state.get("input") or {}, session.cwd)
                if state.get("status") == "error":
                    current.errors.append(clip(str(state.get("error", "")), ERROR_CHARS))
    return session


READERS: dict[str, Callable[[Path, str], Session]] = {
    "claude": read_claude_transcript,
    "pi": read_pi_transcript,
    "opencode": read_opencode_export,
}


def record_tool_use(turn: Turn, name: str, tool_input: object, cwd: str) -> None:
    if not isinstance(tool_input, dict):
        return
    if name.lower() in EDIT_TOOLS:
        path = next((str(tool_input[k]) for k in PATH_KEYS if tool_input.get(k)), "")
        if path and relative_to(path, cwd) not in turn.files:
            turn.files.append(relative_to(path, cwd))
    elif name.lower() in SHELL_TOOLS and first_line(tool_input.get("command")):
        turn.commands.append(first_line(tool_input.get("command")))


def skip_reason(session: Session, worktree: list[str]) -> str | None:
    """Return why the session is not worth a source file, or None when it is.

    Example: skip_reason(Session(first_command="/ingest", ...), []) returns "omoikane operation /ingest".
    """
    if session.first_command in OMOIKANE_COMMANDS:
        return f"omoikane operation {session.first_command}"
    if session.parent:
        return f"subagent of {session.parent}"
    if not session.turns:
        return "no prompts"
    if not session.files and not worktree:
        return "no files edited"
    return None


def run_git(cwd: str, *args: str) -> str:
    if not cwd or not Path(cwd).is_dir():
        return ""
    try:
        out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout if out.returncode == 0 else ""


def git_status(cwd: str) -> list[str]:
    """Changed paths in the working tree at capture time; catches edits made through shell commands, not edit tools."""
    return [line for line in run_git(cwd, "status", "--short").splitlines() if line.strip()][:50]


def git_branch(cwd: str) -> str:
    """Current branch, for harnesses whose transcript does not record it (Claude Code's does)."""
    return run_git(cwd, "rev-parse", "--abbrev-ref", "HEAD").strip()


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
        f"# Coding session {session.day} ({session.short_id}, part {part})",
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


def ingested_parts(session: Session) -> list[int]:
    """`turns:` of every distilled part of this session under raw/sources/sessions/, matched by full session id."""
    parts: list[int] = []
    for path in INGESTED.glob(f"{session.day}-{session.short_id}*.md"):
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
        if parsed and str(parsed[0].get("session")) == session.session_id:
            parts.append(int(str(parsed[0].get("turns", 0)) or 0))
    return parts


def capture(transcript: Path, session_id: str = "", harness: str = "claude", first_command: str = "") -> str:
    session = READERS[harness](transcript, session_id)
    session.first_command = session.first_command or first_command
    session.branch = session.branch or git_branch(session.cwd)
    worktree = git_status(session.cwd)
    reason = skip_reason(session, worktree)
    if reason:
        return f"skip: {reason}"
    parts = ingested_parts(session)
    covered = max(parts, default=0)
    if covered >= len(session.turns):
        return "skip: already ingested"
    part = len(parts) + 1
    suffix = "" if part == 1 else f"-part{part}"
    target = INBOX / f"{session.day}-{session.short_id}{suffix}.md"
    INBOX.mkdir(parents=True, exist_ok=True)
    target.write_text(render(session, session.turns[covered:], part, worktree), encoding="utf-8")
    return f"captured {target.relative_to(OMOIKANE.parent).as_posix()} ({len(session.turns) - covered} turns)"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--harness", choices=sorted(READERS), default="claude")
    parser.add_argument("--transcript", type=Path, help="session file; default: transcript_path from the Claude Code hook payload on stdin")
    parser.add_argument("--session-id", default="")
    parser.add_argument("--first-command", default="", help="first slash command of the session, when the harness reports it")
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
    print(f"session-capture: {capture(transcript, session_id, args.harness, args.first_command)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - a capture failure must never block the harness from stopping
        print(f"session-capture: error {type(exc).__name__}: {exc}")
        sys.exit(0)
