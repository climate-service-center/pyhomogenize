import os


def check_existance(files):
    """Check if requested files are available."""
    stop = False
    commands = ""
    if not files:
        print("No input files selected.")
        return
    for file in files:
        if not os.path.isfile(file):
            stop = True
            commands += f"{file} is not available\n"
    if stop:
        print(commands)
        return
    return True


def get_operator(object, name, type="attribute"):
    """Get operator."""
    if not name:
        print(f"No {type} is selected.")
        return
    try:
        return getattr(object, name)
    except Exception:
        print(f"Choosen {type} {name} is not available.")
        return
