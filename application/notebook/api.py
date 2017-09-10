# -*- coding:utf-8 -*-
import json
import os
import re

from madliar.http.response import HttpResponse

from application.notebook import dao
from etc.config import APP_NOTE_BOOK_CONFIG


def json_to_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")


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


def handler(request):
    if request.method.lower() != "post":
        return json_to_response({"err_code": 403, "err_msg": "Only POST method supported."})
    
    action = request.POST.get("action")
    try:
        http_response = supported_action.run(action, request)
    except supported_action.ActionDoesNotExisted:
        http_response = json_to_response({"err_code": 404, "err_msg": "Action(%s) is not supported." % action})

    return http_response


@supported_action(action="login")
def login(request):
    email = request.POST.get("email")
    password = request.POST.get("password", "")
    email_pattern = re.compile(r"^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$")
    if not email_pattern.match(email):
        return json_to_response({"err_code": 403, "err_msg": u"错误的邮箱。"})

    if not 5 < len(password) < 48:
        return json_to_response({"err_code": 403, "err_msg": u"密码过长或过短。"})

    result, token = dao.login(email=email, password=password)
    response = json_to_response({
        "err_code": 0 if isinstance(token, (str, unicode)) and len(token) == 64 else 403,
        "token" if result else "err_msg": token,
        "email": email,
    })
    return response


@supported_action(action="regist")
def regist(request):
    email = request.POST.get("email")
    password = request.POST.get("password", "")
    email_pattern = re.compile(r"^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$")
    if not email_pattern.match(email):
        return json_to_response({"err_code": 403, "err_msg": u"错误的邮箱。"})

    if not 5 < len(password) < 48:
        return json_to_response({"err_code": 403, "err_msg": u"密码过长或过短。"})

    result, token = dao.regist(email, password)
    response = json_to_response({
        "err_code": 0 if isinstance(token, (str, unicode)) and len(token) == 64 else 403,
        "token" if result else "err_msg": token,
        "email": email,
    })
    return response


@supported_action(action="logout")
def logout(request):
    email = request.COOKIES.get("email")
    if email:
        dao.logout(email)
    return json_to_response({"err_code": 0})


def login_required(func):
    def wraped_func(*args, **kwargs):
        request = args[0] or kwargs.get("request")
        if not request:
            raise TypeError("Error param request: %s." % request)
        mad_token = request.COOKIES.get("madToken")
        email = request.COOKIES.get("email")

        result = dao.check_login(email, mad_token)
        if not result:
            return json_to_response({"err_code": 403, "err_msg": u"您的认证已经过期，请重新登录。"})
        return func(*args, **kwargs)
    return wraped_func


@supported_action(action="get_file_list")
@login_required
def get_file_list(request):
    node_id = request.POST.get("id")
    email = request.COOKIES.get("email")
    if node_id == "#":
        return json_to_response([{"id": ".", "text": email, "children": True}])

    app_root_folder = APP_NOTE_BOOK_CONFIG.get("user_root_foler")
    user_root_foler = os.path.join(app_root_folder, email)
    path = os.path.join(user_root_foler, node_id)
    if not os.path.isdir(path):
        return json_to_response([])

    children = os.listdir(path)
    data = []
    for child in children:
        this_node_path = os.path.join(path, child)
        if os.path.isdir(this_node_path):
            data.append({
                "id": os.path.join(node_id, child),
                "type": "folder",
                "text": child,
                "children": True,
            })
        if os.path.isfile(this_node_path):
            data.append({
                "id": os.path.join(node_id, child),
                "type": "file",
                "text": child,
            })
    return json_to_response(data)


def check_path_string_is_avaliable(text):
    if not isinstance(text, unicode):
        try:
            text = text.decode("utf-8")
            if not isinstance(text, unicode):
                return False
        except UnicodeEncodeError:
            return False
    return bool(re.match(u"^[a-zA-Z0-9_\u4e00-\u9fa5]+$", text))
