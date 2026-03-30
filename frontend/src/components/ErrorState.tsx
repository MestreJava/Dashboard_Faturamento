import { AlertTriangle, RotateCw } from "lucide-react";

import { cn } from "@/lib/utils";

export default function ErrorState(props: { title: string; details?: string; onRetry?: () => void; className?: string }) {
  return (
    <div className={cn("rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-900", props.className)}>
      <div className="flex items-start gap-3">
        <AlertTriangle className="mt-0.5 h-5 w-5" />
        <div className="min-w-0 flex-1">
          <div className="text-sm font-semibold">{props.title}</div>
          {props.details ? <div className="mt-1 text-xs text-red-800 break-words">{props.details}</div> : null}
        </div>
        {props.onRetry ? (
          <button
            type="button"
            onClick={props.onRetry}
            className="inline-flex items-center gap-2 rounded-lg border border-red-200 bg-white px-3 py-1.5 text-xs font-medium hover:bg-red-100"
          >
            <RotateCw className="h-4 w-4" />
            Retry
          </button>
        ) : null}
      </div>
    </div>
  );
}

