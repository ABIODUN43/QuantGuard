# QuantGuard AI Deployment

This project is ready for a standard MVP deployment:

- Frontend: Render Static Site, Vercel, Netlify, or the included Nginx Docker image.
- Backend: Render, Railway, Azure App Service, AWS, or the included FastAPI Docker image.
- Database: managed PostgreSQL.
- Reports: local container volume for MVP; move to S3, Azure Blob, or Cloudflare R2 later.

## Local Production Smoke Test

1. Copy the production env example:

   ```bash
   cp .env.production.example .env.production
   ```

2. Edit `.env.production` and set strong secrets.

3. Start the production stack:

   ```bash
   docker compose --env-file .env.production -f docker-compose.prod.yml up --build
   ```

4. Open:

   - Frontend: `http://localhost:8080`
   - Backend health: `http://localhost:8000/health`

## Backend on Render

Use `render.yaml` as a blueprint. Render will create:

- `quantguard-api`
- `quantguard-postgres`
- `quantguard-web`

The Blueprint sets the frontend to use:

```text
VITE_SERVER_BASE=https://quantguard-api.onrender.com
VITE_API_BASE=https://quantguard-api.onrender.com/api/v1
```

Render should also have:

```text
QG_ENVIRONMENT=production
QG_ENFORCE_HTTPS=true
QG_SECRET_KEY=<generated secret>
QG_DATABASE_URL=<managed postgres connection string>
QG_CORS_ORIGINS=["https://quantguard-web.onrender.com"]
```

The Blueprint uses Render's `basic-256mb` PostgreSQL plan because legacy Postgres plans such as `starter` are no longer accepted for new databases.

The backend Docker command runs `alembic upgrade head` before starting FastAPI.

## Frontend on Render

The Blueprint deploys `quantguard-web` as a Render Static Site.

Expected frontend URL:

```text
https://quantguard-web.onrender.com
```

If Render assigns a different custom URL, update:

- Backend `QG_CORS_ORIGINS`
- Frontend `VITE_SERVER_BASE`
- Frontend `VITE_API_BASE`

## Frontend on Vercel

Set these Vercel environment variables:

```text
VITE_SERVER_BASE=https://your-backend-domain.onrender.com
VITE_API_BASE=https://your-backend-domain.onrender.com/api/v1
```

Build settings:

```text
Framework: Vite
Build command: npm run build
Output directory: dist
```

The included `vercel.json` handles single-page app routing.

## GitHub Actions

The CI workflow runs:

- backend tests
- frontend tests
- frontend production build
- backend Docker image build
- frontend Docker image build

Optional deploy hooks are supported on pushes to `main`.

Add these repository secrets only after creating deploy hooks:

```text
RENDER_DEPLOY_HOOK_URL
VERCEL_DEPLOY_HOOK_URL
```

## Managed PostgreSQL

Use one managed database per environment:

- development/staging
- production

Run backups daily on the provider. For manual backup:

```bash
pg_dump "$DATABASE_URL" > quantguard-backup.sql
```

Restore:

```bash
psql "$DATABASE_URL" < quantguard-backup.sql
```

## Monitoring and Error Tracking

Recommended production setup:

- Render/Railway/Azure logs for backend runtime logs.
- Sentry for frontend and backend exceptions.
- UptimeRobot or Better Stack for `/health` monitoring.
- Provider-managed PostgreSQL metrics for database health.

Environment variables to add when Sentry is implemented:

```text
SENTRY_DSN
VITE_SENTRY_DSN
```

## Deployment Checklist

- Create GitHub repository.
- Push `main`.
- Create Render backend from `render.yaml`.
- Create Vercel frontend from the repo.
- Set frontend `VITE_*` backend URLs.
- Set backend `QG_CORS_ORIGINS` to the frontend URL.
- Confirm `/health` returns healthy.
- Register, onboard, upload demo data, run analysis, generate a report.
