from madliar.template import render
from application.notebook import dao


def handler(request):
    mad_token = request.COOKIES.get("madToken")
    email = request.COOKIES.get("email")

    result = dao.check_login(email, mad_token)
    context = {"login_info": {"email": email}} if result else {}
    return render(
        "template/notebook/index.html",
        context=context
    )
