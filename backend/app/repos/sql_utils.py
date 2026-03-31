from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..schemas import Filters


@dataclass(frozen=True)
class SqlWhere:
  sql: str
  args: list[Any]


def build_where(f: Filters, alias: str = "f") -> SqlWhere:
  clauses: list[str] = []
  args: list[Any] = []

  def add(cond: str, value: Any) -> None:
    args.append(value)
    clauses.append(cond.replace("$", f"${len(args)}"))

  if f.date_from is not None:
    add(f"{alias}.event_date >= $", f.date_from)
  if f.date_to is not None:
    add(f"{alias}.event_date <= $", f.date_to)
  if f.source_system is not None:
    add(f"{alias}.source_system = $", f.source_system)
  if f.hospital is not None:
    add(f"{alias}.hospital_name = $", f.hospital)
  if f.status is not None:
    add(f"{alias}.status = $", f.status)
  if f.procedure_category is not None:
    add(f"{alias}.procedure_category = $", f.procedure_category)

  if not clauses:
    return SqlWhere(sql="", args=args)
  return SqlWhere(sql=" where " + " and ".join(clauses), args=args)

