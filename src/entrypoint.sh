#!/bin/bash


python3 manage.py makemigrations;
python3 manage.py migrate --noinput;
python3 manage.py collectstatic --noinput;
gunicorn --bind=0.0.0.0:8000 --timeout=90 --reload article_api.wsgi:application;