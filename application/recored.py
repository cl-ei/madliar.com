import os
import json
import datetime
from madliar.http.response import HttpResponse

from etc.config import LOG_PATH
from etc.log4 import logging


class supported_action(object):
    ActionDoesNotExisted = type("supported_action__ActionDoesNotExisted", (Exception, ), {})
    __function = {}

    def __init__(self, action):
        self.__action = action

    def __call__(self, func):
        self.__class__.__function[self.__action] = func
        return func

    @classmethod
    def run(cls, action, *args, **kwargs):
        picked_func = cls.__function.get(action)
        if callable(picked_func):
            return picked_func(*args, **kwargs)
        else:
            raise cls.ActionDoesNotExisted


def record(request):
    if request.method.lower() != "post":
        return HttpResponse("")

    action = request.POST.get("action")
    try:
        http_response = supported_action.run(action, request)
    except supported_action.ActionDoesNotExisted:
        http_response = HttpResponse("Action does not support.")

    return http_response


@supported_action("chat_log")
def add_chat_log(request):
    room_id = request.POST.get("room_id")
    try:
        raw_msg_list = request.POST.get("msg_list")
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


@supported_action("prize_log")
def add_prize_log(request):
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
