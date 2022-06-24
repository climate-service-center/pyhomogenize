import os


def check_existance(files):
    """
    Check if requested files are available
    Exit if not.
    """
    stop = False
    commands = ""
    if not files:
        print("No input files selected.")
        return
    for file in files:
        if not os.path.isfile(file):
            stop = True
            commands += "{} is not available\n".format(file)
    if stop:
        print(commands)
        return
    return True


def get_operator(object, name, type="attribute"):
    if not name:
        print("No {} is selected.".format(type))
        return
    try:
        return getattr(object, name)
    except Exception:
        print("Choosen {} {} is not available.".format(type, name))
        return
