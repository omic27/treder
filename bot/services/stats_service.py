from __future__ import annotations

from pathlib import Path

from bot.services.trades_service import get_trades
from bot.utils.csv_io import read_csv_rows


def equity_file(project_root: Path) -> Path:
    return project_root / "data" / "equity_curve.csv"


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text or text == "-":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def get_current_deposit(project_root: Path) -> float | None:
    rows = read_csv_rows(equity_file(project_root))
    if not rows:
        return None
    return _to_float(rows[-1].get("deposit_after"))


def build_stats_summary(project_root: Path) -> dict[str, float | int | None]:
    trades = get_trades(project_root)
    total = len(trades)

    result_values = [_to_float(row.get("result_usdt")) for row in trades]
    result_values = [value for value in result_values if value is not None]

    wins = [value for value in result_values if value > 0]
    losses = [value for value in result_values if value < 0]

    result_r_values = [_to_float(row.get("result_r")) for row in trades]
    result_r_values = [value for value in result_r_values if value is not None]

    total_pnl = sum(result_values) if result_values else 0.0
    win_rate = (len(wins) / len(result_values) * 100.0) if result_values else None
    avg_r = (sum(result_r_values) / len(result_r_values)) if result_r_values else None

    return {
        "total_trades": total,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": win_rate,
        "total_pnl": total_pnl,
        "average_r": avg_r,
        "current_deposit": get_current_deposit(project_root),
    }


def update_stats_report(project_root: Path) -> Path:
    stats = build_stats_summary(project_root)
    report_path = project_root / "reports" / "stats.md"
    win_rate_text = "-" if stats["win_rate"] is None else f"{stats['win_rate']:.2f}%"
    average_r_text = "-" if stats["average_r"] is None else f"{stats['average_r']:.2f}"
    current_deposit_text = (
        "-" if stats["current_deposit"] is None else f"{stats['current_deposit']:.2f} USDT"
    )
    report = (
        "# Stats Report\n\n"
        f"## total trades\n{stats['total_trades']}\n\n"
        f"## win rate\n{win_rate_text}\n\n"
        "## average win\n-\n\n"
        "## average loss\n-\n\n"
        f"## average R\n{average_r_text}\n\n"
        f"## total pnl\n{stats['total_pnl']:.2f} USDT\n\n"
        f"## current deposit\n{current_deposit_text}\n\n"
        "## max drawdown\n-\n\n"
        "## best setups\n-\n\n"
        "## worst setups\n-\n\n"
        "## rule violations\n-\n\n"
        "## latest trades\n-\n"
    )
    report_path.write_text(report, encoding="utf-8")
    return report_path
