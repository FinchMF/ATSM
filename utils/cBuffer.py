
import numpy as np

class CBuffer(object):

    def __init__(self, channels: int, max_length: int):

        self.__data: np.ndarray = np.zeros((channels, max_length), dtype=np.float32)
        self.__channels: int = channels
        self.__max_length: int = max_length

        self.__offset: int = 0
        self.__ready: int = 0
        self.__length: int = 0


    @property
    def data(self) -> np.ndarray:
        return self.__data

    @data.setter
    def data(self, x: np.ndarray):
        self.__data = x

    @property
    def channels(self) -> int:
        return self.__channels

    @channels.setter
    def channels(self, x: int):
        self.__channels: int = x

    @property
    def max_length(self) -> int:
        return self.__max_length
    
    @max_length.setter
    def max_length(self, x: int):
        self.__max_length: int = x

    @property
    def offset(self) -> int:
        return self.__offset

    @offset.setter
    def offset(self, x: int):
        self.__offset: int = offset

    @property
    def ready(self) -> int:
        return self.__ready

    @ready.setter
    def ready(self, x: int):
        self.__ready: int = x

    @property
    def length(self) -> int:
        return self.__length

    @length.setter
    def length(self, x: int):
        self__.length: int = x

    @property
    def remaining_length(self) -> int:
        return self.__max_length - self.__ready


    def __repr__(self):
        return f'CBuffer(offset={self.offset}, lenght={self.length},\
                 ready={self.ready}, data=\n{repr(self.to_array())}'

    def compareBuffer(self, n: int):
        """function to evaluate channels in a buffer"""
        if n != self.data.shape[0]:
            raise ValueError('buffers should have the same number of channels')

    def checkCBufferSpace(self, n: int, length: bool = False, 
                                        max_: bool = False, 
                                        ready: bool = False):
        """function evaluate space in :class:`CBuffer`"""
        
        if not max_:
            if n > self.length:
                raise ValueError('not enough space in CBuffer')
        
        if max_:
            if n > self.max_length - self.length:
                raise ValueError('not enough space in CBuffer')

        if ready:
            if self.ready + n > self.length:
                raise ValueError('not enough samples ot be marked as ready')
            
    def validateBuffer(self, buffer: np.ndarray):
        """function to validate buffer """
        self.compareBuffer(n=buffer.shape[0])
        self.checkCBufferSpace(n=buffer.shape[1], length=True)

    def computeSlice(self, n: int) -> tuple:
        """function to location signal slice"""
        return self.offset, self.offset + n

    def add(self, buffer: np.ndarray):
        """function to add a buffer element-wise"""

        self.validateBuffer(buffer=buffer)
        n: int = buffer.shape[1]
        start, end = self.computeSlice(n=n)

        if end <= self.max_length:
            self.data[:, start:end] += buffer[:, :n]

        else:
            end -= self.max_length
            self.data[:, start:] += buffer[:, :self.max_length - start]
            self.data[:, :end] += buffer[:, self.max_length - start:n]

    def divide(self, array: np.ndarray):
        """function to divide each channel element-wise by passed array"""

        n: int = len(array)
        self.checkCBufferSpace(n=n, length=True)
        start, end = self.computeSlice(n=n)

        if end <= self.max_length:
            self.data[:, start:end] /= array[:n]

        else:
            end -= self.max_length
            self.data[:, start:] /= array[:self.max_length - start]
            self.data[:, :end] /= array[self.max_length - start:n]

    def peek(self, buffer: np.ndarray) -> int:
        """reads samples from CBuffer without removing and adds them to buffer"""
        n: int = buffer.shape[0]
        self.compareBuffer(n=n)
        start, end = self.computeSlice(n=min(buffer.shape[1], self.ready))

        if end <= self.max_length:
            np.copyto(buffer[:, :n], self.data[:, start:end])
        
        else:
            end -= self.max_length
            np.copyto(buffer[:, :self.max_length - start], self.data[:, start:])
            np.copyto(buffer[:, self.max_length - start:n], self.data[:, :end])

        return n

    def read(self, buffer: np.ndarray) -> int:
        """reads samples implementing self.peek,
           then removes them from CBuffer implementing self.remove()"""
        n: int = self.peek(buffer=buffer)
        self.remove(n=n)
        return n

    def read_from(self, reader) -> int:
        """reads samples from reader and returns number of samples read"""
        start: int = (self.offset + self.length) % self.max_length
        end: int = start + self.max_length - self.length

        if end <= self.max_length:
            n: int = reader.read(self.data[:, start:end])

        else:
            end -= self.max_length

            n: int = reader.read(self.data[:, start:])
            n += reader.read(self.data[:, :end])

        self.length += n
        self.ready = self.length

        return n

    def remove(self, n: int) -> int:
        """function to remove samples already read"""
        if n >= self.length:
            n: int = self.length

        start, end = self.computeSlice(n=n)

        if end <= self.max_length:
            self.data[:, start:end]: int = 0

        else:
            end -= self.max_length
            self.data[:, start:]: int = 0
            self.data[:, :end]: int = 0

        self.offset += n
        self.offset %= self.max_length
        self.length -= n

        self.ready -= n
        if self.ready < 0:
            self.ready: int = 0

        return n

    def right_pad(self, n: int):
        """function to pad end of buffer with zeros"""
        self.checkCBufferSpace(n=n, max_=True)
        self.length += n

    def set_ready(self, n: int):
        """function to mark samples as ready to be ready"""
        self.checkCBufferSpace(n=n, ready=True)
        self.ready += n

    def to_array(self):
        """function to copy data in CBuffer"""
        out: np.ndarray = np.empty((self.channels, self.ready))
        self.peek(out)
        return out
        
    def write(self, buffer: np.ndarray) -> int:
        """function to write samples from buffer to CBuffer"""
        self.compareBuffer(n=buffer.shape[1])
        n = min(buffer.shape[1], self.max_length - self.length)

        start: int = (self.offset + self.length) % self.max_length
        end: int = start + n

        if end <= self.max_length:
            np.copyto(self.data[:, start:end], buffer[:, :n])
        
        else:
            end -= self.max_length
            np.copyto(self.data[:, start:], buffer[:, :self.max_length - start])
            np.copyto(self.data[:, :end], buffer[:, self.max_length - start:n])

        self.length += n
        self.ready = self.length

        return n

    def write_to(self, writer) -> int:
        """writes samples to writer and deletes them, then returns number written"""
        start, end = self.computeSlice(n=self.ready)

        if end <= self.max_length:
            n: int = writer.write(self.data[:, start:end])
        
        else:
            end -= self.max_length
            n: int = writer.write(self.data[:, start:])
            n += writer.write(self.data[:, :end])

        self.remove(n)

        return n