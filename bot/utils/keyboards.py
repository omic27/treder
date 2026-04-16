from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from bot.utils.messages import (
    BTN_ADD_TRADE,
    BTN_CHECK_RULES,
    BTN_DEPOSIT,
    BTN_HELP,
    BTN_HISTORY,
    BTN_LAST_TRADES,
    BTN_STATS,
    BTN_TRADE_SCREEN,
    BTN_UPDATE_STATS,
    BTN_WEEKLY_REVIEW,
    INLINE_BACK,
    INLINE_CANCEL,
    INLINE_CONFIRM,
    INLINE_CONFIRM_TRADE,
    INLINE_EDIT,
    INLINE_MAIN_MENU,
    INLINE_NEXT,
    INLINE_REFRESH,
    INLINE_SHOW_DRAFT,
    INLINE_CANCEL_TRADE,
)

CB_MAIN_MENU = "action:main_menu"
CB_STATS = "action:stats"
CB_DEPOSIT = "action:deposit"
CB_LAST_TRADES = "action:lasttrades"
CB_ADD_TRADE = "action:addtrade"
CB_SCREEN = "action:screen"
CB_UPDATE = "action:update"
CB_CHECK_RULES = "action:checkrules"
CB_WEEKLY = "action:weekly"
CB_HISTORY = "action:history"
CB_PENDING = "action:pending"
CB_ADD_TRADE_CONFIRM = "action:addtrade:confirm"
CB_ADD_TRADE_EDIT = "action:addtrade:edit"
CB_ADD_TRADE_CANCEL = "action:addtrade:cancel"
CB_HISTORY_PAGE_PREFIX = "history:page:"
CB_DRAFT_SHOW_PREFIX = "draft:show:"
CB_DRAFT_CONFIRM_PREFIX = "draft:confirm:"
CB_DRAFT_CANCEL_PREFIX = "draft:cancel:"


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(BTN_STATS), KeyboardButton(BTN_DEPOSIT)],
        [KeyboardButton(BTN_LAST_TRADES), KeyboardButton(BTN_ADD_TRADE)],
        [KeyboardButton(BTN_TRADE_SCREEN), KeyboardButton(BTN_UPDATE_STATS)],
        [KeyboardButton(BTN_CHECK_RULES), KeyboardButton(BTN_WEEKLY_REVIEW)],
        [KeyboardButton(BTN_HISTORY), KeyboardButton(BTN_HELP)],
    ]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True, is_persistent=True)


def stats_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(INLINE_REFRESH, callback_data=CB_UPDATE)],
            [InlineKeyboardButton(BTN_HISTORY, callback_data=CB_HISTORY)],
            [InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)],
        ]
    )


def deposit_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(INLINE_REFRESH, callback_data=CB_DEPOSIT)],
            [InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)],
        ]
    )


def last_trades_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(INLINE_REFRESH, callback_data=CB_LAST_TRADES)],
            [InlineKeyboardButton(BTN_HISTORY, callback_data=CB_HISTORY)],
            [InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)],
        ]
    )


def history_inline_keyboard(page: int, total_pages: int) -> InlineKeyboardMarkup:
    nav_row: list[InlineKeyboardButton] = []
    if page > 0:
        nav_row.append(
            InlineKeyboardButton(INLINE_BACK, callback_data=f"{CB_HISTORY_PAGE_PREFIX}{page - 1}")
        )
    if page < total_pages - 1:
        nav_row.append(
            InlineKeyboardButton(INLINE_NEXT, callback_data=f"{CB_HISTORY_PAGE_PREFIX}{page + 1}")
        )

    rows = [nav_row] if nav_row else []
    rows.append([InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)])
    return InlineKeyboardMarkup(rows)


def update_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(BTN_STATS, callback_data=CB_STATS)],
            [InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)],
        ]
    )


def rules_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(INLINE_REFRESH, callback_data=CB_CHECK_RULES)],
            [InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)],
        ]
    )


def weekly_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(INLINE_REFRESH, callback_data=CB_WEEKLY)],
            [InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)],
        ]
    )


def add_trade_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(INLINE_CONFIRM, callback_data=CB_ADD_TRADE_CONFIRM)],
            [InlineKeyboardButton(INLINE_EDIT, callback_data=CB_ADD_TRADE_EDIT)],
            [InlineKeyboardButton(INLINE_CANCEL, callback_data=CB_ADD_TRADE_CANCEL)],
            [InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)],
        ]
    )


def pending_trade_inline_keyboard(intake_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(INLINE_CONFIRM_TRADE, callback_data=f"{CB_DRAFT_CONFIRM_PREFIX}{intake_id}")],
            [InlineKeyboardButton(INLINE_SHOW_DRAFT, callback_data=f"{CB_DRAFT_SHOW_PREFIX}{intake_id}")],
            [InlineKeyboardButton(INLINE_CANCEL_TRADE, callback_data=f"{CB_DRAFT_CANCEL_PREFIX}{intake_id}")],
            [InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)],
        ]
    )


def pending_list_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(INLINE_REFRESH, callback_data=CB_PENDING)],
            [InlineKeyboardButton(INLINE_MAIN_MENU, callback_data=CB_MAIN_MENU)],
        ]
    )
