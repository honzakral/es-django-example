FROM python:3-alpine

MAINTAINER Nick Lang <nick@nicklang.com>

RUN apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main --no-cache py3-psycopg2 postgresql-dev gcc python3-dev musl-dev git

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt 
RUN pip install -r requirements.txt

COPY . /code

EXPOSE 80

CMD python manage.py runserver 0.0.0.0:80