tdms2axg
========

*A simple script for converting National Instruments TDMS files to AxoGraph
files*

|PyPI badge| |GitHub badge|

Installation
------------

Install the latest version using ``pip``::

    pip install -U tdms2axg

Command Line Interface
----------------------

Installing the package adds the ``tdms2axg`` command, accessible from the
command line::

    usage: tdms2axg [-h] [-f] [-q] file

    A simple script for converting National Instruments TDMS files to AxoGraph
    files. The AxoGraph (AXGX) file is saved with the same name and in the same
    directory as the TDMS file. By default, an existing AxoGraph file will not be
    overwritten; use --force to overwrite.

    positional arguments:
      file         the path to a TDMS file

    optional arguments:
      -h, --help   show this help message and exit
      -f, --force  overwrite the output file if it already exists
      -q, --quiet  run silently

Python Interface
----------------

The main functionality of the package can also be accessed programmatically:

.. code-block:: python

    from tdms2axg import tdms2axg
    tdms2axg('my_data.tdms')


.. |PyPI badge| image:: https://img.shields.io/pypi/v/tdms2axg.svg?logo=python&logoColor=white
    :target: PyPI_
    :alt: PyPI project

.. |GitHub badge| image:: https://img.shields.io/badge/github-source_code-blue.svg?logo=github&logoColor=white
    :target: GitHub_
    :alt: GitHub source code

.. _GitHub: https://github.com/jpgill86/tdms2axg
.. _PyPI:   https://pypi.org/project/tdms2axg
