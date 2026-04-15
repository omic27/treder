from __future__ import annotations

import math
from pathlib import Path

from bot.utils.csv_io import append_csv_row, read_csv_rows

TRADE_FIELDS = [
    "trade_id",
    "date_time",
    "symbol",
    "side",
    "setup_name",
    "timeframe_context",
    "entry",
    "stop_loss",
    "tp1",
    "tp2",
    "leverage",
    "deposit_before",
    "risk_usdt",
    "position_size_usdt",
    "result_usdt",
    "result_r",
    "status",
    "followed_plan",
    "notes",
]


def trades_file(project_root: Path) -> Path:
    return project_root / "data" / "trades.csv"


def get_trades(project_root: Path) -> list[dict[str, str]]:
    return read_csv_rows(trades_file(project_root))


def get_last_trades(project_root: Path, limit: int = 5) -> list[dict[str, str]]:
    rows = get_trades(project_root)
    if not rows:
        return []
    return list(reversed(rows[-limit:]))


def get_history_page(
    project_root: Path,
    *,
    page: int,
    page_size: int = 10,
) -> tuple[list[dict[str, str]], int, int, int]:
    rows = list(reversed(get_trades(project_root)))
    total_rows = len(rows)
    if total_rows == 0:
        return [], 0, 1, 0

    total_pages = max(1, math.ceil(total_rows / page_size))
    safe_page = min(max(page, 0), total_pages - 1)
    start = safe_page * page_size
    end = start + page_size
    return rows[start:end], safe_page, total_pages, total_rows


def add_trade(project_root: Path, trade: dict[str, str]) -> None:
    normalized = {field: trade.get(field, "-") for field in TRADE_FIELDS}
    append_csv_row(trades_file(project_root), normalized, TRADE_FIELDS)


def get_add_trade_template() -> str:
    return (
        "Одна строка CSV в строгом порядке полей:\n"
        + ",".join(TRADE_FIELDS)
        + "\n"
        "Если значения нет, поставьте '-'."
    )
