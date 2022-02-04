FROM python:3.9.10-slim-buster

# WORKDIR /usr/src

COPY ./alembic /app/alembic/
COPY ./app /app/app
COPY ./alembic.ini /app/
COPY ./Pipfile /app/
COPY ./Pipfile.lock /app/

RUN pip install pipenv
RUN pipenv install --deploy

#EXPOSE 8000

#CMD alembic upgrade head && python app/main.py
#CMD pipenv run python ./app/main.py