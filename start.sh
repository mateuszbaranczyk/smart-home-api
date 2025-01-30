#!/bin/sh

python home_api/manage.py collectstatic --noinput

python home_api/manage.py makemigrations
python home_api/manage.py migrate
python home_api/manage.py createsuperuser --noinput

gunicorn home_api.wsgi:application --bind 0.0.0.0:$PORT --workers 1
