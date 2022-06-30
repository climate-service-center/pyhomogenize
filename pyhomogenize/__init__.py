# -*- coding: utf-8 -*-
# flake8: noqa

"""Top-level package for pyhomogenize."""

from ._basics import basics
from ._netcdf_basics import netcdf_basics
from ._read_write import get_var_name, open_xrdataset, save_to_netcdf
from ._time_compare import time_compare
from ._time_control import time_control
from .data import netcdf as test_netcdf
from .pyhomogenize import pyhomogenize

__author__ = """Ludwig Lierhammer"""
__email__ = "ludwig.lierhammer@hereon.de"
__version__ = "0.1.4"

_all__ = [
    "basics",
    "netcdf_basics",
    "time_compare",
    "time_control",
    "test_netcdf",
    "pyhomogenize",
    "open_xrdataset",
    "get_var_name",
    "save_to_netcdf",
]
