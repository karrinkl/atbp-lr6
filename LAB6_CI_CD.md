# Лабораторная работа №6: CI/CD для комплексных тестов

В проект добавлен полноценный CI/CD пайплайн под текущий стек (Flask + pytest + behave + Playwright):

- Параллельные job для `unit`, `api (BDD)` и `ui`.
- Матрица ОС (`ubuntu`, `windows`, `macos`) и версий Python (`3.10`, `3.11`, `3.12`) для unit/api.
- Матрица браузеров (`chromium`, `firefox`, `webkit`) для UI.
- Проверка workflow линтером `actionlint`.
- Генерация Allure-отчета из всех типов тестов.
- Публикация Allure на GitHub Pages (для ветки `main`).
- Telegram-уведомление о результате прогона.
- Docker-этап (продвинутый уровень): запуск тестов внутри контейнера.
- Кэширование зависимостей `pip` и браузеров Playwright.

## Что добавлено

- Workflow: `.github/workflows/ci.yml`
- Unit-тесты: `tests/unit/test_converter_unit.py`
- UI-тесты: `tests/ui/test_converter_ui.py`
- Общая фикстура тестов: `tests/conftest.py`
- Скрипты для запуска тестов с сервером:
  - `scripts/wait_for_url.py`
  - `scripts/run_with_server.py`
- Файлы зависимостей:
  - `requirements.txt`
  - `requirements-dev.txt`
- Конфиг pytest: `pytest.ini`
- Make-цели для локального запуска: `Makefile`
- Docker: `Dockerfile`
- Добавлен endpoint health-check: `/health` в `app.py`

## Локальный запуск

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install --with-deps
```

Запуск по типам тестов:

```bash
pytest tests/unit --alluredir=allure-results/unit
python scripts/run_with_server.py --server-cmd "python app.py" --target-url "http://127.0.0.1:5000/health" -- behave -f allure_behave.formatter:AllureFormatter -o allure-results/api features
python scripts/run_with_server.py --server-cmd "python app.py" --target-url "http://127.0.0.1:5000/health" -- pytest tests/ui --browser chromium --alluredir=allure-results/ui
```

Генерация отчета Allure:

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

## Настройка секретов в GitHub

В репозитории добавить:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Без этих секретов Telegram-шаг будет автоматически пропущен.

## Проверка workflow через actionlint локально

Linux/macOS:

```bash
bash <(curl https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
actionlint .github/workflows/ci.yml
```

Windows (через Docker):

```bash
docker run --rm -v "$PWD:/repo" -w /repo rhysd/actionlint:latest actionlint .github/workflows/ci.yml
```
