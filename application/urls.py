from application.blog.urls import url as blog_url_map
from application.blog.views import home_page
from application.music.urls import url as music_url_map
from application.notebook.urls import url as notebook_url_map

url = {
    "^/$": home_page,
    "^/blog": blog_url_map,
    "^/music": music_url_map,
    "^/notebook": notebook_url_map,
}
