from api.routers.executor import init_routes
from api.app import app
import logging
from tests import LocalTestExecutor, LocalTestDatabase

executor = None

def init_executor():
    logging.debug('Instantiating new executor.')
    return LocalTestExecutor(data_src=LocalTestDatabase(), data_dst=LocalTestDatabase())


init_routes(app, init_executor)

