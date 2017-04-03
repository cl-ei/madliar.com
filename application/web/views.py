#
#
#
# def index(request):
#
#     with open("application/templates/index.html") as f:
#         content = f.read()
#
#     return HttpResponse(content)
#
#
# def server(request):
#     path = "application/static/test.jpeg"
#
#     with open(path, "rb") as f:
#         content = f.read()
#
#     return HttpResponse(content, "image/jpeg")
#

from wsgiserver.middleware import HttpResponse


def hello_world(request):
    print request.route_path
    return HttpResponse("<center><h3>Hello world!</h3></center>")


def arg_test_responset(request, num):
    return HttpResponse("<center><h3>Hello world, %s!</h3></center>" % num)


def sub_view_func_test(request):
    return HttpResponse("<center><h3>sub_view_func_test !</h3></center>")

def sub_view_func_test_2(request):
    return HttpResponse("<center><h3>sub_view_func_test_2 !</h3></center>")