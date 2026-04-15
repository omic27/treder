from __future__ import annotations

import logging

from telegram.ext import Application, CommandHandler

from bot.config import get_settings
from bot.handlers.reviews import weekly_command
from bot.handlers.rules import check_rules_command
from bot.handlers.start import help_command, start_command
from bot.handlers.stats import deposit_command, last_trades_command, stats_command, update_command
from bot.handlers.trades import add_trade_command


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def build_application() -> Application:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is empty. Set it in .env.")

    app = Application.builder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("deposit", deposit_command))
    app.add_handler(CommandHandler("lasttrades", last_trades_command))
    app.add_handler(CommandHandler("addtrade", add_trade_command))
    app.add_handler(CommandHandler("update", update_command))
    app.add_handler(CommandHandler("checkrules", check_rules_command))
    app.add_handler(CommandHandler("weekly", weekly_command))
    return app


def main() -> None:
    app = build_application()
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
