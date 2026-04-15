from __future__ import annotations

from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, Update


async def reply_text(
    update: Update,
    text: str,
    *,
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
) -> None:
    query = update.callback_query
    if query is not None:
        await query.answer()
        if query.message is not None:
            await query.message.reply_text(text, reply_markup=reply_markup)
        return

    message = update.effective_message
    if message is not None:
        await message.reply_text(text, reply_markup=reply_markup)


async def edit_or_reply(
    update: Update,
    text: str,
    *,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    query = update.callback_query
    if query is not None and query.message is not None:
        await query.answer()
        await query.edit_message_text(text=text, reply_markup=reply_markup)
        return
    message = update.effective_message
    if message is not None:
        await message.reply_text(text, reply_markup=reply_markup)


def callback_data(update: Update) -> str:
    query = update.callback_query
    if query is None or query.data is None:
        return ""
    return query.data


def parse_history_page(data: str, prefix: str = "history:page:") -> int | None:
    if not data.startswith(prefix):
        return None
    try:
        value = int(data[len(prefix) :])
    except ValueError:
        return None
    return max(0, value)
