"""
module containing WSOLA algorithim
"""
import numpy as np
from ATSM.base import A2S_TSM, Converter
from ATSM.utils import Windows as W

class WSOLAConverter(Converter):

    def __init__(self, channels: int, frame_length: int, 
                       synthesis_hop: int, tolerance: int):

        self.__channels: int = channels
        self.__frame_length: int = frame_length
        self.__synthesis_hop: int = synthesis_hop
        self.__tolerance: int = tolerance

        self.__synthesis_frame: np.ndarray = np.empty((channels, frame_length))
        self.__natural_progression: np.ndarray = np.empyt((channels, frame_length))
        self.__first: bool = True

    @property
    def channels(self) -> int:
        return self.__channels

    @property
    def frame_length(self) -> int:
        return self.__frame_length

    @property
    def synthesis_hop(self) -> int:
        return self.__synthesis_hop

    @property
    def tolerance(self) -> int:
        return self.__tolerance

    @property
    def syntehsis_frame(self) -> np.ndarray:
        return self.__synthesis_frame

    @property
    def natural_progression(self) -> np.ndarray:
        return self.__natural_progression

    @property
    def first(self) -> bool:
        return self.__first

    
    def clear(self):
        self.first: bool = True

    def convert_frame(self, analysis_frame: np.ndarray) -> np.ndarray:

        for k in range(0, self.channels):
            if self.first:
                delta: int = 0
            else:
                cross_correlation: np.ndarray = np.correlate(
                    analysis_frame[k, :-self.synthesis_hop],
                    self.natural_progression[k])
                delta: int = np.argmax(cross_correlation)
                del cross_correlation

            np.copyto(self.syntehsis_frame[k], 
                      analysis_frame[k, delta:delta+self.frame_length])
            delta += self.synthesis_hop
            np.copyto(self.natural_progression[k],
                      analysis_frame[k, delta:delta+self.frame_length])

        self.first: bool = False

        return self.synthesis_frame


class WSOLA(WSOLAConverter):

    def __init__(self, channels: int, speed: float = 1., 
                       frame_length: int = 1024, 
                       analysis_hop: int = None,
                       synthesis_hop: int = None,
                       tolerance: int = None):

        super().__init__(channels=channels, frame_length=frame_length,
                         synthesis_hop=synthesis_hop, tolerance=tolerance)
        self.__converter: Converter = super()
        self.__channels: int = channels
        self.__speed: float = speed
        self.__frame_length: int = frame_length
        self.__analysis_hop: int = analysis_hop
        self.__synthesis_hop: int = synthesis_hop
        self.__tolerance: int = tolerance

    @property
    def converter(self) -> Converter:
        return self.__converter

    @property
    def channels(self) -> int:
        return self.__channels

    @property
    def speed(self) -> float:
        return self.__speed

    @property
    def frame_length(self) -> int:
        return self.__frame_length

    @property
    def analysis_hop(self) -> int:
        return self.__analysis_hop

    @analysis_hop.setter
    def analysis_hop(self, analysis_hop: int):
        self.__analysis_hop: int = analysis_hop

    @property
    def synthesis_hop(self) -> int:
        return self.__synthesis_hop

    @synthesis_hop.setter
    def synthesis_hop(self, synthesis_hop: int):
        self.__synthesis_hop: int = synthesis_hop

    @property
    def tolerance(self) -> int:
        return self.__tolerance
    
    @tolerance.setter
    def tolerance(self, tolerance: int):
        self.__tolerance: int = tolerance

    
    def setVariables(self):

        if self.synthesis_hop is None:
            self.synthesis_hop: int = self.frame_length // 2

        if self.analysis_hop is None:
            self.analysis_hop: int = int(self.synthesis_hop * self.speed)

        if self.tolerance is None:
            self.tolerance: int = self.frame_length // 2

        self.analysis_window: np.ndarray = None
        self.synthesis_window: np.ndarray = W.hanning(self.frame_length)

    def convert(self) -> A2S_TSM:

        self.setVariables()

        return A2S_TSM(
            self.converter, self.channels, self.frame_length,
            self.analysis_hop, self.synthesis_hop,
            self.analysis_window, self.synthesis_window,
            self.tolerance, (self.tolerance + self.synthesis_hop)
        )