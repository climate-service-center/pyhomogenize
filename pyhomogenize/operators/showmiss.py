import pyhomogenize as pyh

help = """
showmiss : Print missing timestamps. At first, merge files if needed.
    usage: pyhomogenize showmiss ifile1 [ifile2 [ifileN]]
"""


def start(args):
    file = pyh.time_control(args.input_files)
    missings = file.get_missings()
    print("Missing time steps: ", missings)
    return missings
