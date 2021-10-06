
class Reader(object):

    @property
    def channels(self):
        raise NotImplementedError()

    @property
    def empty(self):
        raise NotImplementedError()


    def read(self, buffer: list):
        raise NotImplementedError()

    def skip(self, n: int):
        raise NotImplementedError()


class Writer(object):

    @property
    def channels(self):
        raise NotImplementedError()

    
    def write(self, buffer: list):
        raise NotImplementedError()