# Dashboard Project Roadmap

## Project Goal
Build an evolvable web dashboard that combines **GSUS**, **SISAIH01**, and **DATASUS** into the same tables and charts, supports filters, KPIs, averages, approval rates, flow diagrams, and allows export to **Excel** and **PDF**.

---

## Recommended Stack

### Frontend
- **React + TypeScript + Vite**
- **TanStack Query** for server-state and caching
- **TanStack Table** for advanced data tables
- **Apache ECharts** for charts and dashboard visuals
- **React Flow** for fluxograms / process diagrams

### Backend
- **Python 3.12**
- **FastAPI**
- **Pydantic-style schemas** for typed APIs
- **Pandas** only for batch transforms and ETL where needed

### Database / Platform
- **Supabase**
- **Postgres**
- **Supabase Auth**
- **Row Level Security (RLS)**
- **Views / Materialized Views** for analytics
- **Supabase Storage** for files and exports if needed

### Exports
- **Excel:** `XlsxWriter` or `openpyxl`
- **PDF:** `WeasyPrint`

### Future Desktop Path
After the web app is stable:
- **Tauri** for a lighter desktop wrapper
- **Electron** if deeper desktop/Node integrations are needed

---

## Best Language Strategy
Do **not** choose only one language.

Use this split:
- **TypeScript**: frontend screens, filters, charts, tables, UX
- **Python**: ETL, imports, exports, report generation, business rules
- **SQL**: analytics, joins, KPIs, averages, approval rates, aggregations

This is the cleanest architecture because your app needs:
- multiple data sources
- analytics and KPIs
- exports
- future scalability
- possible desktop packaging later

---

## Recommended Initial Architecture

### 1. Raw Ingestion Layer
Create separate raw tables for each source:
- `raw_gsus`
- `raw_sisaih01`
- `raw_datasus`

Keep original fields as intact as possible.

### 2. Canonical Normalized Layer
Create unified structures such as:
- `fact_attendances`
- `fact_procedures`
- `fact_approvals`
- `dim_hospital`
- `dim_professional`
- `dim_patient`
- `dim_date`
- `dim_source_system`

Each normalized record should include:
- `source_system = 'GSUS' | 'SISAIH01' | 'DATASUS'`

This is what allows the frontend to compare the 3 sources inside the same chart or table.

### 3. Analytics Layer
Create SQL views or materialized views like:
- `vw_kpi_approval_rate`
- `vw_kpi_avg_processing_time`
- `vw_kpi_volume_by_source`
- `vw_kpi_hospital_comparison`
- `vw_kpi_monthly_trend`

### 4. API Layer
Expose endpoints for:
- filters
- KPIs
- charts
- tables
- exports

Examples:
- `/kpis/overview`
- `/charts/approval-rate`
- `/tables/unified-records`
- `/exports/report.xlsx`
- `/exports/report.pdf`

### 5. Frontend Layer
Recommended pages:
- Overview dashboard
- Comparative dashboard
- Detailed table explorer
- Flow / process screen
- Export / report center
- Admin / refresh monitoring screen

---

## Real-Time Strategy
Do **not** make everything fully real-time from day one.

Recommended approach:
- raw data arrives
- Python job normalizes it
- analytics views/materialized views refresh
- frontend auto-refreshes or subscribes only to important changes

Good initial “real-time” targets:
- ingestion status
- refresh completion
- “new data available” indicator
- admin monitoring events

---

## Project Roadmap

### Phase 1 — Foundation
Define:
- the first KPIs
- data owners
- user roles
- filters
- refresh frequency
- business rules for approval rate, averages, comparisons

Start with a small KPI set, for example:
- total volume
- approval rate
- average value
- average time
- source comparison
- monthly evolution

### Phase 2 — Data Modeling
Design:
- raw tables
- normalized tables
- dimensions
- relationships
- source mapping rules

This is one of the most important phases of the project.

### Phase 3 — Ingestion
Build Python importers for:
- GSUS
- SISAIH01
- DATASUS

Each importer should:
- validate fields
- normalize dates
- normalize codes
- attach source metadata
- log errors
- be idempotent

### Phase 4 — Analytics MVP
Build the first functional dashboard with:
- 1 overview page
- 3 to 5 charts
- 1 advanced table
- basic filters:
  - date range
  - source
  - hospital
  - status
  - procedure / category

### Phase 5 — Exports
Add:
- Excel export from backend
- PDF export from backend
- export based on current dashboard filters

Do **not** rely only on browser-side exports for serious reporting.

### Phase 6 — Security and Access
Implement:
- Supabase Auth
- RLS
- roles / permissions
- restricted access to raw tables
- curated views or RPC/functions for consumers

### Phase 7 — Performance
As the app grows:
- move heavy logic into views/materialized views
- add indexes
- refresh aggregates by schedule
- paginate tables
- cache filter metadata
- profile slow endpoints

### Phase 8 — Desktop Evolution
Only after the web version is stable:
- package with **Tauri** or **Electron**
- keep the same frontend and backend logic as much as possible

---

## Best Initial Stack for This Project
If starting today, use:
- **Frontend:** React + TypeScript + Vite
- **Data UI:** TanStack Query + TanStack Table
- **Charts:** Apache ECharts
- **Flow diagrams:** React Flow
- **Backend:** FastAPI + Python 3.12
- **Database:** Supabase
- **Exports:** XlsxWriter + WeasyPrint
- **Testing:** Playwright

---

## Direct Recommendation
Start with:

**React + TypeScript + Vite + FastAPI + Supabase**

Avoid starting with:
- pure Python frontend
- desktop-first architecture
- full real-time everywhere
- all 3 sources at once in the first version

Build a clean analytics web app first, then evolve it.

---

## What To Do Now

### 1. Define the MVP
Decide the first:
- 10 KPIs
- 10 filters
- 3 to 5 screens
- user types
- refresh frequency

### 2. Choose the First Source
Do **not** start with GSUS + SISAIH01 + DATASUS all at once.

Start with **1 source only**, make the full flow work, then add the others.

### 3. Create the Project Skeleton
Suggested structure:

```text
/dashboard-project
  /frontend
  /backend
  /docs
  /sql
  /samples
```

### 4. Bootstrap the Stack
Start with:
- frontend: React + TypeScript + Vite
- backend: FastAPI
- database: Supabase

### 5. Build the First Vertical Slice
Your first working version should have:
- one imported data source
- one normalized table
- one KPI endpoint
- one dashboard page
- one chart
- one filtered table
- one Excel export
- one PDF export

### 6. Only After That, Add
- second source
- third source
- more KPIs
- more filters
- realtime refinements

---

## Strongest Recommendation
Before coding too much, define the:
- first 10 KPIs
- first 10 filters

These two lists will shape:
- database schema
- API routes
- dashboard screens
- chart design
- export structure

