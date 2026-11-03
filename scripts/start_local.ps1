param([int]$Port = 8765, [switch]$NoOpen)
$ErrorActionPreference = 'Stop'
$workspacePath = Split-Path -Parent $PSScriptRoot
$url = "http://127.0.0.1:$Port"
$healthUrl = "$url/api/health"
function Get-YougeHealth {
    try { return Invoke-RestMethod -Uri $healthUrl -TimeoutSec 2 } catch { return $null }
}
$existing = Get-YougeHealth
if ($existing -and $existing.app -ne 'youge-local') { throw "Port $Port is used by another application. Please use -Port with another number." }
if (-not $existing) {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCommand) { throw 'Python 3.10+ is required. Install Python, then run this launcher again.' }
    $logFolder = Join-Path $workspacePath '.local'
    New-Item -ItemType Directory -Path $logFolder -Force | Out-Null
    $process = Start-Process -FilePath $pythonCommand.Source -ArgumentList @('-m', 'youge.web', '--port', "$Port") -WorkingDirectory $workspacePath -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logFolder "server-$Port.log") -RedirectStandardError (Join-Path $logFolder "server-$Port.error.log") -PassThru
    $ready = $false
    for ($attempt = 0; $attempt -lt 25; $attempt++) {
        $health = Get-YougeHealth
        if ($health -and $health.app -eq 'youge-local') { $ready = $true; break }
        if ($process.HasExited) { break }
        Start-Sleep -Milliseconds 200
    }
    if (-not $ready) { throw "The local server could not start. See $logFolder\server-$Port.error.log" }
    Set-Content -LiteralPath (Join-Path $logFolder "server-$Port.pid") -Value $process.Id -Encoding ascii
}
Write-Host "Youge local website: $url"
if (-not $NoOpen) { Start-Process $url }
