
import pytest

import pyhomogenize as pyh

def test_check_existance():
    pyh.utilities.check_existance([])
    pyh.utilities.check_existance(pyh.test_netcdf)
    pyh.utilities.check_existance(['test_netcdf'])
    pyh.utilities.check_existance(pyh.test_netcdf + ['test_netcdf'])

def test_get_operator_none():
    pyh.utilities.get_operator(pyh.op, '', type='operator')

def test_get_operator_false():
    assert pyh.utilities.get_operator(pyh.op, 'test', type='operator')

def test_get_operator_merge():
    assert pyh.utilities.get_operator(pyh.op, 'merge', type='operator')

def test_get_operator_showvar():
    assert pyh.utilities.get_operator(pyh.op, 'showvar', type='operator')

def test_get_operator_seltimerange():
    assert pyh.utilities.get_operator(pyh.op, 'seltimerange', type='operator')

def test_get_operator_showtimestamps():
    assert pyh.utilities.get_operator(pyh.op, 'showtimestamps', type='operator')

def test_get_operator_showdups():
    assert pyh.utilities.get_operator(pyh.op, 'showdups', type='operator')

def test_get_operator_showmiss():
    assert pyh.utilities.get_operator(pyh.op, 'showmiss', type='operator')

def test_get_operator_showreds():
    assert pyh.utilities.get_operator(pyh.op, 'showreds', type='operator')

def test_get_operator_timecheck():
    assert pyh.utilities.get_operator(pyh.op, 'timecheck', type='operator')
