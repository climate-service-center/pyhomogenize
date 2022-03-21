
import logging
import sys
from .. import classes 

help="""
showdups : Print duplicated timestamps. At first, merge files if needed.
    usage: pyhomogenize showdups -i ifile1 [ifile2 [ifileN]]
"""

def start(args):
    file = classes.time_control(args.input_files)
    print(file.get_duplicates())
    
