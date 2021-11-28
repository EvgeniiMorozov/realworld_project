FROM python:3.9-buster

WORKDIR /app

COPY services/backend/alembic alembic/
COPY services/backend/src src/
COPY services/backend/alembic.ini ./
COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --deploy

EXPOSE 8000

#CMD alembic upgrade head && python ./src/main.py
CMD python ./src/main.py