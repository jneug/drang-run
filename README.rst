=========
drang-run
=========

  A simple command line tool to create sequences of numbers.

``drang-run`` is comparable to  ``jot`` or ``seq``, but with a more intuitive interface. It was inspired (and named after) `a post by Dr. Drang <https://leancrew.com/all-this/2020/09/running-numbers/>`_.

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

