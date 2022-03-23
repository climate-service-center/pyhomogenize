
import pytest

import pyhomogenize as pyh

from . import has_dask, requires_dask
from . import has_xarray, requires_xarray
from . import has_numpy, requires_numpy
from . import has_iteration_utilities, requires_iteration_utilities

def test_cli_ops():
    parser = pyh.create_parser()
    args = parser.parse_args(['-ops'])
    pyh.pyhomogenize(args)

def test_cli_merge():
    parser = pyh.create_parser()
    args = parser.parse_args(['merge','-i',pyh.test_netcdf[0],pyh.test_netcdf[1]])
    assert pyh.pyhomogenize(args)

def test_cli_seltimerange():
    parser = pyh.create_parser()
    args = parser.parse_args(['seltimerange,20070501,20070630','-i',pyh.test_netcdf[0]])
    assert pyh.pyhomogenize(args)

def test_cli_showdups():
    parser = pyh.create_parser()
    args = parser.parse_args(['showdups','-i',pyh.test_netcdf[0]])
    pyh.pyhomogenize(args)

def test_cli_showmiss():
    parser = pyh.create_parser()
    args = parser.parse_args(['showmiss','-i',pyh.test_netcdf[0]])
    pyh.pyhomogenize(args)

def test_cli_showreds():
    parser = pyh.create_parser()
    args = parser.parse_args(['showreds','-i',pyh.test_netcdf[0]])
    pyh.pyhomogenize(args)

def test_cli_showtimestamps():
    parser = pyh.create_parser()
    args = parser.parse_args(['showtimestamps','-i',pyh.test_netcdf[0]])
    pyh.pyhomogenize(args)

def test_cli_showvar():
    parser = pyh.create_parser()
    args = parser.parse_args(['showvar','-i',pyh.test_netcdf[0]])
    pyh.pyhomogenize(args)

def test_cli_timecheck_all():
    parser = pyh.create_parser()
    args = parser.parse_args(['timecheck','-i',pyh.test_netcdf[0]])
    assert pyh.pyhomogenize(args)

def test_cli_timecheck_sel():
    parser = pyh.create_parser()
    args = parser.parse_args(['timecheck,duplicates','-i',pyh.test_netcdf[0]])
    assert pyh.pyhomogenize(args)
