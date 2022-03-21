
import logging
from pyhomogenize import time_control

help="""
showtimerange : Show available timestamps. At first, merge files if needed.
    usage: pyhomogenize showtimerange -i ifile1 [ifile2 [ifileN]]
"""

def start(args):
    file = time_control(args.input_files)
    print(file.time)
