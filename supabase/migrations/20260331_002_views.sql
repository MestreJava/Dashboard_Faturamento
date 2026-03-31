create or replace view public.vw_filters_metadata as
select
  coalesce(
    (select jsonb_agg(distinct f.source_system order by f.source_system) from public.fact_case_events f),
    '[]'::jsonb
  ) as sources,
  coalesce(
    (select jsonb_agg(distinct f.hospital_name order by f.hospital_name) from public.fact_case_events f where f.hospital_name is not null and f.hospital_name <> ''),
    '[]'::jsonb
  ) as hospitals,
  coalesce(
    (select jsonb_agg(distinct f.status order by f.status) from public.fact_case_events f),
    '[]'::jsonb
  ) as statuses,
  coalesce(
    (select jsonb_agg(distinct f.procedure_category order by f.procedure_category) from public.fact_case_events f where f.procedure_category is not null and f.procedure_category <> ''),
    '[]'::jsonb
  ) as procedure_categories,
  (select min(f.event_date) from public.fact_case_events f) as min_date,
  (select max(f.event_date) from public.fact_case_events f) as max_date;

create or replace view public.vw_status_by_source as
select
  f.status,
  f.source_system,
  count(*)::int as total
from public.fact_case_events f
group by f.status, f.source_system;

create or replace view public.vw_monthly_volume as
select
  to_char(date_trunc('month', f.event_date)::date, 'YYYY-MM') as month,
  f.source_system,
  count(*)::int as total
from public.fact_case_events f
group by 1, 2;

