
STATUS_MAP = {
    404: "404 NOT FOUND",
}


class HttpResponse(object):
    def __init__(self, content="", status=200):
        self._status = STATUS_MAP.get(status, "200 OK")
        self._content = content

    @property
    def status(self):
        return self._status

    @property
    def content(self):
        return self._content
