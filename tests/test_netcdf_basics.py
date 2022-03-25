
import pytest

import pyhomogenize as pyh

from . import has_dask, requires_dask
from . import has_xarray, requires_xarray
from . import has_numpy, requires_numpy
from . import has_iteration_utilities, requires_iteration_utilities


def test_netcdf_basics():
    netcdffile=pyh.test_netcdf
    netcdfbasics = pyh.netcdf_basics(netcdffile)
    assert netcdfbasics.files
    assert netcdfbasics.ds
    assert netcdfbasics.name
    assert netcdfbasics.write(output='test.nc')


def test_netcdf_basics_fmt():
    netcdffile=pyh.test_netcdf
    netcdfbasics = pyh.netcdf_basics(netcdffile, fmt='%Y%m%d')
    assert netcdfbasics.fmt

