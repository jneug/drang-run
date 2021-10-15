=========
drang-run
=========

  A simple command line tool to create sequences of numbers.

``drang-run`` is comparable to  ``jot`` or ``seq``, but with a more intuitive
interface. It was inspired (and named after) `a post by Dr. Drang
<https://leancrew.com/all-this/2020/09/running-numbers/>`_.

Installation
============

Just install like any other package:

.. code-block:: fish

   pip3 install drang-run

This will install the ``run`` command.

.. code-block:: fish

   run --version

Usage
=====

Basic usage includes up to three arguments:

.. code-block:: fish

   run [START] STOP [STEP]

``START`` and ``STEP`` are optional and have 1 as default.

.. code-block:: fish

   $>run 4
   1
   2
   3
   4
   $>run 5 8
   5
   6
   7
   8
   $>run 0 10 3
   0
   3
   6
   9

Reverse the sequence with ``-r``:

.. code-block:: fish

   $>run 4 -r
   4
   3
   2
   1

Format the output with ``--format``. The option accepts any kind of Python format
string.

.. code-block:: fish

   $>run 998 1002 --format "{: >4}."
    998.
    999.
   1000.
   1001.
   1002.

You can use decimals for ``START``, ``STOP`` and ``STEP``:

.. code-block:: fish

   $>run 1.1 1.5 .15
   1.1
   1.25
   1.4

.. note::

   If at least one argument is a decimal, the output will be formatted as
	 decimals as well.

   .. code-block:: fish

	    $>run 1.0 4 1
			1.0
			2.0
			3.0
			4.0

   You can always change this by using appropriate format strings.

   .. code-block:: fish

	    $>run 1.0 4 1 --format "{:g}"
			1
			2
			3
			4

   And if needed, you can simply add trailing zeros to integers.

   .. code-block:: fish

      $>run 1.0 4 1 --format "{}.0"
			1
			2
			3
			4

Using letters will generate character sequences:

.. code-block:: fish

   $>run d g
   d
   e
   f
   g

By default, the sequence is separated by a newline character ``\n``, but you can change
this with ``-s``:

.. code-block:: fish

   $>run d g -s "\t"
   d       e       f       g

Run additional sequences with ``--also START STOP STEP``:

.. code-block:: fish

   $>run 1 2 -- also 3 4 1
   1-3
   1-4
   2-3
   2-4

Of course, this can be used with characters and be formatted:

.. code-block:: fish

   $>run 1 2 -- also b c 1 --format "{0:02}. {1}_{1}"
   01. a_a
   01. b_b
   02. a_a
   02. b_b

.. Note::

   The sequences can be referenced by order of appearance in the format string. ``-r``
	 will reverse *all* sequences.
