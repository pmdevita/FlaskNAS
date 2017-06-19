import json
import argon2
import os
from core.constants import LOGINS, argon_settings

def _byteencode(arr):
    """
    Encodes bytes to string
    :param arr: bytes
    :return: str
    """
    string = ""
    for i in list(arr):
        string = string + chr(i)
    return string


def _bytedecode(string):
    """
    Decodes string to bytes
    :param arr: str
    :return: byteas
    """
    arr = []
    for i in string:
        arr.append(ord(i))
    return bytes(arr)

class Login:
    def __init__(self, db=False):
        if not db:
            try:
                with open(LOGINS) as f:
                    self._logins = json.load(f)
            except FileNotFoundError:
                self._logins = {}

    def _hash(self, string, salt):
        """
        Hashes string with salt, argon2, and params from constants
        :param string: Thing to hash
        :param salt: Salt to hash it with
        :return: bytearray
        """
        return argon2.argon2_hash(password=string, salt=salt, t=argon_settings["t"],
                         m=argon_settings["m"], p=argon_settings["p"])

    def to_hash(self, password, salt=None):
        if not salt:
            salt = os.urandom(20)

        phash = self._hash(password, salt)

        return [phash, salt]
