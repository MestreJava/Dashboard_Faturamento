from __future__ import annotations

from ..db import pool
from ..sample_data import Record
from ..schemas import Filters
from .sql_utils import build_where


async def get_unified_records(f: Filters, page: int, page_size: int) -> tuple[int, list[Record]]:
  w = build_where(f, alias="r")
  count_q = f"select count(*)::int as total from public.fact_case_events r{w.sql}"
  total_row = await pool().fetchrow(count_q, *w.args)
  total = int(total_row["total"] if total_row else 0)

  offset = (page - 1) * page_size
  data_q = f"""
    select
      r.id::text as id,
      r.event_date as date,
      r.source_system,
      coalesce(r.hospital_name, '') as hospital,
      r.status,
      coalesce(r.procedure_category, '') as procedure_category,
      coalesce(r.approved, false) as approved,
      coalesce(r.value, 0.0) as value,
      coalesce(r.processing_days, 0) as processing_days
    from public.fact_case_events r
    {w.sql}
    order by r.event_date desc, r.id desc
    limit ${len(w.args) + 1} offset ${len(w.args) + 2}
  """

  rows = await pool().fetch(data_q, *w.args, page_size, offset)
  out = [
    Record(
      id=r["id"],
      date=r["date"],
      source_system=r["source_system"],
      hospital=r["hospital"],
      status=r["status"],
      procedure_category=r["procedure_category"],
      approved=bool(r["approved"]),
      value=float(r["value"]),
      processing_days=int(r["processing_days"]),
    )
    for r in rows
  ]
  return total, out


async def get_records_for_export(f: Filters, limit: int = 5000) -> list[Record]:
  w = build_where(f, alias="r")
  data_q = f"""
    select
      r.id::text as id,
      r.event_date as date,
      r.source_system,
      coalesce(r.hospital_name, '') as hospital,
      r.status,
      coalesce(r.procedure_category, '') as procedure_category,
      coalesce(r.approved, false) as approved,
      coalesce(r.value, 0.0) as value,
      coalesce(r.processing_days, 0) as processing_days
    from public.fact_case_events r
    {w.sql}
    order by r.event_date desc, r.id desc
    limit ${len(w.args) + 1}
  """

  rows = await pool().fetch(data_q, *w.args, limit)
  return [
    Record(
      id=r["id"],
      date=r["date"],
      source_system=r["source_system"],
      hospital=r["hospital"],
      status=r["status"],
      procedure_category=r["procedure_category"],
      approved=bool(r["approved"]),
      value=float(r["value"]),
      processing_days=int(r["processing_days"]),
    )
    for r in rows
  ]
