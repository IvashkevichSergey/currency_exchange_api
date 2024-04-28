from typing import Annotated
from fastapi import APIRouter, Body
from app.utils.currency_exch_api import get_all_currencies, exchange_currencies, get_rate

currency_router = APIRouter(prefix="/currency")


@currency_router.get("/",
                     summary="Get all available currencies",
                     response_description="List of currencies")
def get_currencies():
    """
    Get all available currencies for operating from external API
    """
    return get_all_currencies()


@currency_router.post("/exchange",
                      summary="Request exchange information",
                      response_description="Exchange info")
def change_currency(change_from: Annotated[str, Body(embed=True)],
                    change_to: Annotated[str, Body(embed=True)],
                    amount: Annotated[int, Body(embed=True)]):
    """
    Request exchange information
    """
    result = exchange_currencies(change_from, change_to, amount)
    return f"{amount} {change_from} equals to {result} {change_to}"


@currency_router.post("/rates",
                      summary="Request current exchange rates",
                      response_description="Info about requested exchange rate")
def change_rates(change_from: Annotated[str, Body(embed=True)],
                 change_to: Annotated[str, Body(embed=True)]):
    """
    Request current exchange rates
    """
    change_rate = get_rate(change_from, change_to)
    return f"Current exchange rate for 1 {change_from} is {change_rate} {change_to}"
