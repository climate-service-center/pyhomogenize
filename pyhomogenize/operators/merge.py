import pyhomogenize as pyh

help = """
merge : Merge given input files
    usage: pyhomogenize merge -i ifile1 [ifile2 [ifileN]] -o ofile
"""


def start(args):
    file = pyh.netcdf_basics(args.input_files)
    if not args.output_file:
        print("No output file selecetd. Use -o <ofile>.")
    else:
        file.write(output=args.output_file)
    return file.ds
