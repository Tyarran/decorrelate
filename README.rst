Decorrelate
###########


.. image:: https://travis-ci.org/rcommande/decorrelate.svg?branch=master
    :target: https://travis-ci.org/rcommande/decorrelate


Sometime, you need to control when your decorators will be actived. For example, in your unit tests, you may want to test the original function and not the decorated function. "Decorrelate" is an helper who help you to perform this task. This is very minimalist. If your needs are complexe, you must look at the `Venusian`_ module or another.

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
    >>>    decorrelate.register(wrapped, callback)
    >>>    return wrapped

This is an simple decorator that adds a attribute "wrapped" to a callable. This decorator registers the original callable with a callback and returns the original callable directly **and not a "wrapped callable"**.


The callback is a simple function that returns the decorated callable and will be called by "Decorrelate" when we shall need it.


.. code-block:: pycon

    >>> @decorator
    >>> def a_function():
    >>>    print("a function")

    >>> a_function()
    "a function"

    hasattr(a_function, "wrapped")
    False


At this moment, "a_function" function is not decorated. But now, we want it. We have just to call the **decorrelate.activates()** function :

.. code-block:: pycon

   >>> decorrelate.activates()
   >>> hasattr(a_function, "wrapped")
   True
   a_function.wrapped
   True

"a_function" is now wrapped by our decorator.


.. _Venusian: https://pypi.python.org/pypi/venusian/1.0
