FROM python:3.9-slim

COPY requirements.txt /tmp/requirements.txt
RUN  pip3 install -r /tmp/requirements.txt

RUN python -c "import stanza; stanza.download('et')"

# Create the /models directory inside the image
RUN mkdir -p /models
# Copy the contents of the local directory to /models
COPY /Docker_Project/anonymisation_internal/anonymisation_api/anonymise/models /models

COPY . /app/

WORKDIR /app


