import requests


print("--- Конвертер стипендії ---")

url_privat = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
exchange_rates = requests.get(url_privat).json()

stependia_str = input("Ваша стипендія в UAH?: ")
valuta = input("В яку валюту перевести? (USD або EUR): ").upper()

stependia = float(stependia_str) 

is_found = False
for rate in exchange_rates:
    if rate["ccy"] == valuta:
        result = round(stependia / float(rate["buy"]), 2)
        print(f"Ваша стипендія у {valuta} = {result}")
        is_found = True
        break

if not is_found:
    print("Таку валюту не знайдено. Доступні: USD, EUR.")



print("\n--- Інформація про валюту країни ---")

country_name = "Luxembourg"
url_country = f"https://restcountries.com/v3.1/name/{country_name}"

country_data_list = requests.get(url_country).json()

country_info = country_data_list[0]
name = country_info['name']['common']

currencies_dict = country_info['currencies'] 
currency_info = list(currencies_dict.values())[0]
currency_name = currency_info['name']

print(f"{name} - {currency_name}")
