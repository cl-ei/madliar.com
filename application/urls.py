from application.blog.urls import url as blog_url_map
from application.blog.views import home_page, favicon_response, record

url = {
    "^/$": home_page,
    "^/favicon.ico/?$": favicon_response,
    "^/blog": blog_url_map,
    "^/record/?$": record
}
