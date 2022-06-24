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

netcdffile = [pyh.test_netcdf[1], pyh.test_netcdf[3]]
time_control = pyh.time_control(netcdffile)


def test_get_duplicates():
    time_control.get_duplicates()


def test_get_missings():
    time_control.get_missings()


def test_get_redundants():
    time_control.get_redundants()


def test_check_timestamps():
    assert time_control.check_timestamps(output="test.nc")
    assert time_control.check_timestamps(selection="duplicates")
    assert time_control.check_timestamps(selection=["duplicates", "missings"])


def test_select_time_range():
    assert time_control.select_time_range(
        ["2007-06-01", "2008-06-30"], output="test.nc"
    )


def test_within_time_range():
    time_control.within_time_range(["2007-06-01", "2008-06-30"])
    time_control.within_time_range(["2006-06-01", "2008-06-30"])
    time_control.within_time_range(["20070601", "20080630"], fmt="%Y%m%d")


def test_select_limited_time_range():
    time_control.select_limited_time_range(
        output="test.nc", smonth=[3, 6, 9, 12], emonth=[2, 5, 8, 11]
    )
