import json
import argon2
import os
from core.constants import LOGINS, argon_settings


class UserAlreadyExists(Exception):
    pass


class IncorrectCredentials(Exception):
    pass

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
    def __init__(self):
        try:
            with open(LOGINS) as f:
                self._logins = json.load(f)
        except FileNotFoundError:
            self._logins = {}

    def create(self, username, password):
        if username in self._logins:
            raise UserAlreadyExists()

        salt = os.urandom(20)
        phash = self._hash(password, salt)

        self._logins[username] = [_byteencode(salt), _byteencode(phash)]

        self._save()

    def _save(self):
        with open(LOGINS, "w") as f:
            json.dump(self._logins, f)

    def get(self, username, password):

        if username not in self._logins:
            salt = os.urandom(20)
            self._hash(password, salt)
            raise IncorrectCredentials()

        salt = _bytedecode(self._logins[username][0])
        phash = self._hash(password, salt)

        if phash == _bytedecode(self._logins[username][1]):
            return True
        else:
            raise IncorrectCredentials()

    def _hash(self, string, salt):
        """
        Hashes string with salt, argon2, and params from constants
        :param string: Thing to hash
        :param salt: Salt to hash it with
        :return: bytearray
        """
        return argon2.argon2_hash(password=string, salt=salt, t=argon_settings["t"],
                         m=argon_settings["m"], p=argon_settings["p"])