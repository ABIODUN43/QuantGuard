# QuantGuard AI Data Lifecycle Policy

## Soft Delete

Business-owned records are not physically deleted by default. Tables include:

- `deleted_at`
- `archived_at`

When a user deletes data, the API should set `deleted_at` and exclude those rows from normal queries. Physical deletion is reserved for explicit account erasure workflows, legal requests, or administrator maintenance windows.

## Archival

Set `archived_at` for old records that should remain available for reports/audits but should not appear in active dashboard calculations by default.

Recommended MVP archival rules:

- Financial records older than 7 years: archive.
- Reports older than 3 years: archive or move file artifacts to cold storage.
- Scenario results older than 2 years: archive.
- Economic indicators: keep indefinitely unless storage pressure requires aggregation.

## Account Deletion

When a business owner requests account deletion:

1. Set `deleted_at` on the user and businesses immediately.
2. Set `deleted_at` on all child records for that business.
3. Revoke active tokens.
4. Keep data in recoverable soft-delete state for 30 days.
5. After 30 days, permanently purge or anonymize records unless legal retention applies.

## Backup Strategy

Production PostgreSQL should use:

- Daily logical backups with `pg_dump --format=custom`.
- Weekly full backups retained for at least 8 weeks.
- Monthly backups retained for at least 12 months.
- Restore drills at least once per quarter.

Use:

```powershell
.\scripts\backup_postgres.ps1
.\scripts\restore_postgres.ps1 -BackupFile .\backups\quantguard_YYYYMMDD_HHMMSS.dump
```

## Restore Strategy

Restore into a staging database first whenever possible:

1. Create a fresh database.
2. Run `pg_restore`.
3. Run app smoke tests.
4. Promote or cut over only after verification.

Never restore over production without an approved maintenance window and a fresh pre-restore backup.
