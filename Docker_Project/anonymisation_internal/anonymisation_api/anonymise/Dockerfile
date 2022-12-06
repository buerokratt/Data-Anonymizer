FROM python:3.7-slim


RUN apt-get -y update && apt-get install -y unixodbc-dev gcc g++ &&\
   apt-get install -y --no-install-recommends build-essential  \
   curl wget nginx ca-certificates npm \
   && npm install pm2 -g \
   && pip install --upgrade pip setuptools \
   && rm -rf /var/lib/apt/lists/*
RUN pip install dataclasses
RUN pip install datasets
RUN pip install transformers>=4.1
RUN pip install torch
RUN pip install seqeval
RUN pip install nltk
RUN pip install Flask gunicorn celery Redis
RUN pip install importlib-metadata==4.13.0
COPY requirements.txt .
RUN pip install -r requirements.txt



COPY . ./

EXPOSE 5001

CMD ["gunicorn", "--bind", ":5001", "--timeout", "900", "accept_request:app"]
#CMD ["python3", "accept_request.py"]