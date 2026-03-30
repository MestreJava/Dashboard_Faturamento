import ExportButtons from "@/components/ExportButtons";
import FilterBar from "@/components/FilterBar";
import KpiCards from "@/components/KpiCards";
import MonthlyVolumeChart from "@/components/MonthlyVolumeChart";
import UnifiedRecordsTable from "@/components/UnifiedRecordsTable";
import { useFiltersStore } from "@/stores/filtersStore";

export default function Home() {
  const filters = useFiltersStore((s) => s.filters);

  return (
    <div className="min-h-screen bg-zinc-50">
      <div className="mx-auto max-w-7xl px-4 py-6">
        <div className="flex items-center justify-between gap-4">
          <div>
            <div className="text-lg font-semibold text-zinc-900">Dashboard Faturamento</div>
            <div className="mt-1 text-xs text-zinc-500">MVP overview with filters, KPIs, chart, table, and exports</div>
          </div>
          <div className="rounded-full border border-zinc-200 bg-white px-3 py-1 text-xs font-medium text-zinc-700">local</div>
        </div>

        <div className="mt-5">
          <FilterBar />
        </div>

        <div className="mt-4">
          <KpiCards filters={filters} />
        </div>

        <div className="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <MonthlyVolumeChart filters={filters} />
          </div>
          <div className="lg:col-span-1">
            <ExportButtons filters={filters} />
          </div>
        </div>

        <div className="mt-4">
          <UnifiedRecordsTable filters={filters} />
        </div>
      </div>
    </div>
  );
}
