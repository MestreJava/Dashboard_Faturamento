import { Download } from "lucide-react";

import { Card, CardContent, CardHeader } from "@/components/Card";
import { apiUrl, filtersToQuery } from "@/api/client";
import type { Filters } from "@/api/types";

function ExportButton(props: { label: string; href: string }) {
  return (
    <a
      className="inline-flex items-center justify-center gap-2 rounded-lg bg-zinc-900 px-3 py-2 text-sm font-medium text-white hover:bg-zinc-800"
      href={props.href}
    >
      <Download className="h-4 w-4" />
      {props.label}
    </a>
  );
}

export default function ExportButtons(props: { filters: Filters }) {
  const qp = filtersToQuery(props.filters);
  const xlsx = apiUrl(`/exports/report.xlsx?${qp.toString()}`);
  const pdf = apiUrl(`/exports/report.pdf?${qp.toString()}`);

  return (
    <Card>
      <CardHeader>
        <div className="text-sm font-semibold text-zinc-900">Exports</div>
        <div className="mt-1 text-xs text-zinc-500">Downloads reflect the current filters</div>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col gap-2">
          <ExportButton label="Download Excel" href={xlsx} />
          <ExportButton label="Download PDF" href={pdf} />
        </div>
      </CardContent>
    </Card>
  );
}

