from wsgiserver.middleware import HttpResponse


def index(request):
    request.POST.get("key")

    with open("application/templates/index.html") as f:
        content = f.read()

    return HttpResponse(content)


def server():
    pass
