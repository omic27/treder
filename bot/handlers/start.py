from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


def _help_text() -> str:
    return (
        "Available commands:\n"
        "/start - bot info\n"
        "/help - show commands\n"
        "/stats - trading summary\n"
        "/deposit - current deposit\n"
        "/lasttrades - show last trades\n"
        "/addtrade - show trade input template\n"
        "/update - refresh stats report\n"
        "/checkrules - validate risk rules\n"
        "/weekly - show weekly review"
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    text = (
        "BTC Trading OS bot v1\n"
        "This bot manages local journal/statistics files only.\n"
        "It does not place trades and does not connect to any exchange.\n\n"
        + _help_text()
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await update.message.reply_text(_help_text())
