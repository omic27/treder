from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import get_settings
from bot.services.review_service import read_weekly_review


async def weekly_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    text = read_weekly_review(settings.project_root)
    await update.message.reply_text(text[:4000])
