"""
website config.

"""

import os


EMAIL_CONFIG = {
    "mail_host": 'smtp.caoliang.net',
    "mail_user": 'i@caoliang.net',
    "mail_pass": '000000',
    "sender": 'i@caoliang.net',
}

if os.name in ("nt", ):
    PROJECT_ROOT = "./"
    REDIS_CONFIG = {}

    # for blog app:
    PARSED_ARTICLE_JSON = "static/blog/"

    # for notebook app
    APP_NOTE_BOOK_CONFIG = {
        "user_root_foler": "./",
    }
    APP_LOG_PATH = "./"

    # for music app
    MUSIC_FOLDER = "./music"

else:
    PROJECT_ROOT = "/home/wwwroot/madliar.com"
    APP_NOTE_BOOK_CONFIG = {
        "user_root_foler": "/home/wwwroot/notebook",
    }
    APP_LOG_PATH = "/home/wwwroot/log"
    REDIS_CONFIG = {}
    MUSIC_FOLDER = "./music"
