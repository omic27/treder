from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    bot_owner_chat_id: int | None
    project_root: Path
    enable_git_push: bool


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_settings() -> Settings:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    owner_chat_id_raw = os.getenv("BOT_OWNER_CHAT_ID", "").strip()
    owner_chat_id = int(owner_chat_id_raw) if owner_chat_id_raw else None

    default_root = Path(__file__).resolve().parents[1]
    project_root = Path(os.getenv("PROJECT_ROOT", str(default_root))).expanduser().resolve()

    return Settings(
        telegram_bot_token=token,
        bot_owner_chat_id=owner_chat_id,
        project_root=project_root,
        enable_git_push=_to_bool(os.getenv("ENABLE_GIT_PUSH"), default=False),
    )
