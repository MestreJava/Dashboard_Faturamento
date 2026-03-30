import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { apiGet, filtersToQuery } from "@/api/client";
import type { FilterMetadata, Filters, MonthlyVolumeSeries, OverviewKpis, PagedUnifiedRecords } from "@/api/types";

export function useFilterMetadata() {
  return useQuery<FilterMetadata, Error>({
    queryKey: ["filters-metadata"],
    queryFn: () => apiGet<FilterMetadata>("/filters/metadata"),
    staleTime: 5 * 60 * 1000,
  });
}

export function useOverviewKpis(filters: Filters) {
  const qp = filtersToQuery(filters);
  return useQuery<OverviewKpis, Error>({
    queryKey: ["kpis-overview", Object.fromEntries(qp.entries())],
    queryFn: () => apiGet<OverviewKpis>(`/kpis/overview?${qp.toString()}`),
  });
}

export function useMonthlyVolume(filters: Filters) {
  const qp = filtersToQuery(filters);
  return useQuery<MonthlyVolumeSeries, Error>({
    queryKey: ["chart-monthly-volume", Object.fromEntries(qp.entries())],
    queryFn: () => apiGet<MonthlyVolumeSeries>(`/charts/monthly-volume?${qp.toString()}`),
  });
}

export function useUnifiedRecords(filters: Filters, page: number, pageSize: number) {
  const qp = filtersToQuery(filters);
  qp.set("page", String(page));
  qp.set("page_size", String(pageSize));
  return useQuery<PagedUnifiedRecords, Error>({
    queryKey: ["table-unified-records", page, pageSize, Object.fromEntries(qp.entries())],
    queryFn: () => apiGet<PagedUnifiedRecords>(`/tables/unified-records?${qp.toString()}`),
    placeholderData: keepPreviousData,
  });
}

