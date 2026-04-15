from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.services.trades_service import get_add_trade_template
from bot.utils.keyboards import add_trade_inline_keyboard
from bot.utils.messages import (
    add_trade_template_text,
    addtrade_cancel_stub,
    addtrade_confirm_stub,
    addtrade_edit_stub,
    screenshot_stub_text,
)
from bot.utils.navigation import reply_text


async def add_trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    template = get_add_trade_template()
    await reply_text(update, add_trade_template_text(template), reply_markup=add_trade_inline_keyboard())


async def trade_screenshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, screenshot_stub_text())


async def add_trade_confirm_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, addtrade_confirm_stub())


async def add_trade_edit_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, addtrade_edit_stub())


async def add_trade_cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, addtrade_cancel_stub())
