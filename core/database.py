import os
from pony.orm import *
import core.constants as consts
from core.login import Login
from core.service_configuration import Samba, ConfigDict

READWRITE = "readwrite"
READ = "read"

db = Database()


class User(db.Entity):
    username = PrimaryKey(str)
    salt = Required(bytes)
    password = Required(bytes)
    op = Required(bool)
    #read = Set('Share', reverse='read')
    #readwrite = Set('Share', reverse='readwrite')


    def op_user(self, current_user, op):
        pass


# class Share(db.Entity):
#     name = PrimaryKey(str)
#     read = Set(User, reverse='read')
#     readwrite = Set(User, reverse='readwrite')
#
#     def rename(self, current_user, op):
#         pass
#
#     def update_user(self, current_user, user, mode):
#         pass

db.bind("sqlite", os.path.join("../", consts.SHARES), create_db=True)

db.generate_mapping(create_tables=True)

# sql_debug(True)


class Users:
    def __init__(self):
        self._password = Login(db=True)
        with db_session:
            users = select(u for u in User)[:]

        # Are we doing first time setup?
        if not users:
            self.no_users = True
        else:
            self.no_users = False

    def login(self, username, password):
        with db_session:
            user = select(u for u in User if u.username == username)[:]
        if len(user) == 1:
            if self._password.to_hash(password, user[0].salt)[0] == user[0].password:
                return True
            else:
                return False
        else:
            return False

    def create_user(self, current_user, new_user, password):
        if _user_op(current_user):
            phash, salt = self._password.to_hash(password)
            with db_session:
                User(username=new_user, salt=salt, password=phash, op=False)

    def create_first_user(self, new_user, password):
        if not self.no_users:
            raise Exception("There are users, no need to make a first account")
        phash, salt = self._password.to_hash(password)
        with db_session:
            User(username=new_user, salt=salt, password=phash, op=True)

    def get(self, current_user):
        if _user_op(current_user):
            with db_session:
                users = select(u for u in User)[:]
            return users


class Shares:
    def __init__(self):
        self.path = consts.SAMBA
        # Determine if config needs to moved
        try:
            with open(self.path) as f:
                tag = f.readline()
                tag = tag + f.readline()
            if tag != consts.SAMBA_FILETAG: # Config is not ours
                os.rename(self.path, self.path + ".old")
                self._new_config()
        except FileNotFoundError:   # Config doesn't exist
            self._new_config()
        self._samba = Samba(self.path)
        self.global_config = self._samba.config["[global]"]

    def _new_config(self):
        with open(self.path, "w") as f:
            f.write(consts.SAMBA_FILETAG)
        s = Samba(self.path)
        s.config.update(consts.SAMBA_DEFAULT_CONFIG)
        s.save()

    def create_share(self, name):
        pass



# class Shares:
#     def __init__(self):
#         pass
#
#     def create_share(self, current_user, new_share):
#         pass
#
#     def get(self, current_user):
#         if _user_op(current_user):
#             with db_session:
#                 shares = select(s for s in Share)[:]
#             return shares


def _user_op(user):
    with db_session:
        user = select(u for u in User if u.username == user)[:]
    if user:
        return user[0].op
    return False



