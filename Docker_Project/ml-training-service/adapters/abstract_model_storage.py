from abc import ABC, abstractmethod


class AbstractModelStorage(ABC):
    @abstractmethod
    def get_model(self, *args):
        raise NotImplementedError

    @abstractmethod
    def put_model(self, *args):
        raise NotImplementedError
