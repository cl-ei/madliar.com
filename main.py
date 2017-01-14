import os
import sys

from wsgiserver.core import Core

"""
Run this script to start a tiny web server
based on wsgi communicating protocol.

"""

config = {
    "host": "localhost",
    "port": 80,
}

if __name__ == '__main__':
    server = Core(**config)
    server.start_server()
