from fastapi import FastAPI
from uvicorn import run
from loguru import logger

from db.base import database
from endpoints.router import api_router


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


if __name__ == "__main__":
    run("main:app", port=5000, host="0.0.0.0", reload=True)
