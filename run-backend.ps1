param(
  [int]$Port = 8002,
  [string]$BindHost = "127.0.0.1"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location $repoRoot

. "$repoRoot\.venv\Scripts\Activate.ps1"

Set-Location "$repoRoot\backend"

python -m uvicorn app.main:app --reload --host $BindHost --port $Port
