from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import get_settings
from bot.services.rules_service import evaluate_rules
from bot.utils.keyboards import rules_inline_keyboard
from bot.utils.messages import rules_ok_text, rules_violations_text
from bot.utils.navigation import reply_text


async def check_rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    violations = evaluate_rules(settings.project_root)

    if not violations:
        await reply_text(update, rules_ok_text(), reply_markup=rules_inline_keyboard())
        return

    await reply_text(
        update,
        rules_violations_text(violations)[:4000],
        reply_markup=rules_inline_keyboard(),
    )
