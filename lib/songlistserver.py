import os
import json
import redis
import pickle
import platform
import logging
from traceback import format_exc
from threading import Thread
from websocket_server import WebsocketServer


REDIS_CONFIG = {
}
REDIS_SONGLIST_KEY = "L"

if platform.system().lower() == "windows":
    LOG_PATH = "./log/"
else:
    LOG_PATH = "/home/wwwroot/log/bili/"

fh = logging.FileHandler(os.path.join(LOG_PATH, "songlistserver.log"), encoding="utf-8")
fh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger = logging.getLogger("songlistserver")
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logging = logger


class RedisMessageQueue(object):
    def __init__(self, channel="lyydg", r=None):
        self.__conn = r if r else redis.Redis(**REDIS_CONFIG)
        self.channel = channel
        self._monitor_q = None

    def send_msg(self, msg):
        b = pickle.dumps(msg)
        self.__conn.publish(self.channel, b)
        return True

    def __init_monitor_q(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.listen()
        pub.parse_response()
        self._monitor_q = pub

    def accept_msg(self):
        if self._monitor_q is None:
            self.__init_monitor_q()
        while True:
            r = self._monitor_q.parse_response()
            try:
                return pickle.loads(r[-1])
            except Exception:
                continue


def get_song_list(r=None):
    if not r:
        r = redis.Redis(**REDIS_CONFIG)
    try:
        song_list = pickle.loads(r.get(REDIS_SONGLIST_KEY))
    except pickle.UnpicklingError:
        song_list = []
        r.set(REDIS_SONGLIST_KEY, pickle.dumps(song_list))
        logging.error("pickle.UnpicklingError happend when get_song_list.")
    return sorted(song_list, key=lambda x: float(x[2]))


def del_a_song(song_id):
    r = redis.Redis(**REDIS_CONFIG)
    try:
        song_list = pickle.loads(r.get(REDIS_SONGLIST_KEY))
    except pickle.UnpicklingError:
        song_list = []

    new_song_list = []
    for _ in song_list:
        if _[2] != song_id:
            new_song_list.append(_)
        else:
            logging.info("Song %s deleted." % _)
    r.set(REDIS_SONGLIST_KEY, pickle.dumps(new_song_list))
    return sorted(new_song_list, key=lambda x: float(x[2]))


def new_client(client, server):
    logging.info("New client connected and was given id %d." % client['id'])


def client_left(client, server):
    logging.info("Client(%d) disconnected." % client['id'])


def message_received(client, server, message):
    if message == "heartbeat":
        server.send_message(client, '{"action": "OK"}')

    elif "songlist" in message:
        r = {"action": "songlist", "data": get_song_list()}
        server.send_message(client, json.dumps(r))

    elif "delsong" in message:
        try:
            song = message[7:]
        except Exception as e:
            logging.error("Error in parsing raw message `delsong`. e: %s, trackback: %s" % (e, format_exc(e)))
        else:
            logging.info("Try del: %s" % song)
            r = {"action": "songlist", "data": del_a_song(song)}
            server.send_message_to_all(json.dumps(r))


if __name__ == "__main__":
    server = WebsocketServer(8080, "haha5")
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    t = Thread(target=server.run_forever)
    t.start()

    mq = RedisMessageQueue()
    while True:
        msg = mq.accept_msg()
        logging.info("Global message: %s" % msg)
        response = {"action": "msg", "data": msg}
        server.send_message_to_all(json.dumps(response))
