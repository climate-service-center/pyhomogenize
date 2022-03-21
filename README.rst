====================================================
Homogenize NetCDF files to CF standard: pyhomogenize
====================================================

.. image:: https://github.com/ludwiglierhammer/pyhomogenize/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/ludwiglierhammer/pyhomogenize/actions/workflows/ci.yml
    
.. image:: https://codecov.io/gh/ludwiglierhammer/pyhomogenize/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ludwiglierhammer/pyhomogenize
    
.. image:: https://readthedocs.org/projects/pyhomogenize/badge/?version=latest
    :target: https://pyhomogenize.readthedocs.io/en/latest/?version=latest
    :alt: Documentation Status  
        
.. image:: https://pyup.io/repos/github/ludwiglierhammer/pyhomogenize/shield.svg
    :target: https://pyup.io/repos/github/ludwiglierhammer/pyhomogenize/
    :alt: Updates   



Tool to homogenize netCDF to CF standard files using xarray

See https://cfconventions.org

* Free software: MIT license
* Documentation: https://pyhomogenize.readthedocs.io

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
  
Instalation
-----------
You can install the package directly from github using pip:

.. code-block:: console

     pip install git+https://github.com/ludwiglierhammer/pyhomogenize

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

* pandas

* intake-esm

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

