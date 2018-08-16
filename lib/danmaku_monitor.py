import json
import platform
import websocket
import time
import datetime
import sys
import os
import logging
import pickle
import redis
from threading import Thread

ROOM_ID = 4424139
monitor_url = "ws://broadcastlv.chat.bilibili.com:2244/sub"
PACKAGE_HEADER_LENGTH = 16
CONST_MIGIC = 16
CONST_VERSION = 1
CONST_PARAM = 1
CONST_HEART_BEAT = 2
CONST_MESSAGE = 7

if platform.system().lower() == "windows":
    LOG_PATH = "./log/%s/" % ROOM_ID
else:
    LOG_PATH = "/home/wwwroot/log/bili/%s/" % ROOM_ID

fh = logging.FileHandler(os.path.join(LOG_PATH, "prize.log"), encoding="utf-8")
fh.setFormatter(logging.Formatter('%(message)s'))
logger = logging.getLogger("prize")
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
p_logging = logger

fh = logging.FileHandler(os.path.join(LOG_PATH, "chat.log"), encoding="utf-8")
fh.setFormatter(logging.Formatter('%(message)s'))
logger = logging.getLogger("chat")
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
c_logging = logger

fh = logging.FileHandler(os.path.join(LOG_PATH, "mix.log"), encoding="utf-8")
fh.setFormatter(logging.Formatter('%(message)s'))
logger = logging.getLogger("mix")
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logging = logger


REDIS_CONFIG = {}
REDIS_SONGLIST_KEY = "L"
ODER_SONG_INTERVAR = 180


class RedisMessageQueue(object):
    def __init__(self, channel="lyydg", r=None):
        self.__conn = r if r else redis.Redis(**REDIS_CONFIG)
        self.channel = channel

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
        # TODO: ADD log
    return sorted(song_list, key=lambda x: x[2])


def show_song_list():
    print(get_song_list())


def insert_song(song, user, timestamp):
    r = redis.Redis(**REDIS_CONFIG)
    song_list = get_song_list(r)
    if len(song_list) > 50:
        print("Song list MAX!")
        pass  # Send error log
    for d in song_list:
        if song == d[0]:
            if len(song) > 12:
                song = song[:11] + "..."
            msg = "%s 已存在！" % song
            print(msg)
            RedisMessageQueue(r=r).send_msg(msg)
            return
        if user == d[1]:
            if float(timestamp) - float(d[2]) < ODER_SONG_INTERVAR:
                if len(user) > 7:
                    user = user[:7] + "..."
                msg = "请%s等%d秒后再点歌!" % (user, ODER_SONG_INTERVAR - int(time.time() - float(d[2])))
                print(msg)
                RedisMessageQueue(r=r).send_msg(msg)
                return
    song_list.append([song, user, timestamp])
    result = r.set(REDIS_SONGLIST_KEY, pickle.dumps(song_list))
    if len(song) > 12:
        song = song[:11] + "..."
    RedisMessageQueue(r=r).send_msg("%s 点歌成功！" % song)
    return result


def parse_danmaku(msg):
    cmd = msg.get("cmd")
    if cmd == "DANMU_MSG":
        content = msg.get("info", "")
        raw_msg = content[1]
        user = content[2][1]
        ul = content[4][0]
        try:
            decoration = content[3][1]
            dl = content[3][0]
        except Exception:
            decoration = ""
            dl = ""

        datetime_str = str(datetime.datetime.now())

        msg = '[{}] [UL {: >2}] [{:　<4}{: >2}] {} -> {}'.format(datetime_str, ul, decoration, dl, user, raw_msg)
        c_logging.info(msg)
        logging.info(msg)
        print(msg)

        if "点歌" in raw_msg:
            prefix, postfix = raw_msg.split("点歌", 1)
            if len(prefix) > 2:
                print("Invalid -> ", raw_msg)
                return
            song_name = postfix.strip()
            if song_name:
                timest = "%.7f" % time.time()
                insert_song(song_name, user, timest)
                show_song_list()

    elif cmd == "SEND_GIFT":
        datetime_str = str(datetime.datetime.now())
        data = msg.get("data")
        uid = data.get("uid", "        ")
        user = data.get("uname", "")
        gift_name = data.get("giftName", "")
        gift_type = data.get("coin_type", "")
        count = data.get("num", "")
        msg = "[{}] [{: ^14}][{}] -> [{}][{}] * [{}]".format(datetime_str, uid, user, gift_name, gift_type, count)
        print(msg)
        p_logging.info(msg)
        logging.info(msg)
    elif cmd == "COMBO_END":
        datetime_str = str(datetime.datetime.now())
        data = msg.get("data")
        uid = "       "
        user = data.get("uname", "")
        gift_name = data.get("gift_name", "")
        gift_type = ""
        count = data.get("combo_num", "")
        msg = "[{}] [{: ^14}][{}] -> [{}][{}] * [{}]".format(datetime_str, uid, user, gift_name, gift_type, count)
        print(msg)
        p_logging.info(msg)
        logging.info(msg)


def on_message(ws_obj, message):
    while message:
        length = (message[0] << 24) + (message[1] << 16) + (message[2] << 8) + message[3]
        current_msg = message[:length]
        message = message[length:]
        if len(current_msg) > 16 and current_msg[16] != 0:
            try:
                msg = current_msg[16:].decode("utf-8", errors="ignore")
                msg = json.loads(msg)
                parse_danmaku(msg)
            except Exception as e:
                print("e: %s, m: %s" % (e, current_msg))


def on_error(ws_obj, error):
    print(error)
    raise RuntimeError("WS Error!")


def on_close(ws_obj):
    raise RuntimeError("WS Closed!")


def on_open(ws_obj):
    print("ws opened: %s" % ws_obj)
    send_join_room(ws_obj)


def send_heart_beat(ws_obj):
    hb = generate_packet(CONST_HEART_BEAT)
    while True:
        time.sleep(10)
        ws_obj.send(hb)


def send_join_room(ws_obj, uid=None):
    roomid = ROOM_ID
    if not uid:
        from random import random
        from math import floor
        uid = int(1E15 + floor(2E15 * random()))

    package = '{"uid":%s,"roomid":%s}' % (uid, roomid)
    binmsg = generate_packet(CONST_MESSAGE, package)
    ws_obj.send(binmsg)
    t = Thread(target=send_heart_beat, args=(ws_obj, ))
    t.start()


def generate_packet(action, payload=""):
    payload = payload.encode("utf-8")
    packet_length = len(payload) + PACKAGE_HEADER_LENGTH
    buff = bytearray(PACKAGE_HEADER_LENGTH)

    # package length
    buff[0] = (packet_length >> 24) & 0xFF
    buff[1] = (packet_length >> 16) & 0xFF
    buff[2] = (packet_length >> 8) & 0xFF
    buff[3] = packet_length & 0xFF

    # migic & version
    buff[4] = 0
    buff[5] = 16
    buff[6] = 0
    buff[7] = 1

    # action
    buff[8] = 0
    buff[9] = 0
    buff[10] = 0
    buff[11] = action

    # migic parma
    buff[12] = 0
    buff[13] = 0
    buff[14] = 0
    buff[15] = 1

    return buff + payload


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        url=monitor_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
