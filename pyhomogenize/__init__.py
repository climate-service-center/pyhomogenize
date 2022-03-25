"""Top-level package for pyhomogenize."""

from . import _consts as consts
from . import _utilities as utilities
from .data import netcdf as test_netcdf
from . import operators as op
from .cli import create_parser

from ._basics import basics
from ._netcdf_basics import netcdf_basics
from ._time_control import time_control
from ._time_compare import time_compare

from .pyhomogenize import pyhomogenize

__author__ = """Ludwig Lierhammer"""
__email__ = 'ludwig.lierhammer@hzg.de'
__version__ = '0.1.0'
