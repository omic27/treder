from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bot.config import get_settings
from bot.services.stats_service import build_stats_summary, update_stats_report


def main() -> None:
    settings = get_settings()
    path = update_stats_report(settings.project_root)
    stats = build_stats_summary(settings.project_root)
    print(f"Статистика обновлена: {path}")
    print(
        "Итог: "
        f"сделок={stats['total_trades']}, "
        f"pnl={float(stats['total_pnl']):.2f} USDT, "
        f"депозит={stats['current_deposit'] if stats['current_deposit'] is not None else 'нет данных'}"
    )


if __name__ == "__main__":
    main()
