from api.routers.executor import init_routes
from api.app import app
import logging
from executor.ner_trainer import NERTrainer, ReSQLSource, ModelStorageDisk
import config

executor = None

def init_executor() -> NERTrainer:
    logging.debug('Instantiating new executor.')
    return NERTrainer(data_src=ReSQLSource(), 
                      data_dst=ModelStorageDisk(config.get_remote_model_dir()),
                      config_path=config.get_model_config())

init_routes(app, init_executor)
