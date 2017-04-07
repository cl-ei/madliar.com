from .blog.urls import url as blog_url_map
from .blog.views import home_page

url = {
    "^/$": home_page,
    "^/blog": blog_url_map,
}
