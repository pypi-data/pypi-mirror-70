=====
Usage
=====

BioFaker can be used both from the command line and as a python module.

Command Line
============

Create a fake DNA sequence of 40 nucleotides with the standard alphabet:

.. code-block:: console

    $ biofaker dna --length 40 --alphabet unambiguous

Comprehensive help about the BioFaker CLI can be found with ``biofaker --help``

Python Module
=============

Create a ``BioFaker`` instance:

.. code-block:: python

    from biofaker.biofaker import BioFaker

    faker = BioFaker()

Create a fake DNA sequence of 40 nucleotides with the standard alphabet:

.. code-block:: python

    faker.dna(length=40, alphabet="unambiguous")
