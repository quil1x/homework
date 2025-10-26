import requests
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/convert")
async def convert_currency(
        currency: str = Query(),
        amount: float = Query()
):
    rates = requests.get("https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5").json()
    currency_code = currency.upper()

    rate_value = next(
        (float(rate["buy"]) for rate in rates if rate["ccy"] == currency_code),
        None
    )

    if rate_value:
        converted_amount = amount * rate_value
        return {
            "source_currency": currency_code,
            "converted_amount": round(converted_amount, 2)
        }

    return {"error": "Currency not supported"}