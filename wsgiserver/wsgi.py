"""
The public interface to WSGI support. It returns a WSGI callable.

"""

from .core import get_application


application = get_application()

