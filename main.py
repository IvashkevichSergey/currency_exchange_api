from fastapi import FastAPI

from app.api.routers.currency import currency_router
from app.api.routers.users import auth_router

app = FastAPI()
app.include_router(auth_router, tags=["Auth"])
app.include_router(currency_router, tags=["Currency"])
