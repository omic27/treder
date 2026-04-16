from __future__ import annotations

import json
import re
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any

from bot.utils.csv_io import append_csv_row, ensure_csv_header, read_csv_rows

BASE_TRADE_FIELDS = [
    "trade_id",
    "date_time",
    "symbol",
    "side",
    "setup_name",
    "timeframe_context",
    "entry",
    "stop_loss",
    "tp1",
    "tp2",
    "leverage",
    "deposit_before",
    "risk_usdt",
    "position_size_usdt",
    "result_usdt",
    "result_r",
    "status",
    "followed_plan",
    "notes",
]

EXTRA_TRADE_FIELDS = [
    "deposit_after",
    "screenshot_path",
    "source",
    "created_at",
]

TRADE_FIELDS = BASE_TRADE_FIELDS + EXTRA_TRADE_FIELDS

CONFIRM_REQUIRED_FIELDS = [
    "symbol",
    "side",
    "entry",
    "stop_loss",
    "tp1",
    "tp2",
    "leverage",
    "deposit_before",
    "deposit_after",
    "risk_usdt",
    "position_size_usdt",
    "result_usdt",
    "result_r",
    "status",
    "followed_plan",
    "notes",
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text or text == "-":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _safe_filename(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", name).strip("_") or "file"


def _storage_paths(project_root: Path) -> dict[str, Path]:
    return {
        "screenshots": project_root / "data" / "screenshots",
        "pending_dir": project_root / "data" / "pending",
        "logs": project_root / "data" / "logs",
        "pending_json": project_root / "data" / "pending_trades.json",
        "intake_log": project_root / "data" / "bot_intake_log.csv",
        "trades": project_root / "data" / "trades.csv",
        "equity": project_root / "data" / "equity_curve.csv",
        "journal": project_root / "reports" / "trade_journal.md",
    }


def ensure_storage(project_root: Path) -> None:
    paths = _storage_paths(project_root)
    paths["screenshots"].mkdir(parents=True, exist_ok=True)
    paths["pending_dir"].mkdir(parents=True, exist_ok=True)
    paths["logs"].mkdir(parents=True, exist_ok=True)

    if not paths["pending_json"].exists():
        paths["pending_json"].write_text("[]\n", encoding="utf-8")

    ensure_csv_header(
        paths["intake_log"],
        [
            "intake_id",
            "created_at",
            "telegram_user_id",
            "telegram_message_id",
            "screenshot_path",
            "has_caption",
            "status",
        ],
    )

    ensure_trades_schema(project_root)
    ensure_csv_header(
        paths["equity"],
        ["date_time", "trade_id", "deposit_after", "change_usdt", "change_pct"],
    )

    if not paths["journal"].exists():
        paths["journal"].write_text("# Trade Journal\n\n", encoding="utf-8")


def trades_file(project_root: Path) -> Path:
    return _storage_paths(project_root)["trades"]


def ensure_trades_schema(project_root: Path) -> None:
    ensure_csv_header(trades_file(project_root), TRADE_FIELDS)


def get_trades(project_root: Path) -> list[dict[str, str]]:
    ensure_storage(project_root)
    return read_csv_rows(trades_file(project_root))


def get_last_trades(project_root: Path, limit: int = 5) -> list[dict[str, str]]:
    rows = get_trades(project_root)
    if not rows:
        return []
    return list(reversed(rows[-limit:]))


def get_history_page(
    project_root: Path,
    *,
    page: int,
    page_size: int = 10,
) -> tuple[list[dict[str, str]], int, int, int]:
    rows = list(reversed(get_trades(project_root)))
    total_rows = len(rows)
    if total_rows == 0:
        return [], 0, 1, 0

    total_pages = max(1, (total_rows + page_size - 1) // page_size)
    safe_page = min(max(page, 0), total_pages - 1)
    start = safe_page * page_size
    end = start + page_size
    return rows[start:end], safe_page, total_pages, total_rows


def _load_pending(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    if isinstance(raw, dict) and isinstance(raw.get("items"), list):
        return [item for item in raw["items"] if isinstance(item, dict)]
    return []


def _save_pending(path: Path, items: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _extract_pairs(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    tokens = re.split(r"\s+", text.strip())
    for token in tokens:
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        key = key.strip().lower()
        value = value.strip()
        if key:
            fields[key] = value
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().lower()
        value = value.strip()
        if key:
            fields[key] = value
    return fields


def new_intake_id() -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"intake_{ts}_{secrets.token_hex(3)}"


def save_screenshot_file(
    project_root: Path,
    *,
    file_bytes: bytes,
    source_name: str,
) -> str:
    ensure_storage(project_root)
    folder = _storage_paths(project_root)["screenshots"] / datetime.now().strftime("%Y-%m")
    folder.mkdir(parents=True, exist_ok=True)

    ext = Path(source_name).suffix.lower() or ".jpg"
    filename = _safe_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{secrets.token_hex(4)}{ext}")
    path = folder / filename
    path.write_bytes(file_bytes)
    return str(path.relative_to(project_root))


def create_pending_trade(
    project_root: Path,
    *,
    telegram_user_id: int,
    telegram_message_id: int,
    screenshot_path: str,
    raw_caption: str,
) -> dict[str, Any]:
    ensure_storage(project_root)
    paths = _storage_paths(project_root)
    items = _load_pending(paths["pending_json"])

    parsed = {
        key: value
        for key, value in _extract_pairs(raw_caption).items()
        if key in CONFIRM_REQUIRED_FIELDS
    }
    missing = [field for field in CONFIRM_REQUIRED_FIELDS if not parsed.get(field)]

    item = {
        "intake_id": new_intake_id(),
        "telegram_user_id": telegram_user_id,
        "telegram_message_id": telegram_message_id,
        "created_at": now_iso(),
        "screenshot_path": screenshot_path,
        "raw_caption": raw_caption,
        "parsed_fields": parsed,
        "missing_fields": missing,
        "status": "pending",
    }

    items.append(item)
    _save_pending(paths["pending_json"], items)

    append_csv_row(
        paths["intake_log"],
        {
            "intake_id": item["intake_id"],
            "created_at": item["created_at"],
            "telegram_user_id": str(telegram_user_id),
            "telegram_message_id": str(telegram_message_id),
            "screenshot_path": screenshot_path,
            "has_caption": "yes" if raw_caption.strip() else "no",
            "status": item["status"],
        },
        [
            "intake_id",
            "created_at",
            "telegram_user_id",
            "telegram_message_id",
            "screenshot_path",
            "has_caption",
            "status",
        ],
    )

    return item


def get_pending_trades(project_root: Path) -> list[dict[str, Any]]:
    ensure_storage(project_root)
    items = _load_pending(_storage_paths(project_root)["pending_json"])
    return list(reversed(items))


def get_pending_by_id(project_root: Path, intake_id: str) -> dict[str, Any] | None:
    for item in get_pending_trades(project_root):
        if str(item.get("intake_id")) == intake_id:
            return item
    return None


def update_pending_status(project_root: Path, intake_id: str, new_status: str) -> bool:
    ensure_storage(project_root)
    path = _storage_paths(project_root)["pending_json"]
    items = _load_pending(path)
    changed = False

    for item in items:
        if str(item.get("intake_id")) == intake_id:
            item["status"] = new_status
            item["updated_at"] = now_iso()
            changed = True
            break

    if changed:
        _save_pending(path, items)
    return changed


def _next_trade_id(project_root: Path) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"tr_{ts}_{secrets.token_hex(2)}"


def _append_trade_journal(project_root: Path, row: dict[str, str]) -> None:
    journal = _storage_paths(project_root)["journal"]
    block = (
        f"## {row.get('created_at', now_iso())}\n"
        f"- trade_id: {row.get('trade_id', '-')}\n"
        f"- symbol: {row.get('symbol', '-')}\n"
        f"- side: {row.get('side', '-')}\n"
        f"- result_usdt: {row.get('result_usdt', '-')}\n"
        f"- result_r: {row.get('result_r', '-')}\n"
        f"- screenshot_path: {row.get('screenshot_path', '-')}\n"
        f"- note: {row.get('notes', '-')}\n\n"
    )
    with journal.open("a", encoding="utf-8") as file:
        file.write(block)


def _append_equity_row(project_root: Path, trade_row: dict[str, str]) -> None:
    paths = _storage_paths(project_root)

    before = _to_float(trade_row.get("deposit_before"))
    after = _to_float(trade_row.get("deposit_after"))
    pnl = _to_float(trade_row.get("result_usdt"))

    if after is None and before is not None and pnl is not None:
        after = before + pnl

    if after is None:
        return

    change_usdt = 0.0 if before is None else after - before
    change_pct = 0.0
    if before not in (None, 0.0):
        change_pct = (change_usdt / before) * 100.0

    append_csv_row(
        paths["equity"],
        {
            "date_time": trade_row.get("date_time", now_iso()),
            "trade_id": trade_row.get("trade_id", "-"),
            "deposit_after": f"{after:.2f}",
            "change_usdt": f"{change_usdt:.2f}",
            "change_pct": f"{change_pct:.2f}",
        },
        ["date_time", "trade_id", "deposit_after", "change_usdt", "change_pct"],
    )


def get_confirmtrade_template() -> str:
    return (
        "intake_id=\n"
        "symbol=BTCUSDT\n"
        "side=long\n"
        "entry=\n"
        "stop_loss=\n"
        "tp1=\n"
        "tp2=\n"
        "leverage=\n"
        "deposit_before=\n"
        "deposit_after=\n"
        "risk_usdt=\n"
        "position_size_usdt=\n"
        "result_usdt=\n"
        "result_r=\n"
        "status=closed\n"
        "followed_plan=yes\n"
        "notes="
    )


def parse_confirmation_payload(text: str) -> dict[str, str]:
    clean = text.strip()
    if clean.startswith("/confirmtrade"):
        clean = clean[len("/confirmtrade") :].strip()
    return _extract_pairs(clean)


def confirm_pending_trade(
    project_root: Path,
    payload: dict[str, str],
) -> tuple[bool, str, dict[str, str] | None]:
    ensure_storage(project_root)

    intake_id = payload.get("intake_id", "").strip()
    if not intake_id:
        return False, "Не указан intake_id.", None

    path = _storage_paths(project_root)["pending_json"]
    items = _load_pending(path)
    pending: dict[str, Any] | None = None
    for item in items:
        if str(item.get("intake_id")) == intake_id:
            pending = item
            break

    if pending is None:
        return False, "Черновик не найден.", None

    if str(pending.get("status")) != "pending":
        return False, f"Черновик в статусе '{pending.get('status')}', подтверждение недоступно.", None

    merged: dict[str, str] = {
        key: str(value)
        for key, value in (pending.get("parsed_fields") or {}).items()
        if key in CONFIRM_REQUIRED_FIELDS
    }
    for key, value in payload.items():
        if key in CONFIRM_REQUIRED_FIELDS:
            merged[key] = value

    missing = [field for field in CONFIRM_REQUIRED_FIELDS if not merged.get(field, "").strip()]
    pending["parsed_fields"] = merged
    pending["missing_fields"] = missing

    if missing:
        _save_pending(path, items)
        return False, "Не хватает полей: " + ", ".join(missing), None

    trade_id = _next_trade_id(project_root)
    created_at = now_iso()
    row = {
        "trade_id": trade_id,
        "date_time": created_at,
        "symbol": merged.get("symbol", "-"),
        "side": merged.get("side", "-"),
        "setup_name": merged.get("setup_name", "-"),
        "timeframe_context": merged.get("timeframe_context", "-"),
        "entry": merged.get("entry", "-"),
        "stop_loss": merged.get("stop_loss", "-"),
        "tp1": merged.get("tp1", "-"),
        "tp2": merged.get("tp2", "-"),
        "leverage": merged.get("leverage", "-"),
        "deposit_before": merged.get("deposit_before", "-"),
        "risk_usdt": merged.get("risk_usdt", "-"),
        "position_size_usdt": merged.get("position_size_usdt", "-"),
        "result_usdt": merged.get("result_usdt", "-"),
        "result_r": merged.get("result_r", "-"),
        "status": merged.get("status", "-"),
        "followed_plan": merged.get("followed_plan", "-"),
        "notes": merged.get("notes", "-"),
        "deposit_after": merged.get("deposit_after", "-"),
        "screenshot_path": str(pending.get("screenshot_path", "-")),
        "source": "screenshot_intake_v1",
        "created_at": created_at,
    }

    append_csv_row(trades_file(project_root), row, TRADE_FIELDS)
    _append_equity_row(project_root, row)
    _append_trade_journal(project_root, row)

    pending["status"] = "confirmed"
    pending["confirmed_at"] = now_iso()
    pending["missing_fields"] = []
    _save_pending(path, items)

    return True, "ok", row


def cancel_pending_trade(project_root: Path, intake_id: str) -> tuple[bool, str]:
    if not intake_id.strip():
        return False, "Не указан intake_id."

    ensure_storage(project_root)
    path = _storage_paths(project_root)["pending_json"]
    items = _load_pending(path)

    for item in items:
        if str(item.get("intake_id")) == intake_id:
            if str(item.get("status")) == "confirmed":
                return False, "Черновик уже подтвержден, отмена недоступна."
            item["status"] = "canceled"
            item["canceled_at"] = now_iso()
            _save_pending(path, items)
            return True, "Черновик отменен."

    return False, "Черновик не найден."
