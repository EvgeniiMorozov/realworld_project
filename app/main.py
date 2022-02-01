import pathlib

from fastapi import FastAPI
from uvicorn import run

from db import database
from endpoints.routers import api_router

# from loguru import logger


CURR_PATH = pathlib.Path()
TO_ALEMBIC_INI = CURR_PATH.parent


app = FastAPI()

app.include_router(api_router, prefix="/api")


@app.get("/")
async def index():
    return {"message": "Test message"}


@app.on_event("startup")
async def startup():
    # logger.info("Connect to database")
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # logger.info("Disconnect to database")
    await database.disconnect()


if __name__ == "__main__":
    run("main:app", port=8000, host="127.0.0.1", reload=False)
