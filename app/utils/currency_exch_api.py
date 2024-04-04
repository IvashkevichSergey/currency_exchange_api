import requests
from fastapi import HTTPException
from requests import Response
from starlette import status

from app.exceptions import ExternalAPIException
from app.settings.config import settings

EXTERNAL_API_URL = 'https://api.apilayer.com/exchangerates_data'
header_params = {'apikey': settings.EXTERNAL_API_KEY}


def response_checker(response: Response, data_str: str):
    if response.json().get("error"):
        raise HTTPException(detail=response.json()["error"],
                            status_code=status.HTTP_400_BAD_REQUEST)
    return response.json()[data_str]


def get_all_currencies():
    try:
        response = requests.get(
            f'{EXTERNAL_API_URL}/symbols',
            headers=header_params
        )
    except Exception as e:
        raise ExternalAPIException(detail=str(e))
    return response_checker(response, "symbols")


def exchange_currencies(change_from, change_to, change_amount):
    try:
        response = requests.get(
            f'{EXTERNAL_API_URL}/convert?to={change_to}&from={change_from}&amount={change_amount}',
            headers=header_params
        )
    except Exception as e:
        raise ExternalAPIException(detail=str(e))
    return response_checker(response, "result")


def get_rate(change_from, change_to):
    try:
        response = requests.get(
            f'{EXTERNAL_API_URL}/convert?to={change_to}&from={change_from}&amount=1',
            headers=header_params
        )
    except Exception as e:
        raise ExternalAPIException(detail=str(e))
    return response_checker(response, "result")
