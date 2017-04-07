from wsgiserver.template import render


def home_page(request):
    print request.GET

    return render("application/blog/templates/index.html", {})


def list_view(request):
    return render(
        "application/blog/templates/index.html",
        {"description": "You are now at list-view."}
    )
