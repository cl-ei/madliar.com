import os
import sys

from wsgiref.simple_server import make_server, demo_app
from .core import get_application


def wsgi_server(host, port):
    sys.stdout.write(str((host, port)))
    return make_server(host, port, get_application())

