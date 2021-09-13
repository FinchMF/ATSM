
from ATSM.a2m import A2S_TSM, Converter
from ATSM.utils.windows import Windows as W


class OLAConverter(Converter):

    def convert_frame(self, analysis_frame: int) -> int:
        return analysis_frame

class OLA:

    @staticmethod
    def convert(channels: int, speed: float = 1., 
            frame_length: int = 256, analysis_hop: int = None,
            synthesis_hop: int = None) -> object:

        if synthesis_hop is None:
            synthesis_hop: int = frame_length // 2
        
        if analysis_hop is None:
            analysis_hop: int = int(synthesis_hop * speed)

        analysis_window: None = None
        synthesis_window: np.ndarray = W.hanning(frame_length)

        converter: Converter = OLAConverter()

        return A2S_TSM(
            converter, channels, frame_length, 
            analysis_hop, synthesis_hop, 
            analysis_window, synthesis_window
        )