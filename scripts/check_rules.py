from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bot.config import get_settings
from bot.services.rules_service import evaluate_rules


def main() -> None:
    settings = get_settings()
    violations = evaluate_rules(settings.project_root)
    if not violations:
        print("Нарушений правил не обнаружено.")
        return

    print("Обнаружены нарушения:")
    for item in violations:
        print(f"- {item}")


if __name__ == "__main__":
    main()
