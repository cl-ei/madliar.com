from .blog.urls import url as blog_url
from .blog.views import home_page
from wsgiserver.middleware import route_include, static_files_response

url = {
    "^/$": home_page,
    "^/blog": route_include(blog_url),
}
