import json
import os

from madliar.template import render

from etc.config import MUSIC_FOLDER, CDN_URL


def handler(request):
    if request.GET.get("ref"):
        encoding = "utf-8"
        view_data = {
            "ref": True,
            "music_list": json.dumps(
                [_.decode(encoding) for _ in os.listdir(MUSIC_FOLDER)],
                ensure_ascii=False
            )
        }
    else:
        view_data = {"ref": False}

    view_data["CDN_URL"] = CDN_URL
    return render(
        "template/music/index.html",
        context=view_data
    )
