from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Iterable

from dateutil.relativedelta import relativedelta

from .sample_data import Record
from .schemas import Filters


def apply_filters(rows: Iterable[Record], f: Filters) -> list[Record]:
  out: list[Record] = []
  for r in rows:
    if f.date_from is not None and r.date < f.date_from:
      continue
    if f.date_to is not None and r.date > f.date_to:
      continue
    if f.source_system is not None and r.source_system != f.source_system:
      continue
    if f.hospital is not None and r.hospital != f.hospital:
      continue
    if f.status is not None and r.status != f.status:
      continue
    if f.procedure_category is not None and r.procedure_category != f.procedure_category:
      continue
    out.append(r)
  return out


def get_metadata(rows: list[Record]):
  sources = sorted({r.source_system for r in rows})
  hospitals = sorted({r.hospital for r in rows})
  statuses = sorted({r.status for r in rows})
  procedures = sorted({r.procedure_category for r in rows})
  min_date = min(r.date for r in rows)
  max_date = max(r.date for r in rows)
  return sources, hospitals, statuses, procedures, min_date, max_date


def compute_overview_kpis(rows: list[Record]):
  total = len(rows)
  if total == 0:
    return {
      "total_volume": 0,
      "approval_rate": 0.0,
      "avg_value": 0.0,
      "avg_processing_days": 0.0,
      "volume_by_source": {},
    }

  approved_count = sum(1 for r in rows if r.approved)
  approval_rate = approved_count / total
  avg_value = sum(r.value for r in rows) / total
  avg_processing = sum(r.processing_days for r in rows) / total

  by_source: dict[str, int] = defaultdict(int)
  for r in rows:
    by_source[r.source_system] += 1

  return {
    "total_volume": total,
    "approval_rate": approval_rate,
    "avg_value": avg_value,
    "avg_processing_days": avg_processing,
    "volume_by_source": dict(sorted(by_source.items(), key=lambda kv: kv[0])),
  }


def _month_key(d: date) -> str:
  return f"{d.year:04d}-{d.month:02d}"


def monthly_volume(rows: list[Record], start: date | None, end: date | None):
  if not rows:
    return []

  min_d = min(r.date for r in rows) if start is None else start
  max_d = max(r.date for r in rows) if end is None else end
  min_m = date(min_d.year, min_d.month, 1)
  max_m = date(max_d.year, max_d.month, 1)

  totals: dict[str, int] = defaultdict(int)
  by_source: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

  for r in rows:
    k = _month_key(r.date)
    totals[k] += 1
    by_source[k][r.source_system] += 1

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

