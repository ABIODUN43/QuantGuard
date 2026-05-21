# QuantGuard AI Security Notes

## Implemented MVP Controls

- HTTPS enforcement is enabled when `QG_ENVIRONMENT=production` or `QG_ENFORCE_HTTPS=true`.
- Secrets are read from environment variables through `QG_*` settings.
- JWT authentication carries the user role claim and protected routes check live database state.
- Role-based access control is available through `require_roles(...)`.
- Password reset uses expiring hashed reset tokens.
- Uploads are limited by `QG_MAX_UPLOAD_BYTES`, extension/content-type checks, and suspicious signature scanning before parsing.
- Rate limiting is enforced per client IP with `QG_RATE_LIMIT_PER_MINUTE`.
- Audit logs record account, auth, upload, export, and privacy actions.
- Data privacy endpoints support account export and soft-delete.

## Production Follow-ups

- Send password-reset tokens by email instead of returning them in API responses.
- Replace in-process rate limiting with Redis when multiple backend instances run.
- Add antivirus scanning such as ClamAV for uploads.
- Store reports in cloud object storage with signed URLs.
- Add admin-only role management UI.
