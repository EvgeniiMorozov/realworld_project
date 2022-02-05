FROM python:3.9.10

WORKDIR /usr/src/api

COPY ./alembic/ ./alembic/
COPY ./app ./app
COPY ./alembic.ini .
#COPY Pipfile ./
#COPY Pipfile.lock ./
COPY ./requirements.txt .

# WORKDIR /app/

#RUN pip install pipenv
#RUN pipenv install --deploy
RUN pip install -r ./requirements.txt

#EXPOSE 8000

#CMD pipenv run alembic upgrade head && pipenv run app/main.py
#CMD pipenv run python ./app/main.py
CMD ["python", "app/main.py"]
