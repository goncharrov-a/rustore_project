# Diploma QA Project (UI + API + Mobile)

Проект разделен на 3 независимых блока:

- UI: RuStore (`https://www.rustore.ru/`)
- API: JSONPlaceholder (`https://fakestoreapi.com`)
- Mobile: Wikipedia APK

## Структура

- `tests/ui` — UI тесты
- `tests/api` — API тесты
- `tests/mobile` — Mobile тесты
- `pages` — PageObjects для UI
- `api/endpoints` — endpoint-классы для API
- `models/api` — pydantic-модели request/response
- `schemas/api` — JSON Schema для валидации API
- `config` — конфиги (в том числе mobile local/remote)

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Линтеры и проверки кода

```bash
make lint       # ruff check
make format     # ruff format
make typecheck  # mypy
make qa         # lint + typecheck
```

## Запуск UI

```bash
pytest tests/ui --alluredir=allure-results
allure serve allure-results
```

Параметры окружения UI:

- `UI_BASE_URL` (по умолчанию `https://www.rustore.ru`)
- `UI_BROWSER` (по умолчанию `chrome`)
- `UI_BROWSER_WIDTH` (по умолчанию `1920`)
- `UI_BROWSER_HEIGHT` (по умолчанию `1080`)
- `SELENOID_URL` (опционально, для удаленного запуска)

## Запуск API

```bash
pytest tests/api --alluredir=allure-results
```

Параметры окружения API:

- `API_BASE_URL` (по умолчанию `https://fakestoreapi.com`)
- `API_TIMEOUT` (по умолчанию `10`)

## Запуск Mobile

```bash
cp .env.mobile.local.example .env.mobile.local
# заполнить под устройство/эмулятор
pytest tests/mobile --alluredir=allure-results
```

Или для BrowserStack:

```bash
cp .env.mobile.remote.example .env.mobile.remote
# заполнить USER/KEY
MOBILE_ENV=remote pytest tests/mobile --alluredir=allure-results
```

## Требования диплома

- UI: 7+ тестов, PageObject, Allure шаги и метки
- API: 5+ тестов, GET/POST/DELETE, схемы, модели, логирование и Allure attachments
- Mobile: 3+ тестов, local/remote pydantic-конфиги, dotenv, Allure steps и видео
