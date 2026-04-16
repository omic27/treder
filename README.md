# treder

BTC futures trading operating system for manual trade journaling, risk control, and analytics.

## Telegram Bot v1 (русский интерфейс)

Бот работает только с локальными файлами проекта (`data/`, `config/`, `reports/`) и помогает с учетом сделок и аналитикой.

### Что бот делает

- Показывает статистику, депозит, последние сделки и историю сделок
- Принимает скрин закрытой сделки и создает черновик
- Подтверждает черновик и сохраняет сделку в CSV
- Запускает ручное обновление статистики
- Проверяет риск-правила по локальным данным
- Показывает недельный обзор

### Чего бот не делает

- Не торгует
- Не подключается к бирже
- Не принимает торговые решения
- Не гарантирует доходность
- Не распознает данные со скрина через OCR в v1

### Главное меню (reply keyboard)

- Статистика
- Депозит
- Последние сделки
- Добавить сделку
- Скрин сделки
- Обновить статистику
- Проверить правила
- Недельный обзор
- История
- Помощь

### Inline-навигация

На релевантных экранах используются кнопки:
- Назад
- Обновить
- Далее
- Подтвердить
- Изменить
- Отменить
- Главное меню

### Настройка `.env`

1. Создайте `.env` из шаблона:

```bash
cp .env.example .env
```

2. Откройте `.env` и вручную укажите токен:

```env
TELEGRAM_BOT_TOKEN=PASTE_NEW_TOKEN_HERE
BOT_OWNER_CHAT_ID=
PROJECT_ROOT=
ENABLE_GIT_PUSH=false
```

Важно: не коммитьте `.env` и не публикуйте токен.

### Установка зависимостей

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Локальный запуск

```bash
python3 -m bot.main
```

### Команды

- `/start` — стартовое сообщение и меню
- `/help` — справка
- `/stats` — статистика
- `/deposit` — депозит
- `/lasttrades` — последние 5 сделок
- `/history` — история по 10 сделок с кнопками Далее/Назад
- `/pending` — черновики сделок
- `/showdraft intake_id=...` — показать черновик
- `/confirmtrade` — шаблон подтверждения
- `/confirmtrade intake_id=... symbol=... side=... ...` — подтвердить черновик
- `/canceltrade intake_id=...` — отменить черновик
- `/addtrade` — шаблон ручного ввода
- `/update` — пересчет статистики
- `/checkrules` — проверка риск-правил
- `/weekly` — недельный обзор

## Скрин сделки v1

Flow:
1. Отправьте боту скрин закрытой сделки.
2. Бот сохранит изображение и вернет `intake_id`.
3. Подтвердите поля через `/confirmtrade`.
4. После подтверждения сделка попадет в учет и статистику.

### Где что хранится

- Скрины: `data/screenshots/YYYY-MM/`
- Черновики: `data/pending_trades.json`
- Intake лог: `data/bot_intake_log.csv`
- Журнал сделок: `reports/trade_journal.md`

### Подтверждение черновика

```text
/confirmtrade
```

Бот вернет шаблон:

```text
intake_id=
symbol=BTCUSDT
side=long
entry=
stop_loss=
tp1=
tp2=
leverage=
deposit_before=
deposit_after=
risk_usdt=
position_size_usdt=
result_usdt=
result_r=
status=closed
followed_plan=yes
notes=
```

Можно отправить одной строкой:

```text
/confirmtrade intake_id=... symbol=BTCUSDT side=long entry=... stop_loss=... ...
```

### Отмена и просмотр черновика

- Отмена: `/canceltrade intake_id=...`
- Просмотр: `/showdraft intake_id=...`
- Список pending: `/pending`

### Безопасность токена

- Не храните токен в коде.
- Используйте только `.env`.
- Не выводите токен в логи.
- Логирование HTTP/Telegram снижено до безопасного уровня.

### Вспомогательные скрипты

- `python3 scripts/update_stats.py`
- `python3 scripts/check_rules.py`
- `python3 scripts/weekly_review.py`
