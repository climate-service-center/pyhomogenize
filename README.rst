====================================================
Homogenize NetCDF files to CF standard: pyhomogenize
====================================================


.. image:: https://img.shields.io/pypi/v/pyhomogenize.svg
        :target: https://gitlab.hzdr.de/gerics/infrastructure/pyhomogenize/

.. image:: https://img.shields.io/travis/ludwiglierhammer/pyhomogenize.svg
        :target: https://travis-ci.com/ludwiglierhammer/pyhomogenize


Tool to homogenize netCDF to CF standard files using xarray

See https://cfconventions.org

* Free software: MIT license


Features
--------

At the moment mainly four python classes are defined.

* netcdf_basics: This class opens one or multiple NetCDF files by calling the class.
  You can manipulate the NetCDF attributes and write it to a new file.

* time_basics: This class creates a fixed frequency CFTimeIndex from user-given start and end dates.

* time_control: This class is a time checker for NetCDF files following CF Metadata Conventions.
  It is based on pyhomogenize's netcdf_basics class. Thus it opens the NetCDF files by calling the class.

* time_match: This class compares to xr.datasets and returns the maximum temporal intersection
  Firstly you have to open the datasets with netcdf_basics or time_control

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

