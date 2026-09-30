"""Headless tests for omoikane/bin/session-capture.py against a fixture transcript. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "omoikane" / "bin"))

import importlib

capture = importlib.import_module("session-capture")
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def user(text: str, **extra: object) -> dict[str, object]:
    return {"type": "user", "timestamp": "2026-09-15T10:00:00Z", "sessionId": "abcdef12-0000", "cwd": "C:/proj",
            "gitBranch": "main", "message": {"role": "user", "content": text}, **extra}


def assistant(*blocks: dict[str, object]) -> dict[str, object]:
    return {"type": "assistant", "timestamp": "2026-09-15T10:05:00Z", "message": {"role": "assistant", "content": list(blocks)}}


def tool_result(text: str, is_error: bool) -> dict[str, object]:
    return {"type": "user", "timestamp": "2026-09-15T10:06:00Z",
            "message": {"role": "user", "content": [{"type": "tool_result", "content": text, "is_error": is_error}]}}


def write_transcript(tmp: Path, entries: list[dict[str, object]]) -> Path:
    path = tmp / "t.jsonl"
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\nnot json\n", encoding="utf-8")
    return path


CODING_SESSION = [
    {"type": "attachment", "attachment": {}},
    user("<local-command-caveat>ignored</local-command-caveat>", isMeta=True),
    user("Fix the parser"),
    assistant({"type": "thinking", "thinking": "hidden"},
              {"type": "text", "text": "Root cause: the regex misses CRLF."},
              {"type": "tool_use", "name": "Edit", "input": {"file_path": "C:/proj/src/parser.py"}},
              {"type": "tool_use", "name": "Bash", "input": {"command": "python -m pytest\nsecond line"}}),
    tool_result("Exit code 1\nAssertionError", True),
    tool_result("ok", False),
    {"type": "user", "isSidechain": True, "message": {"role": "user", "content": "subagent prompt"}},
    user("Now add a test"),
    assistant({"type": "text", "text": "Done, test added."},
              {"type": "tool_use", "name": "Write", "input": {"file_path": "C:/proj/tests/test_parser.py"}}),
]


class ReadTranscript(unittest.TestCase):
    def test_turns_files_commands_errors(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            s = capture.read_claude_transcript(write_transcript(Path(d), CODING_SESSION))
        self.assertEqual(s.session_id, "abcdef12-0000")
        self.assertEqual(s.day, "2026-09-15")
        self.assertEqual([t.prompt for t in s.turns], ["Fix the parser", "Now add a test"])
        self.assertEqual(s.turns[0].files, ["src/parser.py"])
        self.assertEqual(s.turns[0].commands, ["python -m pytest"])
        self.assertEqual(s.turns[0].errors, ["Exit code 1\nAssertionError"])
        self.assertEqual(s.turns[0].notes, ["Root cause: the regex misses CRLF."])
        self.assertEqual(s.files, ["src/parser.py", "tests/test_parser.py"])

    def test_error_text_kept_when_block_has_no_type(self) -> None:
        entries = [user("Fix"), tool_result("ignored", False)]
        entries[1]["message"]["content"] = [{"type": "tool_result", "is_error": True, "content": [{"text": "Traceback boom"}]}]
        with tempfile.TemporaryDirectory() as d:
            s = capture.read_claude_transcript(write_transcript(Path(d), entries))
        self.assertEqual(s.turns[0].errors, ["Traceback boom"])

    def test_slash_command_recorded(self) -> None:
        entries = [user("<command-name>/ingest</command-name><command-args>x.md</command-args>")]
        with tempfile.TemporaryDirectory() as d:
            s = capture.read_claude_transcript(write_transcript(Path(d), entries))
        self.assertEqual(s.first_command, "/ingest")
        self.assertEqual(s.turns[0].prompt, "/ingest")

    def test_every_omoikane_operation_is_skipped(self) -> None:
        # A new prompt missing from the skip list gets its sessions captured and distilled, which loops.
        prompts = sorted((Path(capture.OMOIKANE) / "prompts").glob("*.md"))
        self.assertTrue(prompts)
        for prompt in prompts:
            with self.subTest(op=prompt.stem), tempfile.TemporaryDirectory() as d:
                entries = [user(f"<command-name>/{prompt.stem}</command-name>")]
                s = capture.read_claude_transcript(write_transcript(Path(d), entries))
                self.assertEqual(capture.skip_reason(s, ["M x.py"]), f"omoikane operation /{prompt.stem}")


class ReadPiTranscript(unittest.TestCase):
    """Fixture follows docs/session-format.md of @earendil-works/pi-coding-agent 0.85.1 (v3 tree)."""

    def test_turns_follow_active_branch(self) -> None:
        s = capture.read_pi_transcript(FIXTURES / "pi-session.jsonl")
        self.assertEqual(s.harness, "pi")
        self.assertEqual(s.session_id, "0192f0a1-1111-7000-8000-000000000001")
        self.assertEqual((s.cwd, s.day, s.ended), ("C:/proj", "2026-09-15", "2026-09-15T10:00:08.000Z"))
        self.assertEqual([t.prompt for t in s.turns], ["Fix the parser", "Now add a test"])  # e5 is a dead branch
        self.assertEqual(s.turns[0].files, ["src/parser.py"])
        self.assertEqual(s.turns[0].commands, ["python -m pytest", "git status"])  # tool call, then ! command
        self.assertEqual(s.turns[0].errors, ["Exit code 1\nAssertionError"])
        self.assertEqual(s.turns[0].notes, ["Root cause: the regex misses CRLF."])
        self.assertEqual(s.files, ["src/parser.py", "tests/test_parser.py"])

    def test_entry_without_id_in_a_tree_file_does_not_resurrect_dead_branches(self) -> None:
        lines = (FIXTURES / "pi-session.jsonl").read_text(encoding="utf-8").splitlines()
        lines.insert(3, json.dumps({"type": "label", "timestamp": "2026-09-15T10:00:02.500Z", "targetId": "e1", "label": "x"}))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "mixed.jsonl"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            s = capture.read_pi_transcript(path)
        self.assertEqual([t.prompt for t in s.turns], ["Fix the parser", "Now add a test"])

    def test_legacy_v1_file_without_ids_is_read_linearly(self) -> None:
        entries = [{"type": "session", "version": 1, "id": "old", "timestamp": "2026-01-01T00:00:00.000Z", "cwd": "C:/proj"},
                   {"type": "message", "timestamp": "2026-01-01T00:00:01.000Z", "message": {"role": "user", "content": "hi"}},
                   {"type": "message", "timestamp": "2026-01-01T00:00:02.000Z", "message": {"role": "user", "content": "again"}}]
        with tempfile.TemporaryDirectory() as d:
            s = capture.read_pi_transcript(write_transcript(Path(d), entries))
        self.assertEqual([t.prompt for t in s.turns], ["hi", "again"])


class ReadOpenCodeExport(unittest.TestCase):
    """Fixture has the shape of `opencode export <id>` on 1.18.30, which the plugin reproduces from the SDK."""

    def test_turns_files_commands_errors(self) -> None:
        s = capture.read_opencode_export(FIXTURES / "opencode-export.json")
        self.assertEqual(s.harness, "opencode")
        self.assertEqual(s.session_id, "ses_0123456789abcdefghijklmnop")
        self.assertEqual((s.cwd, s.started, s.ended), ("C:\\proj", "2026-09-15T10:20:00.000Z", "2026-09-15T10:30:00.000Z"))
        self.assertEqual([t.prompt for t in s.turns], ["Fix the parser", "Now add a test"])  # synthetic msg_3 dropped
        self.assertEqual(s.turns[0].files, ["src/parser.py"])
        self.assertEqual(s.turns[0].commands, ["python -m pytest"])
        self.assertEqual(s.turns[0].errors, ["Exit code 1\nAssertionError"])
        self.assertEqual(s.turns[0].notes, ["Root cause: the regex misses CRLF."])
        self.assertEqual(s.files, ["src/parser.py", "tests/test_parser.py"])
        self.assertEqual(s.parent, "")

    def test_command_template_as_first_prompt_is_the_first_command(self) -> None:
        doc = json.loads((FIXTURES / "opencode-export.json").read_text(encoding="utf-8"))
        doc["messages"][0]["parts"][0]["text"] = "Read `omoikane/prompts/distill.md` and follow it. Argument: x.md"
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "cmd.json"
            path.write_text(json.dumps(doc), encoding="utf-8")
            s = capture.read_opencode_export(path)
        self.assertEqual(s.first_command, "/distill")
        self.assertEqual(capture.skip_reason(s, []), "omoikane operation /distill")

    def test_subagent_session_is_skipped(self) -> None:
        doc = json.loads((FIXTURES / "opencode-export.json").read_text(encoding="utf-8"))
        doc["info"]["parentID"] = "ses_parent"
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "sub.json"
            path.write_text(json.dumps(doc), encoding="utf-8")
            s = capture.read_opencode_export(path)
        self.assertEqual(capture.skip_reason(s, []), "subagent of ses_parent")


class SkipRules(unittest.TestCase):
    def test_omoikane_operation_is_skipped(self) -> None:
        s = capture.Session(session_id="x", harness="claude", first_command="/ask", turns=[capture.Turn("q", files=["a"])])
        self.assertEqual(capture.skip_reason(s, []), "omoikane operation /ask")

    def test_no_edits_is_skipped_unless_worktree_dirty(self) -> None:
        s = capture.Session(session_id="x", harness="claude", turns=[capture.Turn("q")])
        self.assertEqual(capture.skip_reason(s, []), "no files edited")
        self.assertIsNone(capture.skip_reason(s, [" M a.py"]))


def claude_session(d: Path, first: str, later: str) -> capture.Session:
    command = lambda text: f"<command-name>/{text[1:]}</command-name>" if text.startswith("/") else text  # noqa: E731
    entries = [user(command(first)), assistant({"type": "tool_use", "name": "Edit", "input": {"file_path": "C:/proj/a.py"}}),
               user(command(later)), assistant({"type": "text", "text": "Answered."})]
    return capture.read_claude_transcript(write_transcript(d, entries))


def pi_session(d: Path, first: str, later: str) -> capture.Session:
    entries = [json.loads(line) for line in (FIXTURES / "pi-session.jsonl").read_text(encoding="utf-8").splitlines()
               if line.startswith("{")]
    for entry in entries:
        if entry.get("id") == "e1":
            entry["message"]["content"] = first
        elif entry.get("id") == "e7":
            entry["message"]["content"] = [{"type": "text", "text": later}]
    return capture.read_pi_transcript(write_transcript(d, entries))


def opencode_session(d: Path, first: str, later: str) -> capture.Session:
    template = lambda text: (f"Read `omoikane/prompts/{text[1:]}.md` and follow it. Argument: q"  # noqa: E731
                             if text.startswith("/") else text)
    doc = json.loads((FIXTURES / "opencode-export.json").read_text(encoding="utf-8"))
    user_texts = [p for m in doc["messages"] if m["info"]["role"] == "user"
                  for p in m["parts"] if p.get("type") == "text" and not p.get("synthetic")]
    user_texts[0]["text"], user_texts[-1]["text"] = template(first), template(later)
    path = d / "doc.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    return capture.read_opencode_export(path)


class OperationOnlyFromTheFirstPrompt(unittest.TestCase):
    # One rule for every harness (#34): the Claude reader latched a command from any turn, so a coding session
    # that ran /ask in turn 4 was dropped whole, while the Pi and OpenCode readers read the first prompt only.
    READERS = {"claude": claude_session, "pi": pi_session, "opencode": opencode_session}

    def test_command_in_a_later_turn_keeps_the_session(self) -> None:
        for harness, read in self.READERS.items():
            with self.subTest(harness=harness), tempfile.TemporaryDirectory() as d:
                s = read(Path(d), "Fix the parser", "/ask")
                self.assertEqual(s.first_command, "")
                self.assertIsNone(capture.skip_reason(s, [" M a.py"]))

    def test_command_as_the_first_prompt_skips_the_session(self) -> None:
        for harness, read in self.READERS.items():
            with self.subTest(harness=harness), tempfile.TemporaryDirectory() as d:
                s = read(Path(d), "/distill", "Now add a test")
                self.assertEqual(capture.skip_reason(s, [" M a.py"]), "omoikane operation /distill")


class Render(unittest.TestCase):
    def test_markdown_has_frontmatter_and_sections(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            s = capture.read_claude_transcript(write_transcript(Path(d), CODING_SESSION))
        md = capture.render(s, s.turns, 1, [" M src/parser.py"])
        self.assertTrue(md.startswith("---\nharness: claude\nsession: abcdef12-0000\npart: 1\nturns: 2\n"))
        for needle in ("## Working tree at capture", "## Files edited", "- `src/parser.py`", "## Turn 2",
                       "### Errors", "Root cause: the regex misses CRLF."):
            self.assertIn(needle, md)
        self.assertNotIn("hidden", md)

    def test_keep_ends_keeps_start_and_end(self) -> None:
        self.assertEqual(capture.keep_ends([10, 10, 10, 10], 25), (1, 1))
        self.assertEqual(capture.keep_ends([10, 10], 100), (2, 0))


if __name__ == "__main__":
    unittest.main()
