"""Skill folders under .claude/skills against omoikane/skills.md, and the limits every harness puts on a skill (#111).

Pi caps a description at 1,024 characters and loads every SKILL.md it finds below a skills folder as a skill
(docs/skills.md of pi-coding-agent 1.0.4); a vendored skill must ship its upstream licence.
"""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "omoikane" / "bin"))
from wikilib import OMOIKANE, REPO  # noqa: E402

SKILLS = REPO / ".claude" / "skills"
MANIFEST = OMOIKANE / "skills.md"
MAX_DESCRIPTION = 1024
OWN = "Omoikane"
ROW = re.compile(r"^\|\s*([a-z][a-z0-9-]*)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|\s*$")
NAME = re.compile(r"^name:\s*(.+?)\s*$", re.M)
DESCRIPTION = re.compile(r"^description:\s*(.*?)\s*$", re.M)


def manifest_rows(text: str) -> dict[str, str]:
    """Skill name to licence for every table row of the manifest; header and separator rows do not match.

    Example: manifest_rows("| how | u | c | MIT | none |") returns {"how": "MIT"}.
    """
    return {m.group(1): m.group(4).strip() for line in text.splitlines() if (m := ROW.match(line))}


def frontmatter(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    return text.split("---", 2)[1] if text.startswith("---") else ""


def findings(skills: Path, manifest: str) -> list[str]:
    """One line per skill folder or manifest row that breaks the rules in the module docstring.

    Example: findings(Path(".claude/skills"), "| gone | u | c | MIT | none |") returns
    ["gone: manifest row names no folder with a SKILL.md"].
    """
    rows = manifest_rows(manifest)
    out = []
    for name, licence in rows.items():
        folder = skills / name
        if not (folder / "SKILL.md").is_file():
            out.append(f"{name}: manifest row names no folder with a SKILL.md")
        elif licence != OWN and not (folder / "LICENSE").is_file():
            out.append(f"{name}: licence {licence} but no LICENSE file in the folder")
    for skill_md in sorted(skills.glob("*/SKILL.md")):
        folder = skill_md.parent
        if (folder / "LICENSE").is_file() and folder.name not in rows:
            out.append(f"{folder.name}: ships a LICENSE but has no row in omoikane/skills.md")
        head = frontmatter(skill_md)
        name = NAME.search(head)
        if not name or name.group(1).strip("\"'") != folder.name:
            out.append(f"{folder.name}: frontmatter name must equal the folder name")
        description = DESCRIPTION.search(head)
        text = description.group(1).strip("\"'") if description else ""
        if not text or text in (">", "|", ">-", "|-"):
            out.append(f"{folder.name}: description missing or not on one line")
        elif len(text) > MAX_DESCRIPTION:
            out.append(f"{folder.name}: description is {len(text)} characters, Pi's limit is {MAX_DESCRIPTION}")
        for nested in sorted(folder.rglob("SKILL.md")):
            if nested != skill_md:
                out.append(f"{folder.name}: nested {nested.relative_to(folder).as_posix()} loads as a skill in Pi")
    return out


def skill(root: Path, name: str, description: str = "Use when testing.", licence: bool = False) -> Path:
    folder = root / name
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {description}\n---\n\nBody.\n", encoding="utf-8")
    if licence:
        (folder / "LICENSE").write_text("MIT", encoding="utf-8")
    return folder


class SkillsManifest(unittest.TestCase):
    def test_repository_skills_match_the_manifest(self) -> None:
        self.assertEqual(findings(SKILLS, MANIFEST.read_text(encoding="utf-8")), [])

    def test_each_rule_fires(self) -> None:
        row = "| {} | https://example.org | abc1234 | {} | none |"
        cases = (
            ("row without folder", lambda r: None, row.format("gone", "MIT"),
             ["gone: manifest row names no folder with a SKILL.md"]),
            ("third-party licence without file", lambda r: skill(r, "a"), row.format("a", "MIT"),
             ["a: licence MIT but no LICENSE file in the folder"]),
            ("own skill needs no file", lambda r: skill(r, "a"), row.format("a", OWN), []),
            ("licence file without row", lambda r: skill(r, "a", licence=True), "",
             ["a: ships a LICENSE but has no row in omoikane/skills.md"]),
            ("vendored and listed", lambda r: skill(r, "a", licence=True), row.format("a", "Apache-2.0"), []),
            ("name differs from folder", lambda r: (r / "b").mkdir() or (r / "b" / "SKILL.md").write_text(
                "---\nname: a\ndescription: x\n---\n", encoding="utf-8"), "",
             ["b: frontmatter name must equal the folder name"]),
            ("folded description", lambda r: skill(r, "a", description=">"), "",
             ["a: description missing or not on one line"]),
            ("long description", lambda r: skill(r, "a", description="x" * 1025), "",
             ["a: description is 1025 characters, Pi's limit is 1024"]),
            ("nested skill", lambda r: skill(skill(r, "a") / "examples", "b"), "",
             ["a: nested examples/b/SKILL.md loads as a skill in Pi"]),
        )
        for name, build, manifest, expected in cases:
            with self.subTest(name), tempfile.TemporaryDirectory() as d:
                build(Path(d))
                self.assertEqual(findings(Path(d), manifest), expected)


if __name__ == "__main__":
    unittest.main()
