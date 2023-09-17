# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.6

ADD . /app/sitat/

WORKDIR /app/sitat/

RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' myuser

EXPOSE 9000

# CMD specifies the command to execute to start the server running.
CMD ["/start.sh"]
# done! :)