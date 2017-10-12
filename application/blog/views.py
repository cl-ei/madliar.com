# -*- coding:utf-8 -*-
import os

from madliar.http.response import HttpResponse
from madliar.template import render

from etc.config import PROJECT_ROOT, PARSED_ARTICLE_JSON, CDN_URL


def favicon_response(request):
    with open("static/img/favicon.png", "rb") as f:
        content = f.read()
    return HttpResponse(content, content_type="image/x-icon")


def home_page(request):
    article_file_path = os.path.join(PROJECT_ROOT, PARSED_ARTICLE_JSON)
    article_js_file_name = os.listdir(article_file_path)[0]
    article_js = os.path.join(PARSED_ARTICLE_JSON, article_js_file_name)
    context = {
        "article_js": article_js,
        "page": {
            "author": "CL",
            "description": u"CL，编程爱好者，这是CL的官方博客，记录生活感悟和学习点滴。",
            "keywords": u"MADLIAR, CL, CL's 疯言疯语, 疯言疯语, 风言风语, CL博客",
        },
        "CDN_URL": CDN_URL,
    }
    return render(
        "template/home_page.html",
        context=context
    )

