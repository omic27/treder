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


def get_max_drawdown(project_root: Path) -> float | None:
    rows = read_csv_rows(equity_file(project_root))
    deposits = [_to_float(row.get("deposit_after")) for row in rows]
    deposits = [value for value in deposits if value is not None]
    if not deposits:
        return None

    peak = deposits[0]
    max_drawdown = 0.0
    for value in deposits:
        if value > peak:
            peak = value
        drawdown = peak - value
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    return max_drawdown


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
    avg_win = (sum(wins) / len(wins)) if wins else None
    avg_loss = (sum(losses) / len(losses)) if losses else None

    return {
        "total_trades": total,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": win_rate,
        "average_win": avg_win,
        "average_loss": avg_loss,
        "total_pnl": total_pnl,
        "average_r": avg_r,
        "current_deposit": get_current_deposit(project_root),
        "max_drawdown": get_max_drawdown(project_root),
    }


def update_stats_report(project_root: Path) -> Path:
    stats = build_stats_summary(project_root)
    report_path = project_root / "reports" / "stats.md"

    def _fmt(value: float | None, suffix: str = "") -> str:
        if value is None:
            return "нет данных"
        return f"{value:.2f}{suffix}"

    report = (
        "# Stats Report\n\n"
        f"## total trades\n{stats['total_trades']}\n\n"
        f"## win rate\n{_fmt(stats['win_rate'], '%')}\n\n"
        f"## average win\n{_fmt(stats['average_win'], ' USDT')}\n\n"
        f"## average loss\n{_fmt(stats['average_loss'], ' USDT')}\n\n"
        f"## average R\n{_fmt(stats['average_r'])}\n\n"
        f"## total pnl\n{float(stats['total_pnl']):.2f} USDT\n\n"
        f"## current deposit\n{_fmt(stats['current_deposit'], ' USDT')}\n\n"
        f"## max drawdown\n{_fmt(stats['max_drawdown'], ' USDT')}\n\n"
        "## best setups\n-\n\n"
        "## worst setups\n-\n\n"
        "## rule violations\n-\n\n"
        "## latest trades\n-\n"
    )
    report_path.write_text(report, encoding="utf-8")
    return report_path
