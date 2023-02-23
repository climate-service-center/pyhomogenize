# -*- coding: utf-8 -*-
# flake8: noqa

import pytest
import xarray as xr

import pyhomogenize as pyh

from . import has_xarray, requires_xarray


def test_date_range_to_frequency_limits():
    basics = pyh.basics()
    start = "2005-03-02"
    end = "2005-12-25"
    smonth = [3, 6, 9, 12]
    emonth = [2, 5, 8, 11]

    frequency = "day"
    assert basics.date_range_to_frequency_limits(
        start, end, frequency=frequency, smonth=smonth, emonth=emonth
    )

    date_range = xr.cftime_range(start, end)
    assert basics.date_range_to_frequency_limits(date_range=date_range)

    frequency = "mon"
    assert basics.date_range_to_frequency_limits(
        start, end, frequency=frequency, smonth=smonth, emonth=emonth
    )

    assert basics.date_range_to_frequency_limits(
        start, end, frequency=frequency, is_month_start=True, is_month_end=True
    )

    frequency = ["MS", "M"]
    assert basics.date_range_to_frequency_limits(start, end, frequency=frequency)
