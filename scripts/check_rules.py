from __future__ import annotations

from bot.config import get_settings
from bot.services.rules_service import evaluate_rules


def main() -> None:
    settings = get_settings()
    violations = evaluate_rules(settings.project_root)
    print("rule_check_result:")
    for item in violations:
        print(f"- {item}")


if __name__ == "__main__":
    main()
