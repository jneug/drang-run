=========
drang-run
=========

  A simple command line tool to print sequences of numbers.

``drang-run`` is comparable to  `jot`_ or `seq`_, but with a more intuitive interface. It was inspired (and named after) `a post by Dr. Drang`_.

Installation
============

Just install like any other package:

.. code-block:: console

   $ pip3 install drang-run

This will install the ``run`` command.

.. code-block:: console

   $ run --version
   run, version 0.4.1

Usage
=====

Basic usage includes up to three arguments:

::

   run [START] STOP [STEP]

``[START]`` and ``[STEP]`` are optional and default to 1.

.. code-block:: console

    $ run 4
    1
    2
    3
    4
    $ run 5 8
    5
    6
    7
    8
    $ run 0 10 3
    0
    3
    6
    9

Reverse the sequence with ``-r``:

.. code-block:: console

    $ run 4 -r
    4
    3
    2
    1

Or switch the arguments:

.. code-block:: console

   $ run 4 1 -1
   4
   3
   2
   1

.. note::
    ``run`` will try to guess the correct direction for the sequence based on the arguments. The example above could be simply written as ``run 4 1``.

    For conflicting sets of arguments, the values for START and STOP will take precedence over STEP. So ``run 1 4 -1`` will be the same as ``run 1 4 1``.

    The only exeption to this is ``STEP = 0`` which will cause an error.

    This also means that ``run`` will almost never produce an empty output because at least ``START`` will be part of the sequence.

Format the output with ``--format``. The option accepts any kind of `Python format string`_.

.. code-block:: console

    $ run 998 1002 --format "{: >4}."
     998.
     999.
    1000.
    1001.
    1002.

You can use decimals for ``[START]``, ``STOP`` and ``[STEP]``:

.. code-block:: console

    $ run 1.1 1.5 .15
    1.1
    1.25
    1.4

.. note::
    If at least one argument is a decimal, the output will be formatted as decimals as well.

    .. code-block:: console

        $ run 1.0 4 1
        1.0
        2.0
        3.0
        4.0

    You can always change this by using appropriate format strings.

    .. code-block:: console

        $ run 1.0 4 1 --format "{:g}"
        1
        2
        3
        4

Using letters for ``[START]`` and ``STOP`` will generate character sequences:

.. code-block:: console

    $ run d g
    d
    e
    f
    g

By default, the items are separated by a newline character ``\n``, but you can change this with ``-s``:

.. code-block:: console

    $ run d g -s "\t"
    d       e       f       g

Run additional sequences with ``--also START STOP STEP``:

.. code-block:: console

    $ run 1 2 --also 3 4 1
    1-3
    1-4
    2-3
    2-4

.. note::
    ``--also`` requires all three arguments to be present.

Of course, this can be used with characters and be formatted:

.. code-block:: console

    $ run 1 2 --also b c 1 --format "{0:02}. {1}_{1}"
    01. a_a
    01. b_b
    02. a_a
    02. b_b

.. note::
    The sequences can be referenced in the format string by order of appearance. ``-r`` will reverse *all* sequences.

Since version 0.4.0 you can define variables with the ``--def`` option. A variable can be set to a simple arithmetic expression that is evaluated with the current counter values. Similar to the format string (``-f``) the counters can be referenced with ``{0}``, ``{1}`` and so on. All defined variables are initialized with ``0`` and can be used in other expressions, even in the definition of themselves.

.. code-block:: console

    $ run 4 --also 1 3 1 --def sum "{0}+{1}" --def akk "{akk}+{sum}" --format "{0} + {1} = {sum} ({akk})"
    1 + 1 = 2 (2)
    1 + 2 = 3 (5)
    1 + 3 = 4 (9)
    2 + 1 = 3 (12)
    2 + 2 = 4 (16)
    2 + 3 = 5 (21)
    3 + 1 = 4 (25)
    3 + 2 = 5 (30)
    3 + 3 = 6 (36)
    4 + 1 = 5 (41)
    4 + 2 = 6 (47)
    4 + 3 = 7 (54)

The expressions allow for some additional functions to be used. Notably the
``randint(max)`` and ``rand()`` functions for genrating random numbers:

.. code-block:: console

    $ run 10 --def r "randint(100)" --format "{r}" -s ,
    51,0,55,50,56,43,20,5,51,90

.. note::
    The expressions are evaluated using the `simpleeval`_ module. Read the docs to see, what expressions are possible. In general, the basic arithmetic operators (``+``, ``-``, ``*``, ``/``, ``*``, ``//``) are supported.


Examples
========

Generating a CSV file with a lists of decimal, binary and hexadecimal numbers:

.. code-block:: console

    $ echo "dec,bin,hex" > hostnames.csv
    $ run 0 255 -f "{0:2},{0:08b},{0:02X}" >> numbers.csv


Generating a list of computers in a network with hostnames and IP.

.. code-block:: console

    $ echo "room,hostname,ip" > hostnames.csv
    $ run 4 --also 1 24 1 --also 1 16 1 -f "{0}{1:02},r{0}{1:02}-{2:02},18.45.{1}{0}.{2}" >> hostnames.csv


.. _jot: https://www.unix.com/man-page/osx/1/jot/
.. _seq: https://www.unix.com/man-page/osx/1/seq/
.. _a post by Dr. Drang: https://leancrew.com/all-this/2020/09/running-numbers/
.. _pip: http://www.pip-installer.org/
.. _Python format string: https://docs.python.org/3.6/library/string.html#formatstrings
.. _simpleeval: https://github.com/danthedeckie/simpleeval
