import { create } from "zustand";

import type { Filters, SourceSystem } from "@/api/types";

type FiltersState = {
  filters: Filters;
  setDateFrom: (v: string | null) => void;
  setDateTo: (v: string | null) => void;
  setSourceSystem: (v: SourceSystem | null) => void;
  setHospital: (v: string | null) => void;
  setStatus: (v: string | null) => void;
  setProcedureCategory: (v: string | null) => void;
  reset: () => void;
};

const initial: Filters = {
  dateFrom: null,
  dateTo: null,
  sourceSystem: null,
  hospital: null,
  status: null,
  procedureCategory: null,
};

export const useFiltersStore = create<FiltersState>((set) => ({
  filters: initial,
  setDateFrom: (v) => set((s) => ({ filters: { ...s.filters, dateFrom: v } })),
  setDateTo: (v) => set((s) => ({ filters: { ...s.filters, dateTo: v } })),
  setSourceSystem: (v) => set((s) => ({ filters: { ...s.filters, sourceSystem: v } })),
  setHospital: (v) => set((s) => ({ filters: { ...s.filters, hospital: v } })),
  setStatus: (v) => set((s) => ({ filters: { ...s.filters, status: v } })),
  setProcedureCategory: (v) => set((s) => ({ filters: { ...s.filters, procedureCategory: v } })),
  reset: () => set({ filters: initial }),
}));

