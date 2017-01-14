from wsgiserver.middleware import HttpResponse


def index(request):
    request.POST.get("key")

    with open("application/templates/index.html") as f:
        content = f.read()

    return HttpResponse(content)


def server():
    pass



# '__getitem__', '__gt__',
# '__hash__', '__init__', '__iter__', '__le__', '__len__',
# '__lt__', '__ne__', '__new__', '__reduce__',
# '__reduce_ex__', '__repr__', '__setattr__',
# '__setitem__', '__sizeof__',
# '__str__', '__subclasshook__',
# 'clear',
# 'copy',
# 'fromkeys',
# 'get',
# 'has_key',
# 'items',
# 'iteritems',
# 'iterkeys',
# 'itervalues',
# 'keys', 'pop',
# 'popitem',
# 'setdefault',
# 'update',
# 'values',
# 'viewitems', 'viewkeys', 'viewvalues']

