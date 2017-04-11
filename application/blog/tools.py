import sys
import os


def parse_article_info(file_path):
    #
    #     mod_time = f_name.split("-")[:3] + [randint(16, 23) for _ in range(3)]
    #     mod_time = datetime.strptime("%s-%s-%s %s:%s:%s" % tuple(mod_time), "%Y-%m-%d %H:%M:%S")
    #     mod_time -= timedelta(hours=8)
    #
    #     with open(os.path.join(ARTICLE_PATH, f_name)) as f:
    #         content = f.read().decode("utf-8")
    #
    #     header, detail = content_analysis(content, True)
    #     try:
    #         article = Article.objects.get(title=header["title"])
    #     except Exception:
    #         article = Article(title=header["title"])
    #
    #     article.author = header.get("author", "CL")
    #     article.category = header.get("category", "观点")
    #
    #     __tags = header.get("tags", "") + "," + header.get("tag", "")
    #     article.tags = re.sub("\s+", " ", __tags.replace(u"，", " ").replace(",", " ")).strip()
    #
    #     article.create_time = mod_time
    #     article.last_modified_time = mod_time
    #     article.description = header.get("description", "")
    #     article.detail = json.dumps({"md": content, "inner_md": detail})
    #     article.is_deleted = False
    #
    #     article.save()
    return {}


def generate_cached_article_json(*args, **kwargs):
    sys.stdout.write("Start load article.")

    from etc.config import POST_ARTICLE_PATH
    file_list = os.listdir(POST_ARTICLE_PATH)

    article_info_list = []
    for file_path in file_list:
        article_info_list.append(parse_article_info(file_path))

    return article_info_list
