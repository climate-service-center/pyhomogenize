
import logging
import sys
from pyhomogenize import time_control

help="""
showreds : Print redundant timestamps. At first, merge files if needed.
    usage: netcdf_time_control showreds ifile1 [ifile2 [ifileN]]
"""

def start(args):
    file = time_control(args.input_files)
    print('Redundant time steps: ', file.get_redundants())
    
