FROM python:3.13-slim

COPY requirements.txt /tmp/requirements.txt
RUN  pip3 install -r /tmp/requirements.txt

RUN python -c "import stanza; stanza.download('et')"
COPY . /app/

WORKDIR /app
