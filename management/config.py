"""
website config.

"""

import os

if os.name in ("nt", ):
    from management.nt_config import *
else:
    from management.posix_config import *


EMAIL_CONFIG = {
    "mail_host": 'smtp.caoliang.net',
    "mail_user": 'i@caoliang.net',
    "mail_pass": '000000',
    "sender": 'i@caoliang.net',
}

INSTALLED_MIDDLEWARE = ()
