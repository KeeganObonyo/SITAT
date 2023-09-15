# Dockerfile

# FROM directive instructing base image to build upon
FROM ubuntu:latest

ADD . /app/sitat/

WORKDIR /app/sitat/

# install python 3 and pip
RUN apt-get update
RUN apt-get install python3 -y
RUN apt install python3-pip -y && pip3 install --upgrade pip

# make python 3 default python environment
RUN alias python=python3

RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' myuser

EXPOSE 9000

# CMD specifies the command to execute to start the server running.
CMD ["/start.sh"]
# done! :)