"""
config if os is windows.

"""

DEBUG = True
PROJECT_ROOT = "./"

ENABLE_SYS_LOG = True
SYS_LOG_PATH = "./"

APP_LOG_PATH = "./"

REDIS_CONFIG = {}
STATICS_URL_MAP = {
    "^/statics": "application/blog/static",
    "^/static": "static",
    "^/music_file": "music",
}

# for blog app:
PARSED_ARTICLE_JSON = "static/blog/"

# for notebook app
APP_NOTE_BOOK_CONFIG = {
    "user_root_foler": "./",
}

# for music app
MUSIC_FOLDER = "./music"
