import sys
import os

def sourceforge_download(link):
    import urllib
    urllib.request.urlopen()

def validate_path(prefix, path):
    fullpath = os.path.join(prefix, path)
    realpath = os.path.realpath(fullpath)
    if str(os.path.commonprefix([prefix, realpath])) == str(prefix):
        return True
    else:
        return False

if __name__ == "__main__":
    sourceforge_download("netatalk")
