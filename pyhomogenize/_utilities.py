
import os
import sys
import logging

def exit(cmd):
    logging.error(cmd)
    sys.exit()

def check_existance(files):
    """
    Check if requested files are available     
    Exit if not.
    """     
    stop = False
    commands = ''
    if not files: 
        exit('No input files selected.')
    for file in files:
        if not os.path.isfile(file):
            stop = True
            commands += '{} is not available\n'.format(file)
    if stop:
        exit(commands)

def get_operator(object, name, type='attribute'):
    if not name:
        exit('No {} is selected.'.format(type))
    try:
        return getattr(object, name)
    except:
        exit('Choosen {} {} is not available.'.format(type, name)) 
