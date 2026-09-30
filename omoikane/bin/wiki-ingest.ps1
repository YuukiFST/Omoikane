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
    if ($Agent -eq "claude") {
        # dontAsk denies whatever the list does not allow. acceptEdits would also auto-approve rm, mv, cp and sed
        # anywhere in the repository (#25). Edit(...) rules cover the Write tool; a leading / anchors at the
        # repository root. Scripts are named exactly: a wildcard would run a file the agent wrote into
        # omoikane/bin/, or one reached through `..`. File moves are left to this script, after the run.
        # On Windows Claude Code runs shell commands through its PowerShell tool, which Bash(...) rules do not
        # cover; without the PowerShell(...) twins the agent cannot run index and lint and never fixes a finding (#17).
        $scripts = "python omoikane/bin/wiki-index.py", "python omoikane/bin/wiki-lint.py"
        $allowed = @("Read", "Glob", "Grep", "Edit(/omoikane/wiki/**)", "Edit(/omoikane/log.md)", "Edit(/omoikane/_review.md)") +
            ($scripts | ForEach-Object { "Bash($_)"; "PowerShell($_)" })
        # --setting-sources project: allow rules and PreToolUse hooks in the user's own settings would otherwise
        # apply here too (a user-level `Bash(git checkout:*)` or a hook answering "allow" reopens AGENTS.md and
        # omoikane/bin/). --tools and --strict-mcp-config keep plugins and MCP servers out; git is denied outright.
        $prompt = "/$op $arg".TrimEnd()
        claude -p $prompt --setting-sources project --strict-mcp-config --tools "Read,Glob,Grep,Edit,Write,Bash,PowerShell" `
            --permission-mode dontAsk --allowedTools ($allowed -join ",") --disallowedTools "Bash(git *),PowerShell(git *)" `
            2>&1 | Tee-Object -FilePath $log -Append | Out-Host
    } else {
        # OpenCode is not scoped here: its permissions live in its own config, which this repository does not ship.
        # `opencode run --command <name> <args>` runs a .opencode/command/<name>.md command (opencode run --help).
        $rest = @($arg | Where-Object { $_ })  # /synthesize takes no argument; do not pass an empty one
        opencode run --command $op @rest 2>&1 | Tee-Object -FilePath $log -Append | Out-Host
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
