import configparser
import pathlib

from fastapi import FastAPI
from uvicorn import run
from loguru import logger

from core.config import settings
from db import database
from endpoints.routers import api_router

CURR_PATH = pathlib.Path()
TO_ALEMBIC_INI = CURR_PATH.parent


app = FastAPI()

app.include_router(api_router, prefix="/api")


@app.get("/")
async def index():
    return {"message": "Test message"}


@app.on_event("startup")
async def startup():
    logger.info("Connect to database")
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    logger.info("Disconnect to database")
    await database.disconnect()


def make_corrections_in_the_alembic_ini():
    if not pathlib.Path(TO_ALEMBIC_INI / "alembic.ini").exists():
        pass
    config = configparser.ConfigParser()


if __name__ == "__main__":
    run("main:app", port=5000, host="0.0.0.0", reload=True)
