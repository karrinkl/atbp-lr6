from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Фиксированные курсы в базовой валюте BYN
RATES_TO_BYN = {
    "USD": 3.20,
    "EUR": 3.50,
    "RUB": 0.035,
    "BYN": 1.00,
}


def convert_amount(from_code: str, to_code: str, amount: float) -> float:
    amount_in_byn = amount * RATES_TO_BYN[from_code]
    result = amount_in_byn / RATES_TO_BYN[to_code]
    return round(result, 2)


@app.route("/")
def index():
    return render_template("index.html", currencies=sorted(RATES_TO_BYN.keys()))


@app.get("/api/rates/<string:code>")
def get_rate(code: str):
    code = code.upper()
    rate = RATES_TO_BYN.get(code)
    if rate is None:
        return jsonify({"error": f"Неподдерживаемая валюта: {code}"}), 404
    return jsonify({"currency": code, "rate_to_byn": rate})


@app.post("/api/convert")
def convert():
    payload = request.get_json(silent=True) or {}

    from_code = str(payload.get("from", "")).upper()
    to_code = str(payload.get("to", "")).upper()
    amount = payload.get("amount")

    if from_code not in RATES_TO_BYN or to_code not in RATES_TO_BYN:
        return jsonify({"error": "Неподдерживаемая валюта"}), 400

    if from_code == to_code:
        return jsonify({"error": "Валюты from и to не должны совпадать"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "Некорректная сумма"}), 400

    if amount < 0:
        return jsonify({"error": "Сумма не может быть отрицательной"}), 400

    converted = convert_amount(from_code, to_code, amount)
    return (
        jsonify(
            {
                "from": from_code,
                "to": to_code,
                "amount": amount,
                "result": converted,
            }
        ),
        200,
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)
