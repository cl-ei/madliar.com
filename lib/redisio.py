"""
Provides Python-object-alike API to access data.
It's based on redis service.

"""

import redis
import pickle


class RedisList(object):
    def __init__(self, key, host='localhost', port=6379, db=8):
        self.__db = redis.Redis(host=host, port=port, db=db)
        self.__key = 'rli_%s' % key

    def push(self, value):
        return self.__db.lpush(self.__key, pickle.dumps(value))

    def pop(self):
        response = self.__db.lpop(self.__key)
        if response is not None:
            response = pickle.loads(response)
        return response

    def delete(self, value, num=0):
        return self.__db.lrem(self.__key, pickle.dumps(value), num)

    def __len__(self):
        return self.__db.llen(self.__key)

    def __getitem__(self, item):
        if not isinstance(item, (int, slice)):
            raise TypeError("Expected int or slice arguments, got %s!" % type(item))

        if isinstance(item, int):
            return pickle.loads(self.__db.lindex(self.__key, item))

        if item.step not in (None, 1):
            raise ValueError("Step must be 1 !")

        start = 0 if item.start is None else item.start
        stop = -1 if item.stop is None or item.stop > 0x6fffffffffffffff else item.stop

        response = self.__db.lrange(self.__key, start, stop)
        return [pickle.loads(_) for _ in response]

    def destroy(self):
        return self.__db.delete(self.__key)


class RedisSet(object):
    def __init__(self, key, host='localhost', port=6379, db=8):
        self.__db = redis.Redis(host=host, port=port, db=db)
        self.__key = 'rst_%s' % key

    def add(self, *args):
        values = [pickle.dumps(_) for _ in args]
        return self.__db.sadd(self.__key, *values)

    def __len__(self):
        return self.__db.scard(self.__key)

    def pop(self):
        response = self.__db.spop(self.__key)
        if response is not None:
            response = pickle.loads(response)
        return response

    def all(self):
        response = self.__db.smembers(self.__key)
        return [pickle.loads(_) for _ in response]

    def destroy(self):
        return self.__db.delete(self.__key)

    def delete(self, *args):
        values = [pickle.dumps(_) for _ in args]
        return self.__db.srem(self.__key, *values)

    def get(self, count=1):
        response = self.__db.srandmember(self.__key, count)
        if response is not None:
            response = [pickle.loads(_) for _ in response]
        return response
