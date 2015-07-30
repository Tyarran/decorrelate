import decorrelate


def decorator(wrapped):
    def callback(callable):
        callable.wrapped = True
        return callable
    result = decorrelate.get_proxy(wrapped, callback)
    return result


@decorator
def a_test_function():
    pass


@decorator
class ATestClass(object):

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self):
        pass


class ATestClassWithDecoratedMethod(object):

    def __init__(self, *args, **kwargs):
        pass

    @decorator
    def a_test_method(self):
        pass

    def __call__(self):
        pass
