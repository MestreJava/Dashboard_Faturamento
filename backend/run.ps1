param(
  [int]$Port = 8002,
  [string]$BindHost = "127.0.0.1"
)

$ErrorActionPreference = "Stop"

$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $backendDir

Set-Location $repoRoot

. "$repoRoot\.venv\Scripts\Activate.ps1"

Set-Location $backendDir

python -m uvicorn app.main:app --reload --host $BindHost --port $Port
