class Registry(object):

    def __init__(self):
        self.registered = []

    def __len__(self):
        return len(self.registered)

    def __iter__(self):
        return (item for item in self.registered)


def singleton():
    registry = Registry()

    def get_registry():
        return registry

    return get_registry


get_registry = singleton()


def register(func, callback, category='default'):
    registry = get_registry()
    registry.registered.append((func, callback, ))


def start():
    registry = get_registry()
    for callable, callback in registry:
        callback_result = callback(callable)
        callable = callback_result
    registry.registered = []
