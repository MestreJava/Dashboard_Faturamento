import ReactECharts from "echarts-for-react";

import { Card, CardContent, CardHeader } from "@/components/Card";
import ErrorState from "@/components/ErrorState";
import { useStatusBySource } from "@/api/hooks";
import type { Filters, SourceSystem } from "@/api/types";

const SOURCES: SourceSystem[] = ["GSUS", "SISAIH01", "DATASUS"];

export default function StatusBySourceChart(props: { filters: Filters }) {
  const q = useStatusBySource(props.filters);

  if (q.isError) {
    return <ErrorState title="Failed to load chart" details={String(q.error)} onRetry={() => q.refetch()} />;
  }

  const points = q.data?.points ?? [];
  const statuses = points.map((p) => p.status);

  const series = SOURCES.map((src) => ({
    name: src,
    type: "bar",
    stack: "total",
    emphasis: { focus: "series" },
    data: points.map((p) => p.by_source[src] ?? 0),
  }));

  const option = {
    grid: { left: 32, right: 16, top: 20, bottom: 90 },
    tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
    legend: { bottom: 8 },
    xAxis: { type: "category", data: statuses, axisLabel: { color: "#52525b", rotate: 30 } },
    yAxis: { type: "value", axisLabel: { color: "#52525b" } },
    series,
  };

  return (
    <Card>
      <CardHeader>
        <div className="text-sm font-semibold text-zinc-900">Status by Source</div>
        <div className="mt-1 text-xs text-zinc-500">Compare GSUS / SISAIH01 / DATASUS by status</div>
      </CardHeader>
      <CardContent>
        {q.isLoading ? (
          <div className="h-[280px] animate-pulse rounded-lg bg-zinc-100" />
        ) : (
          <div className="h-[280px]">
            <ReactECharts option={option} style={{ height: "100%", width: "100%" }} />
          </div>
        )}
      </CardContent>
    </Card>
  );
}

