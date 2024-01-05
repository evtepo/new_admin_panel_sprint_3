#!/bin/bash

python manage.py collectstatic --noinput

python manage.py migrate
python manage.py migrate sessions
python manage.py migrate movies 0001 --fake

uwsgi --strict --ini uwsgi.ini