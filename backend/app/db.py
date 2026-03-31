from __future__ import annotations

import os
from typing import Any

import asyncpg

_pool: asyncpg.Pool | None = None


def db_enabled() -> bool:
  return bool(os.getenv("DATABASE_URL")) and os.getenv("USE_SEED_DATA") != "1"


async def init_db(force: bool = False) -> None:
  global _pool
  if not force and not db_enabled():
    return
  if _pool is not None:
    return
  _pool = await asyncpg.create_pool(
    dsn=os.environ["DATABASE_URL"],
    min_size=1,
    max_size=5,
    command_timeout=60,
  )


async def close_db() -> None:
  global _pool
  if _pool is None:
    return
  await _pool.close()
  _pool = None


def pool() -> asyncpg.Pool:
  if _pool is None:
    raise RuntimeError("Database pool is not initialized")
  return _pool


def row_to_dict(r: asyncpg.Record) -> dict[str, Any]:
  return dict(r)
