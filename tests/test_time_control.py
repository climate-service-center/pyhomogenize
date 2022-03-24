
import pytest

import pyhomogenize as pyh

from . import has_dask, requires_dask
from . import has_xarray, requires_xarray
from . import has_numpy, requires_numpy
from . import has_iteration_utilities, requires_iteration_utilities

netcdffile   = pyh.test_netcdf
time_control = pyh.time_control(netcdffile)

def test_get_duplicates():
    time_control.get_duplicates()

def test_get_missings():
    time_control.get_missings()

def test_get_redundants():
    time_control.get_redundants()

def test_check_timestamps():
    assert time_control.check_timestamps(output='test.nc')
    assert time_control.check_timestamps(selection='duplicates')
    assert time_control.check_timestamps(selection=['duplicates','missings'])
    
def test_select_range():
    assert time_control.select_range(['2007-06-01','2008-06-30'],
                                     output='test.nc')

def test_within_time_range():
    time_control.within_time_range(['2007-06-01', '2008-06-30'])
    time_control.within_time_range(['2006-06-01', '2008-06-30'])
