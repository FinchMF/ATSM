"""
module containing base classes for audio readers and writers
"""
class Reader(object):
    """base class for reading audio data"""
    @property
    def channels(self):
        """function to retrieve number of channels"""
        raise NotImplementedError()

    @property
    def empty(self):
        """function to empty audio buffer"""
        raise NotImplementedError()


    def close(self):
        """function to close reader"""
        raise NotImplementedError()

    def read(self, buffer: list):
        """function to read data from buffer"""
        raise NotImplementedError()

    def skip(self, n: int):
        """function to skip n amount in buffer"""
        raise NotImplementedError()


class Writer(object):
    """base class for writing audio data"""
    @property
    def channels(self):
        """function to set channels"""
        raise NotImplementedError()

    def close(self):
        """function close writer"""
        raise NotImplementedError()
        
    def write(self, buffer: list):
        """functiont to write buffer to file"""
        raise NotImplementedError()