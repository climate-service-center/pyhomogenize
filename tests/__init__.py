"""Unit test package for pyhomogenize.
Test if all necessary modules are available"""

import importlib

import pytest


def _importskip(modname):
    try:
        importlib.import_module(modname)
        has = True
    except ImportError:
        has = False
    func = pytest.mark.skipif(not has, reason=f"requires {modname}")
    return has, func


has_dask, requires_dask = _importskip("dask")
has_xarray, requires_xarray = _importskip("xarray")
has_numpy, requires_numpy = _importskip("numpy")
has_iteration_utilities, requires_iteration_utilities = _importskip(
    "iteration_utilities"
)
