from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.config import get_settings
from bot.handlers.reviews import weekly_command
from bot.handlers.rules import check_rules_command
from bot.handlers.start import help_command, start_command
from bot.handlers.stats import deposit_command, history_command, last_trades_command, stats_command, update_command
from bot.handlers.trades import (
    add_trade_cancel_command,
    add_trade_command,
    add_trade_confirm_command,
    add_trade_edit_command,
    canceltrade_command,
    confirmtrade_command,
    handle_pending_callbacks,
    intake_photo_message,
    pending_command,
    showdraft_command,
    trade_screenshot_command,
)
from bot.services.trades_service import ensure_storage
from bot.utils.keyboards import (
    CB_ADD_TRADE,
    CB_ADD_TRADE_CANCEL,
    CB_ADD_TRADE_CONFIRM,
    CB_ADD_TRADE_EDIT,
    CB_CHECK_RULES,
    CB_DEPOSIT,
    CB_HISTORY,
    CB_HISTORY_PAGE_PREFIX,
    CB_LAST_TRADES,
    CB_MAIN_MENU,
    CB_PENDING,
    CB_SCREEN,
    CB_STATS,
    CB_UPDATE,
    CB_WEEKLY,
)
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
)


class SecretMaskFilter(logging.Filter):
    def __init__(self, secret: str) -> None:
        super().__init__()
        self.secret = secret

    def filter(self, record: logging.LogRecord) -> bool:
        if self.secret:
            if isinstance(record.msg, str):
                record.msg = record.msg.replace(self.secret, "***")
            if record.args:
                record.args = tuple(
                    (str(arg).replace(self.secret, "***") if isinstance(arg, str) else arg)
                    for arg in record.args
                )
        return True


def configure_logging(token: str) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    for logger_name in ("httpx", "httpcore", "telegram", "telegram.ext"):
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    if token:
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            handler.addFilter(SecretMaskFilter(token))


async def route_menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.effective_message.text or "").strip() if update.effective_message else ""

    mapping = {
        BTN_STATS: stats_command,
        BTN_DEPOSIT: deposit_command,
        BTN_LAST_TRADES: last_trades_command,
        BTN_ADD_TRADE: add_trade_command,
        BTN_TRADE_SCREEN: trade_screenshot_command,
        BTN_UPDATE_STATS: update_command,
        BTN_CHECK_RULES: check_rules_command,
        BTN_WEEKLY_REVIEW: weekly_command,
        BTN_HISTORY: history_command,
        BTN_HELP: help_command,
    }

    handler = mapping.get(text)
    if handler is None:
        await help_command(update, context)
        return
    await handler(update, context)


async def route_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await handle_pending_callbacks(update, context):
        return

    query = update.callback_query
    data = query.data if query and query.data else ""

    if data == CB_MAIN_MENU:
        await start_command(update, context)
    elif data == CB_STATS:
        await stats_command(update, context)
    elif data == CB_DEPOSIT:
        await deposit_command(update, context)
    elif data == CB_LAST_TRADES:
        await last_trades_command(update, context)
    elif data == CB_ADD_TRADE:
        await add_trade_command(update, context)
    elif data == CB_SCREEN:
        await trade_screenshot_command(update, context)
    elif data == CB_UPDATE:
        await update_command(update, context)
    elif data == CB_CHECK_RULES:
        await check_rules_command(update, context)
    elif data == CB_WEEKLY:
        await weekly_command(update, context)
    elif data == CB_PENDING:
        await pending_command(update, context)
    elif data == CB_HISTORY or data.startswith(CB_HISTORY_PAGE_PREFIX):
        await history_command(update, context)
    elif data == CB_ADD_TRADE_CONFIRM:
        await add_trade_confirm_command(update, context)
    elif data == CB_ADD_TRADE_EDIT:
        await add_trade_edit_command(update, context)
    elif data == CB_ADD_TRADE_CANCEL:
        await add_trade_cancel_command(update, context)
    else:
        await query.answer("Неизвестное действие", show_alert=False)


def build_application() -> Application:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не задан. Добавьте токен в .env")

    ensure_storage(settings.project_root)
    configure_logging(settings.telegram_bot_token)

    app = Application.builder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("deposit", deposit_command))
    app.add_handler(CommandHandler("lasttrades", last_trades_command))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(CommandHandler("pending", pending_command))
    app.add_handler(CommandHandler("showdraft", showdraft_command))
    app.add_handler(CommandHandler("confirmtrade", confirmtrade_command))
    app.add_handler(CommandHandler("canceltrade", canceltrade_command))
    app.add_handler(CommandHandler("addtrade", add_trade_command))
    app.add_handler(CommandHandler("update", update_command))
    app.add_handler(CommandHandler("checkrules", check_rules_command))
    app.add_handler(CommandHandler("weekly", weekly_command))

    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, intake_photo_message))
    app.add_handler(CallbackQueryHandler(route_callbacks))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_menu_buttons))

    return app


def main() -> None:
    app = build_application()
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
