import pyhomogenize as pyh

help = """
showvar : Print variable names. At first, merge files if needed.
    usage: pyhomogenize showvar -i ifile1 [ifile2 [ifileN]]
"""


def start(args):
    file = pyh.netcdf_basics(args.input_files)
    name = file.name
    print(name)
    return name
