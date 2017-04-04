from wsgiserver.middleware import render


def home_page(request):
    return render("application/blog/templates/index.html", {})
