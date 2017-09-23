from subprocess import Popen, PIPE

class Samba:
    # Create/Edit user password
    def change_password(self, user, password):
        p = Popen(["sudo", "smbpasswd", "-a", user], stdin=PIPE)
        p.communicate("{}\n{}\n".format(password, password))

    def remove_user(self, user):
        p = Popen(["sudo", "smbpasswd", "-x", user])
        p.wait()
    def reload_service(self):
        p = Popen(["sudo", "service", "samba", "reload"])
        p.wait()
