# treder

BTC futures trading operating system for manual trade journaling, risk control, and analytics.

## Telegram Bot v1

Minimal local Telegram bot for journal operations and analytics delivery.

### What the bot does

- Reads local project files from `data/`, `config/`, and `reports/`
- Shows basic stats summary from recorded trades/equity
- Shows current deposit and recent trades
- Runs manual stats update command
- Runs manual risk-rules check command
- Reads and returns weekly review content

### What the bot does NOT do

- Does not place trades
- Does not connect to any exchange API
- Does not make trading decisions
- Does not require external trading integrations in v1

### Local run

1. Create virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create `.env` from `.env.example` and fill at least:

- `TELEGRAM_BOT_TOKEN`
- `PROJECT_ROOT` (optional; defaults to current repository root)

3. Run bot:

```bash
python -m bot.main
```

### Available commands

- `/start`
- `/help`
- `/stats`
- `/deposit`
- `/lasttrades`
- `/addtrade`
- `/update`
- `/checkrules`
- `/weekly`

### Helper scripts

- `python scripts/update_stats.py`
- `python scripts/check_rules.py`
- `python scripts/weekly_review.py`
