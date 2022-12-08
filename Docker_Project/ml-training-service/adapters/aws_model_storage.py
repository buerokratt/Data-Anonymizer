import os
import logging
import boto3
from botocore.exceptions import ClientError
from adapters import AbstractModelStorage


class AWSModelStorage(AbstractModelStorage):
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str):
        self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key)

    def put_model(self, file_path: str, bucket: str, key: str):
        if key is None:
            key = os.path.basename(file_path)
        try:
            response = self.s3_client.upload_file(file_path, bucket, key)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def get_model(self, file_path: str, bucket: str, key: str):
        raise NotImplementedError
