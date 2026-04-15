from __future__ import annotations

from pathlib import Path


def read_weekly_review(project_root: Path) -> str:
    path = project_root / "reports" / "weekly_review.md"
    if not path.exists():
        return "weekly_review.md not found"
    return path.read_text(encoding="utf-8").strip()


def read_monthly_review(project_root: Path) -> str:
    path = project_root / "reports" / "monthly_review.md"
    if not path.exists():
        return "monthly_review.md not found"
    return path.read_text(encoding="utf-8").strip()
