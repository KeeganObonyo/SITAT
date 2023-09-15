#!/bin/sh
# wait for PSQL server to start
sleep 10
 
echo Setting Up.
exec python /app/sitat/manage.py makemigrations
exec python /app/sitat/manage.py migrate
exec python /app/sitat/manage.py collectstatic

echo Starting Gunicorn.
exec gunicorn --reload sitat.sitat.wsgi:application \
    --bind 0.0.0.0:9000