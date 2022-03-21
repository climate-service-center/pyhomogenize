
import logging
import sys
from pyhomogenize import time_control

help="""
showdups : Print duplicated timestamps. At first, merge files if needed.
    usage: pyhomogenize showdups -i ifile1 [ifile2 [ifileN]]
"""

def start(args):
    file = time_control(args.input_files)
    print('Duplicated time steps: ',file.get_duplicates())
    
