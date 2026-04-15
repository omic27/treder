from __future__ import annotations

from pathlib import Path


PLACEHOLDER_TOKENS = {
    "performance summary",
    "what worked",
    "what failed",
    "repeated mistakes",
    "best setups",
    "changes to risk rules",
    "plan for improvement",
}


def read_weekly_review(project_root: Path) -> str:
    path = project_root / "reports" / "weekly_review.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def read_monthly_review(project_root: Path) -> str:
    path = project_root / "reports" / "monthly_review.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def has_meaningful_weekly_content(text: str) -> bool:
    if not text.strip():
        return False

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    content_lines = [line for line in lines if not line.startswith("#")]
    if not content_lines:
        return False

    lowered = [line.lower() for line in content_lines if line != "-"]
    meaningful = [line for line in lowered if line not in PLACEHOLDER_TOKENS]
    return len(meaningful) > 0
