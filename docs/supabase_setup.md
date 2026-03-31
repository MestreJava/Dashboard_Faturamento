# Supabase Setup (Local + Cloud)

## Security note
Never commit Supabase secrets, service role keys, database passwords, or full connection strings into git. Keep them in local `.env` files only.

## Local Supabase (development)
1) Install the Supabase CLI.
2) From the repo root, start Supabase locally:
   - `supabase start`
3) Apply the schema migrations:
   - `supabase db reset`

The migrations are stored in `supabase/migrations/`.

## Cloud Supabase (shared / production)
1) Link your local repo to the cloud project:
   - `supabase link`
2) Push migrations to the cloud project:
   - `supabase db push`

For the backend, use the cloud Postgres connection string provided by Supabase (Settings → Database). Do not use the anon/service keys for FastAPI DB access; use the Postgres connection string.

## Backend configuration
Create `backend/.env` based on `backend/.env.example`, then run the backend:
- From repo root: `./run-backend.ps1`
- Or from `backend/`: `./run.ps1`

By default, if `DATABASE_URL` is set (and `USE_SEED_DATA != 1`) the API uses Postgres; otherwise it falls back to seeded sample data.

## GSUS CSV ingestion
From repo root:
- `./backend/ingest_gsus.ps1 -CsvPath C:\\path\\to\\gsus.csv`

Re-running the same file should not duplicate rows (idempotent import).

