FROM python:3.7-alpine
MAINTAINER AlexanderKhabarov

RUN apk update

WORKDIR /project

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ./run.sh