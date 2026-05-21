param(
  [Parameter(Mandatory=$true)][string]$BackupFile,
  [string]$DatabaseUrl = $env:QG_DATABASE_URL
)

if (-not $DatabaseUrl) {
  Write-Error "QG_DATABASE_URL or -DatabaseUrl is required."
  exit 1
}

if (-not (Test-Path $BackupFile)) {
  Write-Error "Backup file not found: $BackupFile"
  exit 1
}

pg_restore --clean --if-exists --no-owner --no-acl --dbname="$DatabaseUrl" "$BackupFile"
if ($LASTEXITCODE -ne 0) {
  Write-Error "pg_restore failed."
  exit $LASTEXITCODE
}

Write-Output "Database restored from $BackupFile"
