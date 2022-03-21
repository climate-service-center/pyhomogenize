
import logging
import sys
from .. import classes 

help="""
seltimerange : Select user-given time range. At first, merge files if needed.
    usage: pyhomogenize seltimerange,<timestamp1>,<timestapm2> -i ifile1 [ifile2 [ifileN]] -o ofile
    timeformat: %y%m%d[T:%H:%M:%S]
"""

def start(args):
    file = classes.time_control(args.input_files)
    file.select_range(args.arguments, output=args.output_file)
    
