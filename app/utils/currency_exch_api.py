import requests
from fastapi import HTTPException
from requests import Response
from starlette import status
from app.exceptions import ExternalAPIException
from app.settings.config import settings

# Necessary params for requesting external API
EXTERNAL_API_URL = 'https://api.apilayer.com/exchangerates_data'
header_params = {'apikey': settings.EXTERNAL_API_KEY}


def response_checker(response: Response, data_str: str):
    """
    Check if request to external API is responding without error
    :param response: The Response class object, that contains a
    server's response to an HTTP request
    :param data_str: A key (str) parameter that defines data extracted
    from the response
    :return: list of currencies or the exact number of currency
    depending on the data_str param
    :raises fastapi.exceptions.HTTPException: If the response body
            contain error message
    """
    if response.json().get("error"):
        raise HTTPException(detail=response.json()["error"],
                            status_code=status.HTTP_400_BAD_REQUEST)
    return response.json()[data_str]


def get_all_currencies():
    """
    Makes request to external API and returns all supported currencies to
    exchange or raise custom Exception otherwise
    :return: list of currencies
    :raises custom Exception if server does not respond
    """
    try:
        response = requests.get(
            f'{EXTERNAL_API_URL}/symbols',
            headers=header_params
        )
    except Exception as e:
        raise ExternalAPIException(detail=str(e))
    return response_checker(response, "symbols")


def exchange_currencies(change_from: str,
                        change_to: str,
                        change_amount: int):
    """
    Makes request to external API and returns the exact number of currency
    to exchange from one currency to another
    :param change_from: a currency you'd like to exchange
    :param change_to: a currency you'd like to exchange into
    :param change_amount: amount of currency to exchange
    :return: summary about requested exchange
    :raises custom Exception if server does not respond
    """
    try:
        response = requests.get(
            f'{EXTERNAL_API_URL}/convert?to={change_to}&from={change_from}&amount={change_amount}',
            headers=header_params
        )
    except Exception as e:
        raise ExternalAPIException(detail=str(e))
    return response_checker(response, "result")


def get_rate(change_from: str, change_to: str):
    """
    Makes request to external API and returns the exact exchange rate.
    :param change_from: a currency you'd like to exchange
    :param change_to: a currency you'd like to exchange into
    :return: summary about requested exchange
    :raises custom Exception if server does not respond
    """
    try:
        response = requests.get(
            f'{EXTERNAL_API_URL}/convert?to={change_to}&from={change_from}&amount=1',
            headers=header_params
        )
    except Exception as e:
        raise ExternalAPIException(detail=str(e))
    return response_checker(response, "result")
