import re

from wsgiref.simple_server import make_server
from application.urls import urls
from wsgiserver.response import HttpResponse


class Core(object):
    def __init__(self, host="", port=80):
        self.host = host
        self.port = port

    def start_server(self):

        host = self.host
        port = self.port

        httpd = make_server(host, port, Core.response)
        print "Serving at: %s:%s" % (host, port)

        try:
            httpd.serve_forever()
        except Exception as e:
            print e
            httpd.shutdown()

        print "Service Stop."

    @staticmethod
    def response(environ, start_response):
        path = re.sub(r"/+$", r"/", environ["PATH_INFO"] + "/")
        print "path: ", path

        view_func = None
        for url in urls:
            if re.match(url, path):
                view_func = urls[url]

        try:
            response = view_func(environ)
            if isinstance(response, HttpResponse):
                status = response.status
                content = response.content
            elif isinstance(response, str) and len(response):
                status = "200 OK"
                content = response
            else:
                raise TypeError("View function returned a bad response!")

            start_response(status, [('Content-Type', 'text/html')])
            return content
        except Exception as e:
            print e
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return '<h1>Not Found!</h1>'

