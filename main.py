"""
madliar.com
-----------
    This script is used to run in IDE that you cannot add
system argument like the way run in command line.

"""
import os

if __name__ == "__main__":
    if os.name in ("nt", ):
        command = "madliar-manage.exe runserver localhost:8080"
    else:
        command = "madliar-manage runserver localhost:8080"
    os.system(command)
