# -*- coding: utf-8 -*-
# flake8: noqa

import pytest

import pyhomogenize as pyh


def test_check_existance():
    assert pyh._utilities.check_existance([])
    assert pyh._utilities.check_existance(["test.nc"])


def test_get_operator():
    assert pyh._utilities.get_operator(object="", name="")
    assert pyh._utilities.get_operator(name="test")
