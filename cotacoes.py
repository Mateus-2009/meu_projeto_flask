import requests

# Função para buscar as cotações
def get_currency_rates():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    response = requests.get(url)
    data = response.json()

    rates = {
        "USD_BRL": f'{float(data["USDBRL"]["bid"]):.2f}',
        "EUR_BRL": f'{float(data["EURBRL"]["bid"]):.2f}',
        "BTC_BRL": f'{float(data["BTCBRL"]["bid"]):.2f}',
    }
    return rates