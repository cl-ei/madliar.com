from . import views

urls = {
    "^/$": views.index,
    "^/server/": views.server,
}
