from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bot.config import get_settings
from bot.services.review_service import has_meaningful_weekly_content, read_weekly_review


def main() -> None:
    settings = get_settings()
    text = read_weekly_review(settings.project_root)
    if not has_meaningful_weekly_content(text):
        print("Недельный обзор пока не заполнен.")
        return
    print(text)


if __name__ == "__main__":
    main()
