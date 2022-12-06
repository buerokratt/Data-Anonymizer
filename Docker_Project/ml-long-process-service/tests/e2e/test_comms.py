from fastapi.testclient import TestClient

from api.app import app
from api.routers.executor import init_routes
from tests import LocalTestExecutor, LocalTestDatabase


def init_executor():
    return LocalTestExecutor(data_src=LocalTestDatabase(), data_dst=LocalTestDatabase())


init_routes(app, init_executor)
client = TestClient(app)


def test_job_start():
    r = client.post('/task')
    assert r.status_code == 200


def test_get_status():
    states = set()
    while True:
        var = client.get('/status')
        status = var.json()["status"]
        states.add(status)
        if status == 'Done' or not status:
            break
    assert len(states.difference({'Standby', 'Getting data', 'Preprocessing', 'Transforming', 'Writing results', 'Done'})) == 0


def test_starting_sequential():
    for _ in range(5):
        r = client.post('/task')
        assert r.status_code == 200
        states = set()
        while True:
            var = client.get('/status')
            status = var.json()["status"]
            states.add(status)
            if status == 'Done' or not status:
                break
        assert len(states.difference({'Standby', 'Getting data', 'Preprocessing', 'Transforming', 'Writing results', 'Done'})) == 0
