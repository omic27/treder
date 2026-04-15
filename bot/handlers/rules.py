from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import get_settings
from bot.services.rules_service import evaluate_rules


async def check_rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    violations = evaluate_rules(settings.project_root)
    text = "Rule check:\n" + "\n".join(f"- {item}" for item in violations)
    await update.message.reply_text(text[:4000])
