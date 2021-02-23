FROM python:3.9.2-alpine3.13

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies

RUN apk update \
    && apk add build-base postgresql postgresql-dev ibpq
RUN pip install --upgrade pip

RUN mkdir /usr/src/openwnms
WORKDIR /usr/src/openwnms
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .