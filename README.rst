Decorrelate
###########


.. image:: https://travis-ci.org/rcommande/decorrelate.svg?branch=master
    :target: https://travis-ci.org/rcommande/decorrelate


Sometimes, you need to control when your decorators will be actived. For example, in your unit tests, you may want to test the original function and not the decorated function. "Decorrelate" is a very minimalist helper who help you to perform this task. If your needs are more complicated, you must look at the `Venusian`_ module or another.

Installation
++++++++++++

.. code-block:: console

    pip install decorrelate

Usage
+++++

.. code-block:: pycon

    >>> import decorrelate

    >>> def decorator(wrapped):
    >>>    def callback(callable):
    >>>        callable.wrapped = True
    >>>        return callable
    >>>    return decorrelate.get_proxy(wrapped, callback)

This is an simple decorator that adds a "wrapped" attribute to a callable. This decorator call the "decorrelate.get_proxy()" function who return an proxy object which will act as the original function.


The callback function is a simple function that returns the decorated callable and will be called by "Decorrelate" when we shall need it. It's the real decorator. This function takes the original function as the only one parameter and works like a classical decorator wrapper function.


.. code-block:: pycon

    >>> @decorator
    >>> def a_function():
    >>>    print("a function")

    >>> a_function()
    "a function"

    >>> hasattr(a_function, "wrapped")
    False

    >>> isinstance(a_function, decorrelate.Proxy)
    True


At this moment, "a_function" function is not the original function but a "**decorrelate.Proxy()**" object and his behaviour as the same as the original function (in fact, the proxy really calls the original function internally).

The decorator is now not activated as if there was no decorator. But now, we want it. We have just to call the "**decorrelate.activates()**" function :

.. code-block:: pycon

   >>> decorrelate.activates()
   >>> hasattr(a_function, "wrapped")
   True

   >>> a_function.wrapped
   True

   >>> isinstance(a_function, decorrelate.Proxy)
   True

The call to "**decorrelate.activates()**" function was changed the proxy behaviour. Instead of calling the original function, it now calls the wrapped function. To get it, "**decorrelate.activates()**" function had to use the callback function.


"a_function" is now wrapped by our decorator.


.. _Venusian: https://pypi.python.org/pypi/venusian/1.0
