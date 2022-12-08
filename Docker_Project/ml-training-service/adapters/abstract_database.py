from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    
    @abstractmethod
    def read_data(self, *args):
        raise NotImplementedError

    @abstractmethod
    def write_data(self, *args):
        raise NotImplementedError
