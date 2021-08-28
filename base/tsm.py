# -*- coding: utf-8 -*-

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

        finished = False
        while not (finished and reader.empty):
            self.readFrom(reader)
            _, finished = self.writeTo(writer)

        if flush:
            finished = False
            while not finished:
                _, finished = self.flushTo(writer)

        