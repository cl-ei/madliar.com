import cgi
import re
from wsgiref.headers import Headers

STATICS_FILE_MIME_TYPE = (
    (("png", "jpg", "jpeg", "gif"), "image", None),
    (("js", "woff"), "application", ("javascript", "x-font-woff")),
    (("css", ), "text", None),
)


class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res


class WSGIRequest(object):
    def __init__(self, environ):
        self._encoding = "utf-8"

        script_name = path_info = environ.get('SCRIPT_NAME', "")
        path_info = environ.get('PATH_INFO', "/")
        self.path_info = path_info

        self.script_url = environ.get('SCRIPT_URL', " ")
        self.environ = environ
        self.path = '%s/%s' % (script_name.rstrip('/'), path_info.replace('/', '', 1))
        self.__route_path = path_info

        self.META = environ
        self.META['PATH_INFO'] = path_info
        self.META['SCRIPT_NAME'] = script_name
        self.method = environ['REQUEST_METHOD'].upper()

        self.content_type, self.content_params = cgi.parse_header(environ.get('CONTENT_TYPE', ''))

    def _get_scheme(self):
        return self.environ.get('wsgi.url_scheme')

    def _load_post_and_files(self):
        pass

    @property
    def route_path(self):
        return self.__route_path

    @route_path.setter
    def route_path(self, path):
        self.__route_path = path

    @cached_property
    def GET(self):
        # The WSGI spec says 'QUERY_STRING' may be absent.
        raw_query_string = self.environ.get('QUERY_STRING', '')
        pairs = re.compile('[&;]').split(raw_query_string)

        query = dict()
        for pair in pairs:
            k, v = pair.split("=")
            query[k] = v or None
        return query

    def _get_post(self):
        if not hasattr(self, '_post'):
            self._load_post_and_files()
        return self._post

    def _set_post(self, post):
        self._post = post

    def COOKIES(self):
        return self.environ.get('HTTP_COOKIE', '')

    @property
    def FILES(self):
        if not hasattr(self, '_files'):
            self._load_post_and_files()
        return self._files

    POST = property(_get_post, _set_post)


class BaseResponse(object):
    def __init__(self, *args, **kwargs):
        self.status_code = kwargs.get("status_code", 200)
        self.reason_phrase = kwargs.get("reason_phrase", "OK")
        self.cookies = []
        self.charset = kwargs.get("charset", "utf-8")
        self._handler_class = None
        self._content = []
        self.__set_default_headers()
        self.headers.add_header(
            "Content-Type",
            kwargs.get("content_type", "text/html; charset=%s" % self.charset)
        )

    def __set_default_headers(self):
        self.headers = Headers([
            ("Server", "MadLiar"),
            ("Access-Control-Allow-Origin", "*"),
            ("X-Frame-Options", "SAMEORIGIN"),
        ])

    @property
    def content(self):
        return b''.join(self._content)

    @content.setter
    def content(self, value):
        # Consume iterators upon assignment to allow repeated iteration.
        if not hasattr(value, '__iter__'):
            value = [value]

        content = b''.join(map(
            lambda x: bytes(x) if isinstance(x, bytes) else bytes(x.encode(self.charset)),
            value
        ))
        self.headers.add_header("Content-length", str(len(content)))
        self._content = [content]

    def __iter__(self):
        return iter(self._content)


class HttpResponse(BaseResponse):
    def __init__(self, *args, **kwargs):
        BaseResponse.__init__(self, *args, **kwargs)
        content = kwargs.get("content", str(args[0]))
        if type(content) in (bytes, str):
            self.content = content


class Http404Response(BaseResponse):
    def __init__(self, *args, **kwargs):
        BaseResponse.__init__(self, *args, **kwargs)
        self.content = "<center><h3>404 Not Found!</h3></center>"
        self.status_code = 404
        self.reason_phrase = "Not Found"


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


def static_files_response(request, static_path):
    static_file_path = static_path + request.route_path
    try:
        with open(static_file_path, "rb") as f:
            content = f.read()
    except IOError:
        return Http404Response()

    try:
        static_file_ext_name = re.match(r".*\.(.*)", static_file_path).groups()[0].lower()
    except AttributeError:
        return Http404Response()

    for static_file_typedef in STATICS_FILE_MIME_TYPE:
        ext_name_group, mime_type, mime_desc = static_file_typedef
        if static_file_ext_name in ext_name_group:
            content_type = "%s/%s" % (
                mime_type,
                mime_desc[ext_name_group.index(static_file_ext_name)] if mime_desc else static_file_ext_name
            )
            break
    else:
        content_type = None

    return HttpResponse(content, content_type=content_type)


def route_include(url_map):
    return url_map
