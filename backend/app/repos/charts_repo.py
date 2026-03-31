from __future__ import annotations

from collections import defaultdict
from datetime import date
import re
import unicodedata

from dateutil.relativedelta import relativedelta

from ..db import pool
from ..schemas import Filters
from .sql_utils import build_where


def _month_key(d: date) -> str:
  return f"{d.year:04d}-{d.month:02d}"


async def get_monthly_volume(f: Filters) -> list[dict]:
  w = build_where(f, alias="e")
  q = f"""
    select
      date_trunc('month', e.event_date)::date as month_date,
      e.source_system,
      count(*)::int as total
    from public.fact_case_events e
    {w.sql}
    group by 1, 2
    order by 1 asc
  """

  rows = await pool().fetch(q, *w.args)
  if not rows:
    return []

  min_d = min(r["month_date"] for r in rows)
  max_d = max(r["month_date"] for r in rows)
  min_m = date(min_d.year, min_d.month, 1)
  max_m = date(max_d.year, max_d.month, 1)

  totals: dict[str, int] = defaultdict(int)
  by_source: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

  for r in rows:
    k = _month_key(r["month_date"])
    totals[k] += int(r["total"])
    by_source[k][r["source_system"]] += int(r["total"])

  points = []
  cur = min_m
  while cur <= max_m:
    k = _month_key(cur)
    points.append(
      {
        "month": k,
        "total": int(totals.get(k, 0)),
        "by_source": dict(sorted(by_source.get(k, {}).items(), key=lambda kv: kv[0])),
      }
    )
    cur = (cur + relativedelta(months=1))
  return points


def _status_order_key(status: str) -> tuple[int, str]:
  s = status.strip().lower()
  s = unicodedata.normalize("NFKD", s)
  s = "".join(ch for ch in s if not unicodedata.combining(ch))
  s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
  order = [
    "autorizado",
    "apresentado",
    "nao_apresentado",
    "rejeitado",
    "cancelado",
    "reapresentado",
  ]
  try:
    return (order.index(s), s)
  except ValueError:
    return (999, s)


async def get_status_by_source(f: Filters) -> list[dict]:
  w = build_where(f, alias="e")
  q = f"""
    select
      e.status,
      e.source_system,
      count(*)::int as total
    from public.fact_case_events e
    {w.sql}
    group by 1, 2
  """

  rows = await pool().fetch(q, *w.args)
  if not rows:
    return []

  by_status: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
  totals: dict[str, int] = defaultdict(int)
  for r in rows:
    st = r["status"]
    src = r["source_system"]
    cnt = int(r["total"])
    by_status[st][src] += cnt
    totals[st] += cnt

  points = []
  for st in sorted(by_status.keys(), key=_status_order_key):
    points.append(
      {
        "status": st,
        "total": int(totals.get(st, 0)),
        "by_source": dict(sorted(by_status[st].items(), key=lambda kv: kv[0])),
      }
    )
  return points
