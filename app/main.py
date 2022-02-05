from os import getenv as os_getenv

from fastapi import FastAPI
from uvicorn import run

from db import database
from endpoints.routers import api_router


app = FastAPI()

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    run("main:app", port=os_getenv("PORT"), host="127.0.0.1", reload=False)
