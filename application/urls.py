from .blog.urls import url as blog_url
from wsgiserver.middleware import route_include, static_files_response

url = {
    "^/blog": route_include(blog_url),
}
