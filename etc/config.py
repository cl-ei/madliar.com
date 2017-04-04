__all__ = ("DEBUG", "STATICS_URL_MAP")

# email config
mail_host = 'smtp.caoliang.net'
mail_user = 'i@caoliang.net'
mail_pass = '000000'
sender = 'i@caoliang.net'

DEBUG = True

STATICS_URL_MAP = {
    "^/statics": "application/blog/static",
}

