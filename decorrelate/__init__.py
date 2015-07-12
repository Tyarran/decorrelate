class Registry(object):
    _registered = None

    def __init__(self):
        self._registered = {}

    def __len__(self):
        return len(list(self.__iter__()))

    def __iter__(self):
        return (value for categ in self._registered.values() for value in categ)


def singleton():
    registry = Registry()

    def get_registry():
        return registry

    return get_registry


get_registry = singleton()


def register(func, callback, category='default'):
    registry = get_registry()
    if category not in registry._registered:
        registry._registered[category] = []
    registry._registered[category].append((func, callback, ))


def start():
    registry = get_registry()
    for callable, callback in registry:
        callback_result = callback(callable)
        callable = callback_result
    registry._registered = {}
