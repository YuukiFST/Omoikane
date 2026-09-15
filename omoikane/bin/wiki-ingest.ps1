<#
.SYNOPSIS
Ingest every file in omoikane/raw/inbox through the agent, one headless call per file.

Plain sources go through /ingest; captured coding sessions under raw/inbox/sessions go through /distill.
A session file modified less than -QuietMinutes ago may still be growing (Stop fires on every turn), so it waits.

.EXAMPLE
omoikane/bin/wiki-ingest.ps1                      # Claude Code
omoikane/bin/wiki-ingest.ps1 -Agent opencode      # OpenCode
omoikane/bin/wiki-ingest.ps1 -Commit              # git commit after each successful run
#>
param(
    [ValidateSet("claude", "opencode")] [string] $Agent = "claude",
    [switch] $Commit,
    [int] $QuietMinutes = 30
)
$ErrorActionPreference = "Stop"
$omoikane = Split-Path -Parent $PSScriptRoot
$root = Split-Path -Parent $omoikane
Set-Location $root
$log = Join-Path $omoikane ".wiki-ingest.log"
# The agent runs started here maintain the wiki; the session hooks must neither capture nor inject context for them.
$env:OMOIKANE_NO_CAPTURE = "1"

function Log([string] $msg) { "$(Get-Date -Format s) $msg" | Tee-Object -FilePath $log -Append }

$inbox = Join-Path $omoikane "raw/inbox"
$files = Get-ChildItem $inbox -File -Recurse | Where-Object { $_.Name -ne ".gitkeep" }
if (-not $files) { Log "nothing in inbox"; exit 0 }

foreach ($f in $files) {
    $isSession = $f.DirectoryName -eq (Join-Path $inbox "sessions")
    if ($isSession -and $f.LastWriteTime -gt (Get-Date).AddMinutes(-$QuietMinutes)) {
        Log "session still active, waiting: $($f.Name)"; continue
    }
    $op = if ($isSession) { "distill" } else { "ingest" }
    $rel = [IO.Path]::GetRelativePath($root, $f.FullName) -replace "\\", "/"
    $dest = Join-Path $omoikane $(if ($isSession) { "raw/sources/sessions" } else { "raw/sources" })
    Log "$op start $rel"
    if ($Agent -eq "claude") {
        claude -p "/$op $rel" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash(python omoikane/bin/*),Bash(git mv *)" 2>&1 | Tee-Object -FilePath $log -Append
    } else {
        opencode run "/$op $rel" 2>&1 | Tee-Object -FilePath $log -Append
    }
    if ($LASTEXITCODE -ne 0) { Log "$op FAILED $rel"; continue }
    # Agent skipped the move step of the prompt: move the source so the next run does not process it again.
    if (Test-Path $f.FullName) { Move-Item $f.FullName $dest }
    python omoikane/bin/wiki-index.py | Tee-Object -FilePath $log -Append
    python omoikane/bin/wiki-lint.py | Tee-Object -FilePath $log -Append
    if ($Commit) {
        git add -A
        git commit -q -m "feat(wiki): $op $($f.BaseName)" 2>&1 | Tee-Object -FilePath $log -Append
    }
    Log "$op done $rel"
}
