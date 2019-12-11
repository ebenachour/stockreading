FROM python:3.7-slim-stretch
RUN pip install pipenv && apt update && apt install -y libpq-dev python3-dev build-essential
WORKDIR /app
COPY stockreading/Pipfile stockreading/Pipfile.lock ./
RUN pipenv install
COPY stockreading .
EXPOSE 8000
CMD pipenv run  python manage.py makemigrations app ;pipenv run  python manage.py migrate ; pipenv run  python manage.py runserver 0.0.0.0:8000