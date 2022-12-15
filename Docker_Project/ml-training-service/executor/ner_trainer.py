import os
import shutil
import requests
import json
import traceback
import logging

import config
from executor.abstract_executor import AbstractExecutor
from adapters.abstract_database import AbstractDatabase
from adapters.abstract_model_storage import AbstractModelStorage

from models.run_ner import main
from executor.ner_utils import prepare_annotation

class NERTrainer(AbstractExecutor):

    def __init__(self, data_src, data_dst, config_path):
        super().__init__(data_src, data_dst)
        self.config_path = config_path
        if not os.path.exists(config.get_local_model_dir()):
            os.mkdir(config.get_local_model_dir())

    def run(self):
        try:
            self._clear_workspace()

            self.set_state('Getting data')
            self.data = self.data_src.read_data()
            corpora_id = self.data[0].get("corporaId") if len(self.data) > 0 else None
            self.set_state('Preprocessing')
            self._process_data()
            if not self.data:
                raise ValueError('No valid data to train on. Process failed.')
            # self._prepare_labels()

            self.set_state('Transforming')
            self._train_model()

            self.set_state('Writing results')
            self.data_dst.put_model(local_path=f'{config.get_local_model_dir()}/model_artifacts', model_name='bert_new')
            
            self.set_state('Done')
            self.data_src.write_data(corpora_id)
            return 0
        except Exception as e:
            logging.error(f'Training failed: {str(e)}')
            print(traceback.format_exc())
            self.set_state('Failed')
            return 1
    
    def _clear_workspace(self):
        trainpath = f'{config.get_local_model_dir()}/training'
        if os.path.exists(trainpath) and os.path.isdir(trainpath):
            shutil.rmtree(trainpath)
        modelpath = f'{config.get_local_model_dir()}/model_artifacts'
        if os.path.exists(modelpath) and os.path.isdir(modelpath):
            shutil.rmtree(modelpath)

    def _validate_elem(self, elem):
        sentence_text = elem.get('rawText')
        annotations = elem.get('predictions')
        return sentence_text and annotations

    def _process_data(self):
        self.data = [elem for elem in self.data if self._validate_elem(elem)]
        sentences = [prepare_annotation(element) for element in self.data]
        n = len(sentences)
        train = sentences[:int(0.8*n)]
        dev = sentences[int(0.8*n):int(0.9*n)]
        test = sentences[int(0.9*n):]
        json.dump({"documents": [{"sentences": [{"words": words} for words in train]}]}, open(f'{config.get_training_data_root()}/train.json', 'w'))
        json.dump({"documents": [{"sentences": [{"words": words} for words in dev]}]}, open(f'{config.get_training_data_root()}/dev.json', 'w'))
        json.dump({"documents": [{"sentences": [{"words": words} for words in test]}]}, open(f'{config.get_training_data_root()}/test.json', 'w'))

    def _prepare_labels(self):
        annotations = [annotation for elem in self.data for annotation in eval(elem['predictions'])]
        available_labels = set([x['value']['labels'][0] for x in annotations])
        
        labels = [f"B-{label}" for label in available_labels]
        labels.extend([f"I-{label}" for label in available_labels])
        labels = sorted(labels, key=lambda x: x[2:]) + ["O"]
        with open(f'{config.get_training_data_root()}/labels.txt', 'w') as f:
            for label in labels:
                f.write(f"{label}\n")

    def _train_model(self):
        main(self.config_path)


class ReSQLSource(AbstractDatabase):

    def read_data(self):
        r = requests.post(f"{config.get_resql_url()}/get_latest_corpora")
        return r.json()

    def write_data(self, corpora_id):
        requests.post(url = f"{config.get_resql_url()}/upsert_corpora_info", json={"corpora_id": corpora_id})
        pass


class ModelStorageDisk(AbstractModelStorage):
    def __init__(self, model_dir: str):
        self.model_dir = model_dir

    def get_model(self):
        #TODO: maybe we need it?
        pass

    def put_model(self, local_path: str, model_name: str):
        dst_path = f"{self.model_dir}/{model_name}"
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)
        shutil.move(local_path, dst_path)
