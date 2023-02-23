# -*- coding: utf-8 -*-
# flake8: noqa

import pytest

import pyhomogenize as pyh


def test_check_existance():
    pyh._utilities.check_existance([])
    pyh._utilities.check_existance(["test.nc"])


def test_get_operator():
    pyh._utilities.get_operator(object="", name="")
    pyh._utilities.get_operator(object="", name="test")
