# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""conll2003.py adaptation for Estonian NER dataset"""

import datasets
import os.path
import json
import config

logger = datasets.logging.get_logger(__name__)

_DESCRIPTION = """\
Estonian NER dataset

The data files contain two columns separated by a tab symtol. Each word has been put on
a separate line and there is an empty line after each sentence. The first item on each line is a word and the second is the named entity tag. 
The named entity tags use the BIO format, which means that the first word in a named entity has the B_TYPE tag and the following words have the I_TYPE tag. A word with tag O is not part of a named entity. 
"""

_PATH = config.get_training_data_root()
_TRAINING_FILE = "train.json"
_DEV_FILE = "dev.json"
_TEST_FILE = "test.json"


class EstNERConfig(datasets.BuilderConfig):
    """BuilderConfig for ESTNer datasets"""

    def __init__(self, **kwargs):
        """BuilderConfig for EstNER.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(EstNERConfig, self).__init__(**kwargs)


class EstNER(datasets.GeneratorBasedBuilder):
    """EstNER dataset."""

    BUILDER_CONFIGS = [
       EstNERConfig(name="estner", version=datasets.Version("1.0.0"), description="EstNER dataset"),
    ]
    def read_labels(self):
        #TODO: Gotta fix the labels.txt to dynamic
        labels = []
        label_file = os.path.join(_PATH, 'labels.txt')
        with open(label_file, 'r', encoding='utf-8') as f:
            for line in f:
                labels.append(line.strip())
        return labels

    def _info(self):
        labels = self.read_labels()
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=labels


                        )
                    ),
                }
            ),
            supervised_keys=None
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        file_paths = {
            "train": os.path.join(_PATH, _TRAINING_FILE),
            "dev": os.path.join(_PATH, _DEV_FILE),
            "test": os.path.join(_PATH, _TEST_FILE),
        }

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": file_paths["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": file_paths["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": file_paths["test"]}),
        ]

    def _generate_examples(self, filepath):
        tags = self.read_labels()
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            guid = 0
            tokens = []
            ner_tags = []
            for doc in data['documents']:
                for sent in doc['sentences']:
                    for word in sent['words']:
                        tokens.append(word['word'])
                        if word['ner_1'] in tags: #['B-GPE', 'I-GPE', 'O', 'B-PER', 'I-PER', 'B-ORG', 'I-ORG', 'B-LOC', 'I-LOC']:
                            if 'GPE' in word['ner_1']:
                                ner_tags.append(word['ner_1'].replace('GPE', 'LOC'))
                            else:
                                ner_tags.append(word['ner_1'])
                        else:
                            ner_tags.append('O')
                    yield guid, {
                        "id": str(guid),
                        "tokens": tokens,
                        "ner_tags": ner_tags,
                        }
                    guid += 1
                    tokens = []
                    ner_tags = []
