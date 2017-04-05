from wsgiserver.middleware import route_include

from .views import *

url = {
    "^/?$": list_view
}
