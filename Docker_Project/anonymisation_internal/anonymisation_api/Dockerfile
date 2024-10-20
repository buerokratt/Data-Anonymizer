FROM python:3.13-slim

RUN pip install celery
RUN pip install flask
RUN pip install -U "celery[redis]"
RUN pip install Redis
RUN pip install importlib-metadata==4.13.0
RUN pip install dataclasses
RUN pip install datasets
RUN pip install transformers>=4.1
RUN pip install torch
RUN pip install seqeval
RUN pip install nltk
RUN pip install stanza
RUN pip install exrex
RUN pip install estnltk

#
RUN mkdir -p /app
COPY . /app
RUN mkdir -p /app/training
COPY anonymise/training /app/training
COPY anonymise/worker.py /app
COPY anonymise/tasks.py /app

RUN mkdir -p /app/utils
COPY anonymise/utils/__init__.py /app/utils
COPY anonymise/utils/utils.py /app/utils
COPY anonymise/utils/pseudonymisation_utils.py /app/utils
COPY anonymise/utils/tokenization_utils.py /app/utils
COPY anonymise/utils/model_utils.py /app/utils
COPY anonymise/anonymise.py /app
RUN mkdir -p /app/gazetteers
#RUN mkdir -p /app/models
#COPY anonymise/models /app/models
COPY anonymise/gazetteers /app/gazetteers
COPY anonymise/gazetteers /gazetteers
RUN mkdir -p /app/logs
WORKDIR /app

CMD ["celery", "-A","tasks",  "worker", "--pool", "solo", "-l", "INFO","-f", "/app/logs/celery.log"]