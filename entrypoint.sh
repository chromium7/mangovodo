#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --username admin --email "admin@example.com" --noinput

gunicorn django_project.wsgi:application --timeout 120 --bind 0.0.0.0:8000

