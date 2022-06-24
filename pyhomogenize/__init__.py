# -*- coding: utf-8 -*-
# flake8: noqa

"""Top-level package for pyhomogenize."""

import pkg_resources

from . import _consts as consts
from . import _utilities as utilities
from . import operators as op
from ._basics import basics
from ._netcdf_basics import netcdf_basics
from ._time_compare import time_compare
from ._time_control import time_control
from .cli import create_parser
from .data import netcdf as test_netcdf
from .pyhomogenize import pyhomogenize

__author__ = """Ludwig Lierhammer"""
__email__ = "ludwig.lierhammer@hereon.de"
__version__ = "0.1.3"

_all__ = [
    "consts",
    "utilities",
    "op",
    "basics",
    "netcdf_basics",
    "time_compare",
    "time_control",
    "create_parser",
    "test_netcdf",
    "pyhomogenize",
]
