<#
.SYNOPSIS
Register a Windows Task Scheduler job that runs wiki-ingest.ps1 every N minutes.

.EXAMPLE
bin/install-schedule.ps1                 # every 30 min, Claude Code, commits
bin/install-schedule.ps1 -Minutes 60 -Agent opencode
bin/install-schedule.ps1 -Remove
#>
param(
    [int] $Minutes = 30,
    [ValidateSet("claude", "opencode")] [string] $Agent = "claude",
    [switch] $Remove
)
$name = "OmoikaneIngest"
if ($Remove) { Unregister-ScheduledTask -TaskName $name -Confirm:$false; "removed $name"; exit 0 }

$script = Join-Path (Split-Path -Parent $PSScriptRoot) "bin/wiki-ingest.ps1"
$action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-NoProfile -File `"$script`" -Agent $Agent -Commit"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes $Minutes)
Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger -Force | Out-Null
"registered ${name}: every $Minutes min via $Agent"
