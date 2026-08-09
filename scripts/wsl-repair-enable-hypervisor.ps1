$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$logDirectory = Join-Path $projectRoot 'logs'
New-Item -ItemType Directory -Force -Path $logDirectory | Out-Null
$logPath = Join-Path $logDirectory 'wsl-repair-enable-hypervisor.log'

function Write-Log([string]$Message) {
    $Message | Tee-Object -FilePath $logPath -Append
}

Write-Log "WSL repair started: $(Get-Date -Format o)"
Write-Log "Target change: bcdedit /set hypervisorlaunchtype auto"

$control = Get-ItemProperty -LiteralPath 'HKLM:\SYSTEM\CurrentControlSet\Control'
$before = [string]$control.SystemStartOptions
Write-Log "Observed SystemStartOptions: $before"

if ($before -notmatch 'HYPERVISORLAUNCHTYPE=OFF') {
    Write-Log 'STOP: expected HYPERVISORLAUNCHTYPE=OFF was not observed; no change made.'
    exit 2
}

$result = & bcdedit.exe /set hypervisorlaunchtype auto 2>&1
$exitCode = $LASTEXITCODE
foreach ($line in $result) { Write-Log ([string]$line) }
Write-Log "bcdedit exit code: $exitCode"

if ($exitCode -ne 0) {
    Write-Log 'STOP: bcdedit did not accept the change.'
    exit $exitCode
}

Write-Log 'Change accepted. A Windows restart is required before WSL2 can be re-tested.'
Write-Log "WSL repair finished: $(Get-Date -Format o)"
exit 0
