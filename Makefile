.PHONY: install install-dev install-browsers test-unit test-api test-ui test-all allure-generate run

install:
	python -m pip install -r requirements.txt

install-dev:
	python -m pip install -r requirements-dev.txt

install-browsers:
	python -m playwright install --with-deps

test-unit:
	pytest tests/unit --alluredir=allure-results/unit --html=reports/unit-report.html --self-contained-html

test-api:
	python scripts/run_with_server.py --server-cmd "python app.py" --target-url "http://127.0.0.1:5000/health" -- behave -f allure_behave.formatter:AllureFormatter -o allure-results/api features

test-ui:
	python scripts/run_with_server.py --server-cmd "python app.py" --target-url "http://127.0.0.1:5000/health" -- pytest tests/ui --alluredir=allure-results/ui --html=reports/ui-report.html --self-contained-html

allure-generate:
	allure generate allure-results --clean -o allure-report

test-all: test-unit test-api test-ui

run:
	python app.py
