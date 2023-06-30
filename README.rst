====================================================
Homogenize NetCDF files to CF standard: pyhomogenize
====================================================

+----------------------------+-----------------------------------------------------+
| Versions                   | |pypi|                                              |
+----------------------------+-----------------------------------------------------+
| Documentation and Support  | |docs| |versions|                                   |
+----------------------------+-----------------------------------------------------+
| Open Source                | |license| |zenodo|                                  |
+----------------------------+-----------------------------------------------------+
| Coding Standards           | |black| |pre-commit|                                |
+----------------------------+-----------------------------------------------------+
| Development Status         | |status| |build| |coveralls|                        |
+----------------------------+-----------------------------------------------------+

Tool to homogenize netCDF to CF standard files using xarray

See https://cfconventions.org

Documentation
-------------
The official documentation is at https://pyhomogenize.readthedocs.io/

Features
--------

* some useful functions to read and write large netCDF files

* basics: This class creates a fixed frequency CFTimeIndex from user-given start and end dates.
  You can manipulate the CFTimeIndex and crop it to user-specific conditions.

* netcdf_basics: This class opens one or multiple netCDF files by calling the class.
  You can manipulate the netCDF attributes and write it to a new file.

* time_control: This class is a time checker for NetCDF files following CF Metadata Conventions.
  It is based on pyhomogenize's netcdf_basics class. Thus it opens the netCDF files by calling the class.

* time_compare: This class compares the time axes of list entires of multiple xr.datasets, netCDF files and/or time_control objects.


Installation
------------
You can install the package directly with pip:

.. code-block:: console

     pip install pyhomogenize

If you want to contribute, I recommend cloning the repository and installing the package in development mode, e.g.

.. code-block:: console

    git clone https://github.com/ludwiglierhammer/pyhomogenize.git
    cd pyhomogenize
    pip install -e .

This will install the package but you can still edit it and you don't need the package in your :code:`PYTHONPATH`

Requirements
------------

* python3.6 or higher

* cftime

* dask

* iteration_utilities

* xarray

Contact
-------
In cases of any problems, needs or wishes do not hesitate to contact:

ludwig.lierhammer@hereon.de

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

.. |pypi| image:: https://img.shields.io/pypi/v/pyhomogenize.svg
        :target: https://pypi.python.org/pypi/pyhomogenize
        :alt: Python Package Index Build

.. |docs| image:: https://readthedocs.org/projects/pyhomogenize/badge/?version=latest
        :target: https://pyhomogenize.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. |versions| image:: https://img.shields.io/pypi/pyversions/pyhomogenize.svg
        :target: https://pypi.python.org/pypi/pyhomogenize
        :alt: Supported Python Versions

.. |license| image:: https://img.shields.io/github/license/ludwiglierhammer/pyhomogenize.svg
        :target: https://github.com/ludwiglierhammer/pyhomogenize/blob/master/LICENSE
        :alt: License

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black
        :alt: Python Black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ludwiglierhammer/pyhomogenize/main.svg
   :target: https://results.pre-commit.ci/latest/github/ludwiglierhammer/pyhomogenize/main
   :alt: pre-commit.ci status

.. |status| image:: https://www.repostatus.org/badges/latest/active.svg
        :target: https://www.repostatus.org/#active
        :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.

.. |build| image:: https://github.com/ludwiglierhammer/pyhomogenize/actions/workflows/ci.yml/badge.svg
        :target: https://github.com/ludwiglierhammer/pyhomogenize/actions/workflows/ci.yml
        :alt: Build Status

.. |coveralls| image:: https://codecov.io/gh/ludwiglierhammer/pyhomogenize/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/ludwiglierhammer/pyhomogenize
        :alt: Coveralls

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.8099097.svg
        :target: https://doi.org/10.5281/zenodo.8099097
        :alt: DOI
