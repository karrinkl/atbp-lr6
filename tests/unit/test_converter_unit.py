import pytest

from app import app, convert_amount


@pytest.mark.parametrize(
    ("from_code", "to_code", "amount", "expected"),
    [
        ("USD", "BYN", 100, 320.0),
        ("EUR", "BYN", 10, 35.0),
        ("BYN", "RUB", 1, 28.57),
        ("RUB", "EUR", 1000, 10.0),
    ],
)
def test_convert_amount_math(from_code, to_code, amount, expected):
    assert convert_amount(from_code, to_code, amount) == expected


def test_health_endpoint():
    with app.test_client() as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json() == {"status": "ok"}
