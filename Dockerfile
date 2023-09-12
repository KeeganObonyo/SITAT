# use base python image with python 3.6

FROM python:3.6

# add requirements.txt to the image

ADD . /app/sitat/

WORKDIR /app/sitat/

RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' myuser

EXPOSE 9000