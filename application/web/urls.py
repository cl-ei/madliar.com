from application.web import views

urls = {
    "^/$": views.index,
    "^/server/": views.server,
}
