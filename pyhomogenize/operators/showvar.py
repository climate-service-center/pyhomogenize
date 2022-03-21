
import logging
import sys
from .. import classes 

help="""
showvar : Print variable names. At first, merge files if needed.
    usage: pyhomogenize showvar -i ifile1 [ifile2 [ifileN]]
"""

def start(args):
    file = classes.netcdf_basics(args.input_files)
    print(file.name)
    
