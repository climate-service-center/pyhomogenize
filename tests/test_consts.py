
import pytest

import pyhomogenize as pyh

def _get_keys(dictionary):
    return getattr(pyh.consts, dictionary).keys()

def _get_values(dictionary):
    return getattr(pyh.consts, dictionary).values()

def test_frequencies():
    assert _get_keys('frequencies')
    assert _get_values('frequencies')

def test_translator():
    assert _get_keys('translator')
    assert _get_values('translator')

def test_format():
    assert _get_keys('translator')
    assert _get_values('translator')

def test_equalize():
    assert _get_keys('equalize')
    assert _get_values('equalize')

def test_within():
    assert _get_keys('within')
    assert _get_values('within')

def test_naming():
    assert _get_keys('naming')
    assert _get_values('naming')
