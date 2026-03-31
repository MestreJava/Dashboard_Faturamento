from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


SourceSystem = Literal["GSUS", "SISAIH01", "DATASUS"]


class Filters(BaseModel):
  date_from: date | None = None
  date_to: date | None = None
  source_system: SourceSystem | None = None
  hospital: str | None = None
  status: str | None = None
  procedure_category: str | None = None


class FilterMetadata(BaseModel):
  sources: list[SourceSystem]
  hospitals: list[str]
  statuses: list[str]
  procedure_categories: list[str]
  min_date: date
  max_date: date


class OverviewKpis(BaseModel):
  total_volume: int = Field(ge=0)
  approval_rate: float = Field(ge=0, le=1)
  avg_value: float = Field(ge=0)
  avg_processing_days: float = Field(ge=0)
  volume_by_source: dict[str, int]


class MonthlyPoint(BaseModel):
  month: str
  total: int = Field(ge=0)
  by_source: dict[str, int]


class MonthlyVolumeSeries(BaseModel):
  points: list[MonthlyPoint]


class StatusBySourcePoint(BaseModel):
  status: str
  total: int = Field(ge=0)
  by_source: dict[str, int]


class StatusBySourceSeries(BaseModel):
  points: list[StatusBySourcePoint]


class UnifiedRecord(BaseModel):
  id: str
  date: date
  source_system: SourceSystem
  hospital: str
  status: str
  procedure_category: str
  approved: bool
  value: float
  processing_days: int


class PagedUnifiedRecords(BaseModel):
  page: int = Field(ge=1)
  page_size: int = Field(ge=1, le=200)
  total: int = Field(ge=0)
  rows: list[UnifiedRecord]

