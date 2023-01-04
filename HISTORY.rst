=======
History
=======

0.1.0 (2020-11-12)
------------------

* First release on PyPI.

0.1.1 (2022-06-24)
------------------

* Fixed bug in setup.py version number

0.1.2 (2022-06-24)
------------------

* pre-commit.ci bug fixed

0.1.3 (2022-06-24)
------------------

* Read version number from __init__

0.1.4 (2022-06-24)
------------------

* Expand HISTORY.rst

0.2.0 (2022-06-30)
------------------

* Outsource useful functions for reading and writing large netCDF files.
* Use those functiosn directly from pyhomogenize.
* Calling pyhomogenize classes is not needed.

0.2.1 (2022-07-01)
------------------

* rename save_to_netcdf to save_xrdataset
* write input files to ds attributes

0.2.2 (2022-07-05)
------------------

* create chunks if not already existing

0.2.3 (2022-07-11)
------------------

* write CF variables to dataset while calling open_xrdataset

0.2.4 (2022-07-12)
------------------

* add data via pip install

0.2.5 (2023-01-04)
------------------

* precise mid of time range
* add more dependencies (cftime, netcdf4, h5netcdf)
