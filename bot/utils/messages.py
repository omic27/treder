from __future__ import annotations

from typing import Iterable

BTN_STATS = "Статистика"
BTN_DEPOSIT = "Депозит"
BTN_LAST_TRADES = "Последние сделки"
BTN_ADD_TRADE = "Добавить сделку"
BTN_TRADE_SCREEN = "Скрин сделки"
BTN_UPDATE_STATS = "Обновить статистику"
BTN_CHECK_RULES = "Проверить правила"
BTN_WEEKLY_REVIEW = "Недельный обзор"
BTN_HISTORY = "История"
BTN_HELP = "Помощь"

INLINE_BACK = "Назад"
INLINE_REFRESH = "Обновить"
INLINE_NEXT = "Далее"
INLINE_CONFIRM = "Подтвердить"
INLINE_EDIT = "Изменить"
INLINE_CANCEL = "Отменить"
INLINE_MAIN_MENU = "Главное меню"
INLINE_CONFIRM_TRADE = "Подтвердить сделку"
INLINE_SHOW_DRAFT = "Показать черновик"
INLINE_CANCEL_TRADE = "Отменить"


def start_text() -> str:
    return (
        "BTC Trading OS Bot v1\n\n"
        "Я помогаю вести журнал сделок и аналитику по локальным файлам проекта.\n\n"
        "Что умею:\n"
        "- показывать статистику, депозит, последние сделки и историю\n"
        "- принимать скрин закрытой сделки и создавать черновик\n"
        "- подтверждать черновик через /confirmtrade\n"
        "- запускать пересчет статистики и проверку риск-правил\n\n"
        "Чего не умею:\n"
        "- не торгую\n"
        "- не подключаюсь к бирже\n"
        "- не даю гарантий доходности\n\n"
        "Как начать: отправьте скрин сделки или используйте кнопки меню."
    )


def help_text() -> str:
    return (
        "Команды бота:\n"
        "/start - старт и главное меню\n"
        "/help - справка\n"
        "/stats - общая статистика\n"
        "/deposit - текущий депозит\n"
        "/lasttrades - последние 5 сделок\n"
        "/history - история (по 10 сделок)\n"
        "/pending - список черновиков\n"
        "/showdraft intake_id=... - показать черновик\n"
        "/confirmtrade - шаблон подтверждения\n"
        "/confirmtrade intake_id=... symbol=... ... - подтвердить сделку\n"
        "/canceltrade intake_id=... - отменить черновик\n"
        "/addtrade - шаблон ручного ввода сделки\n"
        "/update - пересчет статистики\n"
        "/checkrules - проверка риск-правил\n"
        "/weekly - недельный обзор\n\n"
        "Также доступны кнопки в главном меню."
    )


def placeholder() -> str:
    return "нет данных"


def value_or_placeholder(value: str | None) -> str:
    if value is None:
        return placeholder()
    clean = value.strip()
    return clean if clean and clean != "-" else placeholder()


def stats_text(summary: dict[str, float | int | None]) -> str:
    win_rate = (
        placeholder() if summary.get("win_rate") is None else f"{float(summary['win_rate']):.2f}%"
    )
    avg_win = (
        placeholder()
        if summary.get("average_win") is None
        else f"{float(summary['average_win']):.2f} USDT"
    )
    avg_loss = (
        placeholder()
        if summary.get("average_loss") is None
        else f"{float(summary['average_loss']):.2f} USDT"
    )
    avg_r = (
        placeholder() if summary.get("average_r") is None else f"{float(summary['average_r']):.2f}"
    )
    current_deposit = (
        placeholder()
        if summary.get("current_deposit") is None
        else f"{float(summary['current_deposit']):.2f} USDT"
    )
    max_drawdown = (
        placeholder()
        if summary.get("max_drawdown") is None
        else f"{float(summary['max_drawdown']):.2f} USDT"
    )

    return (
        "Статистика\n"
        f"- Всего сделок: {int(summary.get('total_trades', 0))}\n"
        f"- Винрейт: {win_rate}\n"
        f"- Средняя прибыль: {avg_win}\n"
        f"- Средний убыток: {avg_loss}\n"
        f"- Средний R: {avg_r}\n"
        f"- Общий PnL: {float(summary.get('total_pnl', 0.0)):.2f} USDT\n"
        f"- Текущий депозит: {current_deposit}\n"
        f"- Макс. просадка: {max_drawdown}"
    )


