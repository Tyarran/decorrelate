import pytest


@pytest.fixture
def clean_registry():
    import decorelate

    decorelate.registry.registered = []


def test_register(clean_registry):
    import decorelate

    def func():
        pass

    def callback():
        pass

    decorelate.register(func, callback)

    assert len(decorelate.registry) == 1


def test_original(clean_registry):
    import decorelate

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        decorelate.register(wrapped, callback)
        return wrapped

    @decorator
    def test_func():
        pass

    assert hasattr(test_func, 'wrapped') is False
    assert len(decorelate.registry) == 1


def test_start(clean_registry):
    import decorelate

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        decorelate.register(wrapped, callback)
        return wrapped

    @decorator
    def test_func():
        pass

    assert hasattr(test_func, 'wrapped') is False
    assert len(decorelate.registry) == 1

    decorelate.start()

    assert hasattr(test_func, 'wrapped')
    assert len(decorelate.registry) == 0


def test_start_decorator_with_parameter(clean_registry):
    import decorelate

    def decorator(value, **kwargs):
        def wrapper(wrapped):
            def callback(callable):
                callable.wrapped = True
                callable.value = value
                for key, val in kwargs.items():
                    setattr(callable, key, val)
                return callable
            decorelate.register(wrapped, callback)
            return wrapped
        return wrapper

    @decorator('My value', one=1, two=2, three=3)
    def test_func():
        pass

    assert hasattr(test_func, 'wrapped') is False
    assert hasattr(test_func, 'value') is False
    assert hasattr(test_func, 'one') is False
    assert hasattr(test_func, 'two') is False
    assert hasattr(test_func, 'three') is False
    assert len(decorelate.registry) == 1

    decorelate.start()

    assert hasattr(test_func, 'wrapped')
    assert hasattr(test_func, 'value')
    assert test_func.value == 'My value'
    assert hasattr(test_func, 'one')
    assert test_func.one == 1
    assert hasattr(test_func, 'two')
    assert test_func.two == 2
    assert hasattr(test_func, 'three')
    assert test_func.three == 3
    assert len(decorelate.registry) == 0
