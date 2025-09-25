exchange_rates = [
    {"ccy":"EUR","base_ccy":"UAH","buy":"48.22000","sale":"49.01961"},
    {"ccy":"USD","base_ccy":"UAH","buy":"41.10000","sale":"41.66667"}
]

def stependia_valutes():
    stependia = float(input("Ваша стипендія?: "))
    valutes = input("В яку валюту перевести? Приклад: USD, EUR: ")

    if valutes == "EUR" or valutes == "USD":
        for x in exchange_rates:
            if x["ccy"] == valutes:
                print("Ваша стипендія у", valutes, "=", round(stependia / float(x["buy"]), 2))
    else:
        print("Неправильна валюта")

stependia_valutes()
