from fastapi import FastAPI
from src.db.base import init_db
from uvicorn import run

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def index():
    return {"message": "Test message"}


if __name__ == "__main__":
    run("main:app", port=5000, host="0.0.0.0", reload=True)
