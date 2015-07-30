import pytest
import sys


@pytest.fixture
def clean_registry():
    import decorrelate
    registry = decorrelate.get_registry()
    registry._registered = {}
    ressources_module_name = 'decorrelate.tests.ressources'
    if ressources_module_name in sys.modules:
        del sys.modules[ressources_module_name]


def test_get_proxy(clean_registry):
    import decorrelate
    registry = decorrelate.get_registry()

    def func():
        pass

    def callback():
        pass

    decorrelate.get_proxy(func, callback)

    assert len(registry) == 1


def test_get_proxy_with_category(clean_registry):
    import decorrelate
    registry = decorrelate.get_registry()

    def func():
        pass

    def callback():
        pass

    decorrelate.get_proxy(func, callback, category='test_category')

    assert len(registry) == 1


def test_original(clean_registry):
    import decorrelate
    registry = decorrelate.get_registry()

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        return decorrelate.get_proxy(wrapped, callback)

    @decorator
    def test_func():
        pass

    assert hasattr(test_func, 'wrapped') is False
    assert len(registry) == 1


def test_activates(clean_registry):
    import decorrelate
    registry = decorrelate.get_registry()

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        return decorrelate.get_proxy(wrapped, callback)

    @decorator
    def test_func():
        pass

    assert hasattr(test_func, 'wrapped') is False
    assert len(registry) == 1

    decorrelate.activates()

    assert hasattr(test_func, 'wrapped')
    assert len(registry) == 0


def test_activates_proxy_attributes(clean_registry):
    import decorrelate

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            callable.__doc__ = 'A test function after wrapping'
            return callable
        return decorrelate.get_proxy(wrapped, callback)

    @decorator
    def test_func():
        """A test function"""
        pass

    assert test_func.__doc__ == 'A test function'
    assert isinstance(test_func, decorrelate.Proxy)
    assert test_func.__name__ == 'test_func'
    assert not repr(test_func).startswith('<decorrelate.Proxy object')

    decorrelate.activates()

    assert test_func.__doc__ == 'A test function after wrapping'
    assert isinstance(test_func, decorrelate.Proxy)
    assert test_func.__name__ == 'test_func'
    assert not repr(test_func).startswith('<decorrelate.Proxy object')


def test_activates_decorator_with_parameter(clean_registry):
    import decorrelate
    registry = decorrelate.get_registry()

    def decorator(value, **kwargs):
        def wrapper(wrapped):
            def callback(callable):
                callable.wrapped = True
                callable.value = value
                for key, val in kwargs.items():
                    setattr(callable, key, val)
                return callable
            return decorrelate.get_proxy(wrapped, callback)
        return wrapper

    @decorator('My value', one=1, two=2, three=3)
    def test_func():
        pass

    assert hasattr(test_func, 'wrapped') is False
    assert hasattr(test_func, 'value') is False
    assert hasattr(test_func, 'one') is False
    assert hasattr(test_func, 'two') is False
    assert hasattr(test_func, 'three') is False
    assert len(registry) == 1

    decorrelate.activates()

    assert hasattr(test_func, 'wrapped')
    assert hasattr(test_func, 'value')
    assert test_func.value == 'My value'
    assert hasattr(test_func, 'one')
    assert test_func.one == 1
    assert hasattr(test_func, 'two')
    assert test_func.two == 2
    assert hasattr(test_func, 'three')
    assert test_func.three == 3
    assert len(registry) == 0


def test_activates_with_category(clean_registry):
    import decorrelate
    registry = decorrelate.get_registry()

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        return decorrelate.get_proxy(wrapped, callback, category='a category')

    def decorator2(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        return decorrelate.get_proxy(wrapped, callback)

    @decorator
    def test_func():
        pass

    @decorator2
    def test_func2():
        pass

    assert hasattr(test_func, 'wrapped') is False
    assert len(registry) == 2

    decorrelate.activates(category='a category')

    assert hasattr(test_func, 'wrapped')
    assert len(registry) == 1
    assert len(registry._registered['default']) == 1
    assert len(registry._registered['a category']) == 0


def test_activates_with_same_category(clean_registry):
    import decorrelate
    registry = decorrelate.get_registry()

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        return decorrelate.get_proxy(wrapped, callback, category='a category')

    def decorator2(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        return decorrelate.get_proxy(wrapped, callback, category='a category')

    @decorator
    def test_func():
        pass

    @decorator2
    def test_func2():
        pass

    assert hasattr(test_func, 'wrapped') is False
    assert len(registry) == 2

    decorrelate.activates(category='a category')

    assert hasattr(test_func, 'wrapped')
    assert len(registry) == 0
    assert len(registry._registered['a category']) == 0


def test_singleton(clean_registry):
    import decorrelate

    assert decorrelate.get_registry() == decorrelate.get_registry()
    assert id(decorrelate.get_registry()) == id(decorrelate.get_registry())


def test_decorrate_a_function(clean_registry):
    import decorrelate

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        return decorrelate.get_proxy(wrapped, callback)

    @decorator
    def a_test_function():
        pass

    assert hasattr(a_test_function, 'wrapped') is False
    decorrelate.activates()
    assert hasattr(a_test_function, 'wrapped')


def test_decorrate_a_function_from_another_module(clean_registry):
    import decorrelate
    from decorrelate.tests.ressources import a_test_function

    assert hasattr(a_test_function, 'wrapped') is False
    decorrelate.activates()
    assert hasattr(a_test_function, 'wrapped')


def test_decorrate_a_class(clean_registry):
    import decorrelate

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        return decorrelate.get_proxy(wrapped, callback)

    @decorator
    class ATestClass(object):

        def __init__(self, *args, **kwargs):
            pass

        def __call__(self):
            pass

    assert hasattr(ATestClass(), 'wrapped') is False
    assert repr(ATestClass) == repr(ATestClass._callable)
    decorrelate.activates()
    assert hasattr(ATestClass(), 'wrapped')


def test_decorrate_a_class_from_another_module(clean_registry):
    import decorrelate
    from decorrelate.tests.ressources import ATestClass

    assert hasattr(ATestClass(), 'wrapped') is False
    assert repr(ATestClass) == repr(ATestClass._callable)
    decorrelate.activates()
    assert hasattr(ATestClass(), 'wrapped')


def test_decorrate_a_method(clean_registry):
    import decorrelate

    def decorator(wrapped):
        def callback(callable):
            callable.wrapped = True
            return callable
        return decorrelate.get_proxy(wrapped, callback)

    class ATestClass(object):

        def __init__(self, *args, **kwargs):
            pass

        @decorator
        def a_test_method(self):
            pass

        def __call__(self):
            pass

    assert hasattr(ATestClass().a_test_method, 'wrapped') is False
    decorrelate.activates()
    assert hasattr(ATestClass().a_test_method, 'wrapped')


def test_decorrate_a_method_from_another_module(clean_registry):
    import decorrelate
    from decorrelate.tests.ressources import ATestClassWithDecoratedMethod

    assert hasattr(ATestClassWithDecoratedMethod().a_test_method, 'wrapped') is False
    decorrelate.activates()
    assert hasattr(ATestClassWithDecoratedMethod().a_test_method, 'wrapped')
