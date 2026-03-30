from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
import random
from typing import Literal

SourceSystem = Literal["GSUS", "SISAIH01", "DATASUS"]


@dataclass(frozen=True)
class Record:
  id: str
  date: date
  source_system: SourceSystem
  hospital: str
  status: str
  procedure_category: str
  approved: bool
  value: float
  processing_days: int


def _month_start(d: date) -> date:
  return date(d.year, d.month, 1)


def _add_months(d: date, months: int) -> date:
  y = d.year + (d.month - 1 + months) // 12
  m = (d.month - 1 + months) % 12 + 1
  return date(y, m, 1)


def make_sample_records(n: int = 800) -> list[Record]:
  rnd = random.Random(42)
  sources: list[SourceSystem] = ["GSUS", "SISAIH01", "DATASUS"]
  hospitals = [
    "HOSPITAL CENTRAL",
    "HOSPITAL MUNICIPAL",
    "HOSPITAL REGIONAL",
    "UPA NORTE",
    "UPA SUL",
  ]
  statuses = ["SUBMITTED", "IN_REVIEW", "APPROVED", "REJECTED"]
  procedures = ["CLINICAL", "SURGICAL", "DIAGNOSTIC", "THERAPY", "EMERGENCY"]

  today = date.today()
  start = _add_months(_month_start(today), -24)
  end = today
  days_range = (end - start).days

  rows: list[Record] = []
  for i in range(n):
    d = start + timedelta(days=rnd.randint(0, max(days_range, 1)))
    source = rnd.choices(sources, weights=[0.6, 0.25, 0.15], k=1)[0]
    hospital = rnd.choice(hospitals)
    procedure = rnd.choice(procedures)
    status = rnd.choices(statuses, weights=[0.25, 0.25, 0.35, 0.15], k=1)[0]
    approved = status == "APPROVED" or (status == "IN_REVIEW" and rnd.random() < 0.15)
    base_value = {
      "CLINICAL": 180.0,
      "SURGICAL": 1100.0,
      "DIAGNOSTIC": 240.0,
      "THERAPY": 320.0,
      "EMERGENCY": 260.0,
    }[procedure]
    value = max(10.0, rnd.gauss(base_value, base_value * 0.35))
    processing_days = max(0, int(rnd.gauss(7.5 if approved else 10.5, 3.5)))
    rid = f"R{i+1:05d}"
    rows.append(
      Record(
        id=rid,
        date=d,
        source_system=source,
        hospital=hospital,
        status=status,
        procedure_category=procedure,
        approved=approved,
        value=round(value, 2),
        processing_days=processing_days,
      )
    )

  return rows

