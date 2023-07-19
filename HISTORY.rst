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

0.2.6 (2023-01-24)
------------------

* add `decode_times` and `combine` as keyword argumnets to `open_xrdataset`
* set default value of parallel in `open_xrdataset` to False

0.2.7 (2023-02-03)
------------------

* save_xrdataset is now working if Dataset does not include `time`

0.2.8 (2023-02-13)
------------------

* convert time axis to CFTimeIndex

0.2.9 (2023-02-16)
------------------

* set proleptic_gregorian to standard calendar

0.3.0 (2023-02-22)
------------------

* calculate time_bnds and add them to dataset

0.3.1 (2023-03-16)
------------------

* get CF_variables

0.3.2 (2023-03-22)
------------------

* read and write data with length of time axis is 1
* add time bounds with length of time axis is 1
* drop coordinates from non CF variables

0.3.3 (2023-03-23)
------------------

* testing for python version 3.8, 3.9 and 3.10

0.4.0 (2023-03-23)
------------------

* published on zenodo

0.5.0 (2023-06-13)
------------------

* add time bounds if length of time axis is 1
* convert np.datetime64 object to CFTimeIndex

0.5.1 (2023-06-14
-----------------

* fixing v0.5.1

0.5.2 (2023-06-30)
------------------

* convert time axis to cftime.datetime object
* `open_xrdataset`: set decode_cf to parameters

0.5.3 (2023-07-19)
------------------

* some restructuring in _convert_time
