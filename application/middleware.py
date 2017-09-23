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
        localhost_ip = ("127.0.0.1", "127.0.0.0", "0.0.0.0")
        if not ip_pattern.match(request_ip) or request_ip in localhost_ip:
            request_ip = None
        else:
            start_proc_time = time.time()
            block_bad_request.async_exec(request_ip)
            request_ip = "%15s" % request_ip
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

            access_info = (
                "[ %s ][ %s ][ %.3f ][ %s ][ %s ][ %s ]"
                % (now_time, status, process_time, request_ip, path_info, user_agent)
            )
            access_log_file = os.path.join(
                ACCESS_LOG_PATH,
                "%s.log" % datetime.datetime.now().isoformat()[:10]
            )
            with open(access_log_file, "a+") as f:
                print >> f, access_info

        return response
    return warp_get_response


@async_exec
def block_bad_request(ip):
    logging.debug("Analysis ip: %s" % ip)

    key = "IP_ANA_%s" % ip
    ip_info = memcache.get(key)
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

    from_china = bool(u"\u5e02" in area or u"\u7701" in area)
    logging.debug("IP JUDGE[ BLOCK?, IP, AREA ]: %s %15s %s" % (from_china, ip, area))

    ip_info = {"from_china": from_china, "area": area}
    memcache.set(key, ip_info, timeout=0)

    if from_china:
        return True

    # block black ip
    with open("/home/wwwroot/siteconf/black_ip_list.conf", "a+") as f:
        print >> f, "deny %s;" % ip
    command = "service nginx restart"
    os.system(command)
    return True
