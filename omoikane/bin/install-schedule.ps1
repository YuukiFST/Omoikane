<#
.SYNOPSIS
Register the daily Windows Task Scheduler fallback for the ingest: ingest-timer.py now, with no window.

The ingest normally starts when a coding session goes quiet: session-capture.py arms ingest-timer.py after every
capture (#96). This task catches what no session arms: files dropped into omoikane/raw/inbox/ by hand, and a
waiter lost to a reboot. It runs pythonw.exe, which has no console, and ingest-timer.py starts wiki-ingest.ps1
-Commit with no window; a run already due later, for a session still going, keeps its time. StartWhenAvailable
runs a day missed while the machine was off at the next chance.

-Commit goes through the review gate (review-gate.py): each run works in the worktree <repo>-wiki-auto on branch
wiki/auto, never on this checkout, and pushes one PR to main that merges itself once its checks pass. Needs a
remote `origin` and a `gh auth login` session; a blocked run leaves <repo>-wiki-auto/omoikane/.wiki-ingest.blocked.

.EXAMPLE
omoikane/bin/install-schedule.ps1                 # daily, Claude Code, through the review gate
omoikane/bin/install-schedule.ps1 -Agent opencode
omoikane/bin/install-schedule.ps1 -Remove
#>
param(
    [ValidateSet("claude", "opencode")] [string] $Agent = "claude",
    [switch] $Remove
)
$name = "OmoikaneIngest"
if ($Remove) { Unregister-ScheduledTask -TaskName $name -Confirm:$false; "removed $name"; exit 0 }

# By path: the task does not search PATH the way a shell does. pythonw, not python: python opens a console window.
$pythonw = (Get-Command pythonw.exe -ErrorAction Stop).Source
$timer = Join-Path $PSScriptRoot "ingest-timer.py"
$action = New-ScheduledTaskAction -Execute $pythonw -Argument "`"$timer`" now --agent $Agent" `
    -WorkingDirectory (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$trigger = New-ScheduledTaskTrigger -Daily -At (Get-Date)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
"registered ${name}: daily via $Agent, no window"
