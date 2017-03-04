import re

from wsgiref.simple_server import make_server
from application.urls import urls
from wsgiserver.middleware import HttpResponse, Request, HttpResponseServerError


class Core(object):
    def __init__(self, host="", port=80):
        super(Core, self).__init__()
        self.host = host
        self.port = port

    def __call__(environ, start_response):
        path = re.sub(r"/+$", r"/", environ["PATH_INFO"] + "/")

        view_func = None
        for url in urls:
            if re.match(url, path):
                view_func = urls[url]
                break

        try:
            response = view_func(Request(environ))

            if not isinstance(response, HttpResponse):
                raise TypeError("View function returned a bad response!")

        except Exception as e:
            from StringIO import StringIO
            stdout = StringIO()
            print >>stdout, "Sever Error: %s" % e
            response = HttpResponseServerError()

        status = response.status
        headers = response.headers

        start_response(status, headers)
        return [response.content]

    def start_server(self):

        httpd = make_server(self.host, self.port, Core.get_application())
        print "Serving at: %s:%s" % (self.host, self.port)

        try:
            httpd.serve_forever()
        except Exception as e:
            print e
            httpd.shutdown()

        print "Service Stop."

