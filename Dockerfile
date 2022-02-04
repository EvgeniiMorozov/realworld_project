FROM python:3.9.10

# WORKDIR /usr/src

COPY ./alembic /app/alembic/
COPY ./app /app/app
COPY ./alembic.ini /app/
COPY ./Pipfile /app/
COPY ./Pipfile.lock /app/

WORKDIR /app/

RUN pip install pipenv
RUN pipenv install --deploy

#EXPOSE 8000

CMD alembic upgrade head && pipenv run app/main.py
#CMD pipenv run python ./app/main.py