import multiprocessing as mp
import ctypes


class AbstractExecutor(mp.Process):

    def __init__(self, data_src, data_dst, preprocessor=None, model=None):
        super(AbstractExecutor, self).__init__()
        self.daemon = True  # dies with parent. Can't have zombies around
        self.data_src = data_src
        self.data_dst = data_dst
        self.preprocessor = preprocessor
        self.model = model
        self.state = mp.Manager().Value(ctypes.c_wchar_p, 'Standby')

    def run(self):
        # The main loop where everything happens
        pass

    def _process_data(self):
        raise NotImplementedError

    def _predict(self):
        raise NotImplementedError

    def set_state(self, state: str):
        # Suggested values for state: 'Getting data', 'Preprocessing', 'Transforming', 'Writing results', 'Done'.
        self.state.value = state
    
    def get_state(self):
        return self.state.value
