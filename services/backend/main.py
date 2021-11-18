from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from db.config import TORTOISE_ORM
from db.register import register_tortoise


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get("/")
async def index():
    return {"message": "Test message"}


if __name__ == "__main__":
    run("main:app", port=5000, host="0.0.0.0", reload=True)
