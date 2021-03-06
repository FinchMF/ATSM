"""
module containig implementation of base classes
"""

import wave
import numpy as np
from . import base

class WavIn(base.Reader):

    def __init__(self, filename: str):

        self.__reader = wave.open(filename, 'rb')

    def __enter__(self) -> object:
        return self

    def __exit__(self, _1, _2, _3):
        self.close()

    @property
    def reader(self) -> object:
        return self.__reader

    @property
    def channels(self) -> int:
        return self.__reader.getnchannels()

    @property
    def empty(self) -> bool:
        return self.__reader.tell() == self.reader.getnframes()

    @property
    def samplerate(self) -> float:
        return self.__reader.getframerate()

    @property
    def samplewidth(self) -> int:
        return self.__reader.getsamplewidth()

    
    def close(self):
        self.__reader.close()

    def read(self, buffer: np.ndarray) -> int:
        # implemenation of audio read functionality
        if buffer.shape[0] != self.channels:
            raise ValueError('the buffer should have the number\
                               of channels as the WavIn')
        # read in frames from buffer
        frames: np.ndarray = self.reader.readframes(buffer.shape[1])
        # normalize the volume by dividing each frame's amplitude by the ceiling
        frames: np.ndarray = np.frombuffer(frames, '<i2').astype(np.float32) / 32676
        # separate channels
        frames: np.ndarray = frames.reshape((-1, self.channels)).T
        # copy read data
        n: int = frames.shape[1]
        np.copyto(buffer[:, :n], frames)
        del frames

        return n

    def skip(self, n: int) -> int:
        # implementation of skip functionality
        current_pos: int = self.reader.tell()
        new_pos: int = min(current_pos + n, self.reader.getnframes())
        self.reader.setpos(new_pos)
        # return number of skipped frames
        return new_pos - current_pos


class WavOut(base.Writer):

    def __init__(self, filename: str, channels: int, samplerate: float):

        self.__writer: object = wave.open(filename, 'wb')
        self.__channels: int = channels
        self.writer.setnchannels(channels)
        self.writer.setframerate(samplerate)
        self.writer.setsampwidth(2)

    def __enter__(self) -> object:
        return self

    def __exit__(self, _1, _2, _3):
        self.close()

    @property
    def channels(self) -> int:
        return self.__channels
    
    @property
    def writer(self) -> object:
        return self.__writer

    def close(self):
        self.writer.close()

    def write(self, buffer: np.ndarray) -> int:
        # implementation of audio write functionality
        if buffer.shape[0] != self.channels:
            raise ValueError('the buffer should have the same number\
                              channels as the WavOut')
        # normalize buffer
        np.clip(buffer, -1, 1, out=buffer)
        # expand array of frames to values within amplitude range
        # convert to btyes to written in WAV format 
        n: int = buffer.shape[1]
        frames: bytes = (buffer.T.reshape((-1,)) * 32676).astype(np.int16).tobytes()
        self.writer.writeframes(frames)
        del frames

        return n