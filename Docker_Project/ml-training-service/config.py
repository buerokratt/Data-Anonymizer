import os

def get_api_url() -> str:
    host = os.environ.get('API_HOST', 'localhost')
    port = os.environ.get('API_PORT', '8000')
    return f"http://{host}:{port}"


def get_local_model_dir() -> str:
    return os.environ.get('LOCAL_MODEL_DIR', './models')

def get_remote_model_dir() -> str:
    return os.environ.get('REMOTE_MODEL_DIR', '/models')

def get_finetune_model_path() -> str:
    return get_remote_model_dir() + '/bert_new'

def get_resql_url() -> str:
    host = os.environ.get('RESQL_URL', 'localhost')
    port = os.environ.get('RESQL_PORT', '9020')
    return f"http://{host}:{port}"

def get_training_data_root() -> str:
    return os.environ.get('TRAINING_DATA_ROOT', 'models')

def get_model_config() -> str:
    return os.environ.get('MODEL_TRAINING_CONFIG', 'models/config/new_ner_config.json')