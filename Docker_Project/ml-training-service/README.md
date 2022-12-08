# Model training management application


## Introduction

This application is intended for handling the training of the NER model used in RIA anonymizer. It has an HTTP interface and on demand it spins up a process that starts the training process, gets the data, transforms it as required and trains a new model. 


## Running

To start the application, run `docker-compose build` followed by `MODEL_DIR=<The directory with bert_new model dir> docker-compose --env-file sample.env up`, 
that starts the API. See `{api_url}/docs` for API docs. By default `http://localhost:9090/docs`.

## Testing

To build and run all tests in a container:  
`export MODEL_DIR=<The directory with bert_new model dir>`    
`make all`
