from wsgiserver.middleware import route_include

from .views import *

url = {
    "^/?$": home_page
}
