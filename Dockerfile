FROM python:3.7-alpine
MAINTAINER AlexanderKhabarov

RUN apk update
RUN apk --update add --no-cache gcc
RUN apk --update add --no-cache g++
RUN apk --update add --no-cache libffi-dev
RUN apk --update add --no-cache libxslt-dev

WORKDIR /project

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn -c config/gunicorn.conf run_prod:app