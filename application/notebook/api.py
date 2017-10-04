# -*- coding:utf-8 -*-
import json
import os
import re
import shutil

from madliar.http.response import HttpResponse

from application.notebook import dao
from etc.config import APP_NOTE_BOOK_CONFIG

app_notebook_path = APP_NOTE_BOOK_CONFIG.get("user_root_foler")


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
    response_data = {
        "err_code": 0 if isinstance(token, (str, unicode)) and len(token) == 64 else 403,
        "token" if result else "err_msg": token,
        "email": email,
    }
    if response_data.get("err_code") == 0:
        user_root_floder = os.path.join(app_notebook_path, email)
        os.mkdir(user_root_floder)

    response = json_to_response(response_data)
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


def get_file_type(ex_name):
    return ""


fs_coding = "gbk" if os.name in ("nt", ) else "utf-8"


@supported_action(action="get_file_list")
@login_required
def get_file_list(request):
    """

    :param request:
    :return: json data:
        :id     ->    full path
        :type   ->    folder, bin, text

    """
    node_id = request.POST.get("id")
    if type(node_id) != unicode:
        node_id = node_id.decode("utf-8")

    email = request.COOKIES.get("email")
    if node_id == "#":
        response = [{
            "id": email,
            "type": "folder",
            "text": email,
            "children": True
        }]
        return json_to_response(response)

    if node_id.split("/")[0] != email:
        # 沒有权限
        return json_to_response([])

    path = os.path.join(app_notebook_path, node_id)
    if not os.path.isdir(path):
        return json_to_response([])

    children = os.listdir(path)
    data = []
    for child in children:
        if type(child) != unicode:
            child = child.decode(fs_coding)

        this_node_path = os.path.join(path, child)
        if os.path.isdir(this_node_path):
            data.append({
                # 强制用“/”分割文件路径
                "id": "/".join(os.path.split(os.path.join(node_id, child))),
                "type": "folder",
                "text": child,
                "children": True,
            })
        if os.path.isfile(this_node_path):
            file_ex_name = os.path.splitext(child)[1].lstrip(".")
            data.append({
                "id": "/".join(os.path.split(os.path.join(node_id, child))),
                "type": get_file_type(file_ex_name),
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


@supported_action(action="mkdir")
@login_required
def mkdir(request):
    node_id = request.POST.get("node_id")
    email = request.COOKIES.get("email")
    if node_id.split("/")[0] != email:
        return json_to_response({
            "err_code": 403,
            "err_msg": "你没有权限在此创建目录。"
        })

    elif len(node_id.split("/")) > 9:
        return json_to_response({
            "err_code": 403,
            "err_msg": "目录层级过深，不支持继续创建。"
        })

    if os.name in ("nt", ):
        node_id = "\\".join(node_id.split("/"))
    if type(node_id) != unicode:
        try:
            node_id = node_id.decode("utf-8")
        except Exception:
            return json_to_response({
                "err_code": 403,
                "err_msg": "错误的编码格式。"
            })

    dir_name = request.POST.get("dir_name")
    if type(dir_name) != unicode:
        try:
            dir_name = dir_name.decode("utf-8")
        except Exception:
            return json_to_response({
                "err_code": 403,
                "err_msg": "错误的编码格式。"
            })

    if not os.path.isdir(os.path.join(app_notebook_path, node_id)):
        return json_to_response({
            "err_code": 403,
            "err_msg": "不存在的路径，请重新输入。"
        })

    if not check_path_string_is_avaliable(dir_name):
        return json_to_response({
            "err_code": 403,
            "err_msg": "名称中含有特殊字符，请重新输入。"
        })

    folder_path = os.path.join(node_id, dir_name)
    if os.path.exists(folder_path):
        return json_to_response({
            "err_code": 403,
            "err_msg": "目录已经存在。"
        })
    try:
        os.mkdir(folder_path)
    except Exception as e:
        # TODO: add log
        return json_to_response({
            "err_code": 500,
            "err_msg": "服务器内部错误。"
        })

    return json_to_response({"err_code": 0})


@supported_action(action="rm")
@login_required
def rm(request):
    node_id = request.POST.get("node_id")
    email = request.COOKIES.get("email")
    if node_id.split("/")[0] != email:
        return json_to_response({
            "err_code": 403,
            "err_msg": "你没有权限在此创建目录。"
        })
    if node_id == email:
        return json_to_response({
            "err_code": 403,
            "err_msg": "根目录无法删除！"
        })

    path = node_id
    if os.name in ("nt", ):
        path = "\\".join(path.split("/"))
    if type(path) != unicode:
        try:
            path = path.decode("utf-8")
        except Exception:
            return json_to_response({
                "err_code": 403,
                "err_msg": "错误的编码格式。"
            })
    try:
        shutil.rmtree(path)
    except Exception as e:
        # TODO: add log
        return json_to_response({
            "err_code": 500,
            "err_msg": "服务器内部错误。"
        })

    return json_to_response({"err_code": 0})
