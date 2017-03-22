import json

from cgi import escape
from urlparse import parse_qs


class RequestPOST(object):
    def __init__(self, environ):
        self._content_type = environ["CONTENT_TYPE"]
        self._content = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))

    def __parse_form_data(self):
        # TODO: parse true data.
        return {"raw": self._content}

    def get(self, *args):
        if "text" in self._content_type or "json" in self._content_type:
            return escape(parse_qs(self._content).get(*args)[0])

        elif "form-data" in self._content_type:
            return self.__parse_form_data().get(*args)


class RequestGET(object):
    def __init__(self, environ):
        pass

    def get(self, **args):
        return ""

