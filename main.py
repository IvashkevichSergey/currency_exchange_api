from fastapi import FastAPI

from app.api.routers.users import auth_router

app = FastAPI()
app.include_router(auth_router)