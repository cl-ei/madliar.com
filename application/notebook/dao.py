# -*- coding:utf-8 -*-
import redis
import json
import time
from lib.randomlib import randstr
from lib import memcache


class RedisKeyToJSON(object):
    def __init__(self, key, host='localhost', port=6379, db=8):
        self.__db = redis.Redis(host=host, port=port, db=db)
        self.__key = 'nb_%s' % key

    def write(self, value, timeout=0):
        if not isinstance(value, dict):
            raise TypeError("value must be a dict object.")

        try:
            value = json.dumps(value)
        except (TypeError, ValueError):
            return False

        result = self.__db.set(self.__key, value)
        if not result:
            return result

        if timeout > 0:
            result = self.__db.expire(self.__key, timeout)
        return result

    def read(self):
        value = self.__db.get(self.__key)
        if not value:
            return {}

        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            return {}
        else:
            return value

    def delete(self):
        return self.__db.delete(self.__key)


def check_regist_limit(email):
    s = redis.Redis(host='localhost', port=6379, db=8)
    now_time_str = time.strftime("%Y-%m-%d", time.localtime())
    login_key = "REG_%s" % now_time_str

    existed_registed_user_cnt = s.llen(login_key)
    if existed_registed_user_cnt > 500:
        return False

    s.lpush(login_key, email)
    if existed_registed_user_cnt == 0:
        s.expire(login_key, 3600 * 24)

    return True


def login(email, password):
    user_key = "USER_%s" % email
    s = RedisKeyToJSON(user_key)
    user_info = s.read()

    existed_password = user_info.get("password")
    if password != existed_password:
        return False, u"密码或邮箱错误。"

    new_token = randstr(64)
    user_info.update({
        "token": new_token,
        "expire_time": int(time.time()) + 3600*24*30,
    })
    if s.write(user_info):
        return True, new_token

    return False, u"操作失败。"


def regist(email, password):
    if not check_regist_limit(email):
        return False, u"系统繁忙，请稍后再试。"

    user_key = "USER_%s" % email
    s = RedisKeyToJSON(user_key)
    user_info = s.read()
    if user_info and user_info.get("password"):
        return False, u"用户已经存在，请重新输入或直接登录。"

    new_token = randstr(64)
    user_info.update({
        "token": new_token,
        "password": password,
        "expire_time": int(time.time()) + 3600 * 24 * 30,
    })
    if s.write(user_info):
        return True, new_token

    # TODO: add log.
    s.delete()
    return False, u"操作失败。"


def logout(email):
    user_key = "USER_%s" % email
    s = RedisKeyToJSON(user_key)
    user_info = s.read()
    pass_word = user_info.get("password")
    if pass_word:
        new_info = {"password": pass_word}
        s.write(new_info)
    else:
        s.delete()
    return True, u""


def check_login(email, token):
    user_key = "USER_%s" % email
    s = RedisKeyToJSON(user_key)
    user_info = s.read()
    user_token = user_info.get("token")
    if token != user_token:
        return False

    expire_time = user_info.get("expire_time")
    if not expire_time:
        return False

    now = int(time.time())
    return now < expire_time


# For sharing.
path_to_key_prifix = "PATH_TO_SKEY_%s"  # return key
key_to_path_prifix = "SKEY_TO_PATH_%s"  # return path


def share_file(path):
    s_key = memcache.get(path_to_key_prifix % path)
    if s_key:
        return True, s_key

    for _ in range(300):
        new_key = randstr(16)
        key_to_path = key_to_path_prifix % new_key

        old_path = memcache.get(key_to_path)
        if old_path is None:
            memcache.set(key_to_path_prifix % new_key, path, 0)
            memcache.set(path_to_key_prifix % path, new_key, 0)
            return True, new_key

    return False, ""


def get_shared_file(key):
    return memcache.get(key_to_path_prifix % key)
