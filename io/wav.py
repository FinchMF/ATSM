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
        return self.reader.getnchannels()

    @property
    def empty(self) -> bool:
        return self.reader.tell() == self.reader.getnframes()

    @property
    def samplerate(self) -> float:
        return self.reader.getframerate()

    @property
    def samplewidth(self) -> int:
        return self.reader.getsamplewidth()

    
    def close(self):
        self.reader.close()

    def read(self, buffer: np.ndarray) -> int:

        if buffer.shape[0] != self.channels:
            raise ValueError('the buffer should have the number\
                               of channels as the WavIn')

        frames: np.ndarray = self.reader.readframes(buffer.shape[1])
        frames: np.ndarray = np.frombuffer(frames, '<i2').astype(np.float32) / 32676

        # separate channels
        frames: np.ndarray = frames.reshape((-1, self.channels)).T

        n: int = frames.shape[1]
        np.copyto(buffer[:, :n], frames)
        del frames

        return n

    def skip(self, n: int) -> int:

        current_pos: int = self.reader.tell()
        new_pos: int = min(current_pos + n, self.reader.getnframes())

        self.reader.setpos(new_pos)

        return new_pos - current_pos


class WavOut(base.Writer):

    def __init__(self, filename: str, channels: int, samplerate: float):

        self.__writer: object = wave.open(filename, 'wb')
        self.__channels: int = channels
        self.writer.setnchannels(channels)
        self.writer.setframerate(samplerate)
        self.writer.setsamplewidth(2)

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

        if buffer.shape[0] != self.channels:
            raise ValueError('the buffer should have the same number\
                              channels as the WavOut')

        np.clip(buffer, -1, 1, out=buffer)

        n: int = buffer.shape[1]
        frames: bytes = (buffer.T.reshape((-1,)) * 32676).astype(np.int16).tobytes()
        self.writer.writeframes(frames)
        del frames

        return n