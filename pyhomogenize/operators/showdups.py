import pyhomogenize as pyh

help = """
showdups : Print duplicated timestamps. At first, merge files if needed.
    usage: pyhomogenize showdups -i ifile1 [ifile2 [ifileN]]
"""


def start(args):
    file = pyh.time_control(args.input_files)
    duplicates = file.get_duplicates()
    print("Duplicated time steps: ", duplicates)
    return duplicates
