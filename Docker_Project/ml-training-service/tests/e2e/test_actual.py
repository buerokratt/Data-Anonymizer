# import json
# from fastapi.testclient import TestClient
# import requests_mock

# from api.app import app
# from api.routers.executor import init_routes
# from executor.ner_trainer import NERTrainer, ReSQLSource, ModelStorageDisk
# import config
# import pytest
# import requests

# # Overwrite the method to not copy overwrite the model when done training
# def put_model(self, local_path: str, model_name: str):
#     pass
# ModelStorageDisk.put_model = put_model

# def init_executor() -> NERTrainer:
#     config_path = config.get_model_config()
#     return NERTrainer(data_src=ReSQLSource(), data_dst=ModelStorageDisk(config.get_remote_model_dir()), config_path=config_path)


# init_routes(app, init_executor)
# client = TestClient(app)

# @requests_mock.Mocker(kw="mock", real_http=True)
# def test_job_start(**kwargs):
#     kwargs["mock"].post(f"{config.get_resql_url()}/get_latest_corpora", json=json.load(open('tests/data/resql_data.json')))
#     r = client.post('/task')
#     assert r.status_code == 200


# @requests_mock.Mocker(kw="mock", real_http=True)
# def test_get_status(**kwargs):
#     kwargs["mock"].post(f"{config.get_resql_url()}/get_latest_corpora", json=json.load(open('tests/data/resql_data.json')))
#     states = set()
#     while True:
#         var = client.get('/status')
#         status = var.json()["status"]
#         states.add(status)
#         if status == 'Done' or status == 'Failed' or not status:
#             break
#     assert len(states.difference({'Standby', 'Getting data', 'Preprocessing', 'Transforming', 'Writing results', 'Done'})) == 0


# @requests_mock.Mocker(kw="mock", real_http=True)
# def test_starting_sequential(**kwargs):
#     for _ in range(3):
#         kwargs["mock"].post(f"{config.get_resql_url()}/get_latest_corpora", json=json.load(open('tests/data/resql_data.json')))
#         r = client.post('/task')
#         assert r.status_code == 200
#         states = set()
#         while True:
#             var = client.get('/status')
#             status = var.json()["status"]
#             states.add(status)
#             if status == 'Done' or status == 'Failed' or not status:
#                 break
#         assert len(states.difference({'Standby', 'Getting data', 'Preprocessing', 'Transforming', 'Writing results', 'Done'})) == 0
