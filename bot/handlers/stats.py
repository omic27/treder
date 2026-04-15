from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import get_settings
from bot.services.stats_service import build_stats_summary, get_current_deposit, update_stats_report
from bot.services.trades_service import get_last_trades


def _format_trade_line(trade: dict[str, str]) -> str:
    return (
        f"{trade.get('trade_id', '-')} | {trade.get('date_time', '-')} | "
        f"{trade.get('side', '-')} | pnl={trade.get('result_usdt', '-')}"
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    stats = build_stats_summary(settings.project_root)
    win_rate_text = "-" if stats["win_rate"] is None else f"{stats['win_rate']:.2f}%"
    average_r_text = "-" if stats["average_r"] is None else f"{stats['average_r']:.2f}"
    deposit_text = (
        "-" if stats["current_deposit"] is None else f"{stats['current_deposit']:.2f} USDT"
    )

    text = (
        "Stats summary\n"
        f"Total trades: {stats['total_trades']}\n"
        f"Wins/Losses: {stats['wins']}/{stats['losses']}\n"
        f"Win rate: {win_rate_text}\n"
        f"Average R: {average_r_text}\n"
        f"Total PnL: {stats['total_pnl']:.2f} USDT\n"
        f"Current deposit: {deposit_text}"
    )
    await update.message.reply_text(text)


async def deposit_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    value = get_current_deposit(settings.project_root)
    text = "Current deposit: -" if value is None else f"Current deposit: {value:.2f} USDT"
    await update.message.reply_text(text)


async def last_trades_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    rows = get_last_trades(settings.project_root, limit=5)
    if not rows:
        await update.message.reply_text("No trades found yet.")
        return

    body = "\n".join(_format_trade_line(row) for row in rows)
    await update.message.reply_text(f"Last trades:\n{body}")


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    report_path = update_stats_report(settings.project_root)
    await update.message.reply_text(f"Stats updated: {report_path}")
