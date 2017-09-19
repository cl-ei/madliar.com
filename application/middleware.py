from etc.log4 import logging
from madliar.http.response import Http410Response


def force_return_410_when_not_found(get_response):
    def warp_get_response(request, *args, **kwargs):
        request_url = request.path_info

        response = get_response(request, *args, **kwargs)
        if response.status_code == 404 and (
            request_url.startswith("/blog")
            or request_url.startswith("/static")
        ):
            logging.info(
                "The page(%s) is not avaliable, return 410 instead of 404."
                % request_url
            )
            return Http410Response()
        return response
    return warp_get_response
