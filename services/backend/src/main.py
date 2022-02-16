from fastapi import FastAPI
from uvicorn import run

app = FastAPI()


@app.get("/")
async def index() -> dict:
    return {"message": "Test message"}


if __name__ == "__main__":
    run("main:app", port=5000, host="0.0.0.0", reload=True)
