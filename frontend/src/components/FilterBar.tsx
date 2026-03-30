import { RotateCcw } from "lucide-react";

import { Card } from "@/components/Card";
import ErrorState from "@/components/ErrorState";
import { useFilterMetadata } from "@/api/hooks";
import type { SourceSystem } from "@/api/types";
import { useFiltersStore } from "@/stores/filtersStore";

function SelectField(props: {
  label: string;
  value: string | null;
  options: string[];
  onChange: (v: string | null) => void;
}) {
  return (
    <label className="flex flex-col gap-1">
      <span className="text-xs font-medium text-zinc-600">{props.label}</span>
      <select
        className="h-9 rounded-lg border border-zinc-200 bg-white px-2 text-sm outline-none focus:ring-2 focus:ring-zinc-200"
        value={props.value ?? ""}
        onChange={(e) => props.onChange(e.target.value ? e.target.value : null)}
      >
        <option value="">All</option>
        {props.options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </label>
  );
}

export default function FilterBar() {
  const meta = useFilterMetadata();
  const {
    filters,
    setDateFrom,
    setDateTo,
    setSourceSystem,
    setHospital,
    setStatus,
    setProcedureCategory,
    reset,
  } = useFiltersStore();

  if (meta.isError) {
    return <ErrorState title="Failed to load filters" details={String(meta.error)} onRetry={() => meta.refetch()} />;
  }

  const sources = meta.data?.sources ?? [];
  const hospitals = meta.data?.hospitals ?? [];
  const statuses = meta.data?.statuses ?? [];
  const procedures = meta.data?.procedure_categories ?? [];

  return (
    <Card className="p-4">
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between gap-3">
          <div className="text-sm font-semibold text-zinc-900">Filters</div>
          <button
            type="button"
            onClick={() => reset()}
            className="inline-flex items-center gap-2 rounded-lg border border-zinc-200 bg-white px-3 py-2 text-xs font-medium hover:bg-zinc-50"
          >
            <RotateCcw className="h-4 w-4" />
            Reset
          </button>
        </div>

        <div className="grid grid-cols-1 gap-3 md:grid-cols-6">
          <label className="flex flex-col gap-1 md:col-span-1">
            <span className="text-xs font-medium text-zinc-600">From</span>
            <input
              type="date"
              className="h-9 rounded-lg border border-zinc-200 bg-white px-2 text-sm outline-none focus:ring-2 focus:ring-zinc-200"
              value={filters.dateFrom ?? ""}
              onChange={(e) => setDateFrom(e.target.value ? e.target.value : null)}
              min={meta.data?.min_date}
              max={meta.data?.max_date}
            />
          </label>
          <label className="flex flex-col gap-1 md:col-span-1">
            <span className="text-xs font-medium text-zinc-600">To</span>
            <input
              type="date"
              className="h-9 rounded-lg border border-zinc-200 bg-white px-2 text-sm outline-none focus:ring-2 focus:ring-zinc-200"
              value={filters.dateTo ?? ""}
              onChange={(e) => setDateTo(e.target.value ? e.target.value : null)}
              min={meta.data?.min_date}
              max={meta.data?.max_date}
            />
          </label>

          <div className="md:col-span-1">
            <SelectField
              label="Source"
              value={filters.sourceSystem}
              options={sources}
              onChange={(v) => setSourceSystem(v as SourceSystem | null)}
            />
          </div>
          <div className="md:col-span-1">
            <SelectField label="Hospital" value={filters.hospital} options={hospitals} onChange={setHospital} />
          </div>
          <div className="md:col-span-1">
            <SelectField label="Status" value={filters.status} options={statuses} onChange={setStatus} />
          </div>
          <div className="md:col-span-1">
            <SelectField
              label="Procedure"
              value={filters.procedureCategory}
              options={procedures}
              onChange={setProcedureCategory}
            />
          </div>
        </div>
      </div>
    </Card>
  );
}

