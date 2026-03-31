from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv

from ..db import close_db, init_db
from .gsus_csv import ingest_gsus_csv


def _parser() -> argparse.ArgumentParser:
  p = argparse.ArgumentParser(prog="app.ingest")
  sub = p.add_subparsers(dest="cmd", required=True)

  gsus = sub.add_parser("gsus", help="Ingest GSUS CSV export")
  gsus.add_argument("--csv", required=True)
  gsus.add_argument("--filename", default=None)
  gsus.add_argument("--database-url", default=None)

  return p


async def _run(args: argparse.Namespace) -> int:
  if args.database_url:
    os.environ["DATABASE_URL"] = args.database_url

  await init_db(force=True)
  try:
    if args.cmd == "gsus":
      out = await ingest_gsus_csv(args.csv, source_filename=args.filename)
      print(out)
      return 0
    raise RuntimeError("Unknown command")
  finally:
    await close_db()


def main() -> int:
  load_dotenv()
  args = _parser().parse_args()

  import asyncio

  return asyncio.run(_run(args))


if __name__ == "__main__":
  raise SystemExit(main())
