import re

from application.urls import urls
from wsgiserver.middleware import HttpResponse, Request, HttpResponseServerError
from wsgiref.headers import Headers


class BaseResponse(object):
    def __init__(self, *args, **kwargs):
        self.status_code = 200
        self.reason_phrase = "OK"
        self.cookies = []
        self._handler_class = None
        self.__ = 0
        self._content = []
        self.__set_default_headers()

    def __set_default_headers(self):
        self.headers = Headers([
            ("Server", "Madliar"),
            ("Access-Control-Allow-Origin", "*"),
            ("X-Frame-Options", "SAMEORIGIN"),
        ])
        self.headers.add_header("Content-Type", "text/html", charset="utf-8")

    @property
    def content(self):
        return "Hello world"

    @content.setter
    def content(self, value):
        self.content = [value]
        self._content.append(value)

    def __iter__(self):
        return iter(self._content)


class StreamingHttpResponse(BaseResponse):

    def _set_streaming_content(self, value):
        return self, value


class FileResponse(StreamingHttpResponse):
    """
    A streaming HTTP response class optimized for files.
    """
    block_size = 4096

    def _set_streaming_content(self, value):
        super(FileResponse, self)._set_streaming_content(value)


class HttpResponseRedirectBase(HttpResponse):
    allowed_schemes = ['http', 'https', 'ftp']

    def __init__(self, redirect_to, *args, **kwargs):
        super(HttpResponseRedirectBase, self).__init__(*args, **kwargs)
        self['Location'] = iri_to_uri(redirect_to)
        parsed = urlparse(force_text(redirect_to))
        if parsed.scheme and parsed.scheme not in self.allowed_schemes:
            raise DisallowedRedirect("Unsafe redirect to URL with protocol '%s'" % parsed.scheme)

    url = property(lambda self: self['Location'])

    def __repr__(self):
        return '<%(cls)s status_code=%(status_code)d%(content_type)s, url="%(url)s">' % {
            'cls': self.__class__.__name__,
            'status_code': self.status_code,
            'content_type': self._content_type_for_repr,
            'url': self.url,
        }


class BaseHandler(object):

    def __init__(self):
        pass

    def get_response(self, request):
        return BaseResponse()


class WSGIRequest(object):
    def __init__(self, environ):
        pass
        # script_name = get_script_name(environ)
        # path_info = get_path_info(environ)
        # if not path_info:
        #     # Sometimes PATH_INFO exists, but is empty (e.g. accessing
        #     # the SCRIPT_NAME URL without a trailing slash). We really need to
        #     # operate as if they'd requested '/'. Not amazingly nice to force
        #     # the path like this, but should be harmless.
        #     path_info = '/'
        # self.environ = environ
        # self.path_info = path_info
        # # be careful to only replace the first slash in the path because of
        # # http://test/something and http://test//something being different as
        # # stated in http://www.ietf.org/rfc/rfc2396.txt
        # self.path = '%s/%s' % (script_name.rstrip('/'),
        #                        path_info.replace('/', '', 1))
        # self.META = environ
        # self.META['PATH_INFO'] = path_info
        # self.META['SCRIPT_NAME'] = script_name
        # self.method = environ['REQUEST_METHOD'].upper()
        # self.content_type, self.content_params = cgi.parse_header(environ.get('CONTENT_TYPE', ''))
        # if 'charset' in self.content_params:
        #     try:
        #         codecs.lookup(self.content_params['charset'])
        #     except LookupError:
        #         pass
        #     else:
        #         self.encoding = self.content_params['charset']
        # self._post_parse_error = False
        # try:
        #     content_length = int(environ.get('CONTENT_LENGTH'))
        # except (ValueError, TypeError):
        #     content_length = 0
        # self._stream = LimitedStream(self.environ['wsgi.input'], content_length)
        # self._read_started = False
        # self.resolver_match = None

    def _get_scheme(self):
        return self.environ.get('wsgi.url_scheme')

    def GET(self):
        # The WSGI spec says 'QUERY_STRING' may be absent.
        # raw_query_string = get_bytes_from_wsgi(self.environ, 'QUERY_STRING', '')
        # return http.QueryDict(raw_query_string, encoding=self._encoding)
        pass

    def _get_post(self):
        if not hasattr(self, '_post'):
            self._load_post_and_files()
        return self._post

    def _set_post(self, post):
        self._post = post

    def COOKIES(self):
        # raw_cookie = get_str_from_wsgi(self.environ, 'HTTP_COOKIE', '')
        # return http.parse_cookie(raw_cookie)
        return ""

    @property
    def FILES(self):
        if not hasattr(self, '_files'):
            self._load_post_and_files()
        return self._files

    POST = property(_get_post, _set_post)


class WSGIHandler(BaseHandler):
    request_class = WSGIRequest

    def __init__(self, *args, **kwargs):
        super(WSGIHandler, self).__init__(*args, **kwargs)
        pass

    def __call__(self, environ, start_response):

        request = self.request_class(environ)
        response = self.get_response(request)

        response._handler_class = self.__class__

        status = '%d %s' % (response.status_code, response.reason_phrase)
        start_response(str(status), response.headers.items())

        if getattr(response, 'file_to_stream', None) is not None and environ.get('wsgi.file_wrapper'):
            response = environ['wsgi.file_wrapper'](response.file_to_stream)
        return response


def get_application():
    return WSGIHandler()

