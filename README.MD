# 🧪 Дипломный QA проект: RuStore (UI + API + Mobile)

<p align="center">
  <img src="./media/images/rustore.jpg" alt="RuStore" width="92%">
</p>

<p align="center">
  <img src="./media/icons/python_logo_and_wordmark.svg" height="42" alt="Python">
  <img src="./media/icons/pytest_logo.svg" height="42" alt="Pytest">
  <img src="./media/icons/selene.png" height="42" alt="Selene">
  <img src="./media/icons/selenium.png" height="42" alt="Selenium">
  <img src="./media/icons/requests.png" height="42" alt="Requests">
  <img src="./media/icons/allure_Report.svg" height="42" alt="Allure">
  <img src="./media/icons/appium.svg" height="42" alt="Appium">
  <img src="./media/icons/android.png" height="42" alt="Android">
  <img src="./media/icons/selenoid.svg" height="42" alt="Selenoid">
  <img src="./media/icons/jenkins.svg" height="42" alt="Jenkins">
  <img src="./media/icons/jira.svg" height="42" alt="Jira">
  <img src="./media/icons/telegram.svg" height="42" alt="Telegram">
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue">
  <img alt="Pytest" src="https://img.shields.io/badge/Pytest-25%20tests-0A9EDC">
  <img alt="UI" src="https://img.shields.io/badge/UI-10-success">
  <img alt="API" src="https://img.shields.io/badge/API-8-success">
  <img alt="Mobile" src="https://img.shields.io/badge/Mobile-7-success">
</p>

<p align="center">
  <a href="https://jenkins.autotests.cloud/job/goncharov_final/">Jenkins</a> •
  <a href="https://allure.autotests.cloud/project/5147/dashboards">Allure TestOps</a> •
  <a href="https://jira.autotests.cloud/browse/HOMEWORK-1588">Jira</a>
</p>

---

## Содержание

