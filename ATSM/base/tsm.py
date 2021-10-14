"""
module containing base class for time scale modulation
"""

import progressbar

class TSM(object):
    """object containing time scale modualation functionality"""
    def clear(self):
        """function to clear buffer"""
        raise NotImplementedError

    def flushTo(self, writer: object):
        """function to flush buffer"""
        raise NotImplementedError

    def getMaxOutputLength(self, inputLength: int):
        """function to get output length given input length"""
        raise NotImplementedError

    def readFrom(self, reader: object):
        """function to read from buffer"""
        raise NotImplementedError

    def writeTo(self, writer: object):
        """function to write to buffer"""
        raise NotImplementedError

    def setSpeed(self, speed: float):
        """function to set speed of modulation"""
        raise NotImplementedError

    def run(self, reader: object, writer: object, flush: bool=True):
        """function to run time scale modulation process"""
        # set progress bar for read out in terminal
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        i: int = 0
        # set read and write process
        finished = False
        while not (finished and reader.empty):
            i+=1
            self.readFrom(reader)
            _, finished = self.writeTo(writer)
            bar.update(i)
        # flush and clear data 
        if flush:
            finished = False
            while not finished:
                _, finished = self.flushTo(writer)

            self.clear()