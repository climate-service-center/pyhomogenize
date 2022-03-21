"""Main module."""

import logging
import os
import sys

from . import utilities
from . import operators

def pyhomogenize(args):
    #show all available operators
    if args.operators:
        print(operators.operators)
        return
    #split operator and arguments
    opargs         = args.operator[0].split(',')
    args.operator  = opargs[0]
    args.arguments = opargs[1:]
    #check if selected operator is available
    func = utilities.get_operator(operators, args.operator, type='operator')
    #check if all input files are available
    utilities.check_existance(args.input_files)
    #start operator
    func.start(args)
