"""Main module."""

from . import _operators, _utilities


def pyhomogenize(args):
    """Run pyhomogenize command-line interface."""
    if args.operators:
        print(_operators.operators)
        return
    operator = args.operator[0]
    arguments = args.operator[1:]
    args.operator = operator
    args.arguments = arguments
    # check if selected operator is available
    func = _utilities.get_operator(_operators, args.operator, type="operator")
    if not func:
        return
    # check if all input files are available
    if not _utilities.check_existance(args.input_files):
        return
    # start operator
    return func.start(args)
