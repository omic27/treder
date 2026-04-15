from __future__ import annotations

from bot.config import get_settings
from bot.services.stats_service import build_stats_summary, update_stats_report


def main() -> None:
    settings = get_settings()
    path = update_stats_report(settings.project_root)
    stats = build_stats_summary(settings.project_root)
    print(f"updated: {path}")
    print(f"total_trades={stats['total_trades']} total_pnl={stats['total_pnl']:.2f}")


if __name__ == "__main__":
    main()
