from __future__ import annotations

from datetime import datetime
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from .exports import build_pdf, build_xlsx
from .logic import apply_filters, compute_overview_kpis, get_metadata, monthly_volume
from .sample_data import make_sample_records
from .schemas import FilterMetadata, Filters, MonthlyVolumeSeries, OverviewKpis, PagedUnifiedRecords, UnifiedRecord


app = FastAPI(title="Dashboard Faturamento API", version="0.1.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5182", "http://127.0.0.1:5182"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


DATA = make_sample_records(900)


@app.get("/health")
def health():
  return {"ok": True, "time": datetime.now().isoformat(timespec="seconds")}


def _filters(
  date_from: str | None = None,
  date_to: str | None = None,
  source_system: str | None = None,
  hospital: str | None = None,
  status: str | None = None,
  procedure_category: str | None = None,
) -> Filters:
  df = datetime.fromisoformat(date_from).date() if date_from else None
  dt = datetime.fromisoformat(date_to).date() if date_to else None
  return Filters(
    date_from=df,
    date_to=dt,
    source_system=source_system, 
    hospital=hospital,
    status=status,
    procedure_category=procedure_category,
  )


@app.get("/filters/metadata", response_model=FilterMetadata)
def filters_metadata():
  sources, hospitals, statuses, procedures, min_date, max_date = get_metadata(DATA)
  return {
    "sources": sources,
    "hospitals": hospitals,
    "statuses": statuses,
    "procedure_categories": procedures,
    "min_date": min_date,
    "max_date": max_date,
  }


@app.get("/kpis/overview", response_model=OverviewKpis)
def kpis_overview(
  date_from: str | None = None,
  date_to: str | None = None,
  source_system: str | None = None,
  hospital: str | None = None,
  status: str | None = None,
  procedure_category: str | None = None,
):
  f = _filters(date_from, date_to, source_system, hospital, status, procedure_category)
  rows = apply_filters(DATA, f)
  return compute_overview_kpis(rows)


@app.get("/charts/monthly-volume", response_model=MonthlyVolumeSeries)
def chart_monthly_volume(
  date_from: str | None = None,
  date_to: str | None = None,
  source_system: str | None = None,
  hospital: str | None = None,
  status: str | None = None,
  procedure_category: str | None = None,
):
  f = _filters(date_from, date_to, source_system, hospital, status, procedure_category)
  rows = apply_filters(DATA, f)
  points = monthly_volume(rows, f.date_from, f.date_to)
  return {"points": points}


@app.get("/tables/unified-records", response_model=PagedUnifiedRecords)
def table_unified_records(
  page: int = Query(1, ge=1),
  page_size: int = Query(25, ge=1, le=200),
  date_from: str | None = None,
  date_to: str | None = None,
  source_system: str | None = None,
  hospital: str | None = None,
  status: str | None = None,
  procedure_category: str | None = None,
):
  f = _filters(date_from, date_to, source_system, hospital, status, procedure_category)
  rows = apply_filters(DATA, f)
  rows.sort(key=lambda r: (r.date, r.id), reverse=True)
  total = len(rows)
  start = (page - 1) * page_size
  end = start + page_size
  sliced = rows[start:end]
  out_rows: list[UnifiedRecord] = [
    UnifiedRecord(
      id=r.id,
      date=r.date,
      source_system=r.source_system,
      hospital=r.hospital,
      status=r.status,
      procedure_category=r.procedure_category,
      approved=r.approved,
      value=r.value,
      processing_days=r.processing_days,
    )
    for r in sliced
  ]
  return {"page": page, "page_size": page_size, "total": total, "rows": out_rows}


@app.get("/exports/report.xlsx")
def export_xlsx(
  date_from: str | None = None,
  date_to: str | None = None,
  source_system: str | None = None,
  hospital: str | None = None,
  status: str | None = None,
  procedure_category: str | None = None,
):
  f = _filters(date_from, date_to, source_system, hospital, status, procedure_category)
  rows = apply_filters(DATA, f)
  rows.sort(key=lambda r: (r.date, r.id), reverse=True)
  blob = build_xlsx(rows, f)
  return Response(
    content=blob,
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    headers={"Content-Disposition": "attachment; filename=dashboard_report.xlsx"},
  )


@app.get("/exports/report.pdf")
def export_pdf(
  date_from: str | None = None,
  date_to: str | None = None,
  source_system: str | None = None,
  hospital: str | None = None,
  status: str | None = None,
  procedure_category: str | None = None,
):
  f = _filters(date_from, date_to, source_system, hospital, status, procedure_category)
  rows = apply_filters(DATA, f)
  rows.sort(key=lambda r: (r.date, r.id), reverse=True)
  blob = build_pdf(rows, f)
  return Response(
    content=blob,
    media_type="application/pdf",
    headers={"Content-Disposition": "attachment; filename=dashboard_report.pdf"},
  )

