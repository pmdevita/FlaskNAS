VE_NAME = "NAS-ve"
SETTINGS = "settings.json"
LOGINS = "logins.json"
packages = ["sh", "reconfigure", "flask", "argon2"]
debug = True
argon_settings = {"t": 1000, "m": 12, "p": 1}
directory_caching = 1




# STUFF NOT TO BE PUT ONLINE
rawsecretkey = "39 126  97  73 192  92 185  92 114 246 133 159 119 254  28  71 185 211  30 138  64 187  61  89"
# END OF STUFF

def secretkey():
    key = []
    for i in rawsecretkey.split():
        key.append(int(i))
    return bytes(key)
