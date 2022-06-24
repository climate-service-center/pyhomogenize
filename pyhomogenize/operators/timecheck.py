import pyhomogenize as pyh

help = """
timecheck : By default, delete duplicated and redundant time stamps
from input files and write duplicated, redundant and missing timestamps
to netcdf variable attributes. The selection is changeable.
    usage: pyhomogenize timecheck[,duplicates,redundants,missings]
                        -i ifile1 [ifile2 [ifileN]] -o ofile
"""


def start(args):
    file = pyh.time_control(args.input_files)
    if not args.output_file:
        print("No output file selecetd. Use -o <ofile>.")
    if args.arguments:
        file.check_timestamps(
            selection=args.arguments,
            output=args.output_file,
        )
    else:
        file.check_timestamps(output=args.output_file)
    if not args.output_file:
        if hasattr(file, "duplicated_timesteps"):
            print("Duplicated time steps: ", file.duplicated_timesteps)
        if hasattr(file, "redundant_timesteps"):
            print("Redundant time steps: ", file.redundant_timesteps)
        if hasattr(file, "missing_timesteps"):
            print("Missing time steps: ", file.missing_timesteps)
    return file.ds
