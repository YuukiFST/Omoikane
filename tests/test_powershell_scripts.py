"""Parse every PowerShell script with PowerShell's own parser. Run: python -m unittest discover -s tests

The scripts run unattended (the scheduled task), never in CI; a syntax error would surface only when the task
fires and does nothing (#42). ubuntu-latest ships pwsh.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PWSH = shutil.which("pwsh")
PARSE = (
    "$out = foreach ($f in $args) { $e = $null; "
    "[System.Management.Automation.Language.Parser]::ParseFile($f, [ref]$null, [ref]$e) | Out-Null; "
    "foreach ($x in $e) { \"${f}:$($x.Extent.StartLineNumber): $($x.Message)\" } }; ConvertTo-Json -InputObject @($out)"
)


def parse_errors(paths: list[Path]) -> list[str]:
    """One `file:line: message` per parse error in `paths`, from a single pwsh call."""
    # -File, not -Command: only a script file receives the paths in $args.
    with tempfile.TemporaryDirectory() as d:
        script = Path(d) / "parse.ps1"
        script.write_text(PARSE, encoding="utf-8")
        run = subprocess.run([str(PWSH), "-NoProfile", "-NonInteractive", "-File", str(script), *map(str, paths)],
                             capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(run.stdout)


@unittest.skipUnless(PWSH, "pwsh not on PATH")
class PowerShellScripts(unittest.TestCase):
    def test_every_script_parses(self) -> None:
        scripts = sorted(p for p in REPO.rglob("*.ps1") if ".git" not in p.parts and "node_modules" not in p.parts)
        self.assertTrue(scripts)
        self.assertEqual(parse_errors(scripts), [])

    def test_a_syntax_error_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.ps1"
            bad.write_text('param(\n    [string] $x\nif ($x) { "unclosed"\n', encoding="utf-8")
            errors = parse_errors([bad])
        self.assertTrue(errors)
        self.assertTrue(all(e.startswith(f"{bad}:") for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
