# flake8: noqa

"""Top-level package for pyhomogenize."""

from . import _read_write as read_write
from ._basics import basics
from ._netcdf_basics import netcdf_basics
from ._read_write import (
    era5_combine_time_step,
    era5_to_regular_grid,
    get_var_name,
    open_xrdataset,
    save_xrdataset,
)
from ._time_compare import time_compare
from ._time_control import time_control
from .cli import create_parser
from .data import netcdf as test_netcdf
from .pyhomogenize import pyhomogenize

__author__ = """Ludwig Lierhammer"""
__email__ = "ludwig.lierhammer@hereon.de"
__version__ = "0.5.1"

_all__ = [
    "basics",
    "create_parser",
    "era5_combine_time_step",
    "era5_to_regular_grid",
    "get_var_name",
    "open_xrdataset",
    "pyhomogenize",
    "read_write",
    "save_xrdataset",
    "test_netcdf",
    "time_compare",
    "time_control",
]
