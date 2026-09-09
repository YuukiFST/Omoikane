<#
.SYNOPSIS
Ingest every file in raw/inbox through the agent, one headless call per file.

.EXAMPLE
bin/wiki-ingest.ps1                      # Claude Code
bin/wiki-ingest.ps1 -Agent opencode      # OpenCode
bin/wiki-ingest.ps1 -Commit              # git commit after each successful ingest
#>
param(
    [ValidateSet("claude", "opencode")] [string] $Agent = "claude",
    [switch] $Commit
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$log = Join-Path $root ".wiki-ingest.log"

function Log([string] $msg) { "$(Get-Date -Format s) $msg" | Tee-Object -FilePath $log -Append }

$files = Get-ChildItem (Join-Path $root "raw/inbox") -File | Where-Object { $_.Name -ne ".gitkeep" }
if (-not $files) { Log "nothing in inbox"; exit 0 }

foreach ($f in $files) {
    $rel = "raw/inbox/$($f.Name)"
    Log "ingest start $rel"
    if ($Agent -eq "claude") {
        claude -p "/ingest $rel" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash(python bin/*),Bash(git mv *)" 2>&1 | Tee-Object -FilePath $log -Append
    } else {
        opencode run "/ingest $rel" 2>&1 | Tee-Object -FilePath $log -Append
    }
    if ($LASTEXITCODE -ne 0) { Log "ingest FAILED $rel"; continue }
    # Agent skipped step 6 of prompts/ingest.md: move the source so the next run does not re-ingest it.
    if (Test-Path $f.FullName) { Move-Item $f.FullName (Join-Path $root "raw/sources") }
    python bin/wiki-index.py | Tee-Object -FilePath $log -Append
    python bin/wiki-lint.py | Tee-Object -FilePath $log -Append
    if ($Commit) {
        git add -A
        git commit -q -m "feat(wiki): ingest $($f.BaseName)" 2>&1 | Tee-Object -FilePath $log -Append
    }
    Log "ingest done $rel"
}
