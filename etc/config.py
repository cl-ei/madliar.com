"""
website config.

"""

import os

# ----------------------------- common config ------------------------------ #
EMAIL_CONFIG = {
    "mail_host": 'smtp.caoliang.net',
    "mail_user": 'i@caoliang.net',
    "mail_pass": '000000',
    "sender": 'i@caoliang.net',
}

REDIS_CONFIG = {

}

PARSED_ARTICLE_JSON = "static/blog/js/article"
MUSIC_FOLDER = "./music"


# ----------------------------- windows CONFIG ----------------------------- #
if os.name in ("nt", ):
    PROJECT_ROOT = "./"
    APP_LOG_PATH = "./"

    # for notebook app
    APP_NOTE_BOOK_CONFIG = {
        "user_root_foler": "./",
    }

# ----------------------------- linux CONFIG ----------------------------- #
else:
    PROJECT_ROOT = "/home/wwwroot/madliar.com"
    APP_LOG_PATH = "/home/wwwroot/log"

    APP_NOTE_BOOK_CONFIG = {
        "user_root_foler": "/home/wwwroot/notebook",
    }
