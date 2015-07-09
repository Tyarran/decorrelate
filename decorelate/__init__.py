class Registry(object):
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if len(self.__dict__) == 0:
            self.registered = []

    def __len__(self):
        return len(self.registered)

    def __iter__(self):
        return (item for item in self.registered)


def register(func, callback):
    registry = Registry()
    registry.registered.append((func, callback, ))


def start():
    registry = Registry()
    for callable, callback in registry:
        callback_result = callback(callable)
        callable = callback_result
    registry.registered = []

registry = Registry()
