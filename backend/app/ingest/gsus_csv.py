from __future__ import annotations

import csv
from datetime import date, datetime
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from ..db import pool


def _norm(s: str) -> str:
  s = s.strip().lower()
  s = unicodedata.normalize("NFKD", s)
  s = "".join(ch for ch in s if not unicodedata.combining(ch))
  s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
  return s


def _parse_date(s: str) -> date:
  s = s.strip()
  for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y%m%d"):
    try:
      return datetime.strptime(s, fmt).date()
    except ValueError:
      pass
  return datetime.fromisoformat(s).date()


def _parse_float(s: str | None) -> float | None:
  if s is None:
    return None
  t = s.strip()
  if t == "":
    return None
  t = t.replace(".", "").replace(",", ".") if t.count(",") == 1 and t.count(".") >= 1 else t.replace(",", ".")
  try:
    return float(t)
  except ValueError:
    return None


def _parse_int(s: str | None) -> int | None:
  if s is None:
    return None
  t = s.strip()
  if t == "":
    return None
  try:
    return int(float(t.replace(",", ".")))
  except ValueError:
    return None


def _detect_columns(headers: list[str]) -> dict[str, str]:
  hmap = {_norm(h): h for h in headers}

  def pick(candidates: list[str]) -> str | None:
    for c in candidates:
      k = _norm(c)
      if k in hmap:
        return hmap[k]
    return None

  col_aih = pick(["aih", "num_aih", "numero_aih", "n_aih", "aih_numero"])
  col_status = pick(["status", "situacao", "situacao_aih", "status_aih", "sit_aih"])
  col_date = pick(["event_date", "data", "data_evento", "data_atendimento", "data_internacao", "dt_evento", "dt"])
  col_hospital = pick(["hospital", "nome_hospital", "estabelecimento", "unidade", "hospital_nome"])
  col_proc = pick(["procedure_category", "procedimento", "procedimento_categoria", "categoria_proced", "procedimento_grupo"])
  col_value = pick(["value", "valor", "valor_total", "vl_total", "vlr_total"])
  col_processing = pick(["processing_days", "dias_processamento", "dias", "prazo_dias"])

  if col_aih is None:
    raise ValueError("GSUS CSV is missing an AIH column")
  if col_status is None:
    raise ValueError("GSUS CSV is missing a status/situacao column")
  if col_date is None:
    raise ValueError("GSUS CSV is missing a date column")

  return {
    "aih": col_aih,
    "status": col_status,
    "event_date": col_date,
    "hospital_name": col_hospital or "",
    "procedure_category": col_proc or "",
    "value": col_value or "",
    "processing_days": col_processing or "",
  }


def _approved_from_status(status: str) -> bool | None:
  s = _norm(status)
  if s in {"autorizado", "aprovado"}:
    return True
  if s in {"rejeitado", "cancelado", "nao_apresentado", "não_apresentado"}:
    return False
  return None


def _hash_row(raw: dict[str, Any]) -> str:
  blob = json.dumps(raw, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
  return hashlib.sha256(blob).hexdigest()


async def ingest_gsus_csv(csv_path: str, source_filename: str | None = None) -> dict[str, int]:
  p = Path(csv_path)
  if not p.exists():
    raise FileNotFoundError(str(p))

  inserted_raw = 0
  upserted_events = 0

  with p.open("r", encoding="utf-8-sig", newline="", errors="replace") as f:
    reader = csv.DictReader(f)
    if reader.fieldnames is None:
      raise ValueError("CSV has no header row")
    cols = _detect_columns(reader.fieldnames)

    async with pool().acquire() as conn:
      async with conn.transaction():
        for i, row in enumerate(reader, start=2):
          raw = {k: (v if v is not None else "") for k, v in row.items()}
          aih = (row.get(cols["aih"]) or "").strip()
          status = (row.get(cols["status"]) or "").strip()
          d = _parse_date(row.get(cols["event_date"]) or "")
          hospital_name = (row.get(cols["hospital_name"]) or "").strip() if cols["hospital_name"] else ""
          procedure_category = (row.get(cols["procedure_category"]) or "").strip() if cols["procedure_category"] else ""
          approved = _approved_from_status(status)
          value = _parse_float(row.get(cols["value"])) if cols["value"] else None
          processing_days = _parse_int(row.get(cols["processing_days"])) if cols["processing_days"] else None

          if aih == "" or status == "":
            continue

          import_hash = _hash_row(
            {
              "source": "GSUS",
              "aih": aih,
              "status": status,
              "event_date": d.isoformat(),
              "hospital_name": hospital_name,
              "procedure_category": procedure_category,
              "value": value,
              "processing_days": processing_days,
              "raw": raw,
            }
          )

          raw_ins = await conn.execute(
            """
              insert into public.raw_gsus (
                import_hash, source_filename, row_number, aih, event_date, status,
                hospital_name, procedure_category, approved, value, processing_days, raw
              )
              values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12::jsonb)
              on conflict (import_hash) do nothing
            """,
            import_hash,
            source_filename or p.name,
            i,
            aih,
            d,
            status,
            hospital_name if hospital_name != "" else None,
            procedure_category if procedure_category != "" else None,
            approved,
            value,
            processing_days,
            json.dumps(raw, ensure_ascii=False),
          )
          if raw_ins.endswith(" 1"):
            inserted_raw += 1

          ev_ins = await conn.execute(
            """
              insert into public.fact_case_events (
                aih, source_system, status, event_date, hospital_name, procedure_category,
                approved, value, processing_days, raw_import_hash
              )
              values ($1,'GSUS',$2,$3,$4,$5,$6,$7,$8,$9)
              on conflict (source_system, aih, status, event_date) do update set
                hospital_name = excluded.hospital_name,
                procedure_category = excluded.procedure_category,
                approved = excluded.approved,
                value = excluded.value,
                processing_days = excluded.processing_days,
                raw_import_hash = excluded.raw_import_hash
            """,
            aih,
            status,
            d,
            hospital_name if hospital_name != "" else None,
            procedure_category if procedure_category != "" else None,
            approved,
            value,
            processing_days,
            import_hash,
          )
          if ev_ins.startswith("INSERT") or ev_ins.startswith("UPDATE"):
            upserted_events += 1

  return {"raw_inserted": inserted_raw, "events_upserted": upserted_events}

