FROM python:3.9-buster

WORKDIR /app

COPY alembic alembic/
COPY src src/
COPY alembic.ini ./

EXPOSE 8000

CMD alembic upgrade head && python ./src/main.py