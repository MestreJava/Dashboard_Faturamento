# Dashboard Faturamento — Page Design (MVP)

## Overview Dashboard

### Layout
- Header: app title + environment badge
- Filter bar (sticky)
  - Date range (from/to)
  - Source, Hospital, Status, Procedure category dropdowns
  - Reset button
- KPI grid (4–6 cards)
- Main content (two columns on desktop)
  - Left: Monthly Volume chart
  - Right: Exports + quick stats
- Table section
  - Paginated unified records table

### UX Notes
- Loading states:
  - Skeletons for KPI cards and chart
  - Table shows loading overlay
- Errors:
  - Inline alert with retry button
- Exports:
  - One-click download; includes applied filters

### Responsive
- Mobile:
  - Filters stack vertically
  - KPI cards in 2 columns
  - Chart above table

