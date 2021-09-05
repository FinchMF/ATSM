
import numpy as np

from ATSM.utils.windows import Windows as W
from ATSM.utils.CBuffer import CBuffer
from .tsm import TSM

class A2S_TSM(TSM):

    def __init__(self, converter: object, channels: int,
                       frame_length: int, 
                       analysis_hop: int,
                       synthesis_hop: int, 
                       analysis_window: np.ndarray,
                       synthesis_window: np.ndarray,
                       delta_before: int = 0,
                       delta_after: int = 0):

        self.__converter: object = converter
        self.__frame_length: int = frame_length
        self.__analysis_hop: int = analysis_hop
        self.__synthesis_hop: int = synthesis_hop
        self.__analysis_window: np.ndarray = analysis_window
        self.__synthesis_window: np.ndarray = synthesis_window
        self.__delta_before: int = delta_before
        self.__delta_after: int = delta_after

        self.__skip_input_samples: int = 0
        self.__skip_output_samples: int = 0

        self.__normalize_window: np.ndarray = W.product(self.analysis_window,
                                                        self.synthesis_window)
        self.checkNormalWindow()

    @property
    def converter(self) -> object:
        return self.__converter

    @property
    def frame_length(self) -> int:
        return self.__frame_length

    @property
    def analysis_hop(self) -> int:
        return self.__analysis_hop

    @property
    def synthesis_hop(self) -> int:
        return self.__synthesis_hop

    @property
    def analysis_window(self) -> np.ndarray:
        return self.__analysis_window

    @property
    def synthesis_window(self) -> np.ndarray:
        return self.__synthesis_window

    @property
    def delta_before(self) -> int:
        return self.__delta_before

    @property
    def delta_after(self) -> int:
        return self.__delta_after

    @property
    def skip_input_samples(self) -> int:
        return self.__skip_input_samples

    @skip_input_samples.setter
    def skip_input_samples(self, x: int):
        self.__skip_input_samples: int = x

    @property
    def skip_output_samples(self) -> int:
        return self.__skip_output_samples

    @skip_output_samples.setter
    def skip_output_samples(self, x: int):
        self.__skip_output_samples: int = x 

    @property
    def normalize_window(self) -> np.ndarray:
        return self.__normalize_window

    @normalize_window.setter
    def normalize_window(self, x: np.ndarray):
        self.__normalize_window: np.ndarray = x

    @property
    def in_buffer(self) -> np.ndarray:
        return self.__in_buffer

    @in_buffer.setter
    def in_buffer(self, n: np.ndarray):
        self.__in_buffer: np.ndarray = n

    @property
    def out_buffer(self) -> np.ndarray:
        return self.__out_buffer

    @out_buffer.setter
    def out_buffer(self, n: np.ndarray):
        self.__out_buffer: np.ndarray = n

    @property
    def analysis_frame(self) -> np.ndarray:
        return self.__analysis_frame

    @analysis_frame.setter
    def anaylsis_frame(self, n: np.ndarray):
        self.__analysis_frame: np.ndarray = n

    
    def checkNormalWindow(self):
        """function to check normalized window"""
        if self.normalize_window is None:
            self.normalize_window: np.ndarray = np.ones(self.frame_length)

    def initializeBuffers(self):
        """function to initialize buffers"""
        delta: int = self.delta_before + self.delta_after
        self.__in_buffer: np.ndarray = CBuffer(selft.channels, self.frame_length + delta)
        self.__analysis_frame: np.ndarray = np.empty(
            (self.channels, self.frame_length + delta)
        )
        self.__out_buffer: np.ndarray = CBuffer(self.channels, self.frame_length)
        # build normalize buffer





    