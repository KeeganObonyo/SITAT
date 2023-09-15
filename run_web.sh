#!/bin/sh
# wait for PSQL server to start
sleep 10
 
cd /app/sitat/

echo Setting Up.
exec python manage.py makemigrations
exec python manage.py migrate
exec python manage.py collectstatic

echo Starting Gunicorn.
exec gunicorn --reload sitat.sitat.wsgi:application \
    --bind 0.0.0.0:9000