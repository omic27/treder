from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import get_settings
from bot.services.stats_service import build_stats_summary, get_current_deposit, update_stats_report
from bot.services.trades_service import get_history_page, get_last_trades
from bot.utils.keyboards import (
    CB_HISTORY_PAGE_PREFIX,
    history_inline_keyboard,
    last_trades_inline_keyboard,
    stats_inline_keyboard,
    update_inline_keyboard,
    deposit_inline_keyboard,
)
from bot.utils.messages import (
    history_header,
    last_trades_header,
    no_trades_text,
    stats_text,
    deposit_text,
    update_error_text,
    update_success_text,
    value_or_placeholder,
)
from bot.utils.navigation import callback_data, edit_or_reply, parse_history_page, reply_text


def _plan_label(value: str | None) -> str:
    raw = (value or "").strip().lower()
    if raw in {"yes", "true", "1", "да"}:
        return "да"
    if raw in {"no", "false", "0", "нет"}:
        return "нет"
    return "нет данных"


def _compact_trade_line(index: int, trade: dict[str, str]) -> str:
    dt = value_or_placeholder(trade.get("date_time"))
    side = value_or_placeholder(trade.get("side")).upper()
    entry = value_or_placeholder(trade.get("entry"))
    result_usdt = value_or_placeholder(trade.get("result_usdt"))
    result_r = value_or_placeholder(trade.get("result_r"))
    plan = _plan_label(trade.get("followed_plan"))
    return (
        f"{index}. {dt} | {side} | вход: {entry} | "
        f"результат: {result_usdt}$ | R: {result_r} | план: {plan}"
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    summary = build_stats_summary(settings.project_root)
    await reply_text(update, stats_text(summary), reply_markup=stats_inline_keyboard())


async def deposit_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    value = get_current_deposit(settings.project_root)
    await reply_text(update, deposit_text(value), reply_markup=deposit_inline_keyboard())


async def last_trades_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    rows = get_last_trades(settings.project_root, limit=5)
    if not rows:
        await reply_text(update, no_trades_text(), reply_markup=last_trades_inline_keyboard())
        return

    body = "\n".join(_compact_trade_line(i + 1, row) for i, row in enumerate(rows))
    text = f"{last_trades_header(5)}\n\n{body}"
    await reply_text(update, text, reply_markup=last_trades_inline_keyboard())


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    page = 0
    data = callback_data(update)
    parsed_page = parse_history_page(data, prefix=CB_HISTORY_PAGE_PREFIX)
    if parsed_page is not None:
        page = parsed_page

    settings = get_settings()
    rows, safe_page, total_pages, total_rows = get_history_page(
        settings.project_root,
        page=page,
        page_size=10,
    )

    if not rows:
        await edit_or_reply(
            update,
            no_trades_text(),
            reply_markup=history_inline_keyboard(0, 1),
        )
        return

    body = "\n".join(_compact_trade_line(i + 1 + safe_page * 10, row) for i, row in enumerate(rows))
    text = f"{history_header(safe_page, total_pages, total_rows)}\n\n{body}"
    await edit_or_reply(
        update,
        text,
        reply_markup=history_inline_keyboard(safe_page, total_pages),
    )


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()

    try:
        update_stats_report(settings.project_root)
        summary = build_stats_summary(settings.project_root)
        text = update_success_text(
            total_trades=int(summary.get("total_trades", 0)),
            current_deposit=(
                None
                if summary.get("current_deposit") is None
                else float(summary["current_deposit"])
            ),
            total_pnl=float(summary.get("total_pnl", 0.0)),
        )
        await reply_text(update, text, reply_markup=update_inline_keyboard())
    except Exception as error:  # pragma: no cover
        await reply_text(update, update_error_text(error), reply_markup=update_inline_keyboard())
