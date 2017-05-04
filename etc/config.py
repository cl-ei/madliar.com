__all__ = (
    "DEBUG",
    "PROJECT_ROOT",
    "POST_ARTICLE_PATH",
    "PARSED_ARTICLE_JSON",
    "STATICS_URL_MAP",
)

# email config
mail_host = 'smtp.caoliang.net'
mail_user = 'i@caoliang.net'
mail_pass = '000000'
sender = 'i@caoliang.net'

DEBUG = True

PROJECT_ROOT = "./" if DEBUG else "/home/wwwroot/madliar"
POST_ARTICLE_PATH = "template/_post/article"
PARSED_ARTICLE_JSON = "static/blog/js/article"

STATICS_URL_MAP = {
    "^/statics": "application/blog/static",
    "^/static": "static",
}
