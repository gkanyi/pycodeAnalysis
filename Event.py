class Event(object):
    def __init__(self, eventType, data):
        self._type = eventType
        self._data = data

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data