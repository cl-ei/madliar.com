import redis
import pickle
import time
import random
import hashlib

from madliar.management import reg_command
from madliar.utils import get_traceback
from importlib import import_module
from etc.config import REDIS_CONFIG
from etc.log4 import logging

_channel = "async_processor"

connection = None


def get_md5(string):
    return hashlib.md5(string).hexdigest()


class RedisMessageQueue(object):
    def __init__(self):
        self.__conn = redis.Redis(**REDIS_CONFIG)
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
        s = monitor.parse_response()
        try:
            start_proc_time = time.time()

            m_type, channel, msg = s
            msg = pickle.loads(msg)

            target_module = msg.get("target_module")
            target_name = msg.get("target_name")

            task_id = msg.get("id")
            trigger_time = msg.get("trigger_time")
            waitting_time = start_proc_time - float(trigger_time)

            logging.info(
                "[ASYNC]: Received an asynctask(%s) from [%s.%s], wait time: %.3f s."
                % (task_id, target_module, target_name, waitting_time)
            )

            args = msg.get("args", ())
            kwargs = msg.get("kwargs", {})

            m = import_module(target_module)
            target = getattr(m, target_name)
            result = target(*args, **kwargs)

            cost_time = time.time() - start_proc_time
            logging.info(
                "[ASYNC]: Task(%s) from [%s.%s] exec finished, result: %s, cost: %.3f s."
                % (task_id, target_module, target_name, result, cost_time)
            )
        except Exception as e:
            logging.error(
                "[ASYNC]: Task(msg: %s) exec failed: %s, \n%s"
                % (s, e, get_traceback())
            )


def async_exec(f):
    def wrap_exec_func(*args, **kwargs):
        async_args = {
            "target_module": f.__module__,
            "target_name": f.__name__,
            "args": args,
            "kwargs": kwargs,
            "trigger_time": time.time(),
            "uniqkey": random.random(),
        }

        args_md5 = get_md5(pickle.dumps(async_args))
        task_id = "-".join([args_md5[:16], args_md5[16:28], args_md5[28:]])
        async_args["id"] = task_id

        message = pickle.dumps(async_args)

        q = RedisMessageQueue()
        result = q.publish(message)
        logging.info(
            "[ASYNC]: Send async task(%s) from [%s.%s] result: %s"
            % (task_id, f.__module__, f.__name__, result)
        )
        return result
    setattr(f, "async_exec", wrap_exec_func)
    return f


@async_exec
def test_func(*args, **kwargs):
    print "[start test_func: %s, %s]" % (args, kwargs)
    time.sleep(3)
    print "[end test_func: %s, %s]" % (args, kwargs)
