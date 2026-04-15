from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.keyboards import main_menu_keyboard
from bot.utils.messages import help_text, start_text
from bot.utils.navigation import reply_text


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, start_text(), reply_markup=main_menu_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, help_text(), reply_markup=main_menu_keyboard())
