import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export function Card(props: { className?: string; children: ReactNode }) {
  return <div className={cn("rounded-xl border border-zinc-200 bg-white shadow-sm", props.className)}>{props.children}</div>;
}

export function CardHeader(props: { className?: string; children: ReactNode }) {
  return <div className={cn("px-4 py-3 border-b border-zinc-100", props.className)}>{props.children}</div>;
}

export function CardContent(props: { className?: string; children: ReactNode }) {
  return <div className={cn("px-4 py-3", props.className)}>{props.children}</div>;
}

