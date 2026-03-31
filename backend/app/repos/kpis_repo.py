from __future__ import annotations

from typing import Any

from ..db import pool
from ..schemas import Filters
from .sql_utils import build_where


async def get_overview_kpis(f: Filters) -> dict[str, Any]:
  w = build_where(f, alias="b")
  q = f"""
    with base as (
      select
        b.source_system,
        b.approved,
        b.value,
        b.processing_days
      from public.fact_case_events b
      {w.sql}
    ),
    by_source as (
      select source_system, count(*)::int as cnt
      from base
      group by 1
    )
    select
      (select count(*)::int from base) as total_volume,
      (
        case
          when (select count(*) from base) = 0 then 0.0
          else (select coalesce(sum(case when approved then 1 else 0 end), 0)::float from base) / (select count(*)::float from base)
        end
      ) as approval_rate,
      coalesce((select avg(value)::float from base), 0.0) as avg_value,
      coalesce((select avg(processing_days)::float from base), 0.0) as avg_processing_days,
      coalesce((select jsonb_object_agg(source_system, cnt) from by_source), '{{}}'::jsonb) as volume_by_source
  """

  r = await pool().fetchrow(q, *w.args)
  if r is None:
    return {
      "total_volume": 0,
      "approval_rate": 0.0,
      "avg_value": 0.0,
      "avg_processing_days": 0.0,
      "volume_by_source": {},
    }

  return {
    "total_volume": int(r["total_volume"] or 0),
    "approval_rate": float(r["approval_rate"] or 0.0),
    "avg_value": float(r["avg_value"] or 0.0),
    "avg_processing_days": float(r["avg_processing_days"] or 0.0),
    "volume_by_source": dict(r["volume_by_source"] or {}),
  }

