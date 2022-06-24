# -*- coding: utf-8 -*-
# flake8: noqa

import pytest

import pyhomogenize as pyh

from . import (has_dask, has_numpy, has_xarray, requires_dask, requires_numpy,
               requires_xarray)


def test_time_compare():
    netcdffile1 = pyh.test_netcdf[0]
    netcdffile2 = pyh.test_netcdf[2]
    time_control1 = pyh.time_control(netcdffile1)
    time_control2 = pyh.time_control(netcdffile2)

    assert pyh.time_compare(
        time_control1.ds, time_control2.ds
    ).select_max_intersection()
    assert pyh.time_compare(
        [time_control1.ds, time_control2.ds]
    ).select_max_intersection()
    assert pyh.time_compare(
        [time_control1.ds], time_control2.ds
    ).select_max_intersection(output="test.nc")
