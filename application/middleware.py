import re
import time
import datetime

from etc.log4 import logging, access_logging
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


ip_pattern = re.compile(r"((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)")


def recored_access_info(get_response):
    def warp_get_response(request, *args, **kwargs):
        request_ip = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
        if (
            not ip_pattern.match(request_ip)
            or request_ip in ("127.0.0.1", "127.0.0.0", "0.0.0.0")
        ):
            request_ip = None

        if request_ip:
            start_proc_time = time.time()
            user_agent = request.META.get("HTTP_USER_AGENT", "unkown")
            path_info = request.META.get("PATH_INFO", "unkown")
            query_string = request.META.get("QUERY_STRING")
            if query_string:
                path_info = "%s?%s" % (path_info, query_string)

        response = get_response(request, *args, **kwargs)

        if request_ip:
            process_time = time.time() - start_proc_time
            now_time = datetime.datetime.now().isoformat()[11:23]
            status = response.status_code

            access_logging.info(
                "[ %s ][ %s ][ %.3f ][ %s ][ %s ][ %s ]"
                % (now_time, status, process_time, request_ip, path_info, user_agent)
            )
        return response
    return warp_get_response
