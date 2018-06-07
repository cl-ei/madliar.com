import os
from etc.config import LOG_PATH
from madliar.http.response import HttpResponse

from application.blog.urls import url as blog_url_map
from application.blog.views import home_page
from application.music.urls import url as music_url_map
from application.notebook.urls import url as notebook_url_map


def robots_response(request):
    response = HttpResponse(
        content=(
            "User-agent:  *\n"
            "Disallow:  /static/\n"
        ),
        content_type="text/plain",
        charset="utf-8"
    )
    return response


def record(request):
    action = request.POST.get("action", "")
    if action == "chat_log":
        p = {}
        for k in ("room_id", "datetime_str", "user", "ul", "decoration", "dl", "msg"):
            p[k] = request.POST.get(k)
        file_name = os.path.join(LOG_PATH, "chat_%s.log" % p["room_id"])
        content = "[%s][%-5s][%s %s] %s -> %s" % (
            p["datetime_str"], p["ul"], p["decoration"], p["dl"], p["user"], p["msg"]
        )
        with open(file_name, "a+") as f:
            print >> f, content
        return HttpResponse(content)
    return HttpResponse("")


url = {
    r"^/robots?\.txt/?": robots_response,
    r"^/$": home_page,
    r"^/record": record,
    r"^/blog": blog_url_map,
    r"^/music": music_url_map,
    r"^/notebook": notebook_url_map,
}
