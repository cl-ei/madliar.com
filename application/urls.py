from .web import views as web_views


url = {
    "^/web": web_views.hello_world,
    "^/share/(\w+)/?$": web_views.arg_test_responset,
}
