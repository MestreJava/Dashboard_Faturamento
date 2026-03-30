# Dashboard Faturamento — Technical Design (MVP)

## Architecture
- Frontend: React + TypeScript + Vite + Tailwind
- Server-state: TanStack Query
- Table: TanStack Table
- Chart: Apache ECharts
- Backend: FastAPI (Python 3.12)
- Database: Supabase (planned after MVP seed)

## Repo Structure (Target)
```text
/frontend
/backend
/docs
```

## Backend API (MVP)
Base URL: `http://localhost:8002`

### Common Query Params
- `date_from` (ISO date, optional)
- `date_to` (ISO date, optional)
- `source_system` (optional)
- `hospital` (optional)
- `status` (optional)
- `procedure_category` (optional)

### Endpoints
- `GET /health`
- `GET /filters/metadata`
  - Returns available filter values based on dataset.
- `GET /kpis/overview`
  - Returns aggregated KPIs.
- `GET /charts/monthly-volume`
  - Returns monthly counts.
- `GET /tables/unified-records?page=&page_size=`
  - Returns paginated rows + total count.
- `GET /exports/report.xlsx`
- `GET /exports/report.pdf`

## Data Strategy (MVP)
- Use a sample seeded dataset stored in the backend repo for local development.
- All endpoints apply the same filter logic to ensure consistency.
- Later: swap the dataset implementation to Supabase/Postgres while preserving API shapes.

## Security (Planned)
- Supabase Auth + RLS in Phase 6.
- MVP local dev: no auth enforced; implement later behind Supabase JWT verification.

## Frontend Data Flow
- Filter state stored in zustand.
- TanStack Query keys include the filter state.
- Export buttons open backend export URLs with query params.
