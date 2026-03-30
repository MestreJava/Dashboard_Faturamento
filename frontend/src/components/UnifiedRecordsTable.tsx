import { useMemo, useState } from "react";
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { ChevronLeft, ChevronRight } from "lucide-react";

import { Card, CardContent, CardHeader } from "@/components/Card";
import ErrorState from "@/components/ErrorState";
import { useUnifiedRecords } from "@/api/hooks";
import type { Filters, UnifiedRecord } from "@/api/types";
import { cn } from "@/lib/utils";

export default function UnifiedRecordsTable(props: { filters: Filters }) {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);
  const q = useUnifiedRecords(props.filters, page, pageSize);

  const columns = useMemo<ColumnDef<UnifiedRecord>[]>(
    () => [
      { accessorKey: "date", header: "Date", cell: (c) => String(c.getValue()) },
      { accessorKey: "source_system", header: "Source" },
      { accessorKey: "hospital", header: "Hospital" },
      { accessorKey: "status", header: "Status" },
      { accessorKey: "procedure_category", header: "Procedure" },
      {
        accessorKey: "approved",
        header: "Approved",
        cell: (c) => ((c.getValue() as boolean) ? "Yes" : "No"),
      },
      {
        accessorKey: "value",
        header: "Value",
        cell: (c) =>
          Number(c.getValue()).toLocaleString(undefined, { style: "currency", currency: "BRL" }),
      },
      { accessorKey: "processing_days", header: "Days" },
    ],
    []
  );

  const data = q.data?.rows ?? [];
  const total = q.data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (q.isError) {
    return <ErrorState title="Failed to load table" details={String(q.error)} onRetry={() => q.refetch()} />;
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between gap-3">
          <div>
            <div className="text-sm font-semibold text-zinc-900">Unified Records</div>
            <div className="mt-1 text-xs text-zinc-500">{total.toLocaleString()} rows</div>
          </div>
          <div className="flex items-center gap-2">
            <select
              className="h-9 rounded-lg border border-zinc-200 bg-white px-2 text-sm outline-none focus:ring-2 focus:ring-zinc-200"
              value={pageSize}
              onChange={(e) => {
                setPageSize(Number(e.target.value));
                setPage(1);
              }}
            >
              {[10, 25, 50, 100].map((s) => (
                <option key={s} value={s}>
                  {s} / page
                </option>
              ))}
            </select>
            <button
              type="button"
              className="inline-flex h-9 items-center gap-2 rounded-lg border border-zinc-200 bg-white px-3 text-sm font-medium disabled:opacity-50"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1 || q.isFetching}
            >
              <ChevronLeft className="h-4 w-4" />
              Prev
            </button>
            <button
              type="button"
              className="inline-flex h-9 items-center gap-2 rounded-lg border border-zinc-200 bg-white px-3 text-sm font-medium disabled:opacity-50"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages || q.isFetching}
            >
              Next
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="relative overflow-hidden rounded-lg border border-zinc-200">
          <div className="max-h-[420px] overflow-auto">
            <table className="w-full border-collapse text-sm">
              <thead className="sticky top-0 bg-zinc-50">
                {table.getHeaderGroups().map((hg) => (
                  <tr key={hg.id}>
                    {hg.headers.map((h) => (
                      <th key={h.id} className="whitespace-nowrap border-b border-zinc-200 px-3 py-2 text-left text-xs font-semibold text-zinc-700">
                        {h.isPlaceholder ? null : flexRender(h.column.columnDef.header, h.getContext())}
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody>
                {table.getRowModel().rows.map((r) => (
                  <tr key={r.id} className="hover:bg-zinc-50">
                    {r.getVisibleCells().map((c) => (
                      <td key={c.id} className="whitespace-nowrap border-b border-zinc-100 px-3 py-2 text-zinc-800">
                        {flexRender(c.column.columnDef.cell, c.getContext())}
                      </td>
                    ))}
                  </tr>
                ))}
                {!q.isLoading && data.length === 0 ? (
                  <tr>
                    <td colSpan={columns.length} className="px-3 py-8 text-center text-sm text-zinc-500">
                      No results
                    </td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          </div>
          <div
            className={cn(
              "pointer-events-none absolute inset-0 bg-white/60 transition-opacity",
              q.isFetching ? "opacity-100" : "opacity-0"
            )}
          />
        </div>
        <div className="mt-3 flex items-center justify-between text-xs text-zinc-600">
          <div>
            Page {page} / {totalPages}
          </div>
          <div>
            Showing {(page - 1) * pageSize + 1}–{Math.min(page * pageSize, total)}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

