# -*- coding: utf-8 -*-
import cgi
import re

QUERY_STRING_PATTERN = re.compile(r"([^=]+)=(.*)")
QUERY_STRING_SPLIT = re.compile('[&;]')


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

        script_name = environ.get('SCRIPT_NAME', "")
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

    @property
    def route_path(self):
        return self.__route_path

    @route_path.setter
    def route_path(self, path):
        self.__route_path = path

    @staticmethod
    def parse_query_string(raw_qs):
        pairs = [p for p in QUERY_STRING_SPLIT.split(raw_qs) if p]
        query = dict()
        for pair in pairs:
            m = QUERY_STRING_PATTERN.match(pair)
            if m:
                query[m.group(1)] = m.group(2)
        return query

    @cached_property
    def GET(self):
        """The WSGI spec says 'QUERY_STRING' may be absent."""
        raw_query_string = self.environ.get('QUERY_STRING', '')
        query = self.parse_query_string(raw_query_string)
        return query

    @cached_property
    def POST(self):
        if self.method != "POST":
            return dict()
        try:
            request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        if request_body_size > 1024 * 100:
            raise ValueError("POST request body too long: %s Bytes." % request_body_size)

        request_body = self.environ['wsgi.input'].read(request_body_size)
        post_qs = self.parse_query_string(request_body)
        return post_qs

    @cached_property
    def COOKIES(self):
        return self.environ.get('HTTP_COOKIE', '')

    @property
    def FILES(self):
        if not hasattr(self, '_files'):
            self._load_post_and_files()
        return self._files
