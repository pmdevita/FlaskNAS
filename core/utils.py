import sys
import os

def versioncheck():
    if sys.version_info[0] < 3:
        print("Must be using Python 3")
        exit()

def sourceforge_download(link):
    import urllib
    urllib.request.urlopen()

def validate_config(config):
    return True

def validate_path(prefix, path):
    fullpath = os.path.join(prefix, path)
    realpath = os.path.realpath(fullpath)
    if str(os.path.commonprefix([prefix, realpath])) == str(prefix):
        return True
    else:
        return False

if __name__ == "__main__":
    sourceforge_download("netatalk")
