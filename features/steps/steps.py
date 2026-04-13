import os

import requests
from behave import given, then, when


@given('базовый URL API "{base_url}"')
def step_set_base_url(context, base_url):
    context.base_url = base_url


@given('получен курс валюты "{code}"')
def step_get_rate(context, code):
    base_url = getattr(context, "base_url", os.getenv("TEST_BASE_URL", "http://127.0.0.1:5000"))
    context.base_url = base_url

    response = requests.get(f"{base_url}/api/rates/{code}", timeout=10)
    context.rate_response = response
    context.rate_data = response.json()
    context.from_code = code.upper()

    assert response.status_code == 200, f"Ожидался статус 200 для курса, получен {response.status_code}"
    context.from_rate = float(context.rate_data["rate_to_byn"])


@when('выполняется POST запрос конвертации из "{from_code}" в "{to_code}" на сумму "{amount}"')
def step_post_convert(context, from_code, to_code, amount):
    base_url = getattr(context, "base_url", os.getenv("TEST_BASE_URL", "http://127.0.0.1:5000"))
    context.base_url = base_url

    payload = {
        "from": from_code,
        "to": to_code,
        "amount": float(amount),
    }

    context.request_payload = payload
    context.convert_response = requests.post(
        f"{base_url}/api/convert",
        json=payload,
        timeout=10,
    )
    context.convert_data = context.convert_response.json()


@then("ответ имеет статус 200")
def step_status_200(context):
    assert context.convert_response.status_code == 200, (
        f"Ожидался статус 200, получен {context.convert_response.status_code}. "
        f"Ответ: {context.convert_data}"
    )


@then("ответ имеет статус 400")
def step_status_400(context):
    assert context.convert_response.status_code == 400, (
        f"Ожидался статус 400, получен {context.convert_response.status_code}. "
        f"Ответ: {context.convert_data}"
    )


@then("результат конвертации математически корректен")
def step_validate_math(context):
    to_code = context.request_payload["to"].upper()
    amount = float(context.request_payload["amount"])
    result = float(context.convert_data["result"])

    rate_response = requests.get(f"{context.base_url}/api/rates/{to_code}", timeout=10)
    assert rate_response.status_code == 200, (
        f"Не удалось получить курс целевой валюты {to_code}, статус {rate_response.status_code}"
    )
    to_rate = float(rate_response.json()["rate_to_byn"])

    expected = round((amount * context.from_rate) / to_rate, 2)
    assert result == expected, f"Ожидалось {expected}, получено {result}"


@then("в ответе есть поле ошибки")
def step_error_field(context):
    assert isinstance(context.convert_data, dict), "Ответ не является JSON-объектом"
    assert "error" in context.convert_data, "В ответе отсутствует поле error"
    assert context.convert_data["error"], "Поле error пустое"
