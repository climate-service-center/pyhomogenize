# -*- coding: utf-8 -*-
# flake8: noqa

import pytest

import pyhomogenize as pyh

from . import has_dask  # noqa
from . import has_iteration_utilities  # noqa
from . import has_numpy  # noqa
from . import has_xarray  # noqa
from . import requires_dask  # noqa
from . import requires_iteration_utilities  # noqa
from . import requires_numpy  # noqa
from . import requires_xarray  # noqa

netcdffile = pyh.test_netcdf[0]


def test_netcdf_basics():
    netcdfbasics = pyh.netcdf_basics(netcdffile)
    assert netcdfbasics.files
    assert netcdfbasics.ds
    assert netcdfbasics.name
    assert netcdfbasics.write(output="test.nc")


def test_netcdf_basics_fmt():
    netcdfbasics = pyh.netcdf_basics(netcdffile, fmt="%Y%m%d")
    assert netcdfbasics.fmt
