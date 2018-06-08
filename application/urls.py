import os
import json
import datetime
from etc.config import LOG_PATH
from madliar.http.response import HttpResponse

from madliar.config.log4 import logging

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
        room_id = request.POST.get("room_id")
        try:
            raw_msg_list = request.POST.get("msg_list")
            logging.info("msg_list: [%s]" % raw_msg_list)
            msg_list = json.loads(raw_msg_list)
        except Exception as e:
            return HttpResponse("ERROR: %s" % e)

        log_contents = []
        for msg in msg_list:
            datetime_str = msg.get("datetime_str")
            user = msg.get("user")
            ul = msg.get("ul")
            decoration = msg.get("decoration")
            dl = msg.get("dl")
            raw_msg = msg.get("msg")
            if not user or not raw_msg:
                continue

            log_contents.append(
                "[%s][%-5s][%s %s] %s -> %s\n" % (datetime_str, ul, decoration, dl, user, raw_msg)
            )
        if not log_contents:
            return HttpResponse("")

        file_name = os.path.join(LOG_PATH, "chat_%s.log" % room_id)
        content = "".join(log_contents).strip("\n")
        if not isinstance(content, unicode):
            content = content.decode("utf-8", errors="replace")
        with open(file_name, "ab") as f:
            print >> f, content.encode("utf-8", errors="replace")
        return HttpResponse(content)
    elif action == "prize_log":
        try:
            count = int(request.POST.get("count"))
        except Exception:
            return HttpResponse("Error count")
        datetime_str = str(datetime.datetime.now())[:-3]
        provider = request.POST.get("provider")
        prize_type = request.POST.get("type")
        title = request.POST.get("title")
        p_url = request.POST.get("url")

        file_name = os.path.join(LOG_PATH, "prize_accept.log")
        content = "[%s][%s][%s][%s][%s][%s]" % (datetime_str, count, prize_type, provider, p_url, title)
        if not isinstance(content, unicode):
            content = content.decode("utf-8", errors="replace")
        with open(file_name, "ab") as f:
            print >> f, content.encode("utf-8", errors="replace")
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
