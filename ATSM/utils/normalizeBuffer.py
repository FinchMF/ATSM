"""
module containing Normalizing buffer
"""

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

    @offset.setter
    def offset(self, x: int):
        self.__offset: int = x

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

        start = self.offset
        end = self.offset + n

        if end <= self.length:
            self.data[start:end] += window

        else:
            end -= self.length
            self.data[start:] += window[:self.length - start]
            self.data[:end] += window[self.length - start:]

    def remove(self, n: int):
        """function to remove the first n values"""
        if n >= self.length:
            n = self.length
        if n == 0:
            return

        # Compute the slice of data to reset
        start = self.offset
        end = self.offset + n

        if end <= self.length:
            self.data[start:end] = 0
        else:
            end -= self.length
            self.data[start:] = 0
            self.data[:end] = 0

        self.offset += n
        self.offset %= self.length
    
    def to_array(self, start: int = 0, end: int = None) -> np.ndarray:
        """function to return array copied from :class:`NormalizeBuffer` 
           from ``start`` (included) to ``end`` (excluded)"""  

        if end is None:
            end: int = self.length

        start += self.offset
        end += self.offset

        if end <= self.length:
            return np.copy(self.data[start:end])

        end -= self.length
        if start < self.length:
            return np.concatenate((self.data[start:], self.data[:end]))

        start -= self.length
        return np.copy(self.data[start:end])