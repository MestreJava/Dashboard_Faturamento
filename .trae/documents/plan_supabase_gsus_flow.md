# Plan — Supabase + GSUS→SISAIH01→DATASUS Flow (MVP→Real DB)

## Summary
Replace the backend’s seeded in-memory dataset with Supabase Postgres as the source of truth, starting with **GSUS CSV ingestion** keyed by **AIH number**, while keeping the existing API shapes working. Add a new chart endpoint + UI chart to compare **GSUS / SISAIH01 / DATASUS** volumes by Portuguese status (ex: *Autorizado, Apresentado, Não-Apresentado, Rejeitado, Cancelado, Reapresentado*). Keep the system evolvable by introducing a thin “data access layer” so we can add SISAIH01 and DATASUS later without rewriting endpoints.

## Current State Analysis (repo facts)
- Backend (FastAPI) serves filters/KPIs/chart/table/exports using a seeded list created in [sample_data.py](file:///c:/MyProjects/DashboardFaturamento/backend/app/sample_data.py) and referenced in [main.py](file:///c:/MyProjects/DashboardFaturamento/backend/app/main.py).
- Data model is a single “unified record” with fields: date, source_system, hospital, status, procedure_category, approved, value, processing_days ([schemas.py](file:///c:/MyProjects/DashboardFaturamento/backend/app/schemas.py)).
- Frontend uses TanStack Query to call these endpoints and renders a monthly volume chart ([MonthlyVolumeChart.tsx](file:///c:/MyProjects/DashboardFaturamento/frontend/src/components/MonthlyVolumeChart.tsx)).
- No Supabase integration exists yet (no client libs, no DATABASE_URL usage, no SQL migrations present).
- Dev ports are now backend 8002 and frontend 5182; CORS is restricted to the frontend origin in [main.py](file:///c:/MyProjects/DashboardFaturamento/backend/app/main.py).

## Goals / Success Criteria
- Backend reads and writes real data in **Supabase Postgres** (local for dev + cloud for shared/production).
- GSUS CSV ingest loads into Supabase and immediately powers:
  - `/filters/metadata`
  - `/kpis/overview`
  - `/charts/monthly-volume`
  - `/tables/unified-records`
  - `/exports/report.xlsx` and `/exports/report.pdf`
- Add a new comparison chart (API + UI) that shows counts across **GSUS/SISAIH01/DATASUS** broken down by **status (Portuguese)**.
- Architecture remains evolvable: adding SISAIH01 and DATASUS becomes “add ingestion + mapping” rather than “rewrite dashboard”.

## Key Domain Decisions (locked from your instructions)
- Platform: **Supabase**.
- Ingestion order / analysis order: **GSUS first**, **SISAIH01 second**, **DATASUS last**.
- Primary linkage key (default): **AIH number** (used to relate the same case across sources).
- Initial GSUS ingestion format: **CSV export**.
- Environment strategy: **both local Supabase (dev) and cloud Supabase**; local may have extra indexes/aux data, cloud is the shared source.
- Supabase data to consume (now/soon): patients, hospital names, SIGTAP procedure reference table.

## Proposed Changes (what/why/how, grounded to repo paths)

### 1) Add Supabase SQL schema + migrations
**Why:** Make the DB the source of truth with a structure that supports multi-source flow and your Portuguese statuses.

**Changes:**
- Create a `supabase/` folder (Supabase CLI structure) with migrations:
  - `supabase/migrations/*_001_init.sql`
  - `supabase/migrations/*_002_views.sql` (analytics views for KPIs and charts)
- Create tables (minimum set to power current UI + flow chart):
  - `raw_gsus` (staging): stores CSV rows (as JSONB) + extracted typed columns where known (AIH, dates, status, hospital, procedure).
  - `fact_case_events` (canonical): one row per “event/status” per source:
    - `aih` (text, required)
    - `source_system` (text constrained to GSUS/SISAIH01/DATASUS)
    - `status` (text; Portuguese strings supported)
    - `event_date` (date)
    - `hospital_name` (text) and/or `hospital_id` if we add `dim_hospital` early
    - `procedure_code` (text, optional for GSUS initially)
    - numeric metrics used today (`value`, `processing_days`) as nullable
    - uniqueness constraint for idempotent loads (ex: `(source_system, aih, status, event_date)` or an `import_hash`)
  - `dim_sigtap_procedure` (optional in first pass; can be created but populated later).
  - `dim_hospital` (optional in first pass; may start as “name only”, then normalize later).
- Create SQL views:
  - `vw_filters_metadata` (distinct lists + min/max date)
  - `vw_kpis_overview` (aggregate metrics)
  - `vw_monthly_volume` (month → totals + by_source)
  - `vw_status_by_source` (status → counts per source) for the new chart

### 2) Backend: introduce DB access layer + switch endpoints to SQL
**Why:** Keep API stable while swapping the underlying storage from in-memory list → Postgres.

**Changes:**
- Add a DB module (new file) for connection management using `DATABASE_URL`:
  - `backend/app/db.py` (create pool on startup, close on shutdown)
- Add a repository layer (new files) that executes SQL queries used by endpoints:
  - `backend/app/repos/metadata_repo.py`
  - `backend/app/repos/kpis_repo.py`
  - `backend/app/repos/charts_repo.py`
  - `backend/app/repos/records_repo.py`
- Update [main.py](file:///c:/MyProjects/DashboardFaturamento/backend/app/main.py) to:
  - Use DB repos when `DATABASE_URL` is configured
  - Optionally keep the seeded fallback for dev safety (behind a flag), but default to DB once set
- Keep response models in [schemas.py](file:///c:/MyProjects/DashboardFaturamento/backend/app/schemas.py) compatible; extend only when needed for the new chart endpoint.

### 3) Backend: GSUS CSV ingestion pipeline (idempotent)
**Why:** Load real GSUS data first and validate the full pipeline before adding SISAIH01/DATASUS.

**Changes:**
- Add an ingestion module:
  - `backend/app/ingest/gsus_csv.py` (parse CSV; write to `raw_gsus` + `fact_case_events`)
- Add a CLI-like entrypoint script (kept simple, runnable with venv):
  - `backend/ingest_gsus.ps1` (calls a Python module with args)
  - `backend/app/ingest/__main__.py` (argparse)
- Idempotency strategy:
  - Compute `import_hash` for each raw row (ex: sha256 of normalized row JSON) and enforce uniqueness in `raw_gsus`.
  - Insert into `fact_case_events` using `ON CONFLICT DO NOTHING` with a uniqueness constraint.

### 4) New “flow comparison” chart (API + UI)
**Why:** You explicitly need a graph comparing the 3 sources and Portuguese statuses.

**Backend:**
- Add endpoint `GET /charts/status-by-source` returning:
  - ordered list of statuses + per-source counts
  - filterable by date range, hospital, procedure (same query params style as other endpoints)

**Frontend:**
- Add a new component:
  - `frontend/src/components/StatusBySourceChart.tsx` (ECharts stacked bar or grouped bar)
- Add a hook in `frontend/src/api/hooks.ts` and types in `frontend/src/api/types.ts`
- Place the chart on the main dashboard page (likely [Home.tsx](file:///c:/MyProjects/DashboardFaturamento/frontend/src/pages/Home.tsx))

### 5) Environment configuration (local + cloud Supabase)
**Why:** Run the same backend code against local Supabase for development and cloud Supabase for shared use.

**Changes:**
- Add `backend/.env.example` documenting required env vars:
  - `DATABASE_URL=...`
  - optional flags like `USE_SEED_DATA=0/1`
- Add lightweight docs under `docs/` describing:
  - how to start local Supabase
  - how to apply migrations
  - how to point backend at local vs cloud

## Assumptions & Constraints
- AIH is available consistently in GSUS CSV and will be used as the default linkage key across sources.
- We will store Portuguese statuses as plain text (no enforced enum) to stay flexible while the vocabulary stabilizes.
- SIGTAP and hospital normalization can start “name/code only” and be progressively normalized as soon as real reference files/tables are available.
- No Auth/RLS enforcement is added in this step (Phase 6 later), but the schema will be compatible with adding it.

## Verification Steps (acceptance checks)
- Local Supabase starts; migrations apply cleanly (fresh DB).
- GSUS CSV ingestion:
  - re-running the same import does not duplicate rows (idempotent)
  - `fact_case_events` row counts match expectations
- Backend:
  - `/health` OK
  - `/filters/metadata` returns Portuguese statuses present in DB
  - `/kpis/overview`, `/charts/monthly-volume`, `/tables/unified-records` return data from DB (not seed)
  - `/exports/report.xlsx` and `/exports/report.pdf` download and contain DB-driven rows
- Frontend:
  - dashboard loads with filters + existing monthly chart
  - new “status by source” chart renders and updates with filters

## Rollout / Next Iterations (not executed in this plan)
- Add SISAIH01 ingestion + mapping to canonical events (based on AIH).
- Add DATASUS ingestion + mapping and compute “approved in DATASUS” rates.
- Add more KPIs/views, then Phase 6 Supabase Auth + RLS.

