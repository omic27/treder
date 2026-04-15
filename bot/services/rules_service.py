from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from bot.services.trades_service import get_trades


def load_risk_rules(project_root: Path) -> dict:
    path = project_root / "config" / "risk_rules.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


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


def evaluate_rules(project_root: Path) -> list[str]:
    rules = load_risk_rules(project_root)
    trades = get_trades(project_root)

    if not rules:
        return ["risk_rules.json not found or invalid"]

    violations: list[str] = []

    min_lev = rules.get("allowed_leverage", {}).get("min")
    max_lev = rules.get("allowed_leverage", {}).get("max")

    trades_per_day: dict[str, int] = defaultdict(int)
    pnl_per_day: dict[str, float] = defaultdict(float)

    for row in trades:
        trade_id = row.get("trade_id", "unknown")
        dt = row.get("date_time", "")
        trade_day = dt.split("T")[0].split(" ")[0] if dt else "unknown-day"
        trades_per_day[trade_day] += 1

        lev = _to_float(row.get("leverage"))
        if lev is not None and min_lev is not None and lev < float(min_lev):
            violations.append(f"{trade_id}: leverage below minimum ({lev} < {min_lev})")
        if lev is not None and max_lev is not None and lev > float(max_lev):
            violations.append(f"{trade_id}: leverage above maximum ({lev} > {max_lev})")

        pnl = _to_float(row.get("result_usdt"))
        if pnl is not None:
            pnl_per_day[trade_day] += pnl

        notes_blob = f"{row.get('notes', '')} {row.get('status', '')}".lower()
        for never_rule in rules.get("never_rules", []):
            rule_text = str(never_rule).replace("no ", "").strip().lower()
            if rule_text and rule_text in notes_blob:
                violations.append(f"{trade_id}: potential never-rule trigger -> {never_rule}")

    max_trades_per_day = rules.get("max_trades_per_day")
    if max_trades_per_day is not None:
        for day, count in trades_per_day.items():
            if count > int(max_trades_per_day):
                violations.append(f"{day}: trades per day exceeded ({count} > {max_trades_per_day})")

    max_daily_loss = rules.get("max_daily_loss_usdt")
    if max_daily_loss is not None:
        for day, pnl in pnl_per_day.items():
            if pnl < 0 and abs(pnl) > float(max_daily_loss):
                violations.append(f"{day}: daily loss exceeded ({abs(pnl):.2f} > {float(max_daily_loss):.2f})")

    return violations or ["No violations found (or insufficient data)."]
