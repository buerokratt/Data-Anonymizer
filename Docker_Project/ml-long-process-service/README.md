# Base FastAPI code for long running processes

## Quickstart

To start simple example run `docker-compose build` followed by `docker-compose up` 
that starts the API. See `{api_url}/docs` for API docs. By default `http://localhost:8000/docs`.

## Guidelines for new application
* fork the repository
* create executor based on `executor/abstract_executor` (see tests for how one can be created)
* create needed endpoints in `api/routers`
* see `adapters/` for abstract DB and model storage connectors.
* add necessary DB connections (see `config.py` on how to see to get connection strings)
* update `docker-compose.yml` based on your use case
