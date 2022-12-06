FROM python:3.11-slim

COPY requirements.txt /tmp/requirements.txt
RUN  pip3 install -r /tmp/requirements.txt

COPY . /app/

WORKDIR /app
