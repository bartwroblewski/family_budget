FROM python:3.11.5-slim-bullseye as base

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .

RUN apt-get update -y && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

FROM base as dev
ENV DJANGO_SETTINGS_MODULE=family_budget.settings.development
RUN python manage.py makemigrations
RUN python manage.py migrate --run-syncdb
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base as prod
ENV DJANGO_SETTINGS_MODULE=family_budget.settings.production
RUN python manage.py makemigrations
RUN python manage.py migrate --run-syncdb
RUN pip install gunicorn
RUN python manage.py collectstatic --no-input
ENTRYPOINT ["gunicorn", "family_budget.wsgi:application", "--bind", "0.0.0.0:8000"]

