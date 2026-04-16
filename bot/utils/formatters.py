from __future__ import annotations

import json
from typing import Any


def format_money(value: float | None) -> str:
    if value is None:
        return "нет данных"
    return f"{value:.2f} USDT"


def format_percent(value: float | None) -> str:
    if value is None:
        return "нет данных"
    return f"{value:.2f}%"


def safe_text(value: str | None, fallback: str = "нет данных") -> str:
    if value is None:
        return fallback
    clean = value.strip()
    if not clean or clean == "-":
        return fallback
    return clean


def yes_no(value: str | None) -> str:
    raw = (value or "").strip().lower()
    if raw in {"yes", "true", "1", "да"}:
        return "да"
    if raw in {"no", "false", "0", "нет"}:
        return "нет"
    return "нет данных"


def format_pending_trade_summary(item: dict[str, Any]) -> str:
    has_caption = "да" if safe_text(str(item.get("raw_caption", "")), fallback="") else "нет"
    has_screen = "да" if safe_text(str(item.get("screenshot_path", "")), fallback="") else "нет"
    return (
        f"intake_id: {safe_text(str(item.get('intake_id', '')))}\n"
        f"дата: {safe_text(str(item.get('created_at', '')))}\n"
        f"статус: {safe_text(str(item.get('status', '')))}\n"
        f"скрин: {has_screen}\n"
        f"caption: {has_caption}"
    )


def format_draft_view(item: dict[str, Any]) -> str:
    parsed = json.dumps(item.get("parsed_fields", {}), ensure_ascii=False, indent=2)
    missing = ", ".join(item.get("missing_fields", [])) if item.get("missing_fields") else "нет"
    return (
        f"Черновик {safe_text(str(item.get('intake_id', '')))}\n"
        f"- screenshot_path: {safe_text(str(item.get('screenshot_path', '')))}\n"
        f"- raw_caption: {safe_text(str(item.get('raw_caption', '')))}\n"
        f"- parsed_fields:\n{parsed}\n"
        f"- missing_fields: {missing}\n"
        f"- status: {safe_text(str(item.get('status', '')))}"
    )


def format_confirmed_trade_summary(summary: dict[str, Any]) -> str:
    return (
        "Сделка сохранена.\n"
        f"- symbol: {safe_text(summary.get('symbol'))}\n"
        f"- side: {safe_text(summary.get('side'))}\n"
        f"- result_usdt: {safe_text(summary.get('result_usdt'))}\n"
        f"- текущий депозит: {safe_text(summary.get('current_deposit'))}\n"
        f"- всего сделок: {safe_text(summary.get('total_trades'))}"
    )


def format_history_summary(index: int, trade: dict[str, str]) -> str:
    return (
        f"{index}. {safe_text(trade.get('date_time'))} | "
        f"{safe_text(trade.get('symbol')).upper()} {safe_text(trade.get('side')).upper()} | "
        f"вход: {safe_text(trade.get('entry'))} | "
        f"результат: {safe_text(trade.get('result_usdt'))}$ | "
        f"R: {safe_text(trade.get('result_r'))} | "
        f"план: {yes_no(trade.get('followed_plan'))}"
    )
