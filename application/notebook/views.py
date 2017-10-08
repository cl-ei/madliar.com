# -*- coding:utf-8 -*-
import os
from madliar.http.response import HttpResponse, Http404Response, Http500Response, STATICS_FILE_MIME_TYPE
from madliar.template import render
from application.notebook import dao


def handler(request):
    mad_token = request.COOKIES.get("madToken")
    email = request.COOKIES.get("email")

    result = dao.check_login(email, mad_token)
    context = {"login_info": {"email": email}} if result else {}
    return render(
        "template/notebook/index.html",
        context=context
    )


def s(request, key):
    path = dao.get_shared_file(key)
    if not path or not os.path.exists(path):
        return Http404Response()

    try:
        with open(path, "rb") as f:
            content = f.read()
    except Exception:
        # TODO: add log.
        return Http500Response()

    base_name, ex_name = os.path.splitext(path)
    ex_name = ex_name.lstrip(".")

    content_type = "application/octet-stream"
    if not ex_name:
        content_type = "text/plain"
    elif ex_name.lower() in ("md", "markdown"):
        content_type = "text/plain"
    else:
        for ex, content_t in STATICS_FILE_MIME_TYPE:
            if ex_name in ex.split(" "):
                content_type = content_t
                break

    if not content_type.startswith("text"):
        return HttpResponse(content, content_type=content_type)

    if type(content) != unicode:
        try:
            content = content.decode("utf-8")
        except Exception:
            content = u"未能读取文件内容，其中含有不能识别的编码。"

    title = base_name.split("\\" if os.name in ("nt", ) else "/")[-1]
    context_data = {
        "title": title,
        "detail": content,
        "need_trans": ex_name.lower() in ("md", "markdown")
    }
    return render("template/notebook/share.html", context=context_data)
