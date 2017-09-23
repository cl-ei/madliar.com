import json
import urllib
from urllib import urlencode


appkey = "f551cc9ac9dad658b231006f58965077"


def get_ip_info(ip):
    url = "http://apis.juhe.cn/ip/ip2addr"
    params = {
        "ip": ip,
        "key": appkey,
        "dtype": "json",
    }
    params = urlencode(params)
    f = urllib.urlopen("%s?%s" % (url, params))
    content = f.read()
    try:
        res = json.loads(content)
    except (TypeError, ValueError, UnicodeEncodeError):
        res = {}

    err_code = res.get("error_code", -1)
    if err_code == 0:
        data = res.get("result", {}).get("area")
    else:
        data = res.get("reason")
    return err_code, data


if __name__ == '__main__':
    test_ip = "106.11.242.36"
    print "%s, %s" % get_ip_info(test_ip)
