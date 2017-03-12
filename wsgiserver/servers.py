import os
import sys

from wsgiref.simple_server import make_server, demo_app


def wsgi_server(host, port):
    sys.stdout.write(str((host, port)))
    return make_server(host, port, demo_app)

