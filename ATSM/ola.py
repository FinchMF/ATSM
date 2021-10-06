
from ATSM.base import A2S_TSM, Converter
from ATSM.utils import Windows as W


class OLAConverter(Converter):

    def convert_frame(self, analysis_frame: int) -> int:
        return analysis_frame


class OLA(OLAConverter):

    def __init__(self, channels: int, speed: float = 1.,
                       frame_length: int = 256, 
                       analysis_hop: int = None,
                       synthesis_hop: int = None):

        self.__converter: OLAConverter = OLAConverter()
        self.__channels: int = channels
        self.__speed: float = speed
        self.__frame_length: int = frame_length
        self.__analysis_hop: int = analysis_hop
        self.__synthesis_hop: int = synthesis_hop

    @property
    def converter(self) -> OLAConverter:
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


    def setVariables(self):

        if self.synthesis_hop is None:
            self.synthesis_hop: int = self.frame_length // 2
        
        if self.analysis_hop is None:
            self.analysis_hop: int = int(self.synthesis_hop * self.speed)

        self.analysis_window: np.ndarray = None
        self.synthesis_window: np.ndarray = W.hanning(self.frame_length)

    def convert(self) -> A2S_TSM:

        self.setVariables()

        return A2S_TSM(
            converter=self.converter, channels=self.channels, frame_length=self.frame_length,
            analysis_hop=self.analysis_hop, synthesis_hop=self.synthesis_hop,
            analysis_window=self.analysis_window, synthesis_window=self.synthesis_window
        )