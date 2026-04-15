from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitActionResult:
    ok: bool
    message: str


def commit_and_push_placeholder(project_root: Path) -> GitActionResult:
    _ = project_root
    return GitActionResult(
        ok=False,
        message="GitHub automation is disabled in v1. Use manual git commit/push.",
    )
