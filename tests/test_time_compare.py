
import pytest

import pyhomogenize as pyh

from . import has_dask, requires_dask
from . import has_xarray, requires_xarray
from . import has_numpy, requires_numpy

def test_time_compare():
    netcdffile1 = pyh.test_netcdf[0]
    netcdffile2 = pyh.test_netcdf[1]
    time_control1 = pyh.time_control(netcdffile1)
    time_control2 = pyh.time_control(netcdffile2)

    assert pyh.time_compare([time_control1.ds, time_control2.ds]).max_intersection()
