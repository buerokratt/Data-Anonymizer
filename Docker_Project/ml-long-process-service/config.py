import os
from typing import Dict, Union


def get_postgres_uri() -> str:
    host = os.environ.get('POSTGRES_HOST', 'localhost')
    port = os.environ.get('POSTGRES_PORT', 5432)
    password = os.environ.get('POSTGRES_PASSWORD', 'pgpass')
    user = os.environ.get('POSTGRES_USER', 'pgpass')
    db_name = os.environ.get('POSTGRES_DB', 'postgres')
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_aws_s3_params() -> Dict[str, Union[str, None]]:
    return {'aws_access_key_id': os.environ.get('S3_ACCESS_KEY', None),
            'aws_secret_access_key': os.environ.get('S3_SECRET_ACCESS_KEY', None)}


def get_api_url() -> str:
    host = os.environ.get('API_HOST', 'localhost')
    port = os.environ.get('API_PORT', '8000')
    return f"http://{host}:{port}"


def get_local_model_dir() -> str:
    return '/models/'
