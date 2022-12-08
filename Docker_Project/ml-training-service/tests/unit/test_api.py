from fastapi.testclient import TestClient

from api.app import app
from api.routers.executor import init_routes
from tests import LocalTestExecutor, LocalTestDatabase

executor = None


def init_executor():
    return LocalTestExecutor(data_src=LocalTestDatabase(), data_dst=LocalTestDatabase())


init_routes(app, init_executor)
client = TestClient(app)


def test_job_start():
    r = client.post('/task')
    assert r.status_code == 200


def test_get_status():
    r = client.get('/status')
    assert r.status_code == 200

# @pytest.mark.usefixtures('api_is_started')
# def test_job_start():
#     url = config.get_api_url()
#     r = requests.post(f'{url}/start-task')
#     assert r.status_code == 200
    # d = r.json()
    # assert d['embeddingVersion'] is not None
