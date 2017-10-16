"""
config.py for madliar framework.

Only project environ configurations fit to be collected in
this config file, not business logic config.
"""

import os
import platform

DEBUG = False if "linux" in platform.system().lower() else True

INSTALLED_MIDDLEWARE = (
    "application.middleware.recored_access_info",
    "application.middleware.force_return_410_when_not_found",
)

if DEBUG:

    ENABLE_SYS_LOG = True
    SYS_LOG_PATH = "./"

    STATICS_URL_MAP = {
        "^/static": "static",
        "^/music_file": "music",
    }

else:

    ENABLE_SYS_LOG = True
    SYS_LOG_PATH = "/home/wwwroot/log"

    STATICS_URL_MAP = {}
