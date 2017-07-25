from . import *
from .command import *


def get_ip():
    import socket
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myname, myaddr
