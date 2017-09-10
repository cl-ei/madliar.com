"""
config if os is linux.

"""
DEBUG = True
PROJECT_ROOT = "/home/wwwroot/madliar.com"

ENABLE_SYS_LOG = True
SYS_LOG_PATH = "/home/wwwroot/log"

APP_LOG_PATH = "/home/wwwroot/log"

REDIS_CONFIG = {}
STATICS_URL_MAP = {}

# for blog app:
PARSED_ARTICLE_JSON = "static/blog/"

# for notebook app

APP_NOTE_BOOK_CONFIG = {
    "user_root_foler": "/home/wwwroot/notebook",
}

# for music app
MUSIC_FOLDER = "./music"
