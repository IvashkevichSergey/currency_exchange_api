import requests
from app.settings.config import settings

EXTERNAL_API_URL = 'https://api.apilayer.com/exchangerates_data'
header_params = {'apikey': settings.EXTERNAL_API_KEY}


def get_all_currencies():
    try:
        response = requests.get(
            f'{EXTERNAL_API_URL}/symbols',
            headers=header_params
        )
    except Exception as e:
        print(e)
        return False
    return response.json()['symbols']


def exchange_currencies(change_from, change_to, change_amount):
    try:
        response = requests.get(
            f'{EXTERNAL_API_URL}/convert?to={change_to}&from={change_from}&amount={change_amount}',
            headers=header_params
        )
    except Exception as e:
        print(e)
        return False
    return response.json()['result']