.. pygalgen documentation master file, created by
   sphinx-quickstart on Thu May  5 19:06:13 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :hidden:

   modules
   developerGuide
   userGuide
   trtools.tutorial




[NOW OBSOLETE] PyGalGen
========

!!! IMPORTANT NOTICE !!!
--------

PyGalGen has been integrated into `Planemo <https://github.com/galaxyproject/planemo/releases/tag/0.75.11>`_
This tool will not receive further updates. Please use planemo instead.

Usage documentation: https://planemo.readthedocs.io/en/latest/writing_standalone.html?highlight=argparse#creating-galaxy-tools-from-python-scripts-using-argparse

Description
--------

PyGalGen is generator for Galaxy tool definition files. It supports custom plugins, and tool
developers are encouraged to create their own plugins for their specific needs.
This page provides user and developer guides, along with documentation.

Features
--------

- Generate large parts of the wrapper file from the source code itself
- Platform independent, doesn't require installation of the wrapped tool
- Built in support for wrapper macros

Installation
------------

Install PyGalGen by running:

    pip install pygalgen

Contribute
----------

- Issue Tracker: https://github.com/Kulivox/PyGalGen/issues
- Source Code: https://github.com/Kulivox/PyGalGen

Support
-------

If you are having issues, please let me know through github issues.

License
-------

The project is licensed under the MIT license.
