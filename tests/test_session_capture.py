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

    def test_slash_command_recorded(self) -> None:
        entries = [user("<command-name>/ingest</command-name><command-args>x.md</command-args>")]
        with tempfile.TemporaryDirectory() as d:
            s = capture.read_claude_transcript(write_transcript(Path(d), entries))
        self.assertEqual(s.first_command, "/ingest")
        self.assertEqual(s.turns[0].prompt, "/ingest")


class SkipRules(unittest.TestCase):
    def test_omoikane_operation_is_skipped(self) -> None:
        s = capture.Session(session_id="x", harness="claude", first_command="/ask", turns=[capture.Turn("q", files=["a"])])
        self.assertEqual(capture.skip_reason(s, []), "omoikane operation /ask")

    def test_no_edits_is_skipped_unless_worktree_dirty(self) -> None:
        s = capture.Session(session_id="x", harness="claude", turns=[capture.Turn("q")])
        self.assertEqual(capture.skip_reason(s, []), "no files edited")
        self.assertIsNone(capture.skip_reason(s, [" M a.py"]))


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
