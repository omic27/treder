from __future__ import annotations

from bot.config import get_settings
from bot.services.review_service import read_weekly_review


def main() -> None:
    settings = get_settings()
    print(read_weekly_review(settings.project_root))


if __name__ == "__main__":
    main()
