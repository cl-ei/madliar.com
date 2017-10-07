from application.notebook.views import handler, s
from application.notebook.api import handler as api_handler


url = {
    r"/?$": handler,
    r"/api/?$": api_handler,
    r"/([a-zA-Z0-9]{16})/?$": s,
}
