import pyhomogenize as pyh

help = """
showtimestamps : Show available timestamps. At first, merge files if needed.
    usage: pyhomogenize showtimestamps -i ifile1 [ifile2 [ifileN]]
"""


def start(args):
    file = pyh.time_control(args.input_files)
    time = file.time
    print(time)
    return time
