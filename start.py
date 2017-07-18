#!/usr/local/bin/python3
import os, sys

"""
start.py

Setup environment (check for virtual environment, installed packages, and configuration and
create them if needed), switch to the virtual environment, then start Main
"""

home = os.path.dirname(os.path.realpath(__file__))

os.chdir(home)

if os.geteuid() != 0:
    print("Run as root")
    exit()


if sys.version_info[0] < 3:
    print("Must be using Python 3")
    exit()


print("Peter's NAS Manager")

import core.constants as consts

def activateve():
    # Activate virtualenv
    activate_this = os.path.join(home, consts.VE_NAME, "bin/activate_this.py")
    exec(open(activate_this).read(), dict(__file__=activate_this))

def setup():
    # Check if we are on a first run
    # Is our virtualenv setup?

    if not os.path.isdir(consts.VE_NAME):
        if __name__ == "__main__":
            # intialize virtualenv
            from core.setup import envsetup
            envsetup(home)
        else:
            Exception("Not installed yet, run start.py by itself, without WSGI")

    activateve()

    # from core.setup import install
    # install()

    # import core.database
    # core.database.test()

def run(debug=False):
    from core import main
    if debug:
        main.start(debug=debug)
    else:
        return main.start()

app = None

if __name__ == "__main__":  # Started by script itself
    if True:
        print("full setup")
        setup()
    else:
        activateve()
    run(debug=True)
    exit()
else:                       # Started by WSGI server
    app = run()

