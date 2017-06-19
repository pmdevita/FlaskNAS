import os, platform

VE_NAME = "NAS-ve"
# SETTINGS = "settings.json"
CONFIG = "config.json"
LOGINS = "logins.json"
SHARES = "shares.db"

#SAMBA = "/etc/samba/smb.conf"
SAMBA = "smb.conf"
SAMBA_FILETAG = "# Autoconfigured by FlaskNAS\n# If you are using FlaskNAS, DO NOT EDIT\n"
SAMBA_DEFAULT_CONFIG = {
            "[global]": {
                "netbios name": platform.uname()[1],
                "acl allow execute always": "yes",
                "map to guest": "bad user",
                "guest account": "nobody",
                "group": "share",
                "create mask": "0770",
                "force create mode": "0770",
                "directory mask": "2770",
                "force directory mode": "2770",
                "map archive": "no"
            }
        }
SAMBA_DEFAULT_SHARE = {
    "comment": "",
    "path": "",
    "browsable": "yes",
    "oplocks": "yes",
    "valid users": "",
    "read list": "",
    "write list": "",
}


packages = ["sh", "reconfigure", "flask", "argon2", "pony"]
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
