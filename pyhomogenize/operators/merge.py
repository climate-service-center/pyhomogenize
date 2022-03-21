
import logging
import sys
from pyhomogenize import netcdf_basics
help="""
merge : Merge given input files
    usage: pyhomogenize merge -i ifile1 [ifile2 [ifileN]] -o ofile 
"""

def start(args):
    file = netcdf_basics(args.input_files)
    if not args.output_file:
        print('No output file selecetd. Use -o <ofile>.')
        return
    file.write(output=args.output_file)

