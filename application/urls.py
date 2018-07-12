from madliar.http.response import HttpResponse
from application.blog.urls import url as blog_url_map
from application.blog.views import home_page
from application.music.urls import url as music_url_map
from application.notebook.urls import url as notebook_url_map

from application.recored import record


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


def timeout_response(request):
    try:
        wait_time = int(request.GET.get("time_out"))
    except Exception:
        wait_time = 65
    import time
    time.sleep(wait_time)
    return HttpResponse(content="OK", content_type="text/plain")


url = {
    r"^/robots?\.txt/?": robots_response,
    r"^/$": home_page,
    r"^/record": record,
    r"^/blog": blog_url_map,
    r"^/music": music_url_map,
    r"^/notebook": notebook_url_map,
    r"^/timeout": timeout_response,
}
