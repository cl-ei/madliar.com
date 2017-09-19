"""
config.py for madliar framework.

Only project environ configurations fit to be collected in
this config file, not business logic config.
"""

import os

INSTALLED_MIDDLEWARE = (
    "application.middleware.force_return_410_when_not_found",
)

if os.name in ("nt", ):
    DEBUG = True

    ENABLE_SYS_LOG = True
    SYS_LOG_PATH = "./"

    STATICS_URL_MAP = {
        "^/static": "static",
        "^/music_file": "music",
    }

else:
    DEBUG = False

    ENABLE_SYS_LOG = True
    SYS_LOG_PATH = "/home/wwwroot/log"

    STATICS_URL_MAP = {}
