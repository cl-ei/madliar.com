import json

from cgi import escape
from urlparse import parse_qs


class RequestPOST(object):
    def __init__(self, environ):
        if environ["REQUEST_METHOD"] == "POST":
            self._content_type = environ["CONTENT_TYPE"]
            self._content = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))
        else:
            self._content = None

    def __parse_form_data(self):
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


class Request(object):
    def __init__(self, environ):
        self.server_protocol = environ["SERVER_PROTOCOL"]
        self.method = environ["REQUEST_METHOD"]
        self.content_length = environ["CONTENT_LENGTH"]
        self.remote_addr = environ["REMOTE_ADDR"]
        self.path = environ["PATH_INFO"]
        self.content_type = environ["CONTENT_TYPE"]
        self.POST = RequestPOST(environ)
        self.GET = RequestGET(environ)

    def show(self):
        print self.__dict__


STATUS_MAP = {
    404: "404 NOT FOUND",
}


class HttpResponse(object):
    def __init__(self, content="", status=200, headers=None):
        self._status = STATUS_MAP.get(status, "200 OK")
        self._content = content
        self._headers = headers if headers else [('Content-Type', 'text/html')]

    @property
    def status(self):
        return self._status

    @property
    def content(self):
        return self._content

    @property
    def headers(self):
        return self._headers
