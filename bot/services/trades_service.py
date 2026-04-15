from __future__ import annotations

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
    return rows[-limit:] if rows else []


def add_trade(project_root: Path, trade: dict[str, str]) -> None:
    normalized = {field: trade.get(field, "-") for field in TRADE_FIELDS}
    append_csv_row(trades_file(project_root), normalized, TRADE_FIELDS)


def get_add_trade_template() -> str:
    return (
        "Send one CSV line in this exact order:\n"
        + ",".join(TRADE_FIELDS)
        + "\n"
        "Use '-' for missing values."
    )
