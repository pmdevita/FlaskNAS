#!/usr/local/bin/python3
import os, sys, autovenv

"""
start.py

Setup environment (check for virtual environment, installed packages, and configuration and
create them if needed), switch to the virtual environment, then start Main
"""

# Set the current directory to Flask NAS's location
home = os.path.dirname(os.path.realpath(__file__))
os.chdir(home)

# Root Check
if os.geteuid() != 0:
    print("Run as root")
    exit()

# Py3 Check
if sys.version_info[0] < 3:
    print("Must be using Python 3")
    exit()

print("Flask NAS")

import core.constants as consts

v = autovenv.Venv("flask-nas", consts.packages)

def run(v, debug=False):
    from core import main
    if debug:
        main.start(v, debug=debug)
    else:
        return main.start(v)

application = None

if __name__ == "__main__":  # Standalone
    run(v, debug=True)
else:                       # Started by WSGI server
    application = run(v)