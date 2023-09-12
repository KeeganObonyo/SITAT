#!/bin/sh
# wait for PSQL server to start
sleep 10
 
cd /app/sitat/

su -m root -c "python manage.py makemigrations"    

su -m root -c "python manage.py migrate"

su -m root -c "gunicorn --bind 0.0.0.0:9000 sitat.wsgi:application"