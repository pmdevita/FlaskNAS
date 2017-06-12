# import subprocess
#
#
# def cmd(command, verbose = False):
#     p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
#     if verbose:
#         while True:
#             output = p.stdout.readline()
#             if output == '' and p.poll() is not None:
#                 break
#             if output:
#                 print(output.decode("utf-8"), end="")
#         rc = p.poll()
#         return rc
#     else:
#         response = p.communicate()[0].decode("utf-8")
#         return response