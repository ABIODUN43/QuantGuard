param(
  [string]$DatabaseUrl = $env:QG_DATABASE_URL,
  [string]$OutputDir = ".\backups"
)

if (-not $DatabaseUrl) {
  Write-Error "QG_DATABASE_URL or -DatabaseUrl is required."
  exit 1
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$file = Join-Path $OutputDir "quantguard_$timestamp.dump"

pg_dump --format=custom --no-owner --no-acl --file="$file" "$DatabaseUrl"
if ($LASTEXITCODE -ne 0) {
  Write-Error "pg_dump failed."
  exit $LASTEXITCODE
}

Write-Output "Backup written to $file"
