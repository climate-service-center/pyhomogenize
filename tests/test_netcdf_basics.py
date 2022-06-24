# -*- coding: utf-8 -*-
# flake8: noqa

import pytest

import pyhomogenize as pyh

from . import (has_dask, has_iteration_utilities, has_numpy, has_xarray,
               requires_dask, requires_iteration_utilities, requires_numpy,
               requires_xarray)

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
