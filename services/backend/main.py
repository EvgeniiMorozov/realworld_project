from fastapi import FastAPI
from uvicorn import run

from db.base import database


app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Test message"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    run("main:app", port=5000, host="0.0.0.0", reload=True)
