import type { Filters } from "@/api/types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8002";

export function apiUrl(path: string): string {
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${API_BASE_URL}${path.startsWith("/") ? "" : "/"}${path}`;
}

export function filtersToQuery(filters: Filters): URLSearchParams {
  const p = new URLSearchParams();
  if (filters.dateFrom) p.set("date_from", filters.dateFrom);
  if (filters.dateTo) p.set("date_to", filters.dateTo);
  if (filters.sourceSystem) p.set("source_system", filters.sourceSystem);
  if (filters.hospital) p.set("hospital", filters.hospital);
  if (filters.status) p.set("status", filters.status);
  if (filters.procedureCategory) p.set("procedure_category", filters.procedureCategory);
  return p;
}

export async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(apiUrl(path), {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `Request failed: ${res.status}`);
  }
  return (await res.json()) as T;
}

