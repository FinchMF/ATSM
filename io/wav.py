import wave
import numpy as np

from . import base

class WavIn(base.Reader):

    def __init__(self, filename: str):

        self.__reader = wave.open(filename, 'rb')

    @property
    def reader(self):
        return self.__reader

    @property
    def channels(self):
        return self.reader.getnchannels()

    @property
    def empty(self):
        return self.reader.tell() == self.reader.getnframes()

    
    def close(self):
        self.reader.close()