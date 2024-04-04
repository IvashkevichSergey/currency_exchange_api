from typing import Annotated

from fastapi import APIRouter, Body
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.utils.currency_exch_api import get_all_currencies, exchange_currencies, get_rate

currency_router = APIRouter(prefix="/currency")


@currency_router.get("/",
                     summary="Get all available currencies",
                     response_description="List of currencies")
def get_currencies():
    """
    Get all available currencies for operating from external API:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item

     **param** item: User input.
    """
    return get_all_currencies()


@currency_router.post("/exchange",
                      summary="Request exchange information",
                      response_description="Info about exchange")
def change_currency(change_from: Annotated[str, Body(embed=True)],
                    change_to: Annotated[str, Body(embed=True)],
                    amount: Annotated[int, Body(embed=True)]):
    """
    Request exchange information:

    **param**
    - **change_from**: a currency you'd like to exchange
    - **change_to**: a currency you'd like to exchange into
    - **amount**: amount of currency

    **returns**
    - _str_: summary about requested exchange
    """
    result = exchange_currencies(change_from, change_to, amount)
    return f"{amount} {change_from} equals to {result} {change_to}"


@currency_router.post("/rates",
                      summary="Request current exchange rates",
                      response_description="Info about requested exchange rate")
def change_rates(change_from: Annotated[str, Body(embed=True)],
                 change_to: Annotated[str, Body(embed=True)]):
    """
    Request current exchange rates:

    **param**
    - **change_from**: a currency you'd like to exchange
    - **change_to**: a currency you'd like to exchange into

    **returns**
    - _str_: summary about requested exchange rate
    """
    change_rate = get_rate(change_from, change_to)
    return f"Current exchange rate for 1 {change_from} is {change_rate} {change_to}"
