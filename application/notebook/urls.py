from application.notebook.views import handler
from application.notebook.api import handler as api_handler


url = {
    "/?$": handler,
    "/api/?$": api_handler,
}
