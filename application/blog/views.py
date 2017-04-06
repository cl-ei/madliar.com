from wsgiserver.template import render


def home_page(request):
    a = dict()
    a[1] = request.GET
    b = dict()
    b[2] = request.GET
    return render("application/blog/templates/index.html", {1: a, 2: b})


def list_view(request):
    return render(
        "application/blog/templates/index.html",
        {"description": "You are now at list-view."}
    )
