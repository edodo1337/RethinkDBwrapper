FROM python:3-alpine
COPY . /code
WORKDIR /code/
RUN pip install -r rethinkdb

