from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.services.trades_service import get_add_trade_template


async def add_trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await update.message.reply_text(
        "Trade parser is not implemented in v1 yet.\n"
        + get_add_trade_template()
    )
