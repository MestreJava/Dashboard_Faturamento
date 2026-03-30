from __future__ import annotations

from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
import xlsxwriter

from .sample_data import Record
from .schemas import Filters


def build_xlsx(rows: list[Record], f: Filters) -> bytes:
  buf = BytesIO()
  wb = xlsxwriter.Workbook(buf, {"in_memory": True})
  ws = wb.add_worksheet("records")
  meta = wb.add_worksheet("filters")

  header_fmt = wb.add_format({"bold": True, "bg_color": "#F4F4F5"})
  money_fmt = wb.add_format({"num_format": "#,##0.00"})

  headers = [
    "id",
    "date",
    "source_system",
    "hospital",
    "status",
    "procedure_category",
    "approved",
    "value",
    "processing_days",
  ]
  for c, h in enumerate(headers):
    ws.write(0, c, h, header_fmt)

  for i, r in enumerate(rows, start=1):
    ws.write(i, 0, r.id)
    ws.write(i, 1, r.date.isoformat())
    ws.write(i, 2, r.source_system)
    ws.write(i, 3, r.hospital)
    ws.write(i, 4, r.status)
    ws.write(i, 5, r.procedure_category)
    ws.write(i, 6, "YES" if r.approved else "NO")
    ws.write_number(i, 7, float(r.value), money_fmt)
    ws.write_number(i, 8, int(r.processing_days))

  ws.autofilter(0, 0, max(1, len(rows)), len(headers) - 1)
  ws.freeze_panes(1, 0)
  ws.set_column(0, 0, 10)
  ws.set_column(1, 1, 12)
  ws.set_column(2, 2, 12)
  ws.set_column(3, 3, 22)
  ws.set_column(4, 4, 12)
  ws.set_column(5, 5, 18)
  ws.set_column(6, 6, 10)
  ws.set_column(7, 7, 12)
  ws.set_column(8, 8, 16)

  meta.write(0, 0, "generated_at", header_fmt)
  meta.write(0, 1, datetime.now().isoformat(timespec="seconds"))
  meta_pairs = [
    ("date_from", f.date_from.isoformat() if f.date_from else ""),
    ("date_to", f.date_to.isoformat() if f.date_to else ""),
    ("source_system", f.source_system or ""),
    ("hospital", f.hospital or ""),
    ("status", f.status or ""),
    ("procedure_category", f.procedure_category or ""),
  ]
  for i, (k, v) in enumerate(meta_pairs, start=2):
    meta.write(i, 0, k, header_fmt)
    meta.write(i, 1, v)

  wb.close()
  return buf.getvalue()


def build_pdf(rows: list[Record], f: Filters) -> bytes:
  buf = BytesIO()
  c = Canvas(buf, pagesize=A4)
  w, h = A4

  title = "Dashboard Report"
  c.setFont("Helvetica-Bold", 14)
  c.drawString(2 * cm, h - 2 * cm, title)

  c.setFont("Helvetica", 9)
  filter_line = " | ".join(
    [
      f"date_from={f.date_from.isoformat() if f.date_from else ''}",
      f"date_to={f.date_to.isoformat() if f.date_to else ''}",
      f"source={f.source_system or ''}",
      f"hospital={f.hospital or ''}",
      f"status={f.status or ''}",
      f"procedure={f.procedure_category or ''}",
    ]
  )
  c.drawString(2 * cm, h - 2.7 * cm, filter_line)

  c.setFont("Helvetica", 10)
  c.drawString(2 * cm, h - 3.6 * cm, f"Rows: {len(rows)}")

  y = h - 4.6 * cm
  c.setFont("Helvetica-Bold", 9)
  cols = [
    ("date", 2.2 * cm),
    ("source", 2.2 * cm),
    ("hospital", 5.0 * cm),
    ("status", 2.4 * cm),
    ("proc", 2.6 * cm),
    ("appr", 1.6 * cm),
    ("value", 2.2 * cm),
  ]

  x = 2 * cm
  for name, width in cols:
    c.drawString(x, y, name)
    x += width
  y -= 0.45 * cm
  c.setFont("Helvetica", 9)

  max_rows = 45
  for r in rows[:max_rows]:
    if y < 2.2 * cm:
      c.showPage()
      c.setFont("Helvetica", 9)
      y = h - 2.0 * cm
    values = [
      r.date.isoformat(),
      r.source_system,
      r.hospital,
      r.status,
      r.procedure_category,
      "Y" if r.approved else "N",
      f"{r.value:.2f}",
    ]
    x = 2 * cm
    for (name, width), v in zip(cols, values):
      max_chars = max(1, int(width / stringWidth("M", "Helvetica", 9)))
      c.drawString(x, y, v[:max_chars])
      x += width
    y -= 0.42 * cm

  c.showPage()
  c.save()
  return buf.getvalue()

