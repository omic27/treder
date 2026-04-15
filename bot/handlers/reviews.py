from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import get_settings
from bot.services.review_service import has_meaningful_weekly_content, read_weekly_review
from bot.utils.keyboards import weekly_inline_keyboard
from bot.utils.messages import weekly_empty_text
from bot.utils.navigation import reply_text


async def weekly_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    text = read_weekly_review(settings.project_root)

    if not has_meaningful_weekly_content(text):
        await reply_text(update, weekly_empty_text(), reply_markup=weekly_inline_keyboard())
        return

    await reply_text(update, text[:4000], reply_markup=weekly_inline_keyboard())
