# -*- coding: utf-8 -*-
import progressbar

class TSM(object):

    def clear(self):
        raise NotImplementedError

    def flushTo(self, writer):
        raise NotImplementedError

    def getMaxOutputLength(self, inputLength):
        raise NotImplementedError

    def readFrom(self, reader):
        raise NotImplementedError

    def writeTo(self, writer):
        raise NotImplementedError

    def setSpeed(self, speed):
        raise NotImplementedError

    def run(self, reader, writer, flush=True):

        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        i: int = 0
        finished = False
        while not (finished and reader.empty):
            i+=1
            self.readFrom(reader)
            _, finished = self.writeTo(writer)
            bar.update(i)

        if flush:
            finished = False
            while not finished:
                _, finished = self.flushTo(writer)

            self.clear()