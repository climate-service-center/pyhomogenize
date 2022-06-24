import pyhomogenize as pyh

help = """
showreds : Print redundant timestamps. At first, merge files if needed.
    usage: netcdf_time_control showreds ifile1 [ifile2 [ifileN]]
"""


def start(args):
    file = pyh.time_control(args.input_files)
    redundants = file.get_redundants()
    print("Redundant time steps: ", redundants)
    return redundants
