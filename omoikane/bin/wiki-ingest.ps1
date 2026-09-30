<#
.SYNOPSIS
Ingest every file in omoikane/raw/inbox through the agent, one headless call per file.

Plain sources go through /ingest; captured coding sessions under raw/inbox/sessions go through /distill.
A session file modified less than -QuietMinutes ago may still be growing (Stop fires on every turn), so it waits.
After -SynthesizeEvery distills since the last cross-session pass, /synthesize runs once; 0 turns it off.

.EXAMPLE
omoikane/bin/wiki-ingest.ps1                      # Claude Code
omoikane/bin/wiki-ingest.ps1 -Agent opencode      # OpenCode
omoikane/bin/wiki-ingest.ps1 -Commit              # git commit after each successful run
#>
param(
    [ValidateSet("claude", "opencode")] [string] $Agent = "claude",
    [switch] $Commit,
    [int] $QuietMinutes = 30,
    [int] $SynthesizeEvery = 5
)
$ErrorActionPreference = "Stop"
$omoikane = Split-Path -Parent $PSScriptRoot
$root = Split-Path -Parent $omoikane
Set-Location $root
$log = Join-Path $omoikane ".wiki-ingest.log"
# The agent runs started here maintain the wiki; the session hooks must neither capture nor inject context for them.
$env:OMOIKANE_NO_CAPTURE = "1"

function Log([string] $msg) { "$(Get-Date -Format s) $msg" | Tee-Object -FilePath $log -Append }

# One headless agent call; returns $true when the agent exited 0. Output goes to the host, not the pipeline,
# or it would become part of the return value.
function Invoke-Operation([string] $op, [string] $arg) {
    # Ticking a proposal in _review.md is the human's approval; the agent may edit the file, so any tick it adds
    # is undone after the run.
    $review = Join-Path $omoikane "_review.md"
    $before = Join-Path ([IO.Path]::GetTempPath()) "omoikane-review-before.md"
    if (Test-Path $review) { Copy-Item $review $before -Force } else { Set-Content $before "" }
    # The scope (edit only the wiki, the log and _review.md; run only index and lint; no git) lives in
    # headless-scope.py, rendered for each harness, so the two cannot drift (#39). File moves are left to this
    # script, after the run.
    $scope = python omoikane/bin/headless-scope.py $Agent
    if ($LASTEXITCODE -ne 0) { throw "headless-scope.py $Agent failed" }
    if ($Agent -eq "claude") {
        $prompt = "/$op $arg".TrimEnd()
        $flags = @($scope | ConvertFrom-Json)
        claude -p $prompt @flags 2>&1 | Tee-Object -FilePath $log -Append | Out-Host
    } else {
        # OPENCODE_CONFIG_CONTENT is merged over the global and project config (opencode.ai/docs/config); it
        # defines the agent that carries the scope. `opencode run --command <name> <args>` runs a
        # .opencode/command/<name>.md command (opencode run --help).
        $rest = @($arg | Where-Object { $_ })  # /synthesize takes no argument; do not pass an empty one
        $env:OPENCODE_CONFIG_CONTENT = $scope
        try { opencode run --agent omoikane-headless --command $op @rest 2>&1 | Tee-Object -FilePath $log -Append | Out-Host }
        finally { Remove-Item Env:OPENCODE_CONFIG_CONTENT }
    }
    $ok = $LASTEXITCODE -eq 0
    python omoikane/bin/review-ticks.py --before $before | Tee-Object -FilePath $log -Append | Out-Host
    return $ok
}

function Complete-Operation([string] $op, [string] $name) {
    python omoikane/bin/wiki-index.py | Tee-Object -FilePath $log -Append
    python omoikane/bin/wiki-lint.py | Tee-Object -FilePath $log -Append
    if ($Commit) {
        git add -A
        git commit -q -m "feat(wiki): $op $name" 2>&1 | Tee-Object -FilePath $log -Append
    }
}

$inbox = Join-Path $omoikane "raw/inbox"
$files = Get-ChildItem $inbox -File -Recurse | Where-Object { $_.Name -ne ".gitkeep" }
if (-not $files) { Log "nothing in inbox" }

foreach ($f in $files) {
    $isSession = $f.DirectoryName -eq (Join-Path $inbox "sessions")
    if ($isSession -and $f.LastWriteTime -gt (Get-Date).AddMinutes(-$QuietMinutes)) {
        Log "session still active, waiting: $($f.Name)"; continue
    }
    $op = if ($isSession) { "distill" } else { "ingest" }
    $rel = [IO.Path]::GetRelativePath($root, $f.FullName) -replace "\\", "/"
    $dest = Join-Path $omoikane $(if ($isSession) { "raw/sources/sessions" } else { "raw/sources" })
    Log "$op start $rel"
    if (-not (Invoke-Operation $op $rel)) { Log "$op FAILED $rel"; continue }
    # The headless agent may not move files (#25): move the source so the next run does not process it again.
    if (Test-Path $f.FullName) { New-Item -ItemType Directory -Force $dest | Out-Null; Move-Item $f.FullName $dest }
    Complete-Operation $op $f.BaseName
    Log "$op done $rel"
}

# The cross-session pass reads distilled session pages, so it runs after the inbox, never before.
if ($SynthesizeEvery -gt 0) {
    python omoikane/bin/synthesize-due.py --every $SynthesizeEvery | Tee-Object -FilePath $log -Append
    if ($LASTEXITCODE -eq 0) {
        Log "synthesize start"
        if (Invoke-Operation "synthesize" "") { Log "synthesize done" } else { Log "synthesize FAILED" }
        # The log heading is the counter. A run that did not write it would trigger again on every schedule.
        python omoikane/bin/synthesize-due.py --every $SynthesizeEvery | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Add-Content -Path (Join-Path $omoikane "log.md") -Encoding utf8 -Value "`n## [$(Get-Date -Format yyyy-MM-dd)] synthesize | ended without a log entry"
            Log "synthesize wrote no log entry; heading appended so the next run waits"
        }
        Complete-Operation "synthesize" "sessions"
    }
}
