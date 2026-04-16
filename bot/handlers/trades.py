from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.config import get_settings
from bot.services.stats_service import build_stats_summary, update_stats_report
from bot.services.trades_service import (
    cancel_pending_trade,
    confirm_pending_trade,
    create_pending_trade,
    get_add_trade_template,
    get_confirmtrade_template,
    get_pending_by_id,
    get_pending_trades,
    parse_confirmation_payload,
    save_screenshot_file,
)
from bot.utils.formatters import (
    format_confirmed_trade_summary,
    format_draft_view,
    format_pending_trade_summary,
)
from bot.utils.keyboards import (
    pending_list_inline_keyboard,
    pending_trade_inline_keyboard,
)
from bot.utils.messages import (
    add_trade_template_text,
    addtrade_cancel_stub,
    addtrade_confirm_stub,
    addtrade_edit_stub,
    canceltrade_fail_text,
    canceltrade_success_text,
    confirmtrade_missing_text,
    confirmtrade_template_text,
    draft_not_found_text,
    pending_empty_text,
    pending_list_header,
    screenshot_received_text,
    screenshot_wait_text,
    screenshot_stub_text,
)
from bot.utils.navigation import callback_data, reply_text


def _parse_intake_id(text: str) -> str:
    payload = parse_confirmation_payload(text)
    return payload.get("intake_id", "").strip()


def _parse_confirm_payload_from_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> dict[str, str]:
    _ = context
    text = update.effective_message.text if update.effective_message else ""
    return parse_confirmation_payload(text or "")


def _intake_id_from_callback(data: str, prefix: str) -> str:
    if not data.startswith(prefix):
        return ""
    return data[len(prefix) :].strip()


async def add_trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    template = get_add_trade_template()
    await reply_text(update, add_trade_template_text(template))


async def trade_screenshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, screenshot_wait_text())


async def intake_photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    message = update.effective_message
    if message is None:
        return

    source_name = "image.jpg"
    file_id = ""

    if message.photo:
        file_id = message.photo[-1].file_id
        source_name = f"telegram_photo_{message.photo[-1].file_unique_id}.jpg"
    elif message.document and (message.document.mime_type or "").startswith("image/"):
        file_id = message.document.file_id
        source_name = message.document.file_name or "telegram_image.jpg"
    else:
        await reply_text(update, "Поддерживаются только изображения.")
        return

    tg_file = await context.bot.get_file(file_id)
    file_bytes = bytes(await tg_file.download_as_bytearray())

    screenshot_path = save_screenshot_file(
        settings.project_root,
        file_bytes=file_bytes,
        source_name=source_name,
    )

    item = create_pending_trade(
        settings.project_root,
        telegram_user_id=update.effective_user.id if update.effective_user else 0,
        telegram_message_id=message.message_id,
        screenshot_path=screenshot_path,
        raw_caption=message.caption or "",
    )

    await reply_text(
        update,
        screenshot_received_text(str(item.get("intake_id", ""))),
        reply_markup=pending_trade_inline_keyboard(str(item.get("intake_id", ""))),
    )


async def pending_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    items = [item for item in get_pending_trades(settings.project_root) if item.get("status") == "pending"]

    if not items:
        await reply_text(update, pending_empty_text(), reply_markup=pending_list_inline_keyboard())
        return

    top = items[:5]
    body = "\n\n".join(format_pending_trade_summary(item) for item in top)
    text = f"{pending_list_header(len(items))}\n\n{body}"
    await reply_text(update, text, reply_markup=pending_list_inline_keyboard())


async def showdraft_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    text = update.effective_message.text if update.effective_message else ""
    intake_id = _parse_intake_id(text or "")

    if not intake_id:
        await reply_text(update, "Укажите intake_id: /showdraft intake_id=...")
        return

    item = get_pending_by_id(settings.project_root, intake_id)
    if item is None:
        await reply_text(update, draft_not_found_text())
        return

    await reply_text(update, format_draft_view(item), reply_markup=pending_trade_inline_keyboard(intake_id))


async def confirmtrade_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = get_settings()
    payload = _parse_confirm_payload_from_update(update, context)

    if not payload:
        template = get_confirmtrade_template()
        await reply_text(update, confirmtrade_template_text(template))
        return

    ok, message, row = confirm_pending_trade(settings.project_root, payload)
    if not ok:
        await reply_text(update, confirmtrade_missing_text(message))
        return

    update_stats_report(settings.project_root)
    stats = build_stats_summary(settings.project_root)

    summary = {
        "symbol": row.get("symbol", "-"),
        "side": row.get("side", "-"),
        "result_usdt": row.get("result_usdt", "-"),
        "current_deposit": (
            "нет данных"
            if stats.get("current_deposit") is None
            else f"{float(stats['current_deposit']):.2f} USDT"
        ),
        "total_trades": str(stats.get("total_trades", 0)),
    }
    await reply_text(update, format_confirmed_trade_summary(summary))


async def canceltrade_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    settings = get_settings()
    text = update.effective_message.text if update.effective_message else ""
    intake_id = _parse_intake_id(text or "")

    if not intake_id:
        await reply_text(update, "Укажите intake_id: /canceltrade intake_id=...")
        return

    ok, message = cancel_pending_trade(settings.project_root, intake_id)
    if ok:
        await reply_text(update, canceltrade_success_text())
    else:
        await reply_text(update, canceltrade_fail_text(message))


async def handle_pending_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    data = callback_data(update)
    if not data:
        return False

    settings = get_settings()

    if data.startswith("draft:show:"):
        intake_id = _intake_id_from_callback(data, "draft:show:")
        item = get_pending_by_id(settings.project_root, intake_id)
        if item is None:
            await reply_text(update, draft_not_found_text())
            return True
        await reply_text(update, format_draft_view(item), reply_markup=pending_trade_inline_keyboard(intake_id))
        return True

    if data.startswith("draft:cancel:"):
        intake_id = _intake_id_from_callback(data, "draft:cancel:")
        ok, message = cancel_pending_trade(settings.project_root, intake_id)
        if ok:
            await reply_text(update, canceltrade_success_text())
        else:
            await reply_text(update, canceltrade_fail_text(message))
        return True

    if data.startswith("draft:confirm:"):
        intake_id = _intake_id_from_callback(data, "draft:confirm:")
        template = get_confirmtrade_template()
        prefilled = f"intake_id={intake_id}\n" + "\n".join(template.splitlines()[1:])
        await reply_text(update, confirmtrade_template_text(prefilled))
        return True

    return False


async def add_trade_confirm_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, addtrade_confirm_stub())


async def add_trade_edit_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, addtrade_edit_stub())


async def add_trade_cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    await reply_text(update, addtrade_cancel_stub())
