FROM python:3.9-buster

WORKDIR /app

COPY alembic alembic/
COPY app app/
COPY alembic.ini ./
COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --deploy

EXPOSE 8000

#CMD alembic upgrade head && python ./app/main.py
CMD python ./src/main.py