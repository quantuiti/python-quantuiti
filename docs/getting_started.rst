***************
Getting started
***************

.. _PyPI: https://pypi.org/project/quantuiti/

quantuiti is distributed on PyPI_ and can be installed with ``pip``:

.. code:: console

    $ pip install quantuiti

**Create a new python file then import quantuiti engine**


.. code:: python

    from quantuiti import Engine


**Initalize quantuiti engine**

.. code:: python

    Engine = Engine()

**Instantiate algorithm**

.. code:: python

    @Engine.algorithm
    def algo():
    if self.ema(20) > self.ema(100):
        self.buy()
    else:
        self.sell()

**example of an EMA crossover strategy**

.. code:: python

    from quantuiti import Engine
    Engine = Engine()

    @Engine.algorithm
    def algo():
    if self.ema(20) > self.ema(100):
        self.buy()
    else:
        self.sell()