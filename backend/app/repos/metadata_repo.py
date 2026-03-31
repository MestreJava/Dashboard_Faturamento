from __future__ import annotations

from datetime import date
from typing import Any

from ..db import pool
from ..schemas import SourceSystem


async def get_filter_metadata() -> tuple[list[SourceSystem], list[str], list[str], list[str], date, date]:
  q = """
    select
      array_agg(distinct f.source_system order by f.source_system) as sources,
      array_agg(distinct f.hospital_name order by f.hospital_name)
        filter (where f.hospital_name is not null and f.hospital_name <> '') as hospitals,
      array_agg(distinct f.status order by f.status) as statuses,
      array_agg(distinct f.procedure_category order by f.procedure_category)
        filter (where f.procedure_category is not null and f.procedure_category <> '') as procedures,
      min(f.event_date) as min_date,
      max(f.event_date) as max_date
    from public.fact_case_events f
  """

  r = await pool().fetchrow(q)
  if r is None or r["min_date"] is None or r["max_date"] is None:
    today = date.today()
    return ([], [], [], [], today, today)

  sources = [s for s in (r["sources"] or [])]
  hospitals = [h for h in (r["hospitals"] or [])]
  statuses = [s for s in (r["statuses"] or [])]
  procedures = [p for p in (r["procedures"] or [])]
  return (sources, hospitals, statuses, procedures, r["min_date"], r["max_date"])

