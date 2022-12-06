# pylint: disable=redefined-outer-name
import pytest
import requests
from tenacity import retry, stop_after_delay
import config
import logging
import time


logging.basicConfig(format='{asctime} {levelname:7} {message}', style='{', level=logging.INFO)


@retry(stop=stop_after_delay(10))
def wait_for_webapp_to_come_up():
    return requests.get(config.get_api_url())


@pytest.fixture
def api_is_started():
    return wait_for_webapp_to_come_up()


@pytest.fixture(autouse=True)
def slow_down_tests():
    yield
    time.sleep(0)
