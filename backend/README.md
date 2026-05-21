# QuantGuard AI Backend

FastAPI modular monolith for the QuantGuard AI financial intelligence engine.

## Run Locally

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

For PostgreSQL, set the database URL and run migrations:

```powershell
$env:QG_DATABASE_URL="postgresql+psycopg://quantguard:quantguard@localhost:5432/quantguard"
alembic -c alembic.ini upgrade head
```

Without `QG_DATABASE_URL`, local development uses `sqlite:///./quantguard_dev.db` so the app can run immediately.

Seed demo data:

```powershell
python scripts/seed_data.py
```

Back up and restore PostgreSQL:

```powershell
.\scripts\backup_postgres.ps1
.\scripts\restore_postgres.ps1 -BackupFile .\backups\quantguard_YYYYMMDD_HHMMSS.dump
```

See `docs/data_lifecycle.md` for soft-delete, archival, and retention policy.

## MVP Flow

1. `POST /api/v1/auth/register`
2. `POST /api/v1/auth/login`
3. `POST /api/v1/business/onboard`
4. `POST /api/v1/data/manual-entry`
5. `POST /api/v1/analysis/run`
6. `GET /api/v1/forecast/latest`
7. `GET /api/v1/recommendations`
8. `POST /api/v1/scenarios/run`
9. `POST /api/v1/reports/generate`

The backend uses SQLAlchemy persistence with Alembic migrations. PostgreSQL is configured through `QG_DATABASE_URL`; SQLite remains the no-setup local development fallback.
