FROM python:3.9-buster

WORKDIR /app

COPY alembic app/alembic/
COPY app app/app
COPY alembic.ini ./app
COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --deploy

EXPOSE 8000

#CMD alembic upgrade head && python app/main.py
CMD python app/main.py