def deposit_text(value: float | None) -> str:
    if value is None:
        return "Текущий депозит: нет данных"
    return f"Текущий депозит: {value:.2f} USDT"


def last_trades_header(limit: int) -> str:
    return f"Последние сделки (до {limit}):"


def no_trades_text() -> str:
    return "Сделок пока нет. Добавьте записи в data/trades.csv."


def history_header(page: int, total_pages: int, total_rows: int) -> str:
    return (
        f"История сделок (страница {page + 1} из {total_pages})\n"
        f"Всего записей: {total_rows}"
    )


def update_success_text(total_trades: int, current_deposit: float | None, total_pnl: float) -> str:
    deposit = "нет данных" if current_deposit is None else f"{current_deposit:.2f} USDT"
    return (
        "Статистика обновлена.\n"
        f"- Обработано сделок: {total_trades}\n"
        f"- Текущий депозит: {deposit}\n"
        f"- Общий результат: {total_pnl:.2f} USDT\n"
        "- Ошибки: не обнаружены"
    )


def update_error_text(error: Exception) -> str:
    return (
        "Не удалось обновить статистику.\n"
        f"Причина: {error}\n"
        "Проверьте корректность локальных файлов data/ и reports/."
    )


def rules_ok_text() -> str:
    return "Проверка правил\nНарушений нет."


def rules_violations_text(items: Iterable[str]) -> str:
    body = "\n".join(f"- {item}" for item in items)
    return f"Проверка правил\nНайдены нарушения:\n{body}"


def weekly_empty_text() -> str:
    return "Недельный обзор пока не заполнен. Запустите обновление и заполните reports/weekly_review.md."


def add_trade_template_text(template: str) -> str:
    return (
        "Ручной ввод сделки (v1):\n"
        "Скопируйте шаблон ниже, заполните значения и сохраните строку в data/trades.csv.\n\n"
        f"{template}"
    )


def screenshot_wait_text() -> str:
    return "Отправьте изображение закрытой сделки. Я сохраню скрин и создам черновик."


def screenshot_received_text(intake_id: str) -> str:
    return (
        "Скрин получен. Создан черновик сделки.\n"
        f"intake_id: {intake_id}\n"
        "Нужно подтвердить данные перед сохранением."
    )


def pending_empty_text() -> str:
    return "Активных черновиков нет."


def pending_list_header(total: int) -> str:
    return f"Черновики сделок: {total}"


def confirmtrade_template_text(template: str) -> str:
    return (
        "Шаблон подтверждения сделки:\n\n"
        f"{template}\n\n"
        "Отправьте /confirmtrade intake_id=... symbol=... side=... и остальные поля."
    )


def confirmtrade_missing_text(missing_text: str) -> str:
    return missing_text


def draft_not_found_text() -> str:
    return "Черновик не найден."


def canceltrade_success_text() -> str:
    return "Черновик отменен."


def canceltrade_fail_text(reason: str) -> str:
    return reason


def screenshot_stub_text() -> str:
    return "Раздел 'Скрин сделки': отправьте изображение, и я создам черновик."


def addtrade_confirm_stub() -> str:
    return "Подтверждение ввода сделки будет добавлено в следующей версии."


def addtrade_edit_stub() -> str:
    return "Редактирование ввода сделки пока не реализовано."


def addtrade_cancel_stub() -> str:
    return "Действие отменено."