- [О проекте](#о-проекте)
- [Технологии и роль](#технологии-и-роль)
- [Что покрыто](#что-покрыто)
- [Схема работы CI и отчетности](#схема-работы-ci-и-отчетности)
- [Быстрый запуск](#быстрый-запуск)
- [Команды запуска](#команды-запуска)
- [Отчеты и интеграции](#отчеты-и-интеграции)
- [Сценарий защиты (2-3 минуты)](#сценарий-защиты-2-3-минуты)
- [Инженерные фишки проекта](#инженерные-фишки-проекта)
- [Roadmap](#roadmap)

---

## О проекте

Единый дипломный репозиторий по автоматизации тестирования:

1. **UI** — web-тесты [RuStore](https://www.rustore.ru/) с PageObject + Selene
2. **API** — тесты [FakeStore API](https://fakestoreapi.com/docs) через endpoint-слой
3. **Mobile** — Android-тесты Wikipedia APK через Appium

Цель проекта: показать полный QA-контур (Web + API + Mobile) с CI, Allure/TestOps, Jira и Telegram-уведомлениями.

---

## Технологии и роль

| Инструмент            | Что делает в проекте                                  |
|-----------------------|-------------------------------------------------------|
| Python                | Язык автотестов                                       |
| Pytest                | Запуск тестов, фикстуры, маркировка (`ui/api/mobile`) |
| Selene + Selenium     | UI-автоматизация веб-интерфейса RuStore               |
| Requests              | Отправка HTTP-запросов в API-тестах                   |
| Pydantic              | Модели request/response и валидация структуры         |
| JSON Schema           | Проверка схем ответа и запросов API                   |
| Appium + UiAutomator2 | Mobile-автотесты Android-приложения                   |
| Allure Report         | Локальный HTML-отчет по прогонам                      |
| Allure TestOps        | Централизованное хранение прогонов и аналитика        |
| Jenkins               | CI-запуск тестов по параметрам                        |
| Jira                  | Трассировка автотестов к задачам                      |
| Telegram              | Доставка итогового отчета по завершению прогона       |

---

## Что покрыто

| Блок                    | Кол-во | Фокус проверок                                                |
|-------------------------|-------:|---------------------------------------------------------------|
| UI (`tests/ui`)         |     10 | Главная, хедер, поиск, инструкция, футер, карточка приложения |
| API (`tests/api`)       |      8 | GET/POST/DELETE, статус-коды, значения ответа, JSON Schema    |
| Mobile (`tests/mobile`) |      7 | Главный экран, поиск, валидация результатов, негативные кейсы |

### Тестовая матрица

| Scope         | Маркеры          | Команда                                                    |
|---------------|------------------|------------------------------------------------------------|
| Только UI     | `-m ui`          | `pytest tests/ui -m ui --alluredir=allure-results`         |
| Только API    | `-m api`         | `pytest tests/api -m api --alluredir=allure-results`       |
| Только Mobile | `-m mobile`      | `pytest tests/mobile -m mobile --alluredir=allure-results` |
| UI + API      | `-m "ui or api"` | `pytest tests -m "ui or api" --alluredir=allure-results`   |
| Все           | без фильтра      | `pytest tests --alluredir=allure-results`                  |

---

## Схема работы CI и отчетности

```mermaid
flowchart LR
    A["Pytest test suites\n(UI/API/Mobile)"] --> B["Layers\nPageObjects / Endpoints / Mobile flows"]
    B --> C["Execution\nJenkins or local"]
    C --> D["allure-results"]
    D --> E["Allure Report"]
    D --> F["Allure TestOps"]
    E --> G["Telegram notifications"]
    F --> H["Manual tests & analytics"]
    F --> I["Jira links"]
```

### Структура репозитория

```text
.
├── api/endpoints/              # Endpoint-классы API
├── config/                     # Конфиги (в т.ч. mobile)
├── models/api/                 # Pydantic модели
├── pages/                      # UI PageObjects
├── resources/                  # APK / данные
├── schemas/api/                # JSON-схемы
├── tests/
│   ├── ui/
│   ├── api/
│   └── mobile/
├── media/
│   ├── icons/
│   └── images/
├── Jenkinsfile
├── requirements.txt
└── README.MD
```

---

## Быстрый запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Проверка качества:

```bash
make qa
```

---

## Команды запуска

Все тесты:

```bash
pytest tests --alluredir=allure-results
```

UI + API (частый CI-сценарий):

```bash
pytest tests -m "ui or api" --alluredir=allure-results
```

Просмотр отчета локально:

```bash
allure serve allure-results
```

---

## Отчеты и интеграции

- **Allure TestOps:** [goncharov_final_project](https://allure.autotests.cloud/project/5147/dashboards)
- **Jenkins:** [goncharov_final](https://jenkins.autotests.cloud/job/goncharov_final/)
- **Allure Report (последний Jenkins запуск):
  ** [open](https://jenkins.autotests.cloud/job/goncharov_final/lastBuild/allure/)
- **Jira:** [HOMEWORK-1588](https://jira.autotests.cloud/browse/HOMEWORK-1588)

### Allure: главная

<p align="center">
  <img src="media/images/allure_main.jpg" alt="Allure Main" width="86%">
</p>

### Allure: UI

<p align="center">
  <img src="media/images/allure_ui.jpg" alt="Allure UI" width="86%">
</p>

### Allure: API

<p align="center">
  <img src="media/images/allure_api.jpg" alt="Allure API" width="86%">
</p>

### Allure: Mobile

<p align="center">
  <img src="media/images/allure_mobile.jpg" alt="Allure Mobile" width="86%">
</p>

### Allure TestOps: прогон

<p align="center">
  <img src="media/images/testOps.jpg" alt="Allure TestOps Run" width="92%">
</p>

### Telegram-уведомление

<p align="center">
  <img src="media/images/tg.jpg" alt="Telegram Notification" width="34%">
</p>

### Пример mobile-прогона

<p align="center">
  <img src="media/images/demo.gif" alt="Mobile run demo" width="320">
</p>

---

## Инженерные фишки проекта

- Единый стиль Allure-разметки (epic/feature/story, tags, severity, ids).
- Endpoint-слой и модели для API (request/response + schema validation).
- UI attachments: screenshot / page source / browser logs / video URL.
- Jenkins-параметры для гибкого запуска по scope.
- Retry-механизм для нестабильных внешних API-ответов в CI.

---
