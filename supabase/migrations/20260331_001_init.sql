create extension if not exists pgcrypto;

create table if not exists public.raw_gsus (
  id uuid primary key default gen_random_uuid(),
  imported_at timestamptz not null default now(),
  source_filename text,
  row_number integer,
  import_hash text not null,
  aih text,
  event_date date,
  status text,
  hospital_name text,
  procedure_category text,
  approved boolean,
  value numeric(14,2),
  processing_days integer,
  raw jsonb not null
);

create unique index if not exists raw_gsus_import_hash_ux on public.raw_gsus (import_hash);

create table if not exists public.fact_case_events (
  id uuid primary key default gen_random_uuid(),
  aih text not null,
  source_system text not null,
  status text not null,
  event_date date not null,
  hospital_name text,
  procedure_category text,
  approved boolean,
  value numeric(14,2),
  processing_days integer,
  raw_import_hash text,
  created_at timestamptz not null default now(),
  constraint fact_case_events_source_system_ck check (source_system in ('GSUS', 'SISAIH01', 'DATASUS'))
);

create unique index if not exists fact_case_events_ux on public.fact_case_events (source_system, aih, status, event_date);
create index if not exists fact_case_events_event_date_ix on public.fact_case_events (event_date);
create index if not exists fact_case_events_source_ix on public.fact_case_events (source_system);
create index if not exists fact_case_events_status_ix on public.fact_case_events (status);
create index if not exists fact_case_events_hospital_ix on public.fact_case_events (hospital_name);
create index if not exists fact_case_events_procedure_ix on public.fact_case_events (procedure_category);
create index if not exists fact_case_events_aih_ix on public.fact_case_events (aih);

create table if not exists public.dim_hospital (
  id bigserial primary key,
  name text not null unique,
  created_at timestamptz not null default now()
);

create table if not exists public.dim_sigtap_procedure (
  code text primary key,
  name text,
  group_code text,
  group_name text,
  sub_group_code text,
  sub_group_name text,
  created_at timestamptz not null default now()
);

