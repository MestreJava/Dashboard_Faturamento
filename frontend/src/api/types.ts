export type SourceSystem = "GSUS" | "SISAIH01" | "DATASUS";

export type Filters = {
  dateFrom: string | null;
  dateTo: string | null;
  sourceSystem: SourceSystem | null;
  hospital: string | null;
  status: string | null;
  procedureCategory: string | null;
};

export type FilterMetadata = {
  sources: SourceSystem[];
  hospitals: string[];
  statuses: string[];
  procedure_categories: string[];
  min_date: string;
  max_date: string;
};

export type OverviewKpis = {
  total_volume: number;
  approval_rate: number;
  avg_value: number;
  avg_processing_days: number;
  volume_by_source: Record<string, number>;
};

export type MonthlyPoint = {
  month: string;
  total: number;
  by_source: Record<string, number>;
};

export type MonthlyVolumeSeries = {
  points: MonthlyPoint[];
};

export type StatusBySourcePoint = {
  status: string;
  total: number;
  by_source: Record<string, number>;
};

export type StatusBySourceSeries = {
  points: StatusBySourcePoint[];
};

export type UnifiedRecord = {
  id: string;
  date: string;
  source_system: SourceSystem;
  hospital: string;
  status: string;
  procedure_category: string;
  approved: boolean;
  value: number;
  processing_days: number;
};

export type PagedUnifiedRecords = {
  page: number;
  page_size: number;
  total: number;
  rows: UnifiedRecord[];
};

