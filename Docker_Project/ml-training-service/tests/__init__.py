from executor.abstract_executor import AbstractExecutor
from adapters import AbstractDatabase
import time
import sqlite3


class LocalTestExecutor(AbstractExecutor):

    def __init__(self, data_src, data_dst):
        super().__init__(data_src, data_dst)
        self.data_src.write_data('key', {})
        self.data = {}

    def run(self):
        self.set_state('Getting data')
        self.data = self.data_src.read_data('key')
        time.sleep(1)
        self.set_state('Preprocessing')
        self._process_data()
        time.sleep(1)

        self.set_state('Transforming')
        self._predict()
        time.sleep(1)

        self.set_state('Writing results')
        self.data_dst.write_data('key', self.results)
        time.sleep(1)
        
        self.set_state('Done')
        return 0

    def _process_data(self):
        self.data.update({"key": "transformedvalue"})

    def _predict(self):
        self.results = 1 if self.data.get("key") == "transformedvalue" else 0


class LocalTestDatabase(AbstractDatabase):
    def __init__(self):
        self.connection = sqlite3.connect('testdb')
        self.data = {}

    def read_data(self, key):
        return self.data[key]

    def write_data(self, key, data):
        self.data[key] = data
