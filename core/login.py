import argon2
import os
from core.constants import argon_settings

def to_hash(password, salt=None):
    if not salt:
        salt = os.urandom(20)

    phash = argon2.argon2_hash(password=password, salt=salt, t=argon_settings["t"],
                     m=argon_settings["m"], p=argon_settings["p"])

    return [phash, salt]