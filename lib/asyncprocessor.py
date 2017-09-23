import redis
import pickle
import time

from madliar.management import reg_command
from madliar.utils import get_traceback
from importlib import import_module
from etc.config import REDIS_CONFIG
from etc.log4 import logging


_redis_host = REDIS_CONFIG.get("host", "localhost")
_redis_port = REDIS_CONFIG.get("host", 6379)
_redis_db = REDIS_CONFIG.get("db", 8)
_channel = "async_processor"

connection = None


class RedisMessageQueue(object):
    def __init__(self):
        self.__conn = redis.Redis(host=_redis_host, port=_redis_port, db=_redis_db)
        self.channel = _channel

    def publish(self, msg):
        self.__conn.publish(self.channel, msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub


@reg_command(name="run_async_server")
def run_async_processor_server():
    """Run a server to exec async task."""
    obj = RedisMessageQueue()
    monitor = obj.subscribe()
    logging.info("[ASYNC]: Start the Async server.\n")

    while True:
        start_proc_time = time.time()
        s = monitor.parse_response()
        try:
            m_type, channel, msg = s
            msg = pickle.loads(msg)

            target_module = msg.get("target_module")
            target_name = msg.get("target_name")

            logging.info("[ASYNC]: Received an asynctask from [%s.%s]" % (target_module, target_name))

            args = msg.get("args", ())
            kwargs = msg.get("kwargs", {})

            m = import_module(target_module)
            target = getattr(m, target_name)
            result = target(*args, **kwargs)
            logging.info(
                "[ASYNC]: Task from [%s.%s] exec finished, result: %s, cost: %s."
                % (target_module, target_name, result, (time.time() - start_proc_time))
            )
        except Exception as e:
            logging.error(
                "[ASYNC]: Task(msg: %s) exec failed: %s, \n%s"
                % (s, e, get_traceback())
            )


def async_exec(f):
    def wrap_exec_func(*args, **kwargs):
        message = pickle.dumps({
            "target_module": f.__module__,
            "target_name": f.__name__,
            "args": args,
            "kwargs": kwargs,
        })

        q = RedisMessageQueue()
        result = q.publish(message)
        logging.info(
            "[ASYNC]: Send async task from [%s.%s] result: %s"
            % (f.__module__, f.__name__, result)
        )
        return result
    setattr(f, "async_exec", wrap_exec_func)
    return f


@async_exec
def test_func(*args, **kwargs):
    print "[start test_func: %s, %s]" % (args, kwargs)
    time.sleep(3)
    print "[end test_func: %s, %s]" % (args, kwargs)
