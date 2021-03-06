import re
import os
import time
import datetime

from etc.log4 import logging
from etc.config import ACCESS_LOG_PATH
from madliar.http.response import Http410Response
from lib.asyncprocessor import async_exec
from lib import memcache
from lib.juheip import get_ip_info


IP_ANALYSIS_KEY = "IP_ANA_%s"


def get_cached_ip_info(ip):
    key = IP_ANALYSIS_KEY % ip
    return memcache.get(key)


def set_cached_ip_info(ip, info):
    key = IP_ANALYSIS_KEY % ip
    return memcache.set(key, info, timeout=0)


@async_exec
def block_bad_request(ip):
    logging.debug("Analysis ip: %s" % ip)
    ip_info = get_cached_ip_info(ip)
    if ip_info is not None:
        logging.info(
            "Got ip info from cache:%s -> %s, now don't proc it."
            % (ip, ip_info)
        )
        return True

    err_code, area = get_ip_info(ip)
    if err_code != 0:
        logging.error("In `block_bad_request` cannot get ip info: %s" % ip)
        return True

    from_china = bool(
        (u"\u5e02" in area or u"\u7701" in area or u"\u533a" in area)
        and (u"\u5730\u533a" not in area)
    )
    logging.debug("Got the ip(%15s) from %s, from china: %s." % (ip, area, from_china))

    ip_info = {"from_china": from_china, "area": area}
    set_cached_ip_info(ip, info=ip_info)

    if from_china:
        return True

    # block black ip
    with open("/home/wwwroot/siteconf/black_ip_list.conf", "a+") as f:
        print >> f, "deny %s;" % ip
    command = "service nginx restart"
    os.system(command)
    return True


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
        if not ip_pattern.match(request_ip) or request_ip in ("127.0.0.1", "127.0.0.0", "0.0.0.0"):
            return get_response(request, *args, **kwargs)

        start_proc_time = time.time()

        # if get_cached_ip_info(request_ip) is None:
        #    # Cannot get ip info, start a async task to proc it.
        #    block_bad_request.async_exec(request_ip)

        user_agent = request.META.get("HTTP_USER_AGENT", "unkown")
        path_info = request.META.get("PATH_INFO", "unkown")
        query_string = request.META.get("QUERY_STRING")
        if query_string:
            path_info = "%s?%s" % (path_info, query_string)

        response = get_response(request, *args, **kwargs)

        process_time = time.time() - start_proc_time
        now_time = datetime.datetime.now().isoformat()[11:23]
        status = response.status_code
        access_info = (
            "[ %s ][ %s ][ %.3f ][ %15s ][ %s ][ %s ]"
            % (now_time, status, process_time, request_ip, path_info, user_agent)
        )
        access_log_file = os.path.join(
            ACCESS_LOG_PATH,
            "%s.log" % str(datetime.datetime.now().date())
        )
        with open(access_log_file, "a+") as f:
            print >> f, access_info
        return response

    return warp_get_response
