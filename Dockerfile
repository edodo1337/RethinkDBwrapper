FROM python:3-alpine
COPY . /code
WORKDIR /code/
COPY requirements.txt /code/

RUN pip install -r /code/requirements.txt

