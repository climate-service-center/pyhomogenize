
import logging
from pyhomogenize import time_control

help="""
timecheck : By default, delete duplicated and redundant time stamps from input files and write duplicated, redundant and missing timestamps to netcdf variable attributes. THe selection is changeable.
    usage: pyhomogenize timecheck[,duplicates,redundants,missings] -i ifile1 [ifile2 [ifileN]] -o ofile
"""

def start(args):
    file = time_control(args.input_files)
    if args.arguments:
        file.check_timestamps(selection=args.arguments, output=args.output_file)
    else:
        file.check_timestamps(output=args.output_file)
    if not args.output_file: 
        print('Duplicated time steps: ', file.duplicated_timesteps)
        print('Redundant time steps: ', file.redundant_timesteps)
        print('Missing time steps: ', file.missing_timesteps)
