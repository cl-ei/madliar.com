from wsgiserver.middleware import render


def home_page(request):
    return render("application/blog/templates/index.html", {})


def list_view(request):
    return render(
        "application/blog/templates/index.html",
        {"description": "You are now at list-view."}
    )
