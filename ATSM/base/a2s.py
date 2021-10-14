"""
module containing conversion process between 
analysis and synthesis frames during modulation
"""
import numpy as np
from ATSM.utils import Windows as W
from ATSM.utils import CBuffer, NormalizeBuffer
from .tsm import TSM

EPSILON: float = 0.0001

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
        self.__channels: int = channels
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

        # if self.normalize_window is None:
        #     self.normalize_window: np.ndarray = np.ones(self.frame_length)

        # delta: int = self.delta_before + self.delta_after
        # # check cbuffer 
        # self.__in_buffer = CBuffer(self.channels, self.frame_length + delta)
        # self.__analysis_frame: np.ndarray = np.empty(
        #     (self.channels, self.frame_length + delta)
        # )
        # self.__out_buffer = CBuffer(self.channels, self.frame_length)
        # self.__normalize_buffer = NormalizeBuffer(self.frame_length)

        # self.clear()
        
        self.checkNormalWindow()
        self.initializeBuffers()

    @property
    def converter(self) -> object:
        return self.__converter

    @property
    def channels(self) -> int:
        return self.__channels

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

    @delta_before.setter
    def delta_before(self, x: int):
        self.__delta_before: int = x

    @property
    def delta_after(self) -> int:
        return self.__delta_after
    
    @delta_after.setter
    def delta_after(self, x: int):
        self.__delta_after: int = x

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

    @property
    def normalize_buffer(self) -> NormalizeBuffer:
        return self.__normalize_buffer
    
    @normalize_buffer.setter
    def normalize_buffer(self, x: NormalizeBuffer) -> NormalizeBuffer:
        self.__normalize_buffer: NormalizeBuffer = x

    
    def checkNormalWindow(self):
        """function to check normalized window"""
        if self.normalize_window is None:
            # set normalized to to a an array of ones 
            self.normalize_window: np.ndarray = np.ones(self.frame_length)

    def initializeBuffers(self):
        """function to initialize buffers"""
        delta: int = self.delta_before + self.delta_after
        self.__in_buffer: CBuffer = CBuffer(self.channels, self.frame_length + delta)
        self.__analysis_frame: np.ndarray = np.empty(
            (self.channels, self.frame_length + delta)
        )
        self.__out_buffer: CBuffer = CBuffer(self.channels, self.frame_length)
        self.__normalize_buffer: NormalizeBuffer = NormalizeBuffer(self.frame_length)

        self.clear()

    def clear(self):
        # implementation of clear functionality
        self.in_buffer.remove(self.in_buffer.length)
        self.out_buffer.remove(self.out_buffer.length)
        self.out_buffer.right_pad(self.frame_length)
        self.normalize_buffer.remove(self.normalize_buffer.length)
        # move to the middle of the frame
        self.in_buffer.write(np.zeros(
            (self.channels, self.delta_before + self.frame_length // 2)))
        self.skip_output_samples = self.frame_length // 2
        # clear the converter
        self.converter.clear()

    def flushTo(self, writer: object) -> tuple:
        # implemention of flush functionality
        if self.in_buffer.remaining_length == 0:
            raise RuntimeError("There is still data to process in the input buffer, \
                                flush_to only to be called when write_to returns True")
        # flush data from out buffer to audio writer
        n: int = self.out_buffer.write_to(writer)
        if self.out_buffer.ready == 0:
            self.clear()
            result: tuple = (n, True)
        else:
            result: tuple = (n, False)

        return result

    def getMaxOutputLength(self, input_lenght: int) -> int:
        # implementation of max output functionality
        input_length -= self.skip_input_samples
        if input_length <= 0:
            n_frames: int = 0
        else:
            n_frames: int = input_lenth // self.analysis_hop + 1
        # compute number of frames with synthesis hop to find output length
        return n_frames * self.synthesis_hop

    def _process_frame(self):
        """
        read an analysis frame from the input buffer, process it 
        and write to output buffer
        """
        # generate analysis frame and remove unneeded samples
        self.in_buffer.peek(self.analysis_frame)
        self.in_buffer.remove(self.analysis_hop)
        # apply analysis frame to the analysis window
        W.apply(self.analysis_frame, self.analysis_window)
        # generate sythesis frame
        synthesis_frame: int = self.converter.convert_frame(self.analysis_frame)
        # apply synthesis frame to synthesis window
        W.apply(synthesis_frame, self.synthesis_window)
        # add the the synthesis frame to the out buffer
        self.out_buffer.add(synthesis_frame)
        # set normalization window to the normalization buffer
        self.normalize_buffer.add(self.normalize_window)
        # normalize synthesized frames
        normalize: object = self.normalize_buffer.to_array(end=self.synthesis_hop)
        normalize[normalize < EPSILON] = 1
        self.out_buffer.divide(normalize)
        self.out_buffer.set_ready(self.synthesis_hop)
        self.normalize_buffer.remove(self.synthesis_hop)

    def readFrom(self, reader: object) -> int:
        # implementation of read from functionality
        n: int = reader.skip(self.skip_input_samples)
        self.skip_input_samples -= n

        if self.skip_input_samples > 0:
            result: int = n

        else:
            n += self.in_buffer.read_from(reader)
            result: int = n
            if (self.in_buffer.remaining_length == 0 and 
                self.out_buffer.remaining_length >= self.synthesis_hop):
                # store output in the output buffer
                self._process_frame()
                # skip output samples if necessary
                skipped: int = self.out_buffer.remove(self.skip_output_samples)
                self.out_buffer.right_pad(skipped)
                self.skip_output_samples -= skipped
                # set the number of input samples to be skipped
                self.skip_input_samples: int = self.analysis_hop - self.frame_length
                if self.skip_input_samples < 0:
                    self.skip_input_samples = 0

        return result

    def setSpeed(self, speed: float):
        # implementation of declaring speed for modulation functionality
        self.analysis_hop: int = int(self.synthesis_hop * speed)
        self.converter.set_analysis_hop(self.analysis_hop)

    def writeTo(self, writer: object) -> tuple: 
        # implementation of write to file from buffer functionality
        n: int = self.out_buffer.write_to(writer)
        self.out_buffer.right_pad(n)

        if (self.in_buffer.remaining_length > 0 and self.out_buffer.ready == 0):
            result: tuple = (n, True)
        
        else:
            result: tuple = (n, False)

        return result


class Converter(object):
    """base object for converter"""
    def clear(self):
        """function to clear buffers"""
        return

    def convert_frame(self, analysis_frame: int):
        """functiont to convert analysis frames to synthesis frames"""
        raise NotImplementedError

    def set_analysis_hop(self, analysist_hop: int):
        """function to set analysis hop"""
        return