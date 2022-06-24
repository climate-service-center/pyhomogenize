"""Main module."""

from . import _utilities as ut
from . import operators as op


def pyhomogenize(args):
    # show all available operators
    if args.operators:
        print(op.operators)
        return
    operator = args.operator[0]
    arguments = args.operator[1:]
    args.operator = operator
    args.arguments = arguments
    # check if selected operator is available
    func = ut.get_operator(op, args.operator, type="operator")
    if not func:
        return
    # check if all input files are available
    if not ut.check_existance(args.input_files):
        return
    # start operator
    return func.start(args)
