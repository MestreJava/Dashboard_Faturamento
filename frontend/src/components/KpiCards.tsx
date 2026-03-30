import { Card, CardContent, CardHeader } from "@/components/Card";
import ErrorState from "@/components/ErrorState";
import { useOverviewKpis } from "@/api/hooks";
import type { Filters } from "@/api/types";

function StatCard(props: { title: string; value: string; sub?: string }) {
  return (
    <Card>
      <CardHeader>
        <div className="text-xs font-medium text-zinc-600">{props.title}</div>
      </CardHeader>
      <CardContent>
        <div className="text-lg font-semibold text-zinc-900">{props.value}</div>
        {props.sub ? <div className="mt-1 text-xs text-zinc-500">{props.sub}</div> : null}
      </CardContent>
    </Card>
  );
}

export default function KpiCards(props: { filters: Filters }) {
  const q = useOverviewKpis(props.filters);

  if (q.isError) {
    return <ErrorState title="Failed to load KPIs" details={String(q.error)} onRetry={() => q.refetch()} />;
  }

  if (q.isLoading || !q.data) {
    return (
      <div className="grid grid-cols-1 gap-3 md:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-[88px] animate-pulse rounded-xl border border-zinc-200 bg-white" />
        ))}
      </div>
    );
  }

  const d = q.data;
  const approvalPct = `${(d.approval_rate * 100).toFixed(1)}%`;
  const avgValue = d.avg_value.toLocaleString(undefined, { style: "currency", currency: "BRL" });
  const avgProcessing = `${d.avg_processing_days.toFixed(1)} days`;

  const bySource = Object.entries(d.volume_by_source)
    .map(([k, v]) => `${k}: ${v}`)
    .join(" | ");

  return (
    <div className="grid grid-cols-1 gap-3 md:grid-cols-4">
      <StatCard title="Total Volume" value={String(d.total_volume)} sub={bySource} />
      <StatCard title="Approval Rate" value={approvalPct} />
      <StatCard title="Average Value" value={avgValue} />
      <StatCard title="Avg Processing" value={avgProcessing} />
    </div>
  );
}

