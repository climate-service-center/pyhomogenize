
import logging
import sys
from pyhomogenize import time_control

help="""
showmiss : Print missing timestamps. At first, merge files if needed.
    usage: pyhomogenize showmiss ifile1 [ifile2 [ifileN]]
"""

def start(args):
    file = time_control(args.input_files)
    print('Missing time steps: ', file.get_missings())
    
