import pyhomogenize as pyh

help = """
seltimerange : Select user-given time range. At first, merge files if needed.
    usage: pyhomogenize seltimerange,<timestamp1>,<timestapm2>
           -i ifile1 [ifile2 [ifileN]] -o ofile
    timeformat: %y%m%d[T:%H:%M:%S]
"""


def start(args):
    file = pyh.time_control(args.input_files)
    if not args.output_file:
        print("No output file selecetd. Use -o <ofile>.")
    file.select_time_range(args.arguments, output=args.output_file)
    return file.ds
