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


class Request(object):
    def __init__(self, environ):
        self.__environ = environ
        self.server_protocol = environ["SERVER_PROTOCOL"]
        self.method = environ["REQUEST_METHOD"]
        self.content_length = environ["CONTENT_LENGTH"]
        self.remote_addr = environ["REMOTE_ADDR"]
        self.path = environ["PATH_INFO"]
        self.content_type = environ["CONTENT_TYPE"]
        self.__post_object = None

    @property
    def POST(self):
        if self.method != "POST":
            return None

        if not self.__post_object:
            self.__post_object = RequestPOST(self.__environ)

        return self.__post_object

    @property
    def GET(self):
        return RequestGET(self.__environ) if self.method == "GET" else None

    def show(self):
        print self.__dict__


DEFAULT_HEADERS = {
    "Server": "cls.web/pre alpha 1.0",
}


class HttpResponse(object):
    def __init__(self, content, mimetype="text/html"):
        self.__content = content
        self.__status = "200 OK"
        self.__headers = DEFAULT_HEADERS
        self.__headers.update({"Content-Type": mimetype})

    @property
    def status(self):
        return self.__status

    @property
    def content(self):
        return self.__content

    @property
    def headers(self):
        return [(k, self.__headers[k]) for k in self.__headers]


class HttpResponseServerError(object):

    def __init__(self, content=None):
        self.__content = content or "<center><h1>500: Server Internal Error.</h1></center>"

    @property
    def status(self):
        return "500 Internal Server Error"

    @property
    def content(self):
        return self.__content

    @property
    def headers(self):
        _headers = DEFAULT_HEADERS
        _headers.update({"Content-Type": "text/html"})
        return [(k, _headers[k]) for k in _headers]

