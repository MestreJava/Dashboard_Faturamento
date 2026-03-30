import ReactECharts from "echarts-for-react";

import { Card, CardContent, CardHeader } from "@/components/Card";
import ErrorState from "@/components/ErrorState";
import { useMonthlyVolume } from "@/api/hooks";
import type { Filters } from "@/api/types";

export default function MonthlyVolumeChart(props: { filters: Filters }) {
  const q = useMonthlyVolume(props.filters);

  if (q.isError) {
    return <ErrorState title="Failed to load chart" details={String(q.error)} onRetry={() => q.refetch()} />;
  }

  const points = q.data?.points ?? [];
  const months = points.map((p) => p.month);
  const totals = points.map((p) => p.total);

  const option = {
    grid: { left: 32, right: 16, top: 20, bottom: 28 },
    tooltip: { trigger: "axis" },
    xAxis: { type: "category", data: months, axisLabel: { color: "#52525b" } },
    yAxis: { type: "value", axisLabel: { color: "#52525b" } },
    series: [
      {
        name: "Volume",
        type: "bar",
        data: totals,
        itemStyle: { color: "#18181b" },
      },
    ],
  };

  return (
    <Card>
      <CardHeader>
        <div className="text-sm font-semibold text-zinc-900">Monthly Volume</div>
        <div className="mt-1 text-xs text-zinc-500">Counts grouped by month</div>
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

