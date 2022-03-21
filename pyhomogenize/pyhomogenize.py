"""Main module."""

import logging
import os
import sys

from . import _utilities as ut
from . import operators as op

def pyhomogenize(args):
    #show all available operators
    if args.operators:
        print(op.operators)
        return
    operator  = args.operator[0]
    arguments = args.operator[1:]
    args.operator  = operator
    args.arguments = arguments
    #check if selected operator is available
    func = ut.get_operator(op, args.operator, type='operator')
    #check if all input files are available
    ut.check_existance(args.input_files)
    #start operator
    func.start(args)
