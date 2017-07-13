import os
import json
import sys
import shutil
from subprocess import Popen
from core.constants import VE_NAME, packages
import re

def install():
    from sh import aptitude, ErrorReturnCode
    print("\nChecking installed packages...\n")

    # check if we have samba and netatalk already installed
    has_samba = package_installed("samba-common")
    has_netatalk = package_installed("netatalk")
    has_avahi = package_installed("avahi-daemon")

    # check highest version available in package manager
    response = aptitude("versions", "netatalk")
    print(str(response))
    response = re.search("Package netatalk:\ni\\s*(\\S*)", str(response))
    print(response.groups())

    print(has_samba, has_netatalk, has_avahi)
    null = input()

def package_installed(package):
    from sh import dpkg, ErrorReturnCode
    print(package)
    try:
        response = dpkg("-s", package)
        m = re.search("Version:\s(.:)?(\S*)\\n", str(response))
        return m.groups()[1].split(".")
    except ErrorReturnCode as e:
        return False


def envsetup(path="."):
    print("\nSetting up...\n")
    if os.path.isdir(os.path.join(path, VE_NAME)):
        print("Virtual environment already exists. Recreate?")
        answer = input("(y/n)")
        if answer == "y":
            shutil.rmtree(VE_NAME)
        else:
            exit()

    print("Checking for virtualenv")
    try:
        import virtualenv
    except ImportError:
        print("virtualenv is not installed. Run \nsudo " + sys.executable + " -m pip install virtualenv")
        exit()

    print("Creating virtualenv")
    result = Popen([sys.executable, "-m", "virtualenv", os.path.join(path, VE_NAME)])
    result.wait()

    print("Installing packages in virtualenv")
    result = Popen([os.path.join(path, VE_NAME, "bin/pip"), "install"] + packages)
    result.wait()

def test(path):
    print("Installing packages in virtualenv")
    result = Popen([os.path.join(path, VE_NAME, "bin/pip"), "install"] + packages)
    result.wait()

class tempinstall:
    def __init__(self, packages):
        self.packages = []
        for i in packages:
            if not package_installed(i):
                self.packages

def build_netatalk(buildfolder=None):
    if not buildfolder:
        buildfolder = "netatalkbuild"

    os.mkdir(buildfolder)
    os.chdir(buildfolder)

