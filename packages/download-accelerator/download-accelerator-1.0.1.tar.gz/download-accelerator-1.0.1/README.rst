========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-download-accelerator/badge/?style=flat
    :target: https://readthedocs.org/projects/python-download-accelerator
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/AriaBagheri/python-download-accelerator.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/AriaBagheri/python-download-accelerator

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/AriaBagheri/python-download-accelerator?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/AriaBagheri/python-download-accelerator

.. |requires| image:: https://requires.io/github/AriaBagheri/python-download-accelerator/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/AriaBagheri/python-download-accelerator/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/AriaBagheri/python-download-accelerator/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/AriaBagheri/python-download-accelerator

.. |codecov| image:: https://codecov.io/gh/AriaBagheri/python-download-accelerator/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/AriaBagheri/python-download-accelerator

.. |version| image:: https://img.shields.io/pypi/v/download-accelerator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/download-accelerator

.. |wheel| image:: https://img.shields.io/pypi/wheel/download-accelerator.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/download-accelerator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/download-accelerator.svg
    :alt: Supported versions
    :target: https://pypi.org/project/download-accelerator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/download-accelerator.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/download-accelerator
:: |version| v1.0.1


.. end-badges

A python accelerator based on python

* Free software: MIT license

Installation
============

::

    pip install download-accelerator

You can also install the in-development version with::

    pip install https://github.com/AriaBagheri/python-download-accelerator/archive/master.zip


Documentation
=============


https://python-download-accelerator.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
