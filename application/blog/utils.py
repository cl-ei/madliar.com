# -*- coding:utf-8 -*-
import json
import os
import random
import re
import sys

from etc.config import DEBUG, PROJECT_ROOT, POST_ARTICLE_PATH, \
    PARSED_ARTICLE_JSON
from lib.randomlib import randstr


class ArticleParser(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("file_name") or args[0]
        self.path = kwargs.get("file_path") or args[1]
        self.create_time = map(int, self.name.split("-")[:3])

        self.id = 0
        for index, num in enumerate(self.create_time[::-1]):
            self.id += 100**index * num

        with open(os.path.join(self.path, self.name), "r") as f:
            content = f.read()
        if isinstance(content, unicode):
            self.content = content
        else:
            self.content = content.decode("utf-8")

        self.header = None
        self.header_style_pattern = re.compile(r"(\w+)\s*:\s*(.*)")

        self.header_info = {}
        self.body = ""

    def __split_article_header_content(self):
        m = re.match(r"^-{3,}([\s\S]*)", self.content)
        if m:
            content = m.groups()[0]
            self.header, self.body = re.split(r"-{3,}\r?\n", content, maxsplit=1)

    def __parse_header(self):
        for line in self.header.split("\n"):
            line = line.replace(u'　', ":", 1).replace("\r", "")
            match = self.header_style_pattern.match(line)
            if match:
                k, v = match.groups()
                if k in ["tag", "tags"]:
                    k = "tags"
                    tag_list = v.replace(u'，', ",").replace(u' ', ",").split(",")
                    v = [tag.strip(" \r\n") for tag in tag_list if tag]
                else:
                    v = v.strip(" \r\n")
                self.header_info.update({k: v})

    def __parse_body(self):
        preview = self.body.split("<!--more-->")[0]
        preview = re.sub("<img.*>\s+", "", preview)
        preview = re.sub("^\s*#.*\s+", "", preview)
        self.header_info["preview"] = preview

        m = re.match(r"<img\s*src=([^\s]+).*>?", self.body)
        if m:
            first_figure = m.groups()[0].strip("'\"")
        else:
            figure_index = str(random.randint(0, 5))
            first_figure = "/static/blog/img/preview_%s.jpg" % figure_index
        self.header_info["first_figure"] = first_figure

    @property
    def article_info(self):
        self.__split_article_header_content()
        self.__parse_header()
        self.__parse_body()

        article_info = {
            "create_time": u"%s年%s月%s日" % tuple(self.create_time),
            "id": self.id,
            "content": self.body
        }
        article_info.update(self.header_info)

        for k, v in article_info.items():
            if isinstance(v, str):
                article_info[k] = v.decode("utf-8")

        return article_info


def generate_cached_article_json(*args, **kwargs):
    sys.stdout.write("Start load article.\n")

    article_path = os.path.join(PROJECT_ROOT, POST_ARTICLE_PATH)
    file_list = os.listdir(article_path)

    article_list = {}
    for file_name in file_list:
        parser = ArticleParser(file_name=file_name, file_path=article_path)
        article_list[parser.id] = parser.article_info

    detail = json.dumps(
        article_list,
        ensure_ascii=False,
        indent=4 if DEBUG else None
    )
    id_list = json.dumps(sorted(article_list.keys())[::-1])
    total_article = u"".join([
        "window.articleList=", detail, ";",
        "window.articleIdList=", id_list
    ])

    article_js_file_path = os.path.join(PROJECT_ROOT, PARSED_ARTICLE_JSON)
    for existed_file in os.listdir(article_js_file_path):
        print existed_file
        os.remove(os.path.join(article_js_file_path, existed_file))

    article_js_file = os.path.join(PARSED_ARTICLE_JSON, randstr(64) + ".js")
    with open(article_js_file, "w") as f:
        f.write(total_article.encode("utf-8"))
