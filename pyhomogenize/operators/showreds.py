
import logging
import sys
from .. import classes 

help="""
showreds : Print redundant timestamps. At first, merge files if needed.
    usage: netcdf_time_control showreds ifile1 [ifile2 [ifileN]]
"""

def start(args):
    file = classes.time_control(args.input_files)
    print(file.get_redundants())
    
