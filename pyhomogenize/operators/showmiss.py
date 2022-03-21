
import logging
import sys
from .. import classes 

help="""
showmiss : Print missing timestamps. At first, merge files if needed.
    usage: pyhomogenize showmiss ifile1 [ifile2 [ifileN]]
"""

def start(args):
    file = classes.time_control(args.input_files)
    print(file.get_missings())
    
