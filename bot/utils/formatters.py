from __future__ import annotations


def format_money(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.2f} USDT"


def format_percent(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.2f}%"


def safe_text(value: str | None, fallback: str = "-") -> str:
    if value is None:
        return fallback
    clean = value.strip()
    return clean if clean else fallback
