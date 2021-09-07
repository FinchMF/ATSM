
import numpy as np

class NormalizeBuffer(object):

    def __init__(self, length: int):

        self.__data: np.ndarray = np.zeros(length)
        self.__offset: int = 0
        self.__length: int = length


    @property
    def data(self) -> np.ndarray:
        return self.__data

    @property
    def offset(self) -> int:
        return self.__offset

    @property
    def length(self) -> int:
        return self.__length


    def __repr__(self) -> str:
        return f"NormalizeBuffer(offset={self.offset}, length={self.length},\
                 data=\n{repr(self.to_array())}"

    def computeSlice(self, n: int) -> tuple:
        """function to locate signal slice"""
        return self.offset, self.offset + n

    def add(self, window: np.ndarray):
        """function to add a window element wise to :class:'NormalizeBuffer'"""
        n: int = len(window)
        if n > self.length:
            raise ValueError('the window should be smaller than the \
                              NormalizeBuffer')

        start, end = self.computeSlice(n=n)

        if end <= self.length:
            self.data[start:end] += window

        else:
            end -= self.length
            self.data[start:] += window[:self.length - start]
            self.data[:end] += window[self.length - start:]

    def remove(self, n: int):

        pass
    
    def to_array(self, start: int = 0, end: int = None) -> np.ndarray:

        pass   