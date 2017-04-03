from .web import views as web_views
from .web.urls import url as web_url
from wsgiserver.middleware import route_include

url = {
    "^/web": route_include(web_url),
}
