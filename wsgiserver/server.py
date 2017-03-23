from wsgiref.simple_server import make_server
from .core import get_application


def wsgi_server(host, port):
    """Start a simple server."""
    return make_server(host, port, get_application())
