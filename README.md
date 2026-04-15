# treder

BTC futures trading operating system for manual trade journaling, risk control, and analytics.

## Telegram Bot v1

Minimal local Telegram bot for journal operations and analytics delivery.

### What the bot does

- Reads local project files from `data/`, `config/`, and `reports/`
- Shows stats summary from recorded trades/equity
- Shows current deposit and recent trades
- Runs manual stats update command
- Runs manual risk-rules check command
- Reads and returns weekly review content

### What the bot does NOT do

- Does not place trades
- Does not connect to any exchange API
- Does not make trading decisions
- Does not require external trading integrations in v1

### Setup `.env`

1. Create `.env` from template:

```bash
cp .env.example .env
```

2. Open `.env` and manually set token value (do not commit secrets):

```env
TELEGRAM_BOT_TOKEN=PASTE_NEW_TOKEN_HERE
BOT_OWNER_CHAT_ID=
PROJECT_ROOT=
ENABLE_GIT_PUSH=false
```

### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run bot locally

```bash
python3 -m bot.main
```

### Commands

- `/start` - bot info and scope
- `/help` - available commands
- `/stats` - total trades, win rate, total pnl, current deposit, average R
- `/deposit` - current deposit
- `/lasttrades` - latest 5 trades
- `/addtrade` - trade input template
- `/update` - refresh `reports/stats.md`
- `/checkrules` - validate `config/risk_rules.json`
- `/weekly` - show `reports/weekly_review.md`

### Quick command check

- `/start`
- `/stats`
- `/checkrules`

### Helper scripts

- `python3 scripts/update_stats.py`
- `python3 scripts/check_rules.py`
- `python3 scripts/weekly_review.py`
