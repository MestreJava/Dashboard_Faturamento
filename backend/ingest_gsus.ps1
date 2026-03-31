param(
  [Parameter(Mandatory = $true)]
  [string]$CsvPath,
  [string]$Filename = "",
  [string]$DatabaseUrl = ""
)

$ErrorActionPreference = "Stop"

$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $backendDir

Set-Location $repoRoot
. "$repoRoot\.venv\Scripts\Activate.ps1"

Set-Location $backendDir

$argsList = @("gsus", "--csv", $CsvPath)
if ($Filename -ne "") { $argsList += @("--filename", $Filename) }
if ($DatabaseUrl -ne "") { $argsList += @("--database-url", $DatabaseUrl) }

python -m app.ingest @argsList

