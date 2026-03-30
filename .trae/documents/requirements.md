# Dashboard Faturamento — MVP Requirements

## Goal
Provide a first working “vertical slice” of the dashboard platform: one overview page that supports filters, shows KPIs, renders one chart, displays a paginated table, and exports the current filtered view to Excel and PDF.

## Scope (Phase 1–7 only)
- In scope now: Phase 1–7 foundations for an Analytics MVP and exports.
- Out of scope now: Desktop packaging (Phase 8).

## Users
- MVP user: authenticated internal analyst/admin (single role for now).

## MVP Screens
- Overview Dashboard
  - Global filter bar
  - KPI cards
  - One chart (monthly volume)
  - One advanced table (unified records)
  - Export buttons (Excel/PDF)

## Data Sources (MVP)
- Use one source for the first vertical slice.
- Implementation detail for local dev: backend can use a seeded sample dataset until Supabase tables are introduced.

## Filters (MVP)
- Date range (`date_from`, `date_to`)
- Source system (`source_system`)
- Hospital (`hospital`)
- Status (`status`)
- Procedure category (`procedure_category`)

## KPIs (MVP)
- Total volume (count of records)
- Approval rate (% approved)
- Average value
- Average processing time (days)
- Volume by source (for comparison and sanity checks)

## Chart (MVP)
- Monthly volume trend grouped by month (and optionally by source).

## Table (MVP)
- Unified records table
  - Columns: date, source, hospital, status, procedure category, approved, value, processing days
  - Pagination (server-side)
  - Sort by date/value (optional)

## Exports (MVP)
- Excel export of the current filtered dataset.
- PDF export of the current filtered dataset.

## Non-Functional Requirements
- Local development must be runnable with:
  - Frontend: Vite dev server
  - Backend: FastAPI + Uvicorn
- CORS configured for local frontend URL.
- Clear error messages for failed API calls.

## Acceptance Criteria
- Overview page loads without errors.
- Changing any filter updates KPIs, chart, and table.
- Table paginates.
- Clicking Excel/PDF downloads files consistent with current filters.

