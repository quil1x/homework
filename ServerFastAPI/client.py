import requests


def run_client():
    currency = input("Валюта: ").strip()
    amount = float(input("Сума: ").strip())

    server_url = "http://127.0.0.1:8000/convert"

    response = requests.get(server_url, params={"currency": currency, "amount": amount})
    data = response.json()

    if "converted_amount" in data:
        print(f"{amount} {currency.upper()} = {data['converted_amount']} UAH.")
    else:
        print("Помилка.")


if __name__ == "__main__":
    run_client()